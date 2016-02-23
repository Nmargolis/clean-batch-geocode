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

            extra = None

            unit_marker = re.compile(ur'(apt|room|#|unit|suite|bldg|\(|downstairs|upstairs)', re.IGNORECASE)

            # Find a unit marker in street_address
            matches = re.findall(unit_marker, street_address)

            # If there are matches, put everything after first match into the extras string
            # and put everything before the first match into the clean_address string
            if matches:
                start_index = street_address.find(matches[0])
                extra = street_address[start_index:]
                clean_address = street_address[:start_index]

                print "clean_address: {}".format(clean_address)
                print "extra: {}".format(extra)

            # print(row['street_address'], row['city'])
