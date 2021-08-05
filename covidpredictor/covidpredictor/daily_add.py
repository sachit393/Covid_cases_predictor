import bs4, requests, csv
from datetime import datetime, date
from datetime import timedelta
res = requests.get("https://dashboard.kerala.gov.in/covid/index.php")

soup = bs4.BeautifulSoup(res.text, "html.parser")

dailyCasesTag = soup.select("body > div > div.content-wrapper > section.content > div > div:nth-child(1) > div.col-lg-8.col-12 > div > div:nth-child(1) > div > div.inner > h3 > sup")

dailyCasesUnedited = dailyCasesTag[0].text
dailyCasesEdited_1 = dailyCasesUnedited[1:len(dailyCasesUnedited) - 1]
dailyCases = dailyCasesEdited_1[1:]
currentDate = str(date.today()-timedelta(days = 4))
print(currentDate)

def updateCase(currentDate, dailyCases, oldDataList):
  f = open("Covid 19 Confirmed Cases-Kerala.csv", "wt")
  for line in oldDataList:
    f.write(line)
    f.write("\n")

  if currentDate == oldDataList[len(oldDataList)-1][:10]:
      f.close()
  else:
      f.write(currentDate +"," + dailyCases)
      f.write("\n")
      f.close()

def getHistoricalData():
  a_file = open("Covid 19 Confirmed Cases-Kerala.csv", "r")

  list_of_lists = []
  for line in a_file:
    stripped_line = line.strip()
    # line_list = stripped_line.split()
    list_of_lists.append(stripped_line)

  a_file.close()
  return list_of_lists

oldDataList = getHistoricalData()
updateCase(currentDate, dailyCases, oldDataList)
