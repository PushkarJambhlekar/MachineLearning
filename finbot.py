#import urllib2
import urllib
import pandas as pd
import matplotlib.pyplot as plt

def getCsvUrl(sym, startDay, startMonth, startYear, endDay, endMonth, endYear):
    urlBase = "http://chart.finance.yahoo.com/table.csv?"
    vars = {'s':sym,'a':startDay,'b':startMonth,'c':startYear,'d':endDay,'e':endDay,'f':endYear}
    return urlBase + urllib.parse.urlencode(vars)

def getCsvDataframe(sym, startDay, startMonth, startYear, endDay, endMonth, endYear):
    url = getCsvUrl(sym, startDay, startMonth, startYear, endDay, endMonth, endYear)
    return pd.io.parsers.read_csv(url, parse_dates=True, usecols=['Adj Close', 'Date'], na_values=['nan'])

symbolList = ['NVDA', 'MSFG', 'GOOG']
dfSyms = []

def initDf(startDay, startMonth, startYear, endDay, endMonth, endYear):
    global symbolList
    global dfSyms
    i = 0
    for sym in symbolList:
        dfSyms[i] = getCsvDataframe(sym, startDay, startMonth, startYear, endDay, endMonth, endYear)
        i = i+1


def normalizePrice(df):
    return df/df.ix[0, :]

def plotData(df, title='Stock prices'):
    tdf = normalizePrice(df)
    print("df: ", tdf.ix[0:1,:])
    ax = tdf.plot(title=title, fontsize = 2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def get_bollinger_band(rm, rmStd):
    upperB = rm + 2*rmStd
    lowerB = rm - 2*rmStd
    return upperB, lowerB

def globalStats(df, sym):
    ax = df[sym].plot(title='Rolling mean', label=sym)
    
    rmSym = pd.rolling_mean(df[sym],window=20)
    rmStd = pd.rolling_std(df[sym],window=20)
    upperB,lowerB = get_bollinger_band(rmSym, rmStd)

    rmSym.plot(title='Sym rolling mean', ax=ax)
    upperB.plot(title='upperB', ax=ax)
    lowerB.plot(title='lowerB', ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='Upper left')

    plt.show()

def start():
    startDay = 1
    startMonth = 1
    startYear = 2016
    endDay = 1
    endMonth = 6
    endYear = 2017
    global symbolList

    sd = '{}-{}-{}'.format(startDay, startMonth, startYear)
    ed = '{}-{}-{}'.format(endDay, endMonth, endYear)

    dates = pd.date_range(sd, ed)
    df = pd.DataFrame({"Date":dates})
    df.set_index('Date', inplace=True)

    for sym in symbolList:
        df_temp = getCsvDataframe(sym, startDay, startMonth, startYear, endDay, endMonth, endYear)
        df_temp.set_index('Date', inplace=True)
        df_temp = df_temp.rename(columns={'Adj Close':sym})
        print (df_temp.columns)
        print ('Symb: ',sym)
        globalStats(df_temp,sym)
        df = df.join(df_temp, how='inner')

    print (df)
    #plotData(df)

if __name__ == '__main__':
    start()