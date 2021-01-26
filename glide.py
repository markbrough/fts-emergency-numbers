import requests
from lxml import html
import csv
import datetime
SEARCH_URL = "https://glidenumber.net/glide/public/search/search.jsp"
URL = "https://glidenumber.net/glide/public/result/report.jsp"

CSV_FILENAME = "output/glide-emergencies.csv"
HEADERS = ["GLIDE_number", "Event", "Country", "Date", "Event_Code", "Country_Code", "Glide_Serial", "Comments"]

REQUEST_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
}


def download(csv):
  def get_t(row, i):
    return row.xpath("td")[i].text_content().strip()

  def make_date(value):
    year, month, day = value.split("/")
    try:
      return datetime.date(year=int(year),
          month=int(month),
          day=int(day)
        ).isoformat()
    # Some dates are formatted incorrectly as
    #  yyyy/d/mm rather than
    #  yyyy/m/dd
    except ValueError:
      return value


  s = requests.session()
  s.headers.update(REQUEST_HEADERS)

  search_post_data = [
    ("level0", "*"),
    ("level1", "*"),
    ("events", "*"),
    ("keywords", ""),
    ("ftoption", "&"),
    ("fromyear", ""),
    ("frommonth", ""),
    ("fromday", ""),
    ("toyear", ""),
    ("tomonth", ""),
    ("today", ""),
    ("maxhits", "10000"),
    ("sortby", "0"),
    ("X_Resolution", "1920"),
    ("nStart", "0"),
    ("posted", "0"),
    ("process", "/public/result/report.jsp"),
    ("go.x", "Search")
  ]
  print("Opening GLIDEnumber.net")
  s.post(SEARCH_URL, data=search_post_data)

  post_data = [
    ("continueReport", "Continue"),
    ("unlimited", "Y"),
    ("variables", "disasters.sEventId || '-' || sGlide || '-' ||  sLocationCode as GLIDE_number"),
    ("variables", "sEventName as Event"),
    ("variables", "geography.sLocation as Country"),
    ("variables", "(CAST(nyear as varchar(8)) || '/' || CAST(nmonth  as varchar(8)) || '/' || CAST(nday as varchar(8))) as Date"),
    ("variables", "disasters.seventid as Event_Code"),
    ("variables", "slocationcode as Country_Code"),
    ("variables", "sglide as Glide_Serial"),
    ("variables", "scomments as Comments"),
  ]

  print("Requesting list of GLIDE numbers, this may take a moment...")
  r = s.post(URL, data=post_data)
  doc = html.fromstring(r.text)
  rows = doc.xpath("//table[3]")[0].xpath("tr/td/table[2]/tr")
  print("Found {} entries".format(len(rows)))
  for row in rows:
    #if not row.xpath("tr/td[@class='bfS']"): continue
    if (len(row.xpath("td"))!=8):
      print("Irregular column width, skipping")
      continue
    csv.writerow({"GLIDE_number": get_t(row, 0),
      "Event": get_t(row, 1),
      "Country": get_t(row, 2),
      "Date": make_date(get_t(row, 3)),
      "Event_Code": get_t(row, 4),
      "Country_Code": get_t(row, 5),
      "Glide_Serial": get_t(row, 6),
      "Comments": get_t(row, 7)
    })


if __name__ == "__main__":
  with open(CSV_FILENAME, "w") as csv_file:
    csv = csv.DictWriter(csv_file, fieldnames=HEADERS)
    csv.writeheader()
    download(csv)
