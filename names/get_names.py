import logging
import os
import requests
import simplejson as json
import csv

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)


class GetNames:
    def __init__(self):
        self.names_source = "./names.csv"
        self.names = []

    def get_names_list(self):
        with open(self.names_source) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line_count, row in enumerate(csv_reader):
                self.names.append(row[0])
                line_count += 1
            logging.info("Names: {}".format(str(self.names)))
            logging.info("Number of names: {}".format(str(line_count)))
