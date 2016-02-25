import csv
import re
from geocode import geocode_address
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def read_file(source_file, output_file):
    with open(source_file) as csv_source_file:
        with open(output_file, 'w') as csv_output_file:

            fieldnames = ['street_address', 'city', 'unit', 'date_issued', 'clean_address', 'extras', 'geocode_status', 'geocode_place_name', 'lat', 'lon']

            reader = csv.DictReader(csv_source_file)
            writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)

            # Counter to limit rows for testing and to keep track of the number of requests
            i = 0

            # Initiate geocode status counts
            success_count = 0
            check_count = 0
            fail_count = 0
            empty_row_count = 0

            # # Number of rows to test on
            # n = 300

            writer.writeheader()

            for row in reader:

                # # Only do this for the first n rows
                # if i > n:
                #     break

                # Increment the row counter
                i += 1

                # If the street address field is empty, skip it
                if not row['street_address']:
                    print "row {} is empty".format(i)
                    empty_row_count += 1
                    continue

                street_address = row['street_address']

                # TO DO: refactor to make these regex operations seperate functions

                # Create regex to find common delimters of extra information in the street_address field
                unit_marker_regex = re.compile(ur'(apt|room|#|unit|suite|bldg|\(|downstairs|upstairs|;)', re.IGNORECASE)

                # Find a unit marker in street_address
                unit_matches = re.findall(unit_marker_regex, street_address)

                # If there are matches, put everything after first match into the extras string
                # and put everything before the first match into the clean_address string
                if unit_matches:
                    start_index = street_address.find(unit_matches[0])
                    extra = street_address[start_index:]
                    clean_address = street_address[:start_index]
                    # print "clean_address: {}".format(clean_address)

                else:
                    clean_address = street_address
                    extra = None

                # Create regex to find non-digits at beginning of clean_address string
                # For example: "Islander Lodge Motel, 2428 Central Ave"
                non_digit_start_regex = re.compile(ur'^\D*')

                # Find non-digit start in clean_address
                non_digit_matches = re.findall(non_digit_start_regex, clean_address)
                # print non_digit_matches

                # If there are matches, extract the non-digit start and add it to beginning
                # of extras string and remove it from clean_address
                if non_digit_matches:
                    non_digit_start = non_digit_matches[0]
                    # Get the index of the first character in the non-digit start, which should be 0
                    start_index = clean_address.find(non_digit_start)
                    # Get the index of the last character in the non-digit start
                    start_index = start_index + len(non_digit_start)

                    # Add the non-digit start to the extra string
                    if extra:
                        extra = non_digit_start + extra
                    else:
                        extra = non_digit_start

                    # Remove the non-digit start from the clean_address
                    clean_address = clean_address[start_index:]

                # Strip spaces and puntuation off beginning and end of clean_address and extra
                punct_to_strip = ' .,;'

                clean_address = clean_address.strip(' .,;')

                if extra:
                    extra = extra.strip(punct_to_strip)

                clean_address = ', '.join([clean_address, row['city'], 'CA'])

                proxim_lat = 37.8044
                proxim_lon = -122.2697

                # Geocode address and set row variables
                geocode_result = geocode_address(clean_address, proxim_lat=proxim_lat, proxim_lon=proxim_lon)

                # Determine status as success, check or failed

                if geocode_result:
                    if float(geocode_result['relevance']) >= 0.9:
                        # print geocode_result['place_name']
                        # print row['city']

                        # If the geocoder just picked up the city, set status to CHECK
                        if geocode_result['place_name'] == row['city']:
                            geocode_status = "CHECK - CITY ONLY"
                            check_count += 1

                        # If the coordinates are unreasonably far from the proximity coordinates
                        elif abs(float(geocode_result['lat']) - proxim_lat) > 1 or abs(float(geocode_result['lon']) - proxim_lon) > 1:
                            geocode_status = "CHECK - OUT OF RANGE"
                            check_count += 1

                        # Otherwise, mark it as a success
                        else:
                            geocode_status = "SUCCESS"
                            success_count += 1
                    else:
                        geocode_status = "CHECK"
                        check_count += 1

                    geocode_place_name = geocode_result['place_name']
                    lat = geocode_result['lat']
                    lon = geocode_result['lon']

                else:
                    geocode_status = "FAILED"
                    geocode_place_name = None
                    lat = None
                    lon = None
                    fail_count += 1

                print "row {}: {} {}".format(i, clean_address, geocode_status)

                # TO DO: deal with empty rows

                try:
                    writer.writerow({
                        'street_address': row['street_address'],
                        'city': row['city'],
                        'unit': row['unit'],
                        'date_issued': row['date_issued'],
                        'clean_address': clean_address,
                        'extras': extra,
                        'geocode_status': geocode_status,
                        'geocode_place_name': geocode_place_name,
                        'lat': lat,
                        'lon': lon
                    })

                except Exception, e:
                    writer.writerow({
                        'street_address': row['street_address'],
                        'city': row['city'],
                        'unit': row['unit'],
                        'date_issued': row['date_issued'],
                        'clean_address': clean_address,
                        'extras': extra,
                        'geocode_status': geocode_status,
                        'geocode_place_name': e,
                        'lat': None,
                        'lon': None
                        })
                    print str(e)

                # Sleep for 0.1 secs to prevent exceeding the request limits for the mapbox geocoder
                # Should result in fewer than 600 requests per minute with all of the reading/writing and geocoding requests themselves
                time.sleep(0.1)

    print "Success count: {}".format(success_count)
    print "Check count: {}".format(check_count)
    print "Failure count: {}".format(fail_count)

    csv_output_file.close()
    csv_source_file.close()
