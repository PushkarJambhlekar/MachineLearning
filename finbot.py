import urllib2
import urllib
import pandas as pd
import matplotlib.pyplot as plt

def getCsvUrl(sym, startDay, startMonth, startYear, endDay, endMonth,endYear):
    urlBase = "http://chart.finance.yahoo.com/table.csv?"
    vars = {'s':sym,'a':startDay,'b':startMonth,'c':startYear,'d':endDay,'e':endDay,'f':endYear}
    return urlBase + urllib.urlencode(vars)

def getCsvDataframe(sym, startDay, startMonth, startYear, endDay, endMonth,endYear):
    url = getCsvUrl(sym, startDay, startMonth, startYear, endDay, endMonth,endYear)
    return pd.io.parsers.read_csv(url, parse_dates=True, usecols=['Adj Close', 'Date'], na_values=['nan'])

symbolList = ['NVDA', 'MSFG', 'GOOG']
dfSyms = []

def initDf(startDay, startMonth, startYear, endDay, endMonth,endYear):
    global symbolList
    global dfSyms
    i = 0
    for sym in symbolList:
        dfSyms[i] = getCsvDataframe(sym, startDay, startMonth, startYear, endDay, endMonth,endYear)
        i = i+1


def normalizePrice(df):
    return df/df.ix[0,:]

def plotData(df, title='Stock prices'):
    #df = normalizePrice(df)
    ax = df.plot(title=title, fontsize = 2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()


def start():
    startDay = 1
    startMonth = 1
    startYear = 2016
    endDay = 1
    endMonth = 6
    endYear = 2017
    global symbolList

    sd = '{}-{}-{}'.format(startDay,startMonth, startYear)
    ed = '{}-{}-{}'.format(endDay,endMonth, endYear)

    dates = pd.date_range(sd,ed)
    df = pd.DataFrame({"Date":dates})
    df.set_index('Date', inplace=True)

    for sym in symbolList:
        df_temp = getCsvDataframe(sym,startDay,startMonth,startYear,endDay,endMonth,endYear)
        df_temp.set_index('Date',inplace=True)
        df_temp = df_temp.rename(columns={'Adj Close':sym})
        print df_temp.columns
        print 'Symb: ',sym
        df = df.join(df_temp, how='inner')

    print df
    plotData(df)
if __name__ == '__main__':
    start()