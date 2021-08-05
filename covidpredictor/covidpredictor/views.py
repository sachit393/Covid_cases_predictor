from django.shortcuts import render
import pickle
import json as simplejson
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.arima_model import ARIMA

import bs4, requests, csv
from datetime import datetime, date,timedelta

# our home page view
def home(request):
    return render(request, 'index.html')


# custom method for generating predictions
def getPredictions():

    fitted_model = pickle.load(open("covidpredictor/model.sav", "rb"))
    df = pd.read_csv('covidpredictor/Covid 19 Confirmed Cases-Kerala.csv',index_col='Date',parse_dates=True)
    df.index.freq='D'
    prediction =fitted_model.predict(len(df.loc['2020-06-01':]),len(df.loc['2020-06-01':])+5,typ='levels')
    return prediction
# our result page view

# dates = getPredictions().index
# cases = getPredictions().to_list()
# data_list=[['Date','Active Cases']]
# for i in range(0,len(cases)):
#     data_list.append([dates[i].date().strftime('%Y-%m-%d'),cases[i]])
# print(data_list)

def result(request):

    res = requests.get("https://dashboard.kerala.gov.in/covid/index.php")

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    dailyCasesTag = soup.select("body > div > div.content-wrapper > section.content > div > div:nth-child(1) > div.col-lg-8.col-12 > div > div:nth-child(1) > div > div.inner > h3 > sup")

    dailyCasesUnedited = dailyCasesTag[0].text
    dailyCasesEdited_1 = dailyCasesUnedited[1:len(dailyCasesUnedited) - 1]
    dailyCases = dailyCasesEdited_1[1:]
    currentDate = str(date.today()-timedelta(days = 1))
    ####################################
    def updateCase(currentDate, dailyCases, oldDataList):
      f = open("covidpredictor/Covid 19 Confirmed Cases-Kerala.csv", "wt")
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
      a_file = open("covidpredictor/Covid 19 Confirmed Cases-Kerala.csv", "r")

      list_of_lists = []
      for line in a_file:
        stripped_line = line.strip()
        list_of_lists.append(stripped_line)

      a_file.close()
      return list_of_lists

    oldDataList = getHistoricalData()
    updateCase(currentDate, dailyCases, oldDataList)
    ##################################################
    temp_df = pd.read_csv('covidpredictor/Covid 19 Confirmed Cases-Kerala.csv',index_col='Date',parse_dates=True)
    temp_df.index.freq='D'
    temp_df=temp_df.loc['2020-06-01':]
    from matplotlib.pyplot import figure

    figure(figsize=(16, 12), dpi=80)
    plt.plot(temp_df['Confirmed'],color='red',)
    plt.title('No of daily new cases from June 2020 till now in Kerela')
    plt.savefig('static/data.png')

    # MAKING ARIMA MODEL

    model = ARIMA(temp_df['Confirmed'],order=(2,1,5))
    fitted_model = model.fit()

    import pickle
    pickle.dump(fitted_model,open("covidpredictor/model.sav", "wb"))

    dates = getPredictions().index
    cases = getPredictions().to_list()
    data_list=[]
    for i in range(0,len(cases)):
        data_list.append([dates[i].date().strftime('%Y-%m-%d'),cases[i]])
    result1 = data_list[0][1]
    result2 = data_list[1][1]
    result3 = data_list[2][1]
    result4 = data_list[3][1]
    result5 = data_list[4][1]
    date1 = data_list[0][0]
    date2 = data_list[1][0]
    date3 = data_list[2][0]
    date4 = data_list[3][0]
    date5 = data_list[4][0]


    return render(request, 'result.html', {'result1':result1,'result2':result2,'result3':result3,'result4':result4,'result5':result5,
    'date1':date1,'date2':date2,'date3':date3,'date4':date4,'date5':date5
    })
