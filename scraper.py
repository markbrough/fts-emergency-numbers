from os import environ, remove
environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'

import scraperwiki
import glide


class PretendCSVWriter():
    def __init__(self):
        self.data = []

    def writerow(self, row):
        self.data.append(row)


def run():
    pretend_csv = PretendCSVWriter()
    glide.download(pretend_csv)
    scraperwiki.sqlite.save(['GLIDE_number'], pretend_csv.data, "GLIDE_numbers")


run()
