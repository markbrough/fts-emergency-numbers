import requests
from lxml import html
import unicodecsv
SEARCH_URL = "http://glidenumber.net/glide/public/search/search.jsp"
URL = "http://glidenumber.net/glide/public/result/report.jsp"

CSV_FILENAME = "output/glide.csv"
HEADERS = ["GLIDE_number", "Event", "Country", "Date"]

def download(csv):
  def get_t(row, i):
    return row.xpath("td")[i].text_content().strip()
  
  s = requests.session()
  
  search_post_data = [
    ("X_Resolution", "1366"),
    ("events", "*"),
    ("fromday", ""),
    ("frommonth", ""),
    ("fromyear", ""),
    ("ftoption", "&"),
    ("keywords", ""),
    ("level0", "*"),
    ("level1", "*"),
    ("maxhits", "10000"),
    ("nStart", "0"),
    ("posted", "0"),
    ("process", "/public/result/report.jsp"),
    ("sortby", "0"),
    ("today", ""),
    ("tomonth", ""),
    ("toyear", "")
  ]
  s.post(SEARCH_URL, data=search_post_data)
  
  post_data = [
    ("continueReport", "Continue"),
    ("unlimited", "Y"),
    ("variables", "disasters.sEventId || '-' || sGlide || '-' ||  sLocationCode as GLIDE_number"),
    ("variables", "sEventName as Event"),
    ("variables", "geography.sLocation as Country"),
    ("variables", "(CAST(nyear as varchar(8)) || '/' || CAST(nmonth  as varchar(8)) || '/' || CAST(nday as varchar(8))) as Date_")
  ]
  r = s.post(URL, data=post_data)
  doc = html.fromstring(r.text)
  rows = doc.xpath("//table[3]")[0].xpath("tr/td/table[2]/tr")
  print len(rows)
  for row in rows:
    #if not row.xpath("tr/td[@class='bfS']"): continue
    print html.tostring(row)
    print len(row.xpath("th"))
    if (len(row.xpath("td"))!=4): 
      print "Continuing"
      continue
    csv.writerow({"GLIDE_number": get_t(row, 0),
           "Event": get_t(row, 1),
           "Country": get_t(row, 2),
           "Date": get_t(row, 3)})

with open(CSV_FILENAME, "w") as csv_file:
  csv = unicodecsv.DictWriter(csv_file, fieldnames=HEADERS)
  csv.writeheader()
  download(csv)
