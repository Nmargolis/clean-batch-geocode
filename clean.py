import csv
import re


def read_file(source_file, output_file):
    with open(source_file) as csv_source_file:

        # Counter to limit rows for testing
        i = 0

        # Number of rows to test on
        n = 75

        fieldnames = ['street_address', 'city', 'unit', 'date_issued', 'clean_address', 'extras']

        reader = csv.DictReader(csv_source_file)
        # writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        for row in reader:

            # Only do this for the first n rows
            if i > n:
                break
            i += 1

            print(row['street_address'], row['city'])
