import requests
from lxml import etree
import unicodecsv
URL = "http://fts.unocha.org/api/v1/Emergency/year/{0}.xml"

CSV_FILENAME = "output/fts-emergencies.csv"
HEADERS = ["title", "type", "id", "year", "country"]

def download(csv, year):
  print "Obtaining data for {0}".format(year)
  r = requests.get(URL.format(year))
  doc = etree.fromstring(r.text)
  emergencies = doc.xpath("//Emergency")
  for emergency in emergencies:
    # We don't want to include emergencies that already have a GLIDE id
    if emergency.find("glideid").text: continue
    csv.writerow({
      "title": emergency.find("title").text,
      "type": emergency.find("type").text,
      "id": emergency.find("id").text,
      "year": emergency.find("year").text,
      "country": emergency.find("country").text
    })

with open(CSV_FILENAME, "w") as csv_file:
  csv = unicodecsv.DictWriter(csv_file, fieldnames=HEADERS)
  csv.writeheader()
  for year in range (2016,1998,-1):
    download(csv, year)
