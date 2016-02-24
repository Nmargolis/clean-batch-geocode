import csv
import re


def read_file(source_file, output_file):
    with open(source_file) as csv_source_file:

        # Counter to limit rows for testing
        i = 0

        # Number of rows to test on
        n = 100

        fieldnames = ['street_address', 'city', 'unit', 'date_issued', 'clean_address', 'extras']

        reader = csv.DictReader(csv_source_file)
        # writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        for row in reader:

            # Only do this for the first n rows
            if i > n:
                break
            i += 1

            street_address = row['street_address']

            # TO DO: refactor to make these regex operations seperate functions

            # Create regex to find common delimters of extra information in the street_address field
            unit_marker_regex = re.compile(ur'(apt|room|#|unit|suite|bldg|\(|downstairs|upstairs)', re.IGNORECASE)

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
            punct_to_strip = ' .,'

            clean_address = clean_address.strip(' .,')

            if extra:
                extra = extra.strip(punct_to_strip)

            print "stripped clean_address: {}".format(clean_address)
            if extra:
                print "extra: {}".format(extra)


            # print(row['street_address'], row['city'])
