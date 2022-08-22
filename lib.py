# lib.py - Utility functions

# Importing modules
import matplotlib.pyplot as plt
import matplotlib.ticker
from glob import glob
import pandas as pd
import itertools
import datetime
import warnings
import time
import csv
import os

cwd = os.getcwd()
path = cwd + '\Stocks'
warnings.filterwarnings("ignore")

def get_id(txt):
    return txt[:-7].upper()

def make_txt(ID):
    return ID.lower()+'.us.txt'

def timer(seconds):
    return (f'Hour(s):{seconds//3600}, Minute(s):{seconds//60}, Seconds:{int(seconds) % 60}')


def convert_to_txt(travel_moves, filename):
    moves = []
    moves.append(len(travel_moves))
    for x in travel_moves:
        moves.append(str(x[0].strftime("%Y-%m-%d")) + ' ' + x[1] + ' ' + x[2] + ' ' + str(x[3]))
    df = pd.DataFrame(moves)
    df.to_csv(filename, sep = ',',
              header = None, index = None, quoting=csv.QUOTE_NONE, quotechar="",  escapechar=None)

# Restrictions

def check_buy(volume, possessed_stocks, bought, num_stocks, money, price):
    if (num_stocks > 0) and (num_stocks + bought <= int(0.1*volume)) and\
       (num_stocks+bought <= possessed_stocks +1) and \
    (money > num_stocks * price):
        return True
    else:
        return False

def check_sell(volume,possessed_stocks, sold, num_stocks, bought):
    if (num_stocks > 0) and (num_stocks + sold <= int(0.1*volume)) and\
       (sold+num_stocks<=possessed_stocks+bought):
        return True
    else:
        return False


""" The following class
keeps track of all our information, records moves,
calculates the portfolio, balance and performs the basic
operations and intra day moves"""
class tracking():
    def __init__(self, portfolio):
        # These two variables keep track of our history moves/stocktaking
        self.moves = [] # History of moves
        self.time_stocktaking = [] # Our stocktaking for each day
        self.money_per_day = []
        
        # The variables below keep track of daily information
        self.portfolio = portfolio # Dict containing information about all stocks
        self.money = 1 # Our money, we start with 1 dollar
        self.stocks_of_the_day =set()
        self.owned_stocks = set()
        
        # Booleans to control actions
        self.mid_action = False
        self.intra_moves = 0 
        
    def cal_portfolio(self,date):
        sum = 0
        for stock in self.owned_stocks:
            sum += round(self.portfolio[stock]['number of stocks'] * self.portfolio[stock]['close price'],5)
            sum = round(sum, 5)
        self.time_stocktaking.append((date, round(sum+self.money,3)))
        self.money_per_day.append((date, self.money))
    
    def cal_number_of_stocks(self, date): # Use this before cal_portfolio
        for stock in self.owned_stocks:
            self.portfolio[stock]['number of stocks'] += self.portfolio[stock]['bought']
            self.portfolio[stock]['number of stocks'] -= self.portfolio[stock]['sold']
    
    def sell_all_stocks(self,date):
        for stock in self.owned_stocks:
            txt = make_txt(stock)
            df = pd.read_csv(os.path.join(path,txt), parse_dates = ['Date'])
            df = df[df['Date'] == date]
            try:
                if check_sell(int(df['Volume']), self.portfolio[stock]['number of stocks'], 
                         self.portfolio[stock]['sold'], self.portfolio[stock]['number of stocks'],
                              self.portfolio[stock]['bought']):
                    self.sell_high(date, stock, float(df['High']), self.portfolio[stock]['number of stocks'],
                                  float(df['Close']), int(df['Volume']))
                    self.portfolio[stock]['action'] = 'sell high'
            except:
                pass
            
        
    
    def clear_daily_stock_info(self): # Use this after cal_portfolio
        for stock in self.stocks_of_the_day:
            self.portfolio[stock]['bought'] = 0
            self.portfolio[stock]['sold'] = 0
            self.stocks_of_the_day = set()
            self.portfolio[stock]['action'] = None
            self.portfolio[stock]['intra'] = False
            self.mid_action = False
    
    # BASIC OPERATIONS
    def buy_open(self, date, stock, price, num_stocks, close_price, volume):
        if check_buy(volume, self.portfolio[stock]['number of stocks'],
                    self.portfolio[stock]['bought'], num_stocks, self.money, price):
            self.money -=price * num_stocks
            self.money = round(self.money,5)
            self.portfolio[stock]['close price']=round(close_price,5)
            self.portfolio[stock]['bought']+=num_stocks
            self.moves.append([date, 'buy-open', stock, num_stocks])
            self.stocks_of_the_day.add(stock)
            self.owned_stocks.add(stock)
            self.portfolio[stock]['last buy'] = price
            self.portfolio[stock]['action'] = 'buy open'
            self.portfolio[stock]['moves']+=1
    
    def sell_open(self, date, stock, price, num_stocks, close_price,volume):
        if check_sell(volume, self.portfolio[stock]['number of stocks'], 
                     self.portfolio[stock]['sold'], num_stocks, self.portfolio[stock]['bought']):
            self.money += num_stocks * price
            self.money = round(self.money,5)
            self.portfolio[stock]['close price']=round(close_price,5)
            self.portfolio[stock]['sold']+=num_stocks
            self.moves.append([date, 'sell-open', stock, num_stocks])
            self.stocks_of_the_day.add(stock)
            self.portfolio[stock]['action'] = 'sell open'
            self.portfolio[stock]['moves']+=1
        
    def buy_low(self, date, stock, price, num_stocks, close_price, volume, mid_action = False):
        if check_buy(volume, self.portfolio[stock]['number of stocks'],
                    self.portfolio[stock]['bought'], num_stocks, self.money, price):
            self.money -=price * num_stocks
            self.portfolio[stock]['close price']= close_price
            self.portfolio[stock]['bought']+=num_stocks
            self.moves.append([date, 'buy-low', stock, num_stocks])
            self.stocks_of_the_day.add(stock)
            self.owned_stocks.add(stock)
            self.portfolio[stock]['last buy'] = price
            self.portfolio[stock]['action'] = 'buy low'
            self.portfolio[stock]['moves']+=1
            self.mid_action = mid_action
        
    def sell_high(self, date, stock, price, num_stocks, close_price, volume, mid_action = False):
        if check_sell(volume, self.portfolio[stock]['number of stocks'], 
                     self.portfolio[stock]['sold'], num_stocks, self.portfolio[stock]['bought']):
            self.money += num_stocks * price
            self.money = round(self.money,5)
            self.portfolio[stock]['close price']=round(close_price,5)
            self.portfolio[stock]['sold']+=num_stocks
            self.moves.append([date, 'sell-high', stock, num_stocks])
            self.stocks_of_the_day.add(stock)
            self.portfolio[stock]['action'] = 'sell high'
            self.portfolio[stock]['moves']+=1
            self.mid_action = mid_action
        
    def buy_close(self, date, stock, price, num_stocks, close_price, volume):
        if check_buy(volume, self.portfolio[stock]['number of stocks'],
                    self.portfolio[stock]['bought'], num_stocks, self.money, price):
            self.money -=price * num_stocks
            self.money = round(self.money,5)
            self.portfolio[stock]['close price']=round(close_price,5)
            self.portfolio[stock]['bought']+=num_stocks
            self.moves.append([date, 'buy-close', stock, num_stocks])
            self.stocks_of_the_day.add(stock)
            self.owned_stocks.add(stock)
            self.portfolio[stock]['last buy'] = price
            self.portfolio[stock]['action'] = 'buy close'
            self.portfolio[stock]['moves']+=1
    
    def sell_close(self, date, stock, price, num_stocks, close_price, volume):
        if check_sell(volume, self.portfolio[stock]['number of stocks'], 
                     self.portfolio[stock]['sold'], num_stocks, self.portfolio[stock]['bought']):
            self.money += num_stocks * price
            self.money = round(self.money,5)
            self.portfolio[stock]['close price']=round(close_price,5)
            self.portfolio[stock]['sold']+= num_stocks
            self.moves.append([date, 'sell-close', stock, num_stocks])
            self.stocks_of_the_day.add(stock)
            self.portfolio[stock]['action'] = 'sell close'
            self.portfolio[stock]['moves']+=1
        
        
    # INTRA DAY TRADING FUNCTIONS
    
    def intra_open_high(self, date, stock, intra_stocks, Open, High, Close, Volume):
        if check_buy(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['bought'],
                intra_stocks, self.money, Open) and \
        check_sell(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['sold'],
                  intra_stocks, self.portfolio[stock]['bought']+intra_stocks):
            self.buy_open(date, stock, Open, intra_stocks, Close, Volume)
            self.sell_high(date, stock, High, self.portfolio[stock]['bought'], Close, Volume)
            self.portfolio[stock]['intra'] = True
            self.portfolio[stock]['moves']+=2
            self.portfolio[stock]['action'] = 'sell high'
            self.intra_moves+=1
    
    def intra_high_close(self, date, stock, intra_stocks, High, Close, Volume):
        if check_sell(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['sold'],
                     intra_stocks, self.portfolio[stock]['bought']) and \
        check_buy(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['bought'],
                 intra_stocks, self.money, Close):
            self.sell_high(date, stock, High, intra_stocks, Close, Volume)
            self.buy_close(date, stock, Close, intra_stocks, Close, Volume)
            self.portfolio[stock]['intra'] = True
            self.portfolio[stock]['moves']+=2
            self.portfolio[stock]['action'] = 'buy close'
            self.intra_moves+=1
        
    def intra_open_low(self, date, stock, intra_stocks, Open, Low, Close, Volume):
        if check_sell(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['sold'],
                     intra_stocks, self.portfolio[stock]['bought']) and \
        check_buy(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['bought'],
                 intra_stocks, self.money, Close):
            self.sell_open(date, stock, Open, intra_stocks, Close, Volume)
            self.buy_low(date, stock, Low, intra_stocks, Close, Volume)
            self.portfolio[stock]['intra'] = True
            self.portfolio[stock]['moves']+=2
            self.portfolio[stock]['action'] = 'buy low'
            self.intra_moves+=1
            
    def intra_close_low(self, date, stock, intra_stocks, Close, Low, Volume):
        if check_buy(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['bought'],
                intra_stocks, self.money, Low) and \
        check_sell(Volume, self.portfolio[stock]['number of stocks'], self.portfolio[stock]['sold'],
                  intra_stocks, self.portfolio[stock]['bought']+intra_stocks):
            self.buy_low(date, stock, Low, intra_stocks, Close, Volume)
            self.sell_close(date, stock, Close, intra_stocks, Close, Volume)
            self.portfolio[stock]['intra'] = True
            self.portfolio[stock]['moves']+=2
            self.portfolio[stock]['action'] = 'sell close'
            self.intra_moves+=1
    
    # FOR PLOTTING
    
    def portfolio_plot(self):
        dates = []
        portfolio = []
        balance = []
        for i,date in enumerate(self.money_per_day):
            dates.append(date[0])
            portfolio.append(self.time_stocktaking[i][1])
            balance.append(self.money_per_day[i][1])
        
        fig, ax = plt.subplots(figsize = (10,7))
        
        ax.step(dates,balance, label = 'balance')
        ax.step(dates, portfolio, label = 'portfolio')
        ax.set_yscale('log')
        logfmt = matplotlib.ticker.LogFormatterExponent(base=10.0, labelOnlyBase=True)
        ax.yaxis.set_major_formatter(logfmt)
        ax.set_ylabel("$10^x$")
        ax.fill_between(dates , balance , step="pre")
        ax.fill_between(dates , portfolio , balance)
        ax.set_title('Valuation')
        ax.legend()
        plt.savefig('asd.png')
        plt.show()


def generate_dataframe(companies):
    df = pd.DataFrame()
    for company in companies:
        
        df_temp = pd.read_csv(os.path.join(path, make_txt(company)), parse_dates = ['Date'])
        df_temp['ID'] = company
        
        high_low = (df_temp['High'] - df_temp['Low']).max()
        total_days = int(df_temp.shape[0])
        Open_low = (df_temp['Open']-df_temp['Low']).max()
        High_open = (df_temp['High']-df_temp['Open']).max()
        Close_low =(df_temp['Close']-df_temp['Low']).max()
        High_close = (df_temp['High']- df_temp['Close']).max()
        Minimum_val = df_temp['Low'].min()
        Max_val = df_temp['High'].max()
        
        df_temp['Max_val'] = Max_val
        df_temp['Min_val'] = Minimum_val
        df_temp['high_low'] = high_low
        df_temp['open_low'] = Open_low
        df_temp['close_low'] = Close_low
        df_temp['total_days'] = int(total_days)
        df_temp['high_open'] = High_open
        df_temp['high_close'] = High_close
        df_temp['days'] = range(1, total_days+1)
        df_temp['life span'] = df_temp['days']/total_days
        
        for year in range(1962,2018):
            year1 = pd.Timestamp(str(year))
            year2 = pd.Timestamp(str(year+1))

            start_year = df_temp['Date'] >= year1
            end_year = df_temp['Date']< year2
            indices = start_year & end_year
            
            df_temp.loc[indices, 'mean_high'] = df_temp.loc[indices]['High'].sum()/df_temp[indices].shape[0]
            df_temp.loc[indices, 'mean_low'] = df_temp.loc[indices]['Low'].sum()/df_temp[indices].shape[0]
        
        df = pd.concat([df, df_temp])
    
    return df

def initialize_portfolio(companies):
    portfolio = {}
    for company in companies:
        portfolio[company] = {} 
        portfolio[company]['number of stocks'] = 0
        portfolio[company]['close price'] = 0
        portfolio[company]['bought'] = 0
        portfolio[company]['sold'] = 0
        portfolio[company]['action'] = None
        portfolio[company]['intra'] = False
        portfolio[company]['moves'] = 0
    
    return portfolio

# Strategy functions

def sell_high(time_travel, df_company, current_day ,company, life_span_factor =0.9, early_sell_factor = 2, early_sell_volume =0.5,
             late_sell_factor = 1.5, late_sell_volume = 0.8):
    if float(df_company['life span'])<=life_span_factor and\
    float(df_company['High'])>=early_sell_factor*float(df_company['mean_high']):
        time_travel.sell_high(current_day, company, float(df_company['High']),
                             max(int(early_sell_volume*time_travel.portfolio[company]['number of stocks']),1),
                              float(df_company['Close']), int(df_company['Volume']),True)
    
    elif float(df_company['life span'])>life_span_factor and\
    float(df_company['High'])>=late_sell_factor*float(df_company['mean_high']):
        time_travel.sell_high(current_day, company, float(df_company['High']),
                             max(int(late_sell_volume*time_travel.portfolio[company]['number of stocks']),1),
                             float(df_company['Close']), int(df_company['Volume']),True)
        

def buy_low(time_travel, df_company, current_day, company,
            life_span_factor = 0.8, early_buy_factor = 1.3, late_buy_factor = 0.90):
    if float(df_company['life span'])<=life_span_factor and\
    float(df_company['Low'])<=early_buy_factor*float(df_company['mean_low']) and\
    time_travel.mid_action == False:
        time_travel.buy_low(current_day, company, float(df_company['Low']),
                           time_travel.portfolio[company]['number of stocks']+1,
                           float(df_company['Close']), int(df_company['Volume']), True)
        
    elif float(df_company['life span'])>life_span_factor and\
    float(df_company['Low'])<=late_buy_factor*float(df_company['mean_low']) and \
    time_travel.mid_action == False:
        time_travel.buy_low(current_day, company, float(df_company['Low']),
                           time_travel.portfolio[company]['number of stocks']+1,
                           float(df_company['Close']), int(df_company['Volume']), True)
        
def intra_day(time_travel, df_company, current_day, company, intra_day_factor = 0.95):
    
    max_val = max([(float(df_company['High'])-float(df_company['Close'])),
                  (float(df_company['High'])-float(df_company['Open'])),
                  (float(df_company['Close']) - float(df_company['Low'])),
                  (float(df_company['Open'])-float(df_company['Low']))])
    
    if time_travel.portfolio[company]['action'] != 'buy low' and \
    time_travel.portfolio[company]['action'] != 'sell high' and time_travel.portfolio[company]['intra'] == False and \
    (float(df_company['High'])-float(df_company['Close']))>=max(intra_day_factor*float(df_company['high_close']),max_val):
        
        time_travel.intra_high_close(current_day, company,
                                    time_travel.portfolio[company]['number of stocks'],
                                    float(df_company['High']), float(df_company['Close']),
                                    int(df_company['Volume']))
    
    if time_travel.portfolio[company]['action'] != 'buy open' and time_travel.portfolio[company]['action']!='sell open'\
    and time_travel.portfolio[company]['action']!='sell high' and time_travel.portfolio[company]['action']!='buy low' and\
    time_travel.portfolio[company]['intra'] == False and (float(df_company['High'])-float(df_company['Open']))>=\
    max(intra_day_factor*float(df_company['high_open']), max_val):
        
        time_travel.intra_open_high(current_day, company, time_travel.portfolio[company]['number of stocks'],
                                   float(df_company['Open']), float(df_company['High']),
                                   float(df_company['Close']), int(df_company['Volume']))

    if time_travel.portfolio[company]['action']!= 'buy low' and time_travel.portfolio[company]['action']!= 'sell high'\
    and time_travel.portfolio[company]['action']!= 'buy close' and time_travel.portfolio[company]['action']!='sell close'\
    and time_travel.portfolio[company]['intra'] == False and (float(df_company['Close']) - float(df_company['Low']))>=\
    max(intra_day_factor*float(df_company['close_low']),max_val):
        
        time_travel.intra_close_low(current_day, company, time_travel.portfolio[company]['number of stocks'],
                                   float(df_company['Close']), float(df_company['Low']), int(df_company['Volume']))
    
    
    if time_travel.portfolio[company]['action'] != 'buy low' and time_travel.portfolio[company]['action']!='sell high'\
    and time_travel.portfolio[company]['action']!= 'buy open' and time_travel.portfolio[company]['action']!= 'sell open'\
    and time_travel.portfolio[company]['intra'] == False and (float(df_company['Open'])-float(df_company['Low'])) >=\
    max(intra_day_factor*float(df_company['open_low']),max_val):
        
        time_travel.intra_open_low(current_day, company, time_travel.portfolio[company]['number of stocks'],
                                  float(df_company['Open']), float(df_company['Low']), float(df_company['Close']),
                                  int(df_company['Close']))



def trading_loop(time_travel, companies, N = 1000000, sales_margin = 2, life_span_factor_sell = 0.95,
                life_span_factor_buy = 0.95, intra_days = 80, early_buy_factor = 1.4,
                late_buy_factor = 0.98, early_sell_factor = 1, early_sell_volume = 0.3,
                late_sell_factor = 1.3, late_sell_volume = 0.7, intra_day_factor = 1e-7):
    
    # Preparing the data
    df = generate_dataframe(companies)
    df.sort_values(by = ['Date', 'Max_val'], ascending = [True, False], inplace = True)
    moves_per_company = N // len(companies) - sales_margin
    portfolio = initialize_portfolio(companies)
    time_travel = tracking(portfolio)
    start_date = pd.Timestamp('1960-01-01')
    end_date = pd.Timestamp('2017-11-10')
    step = datetime.timedelta(days = 1)
    
    current_day = start_date
    
    while current_day <= end_date:

        df_day = df[df['Date'] == current_day]
        companies = list(df_day['ID'])      

        if current_day <= end_date - datetime.timedelta(days = len(companies)*sales_margin) -\
        datetime.timedelta(days = intra_days):

            if len(companies) > 1:
                for company1, company2 in itertools.combinations(companies, 2): # company1 has higher priority than company2
                    df_company1 = df_day[df_day['ID'] == company1]
                    df_company2 = df_day[df_day['ID'] == company2]

                    time_travel.portfolio[company1]['close price'] = float(df_company1['Close'])
                    time_travel.portfolio[company2]['close price'] = float(df_company2['Close'])

                    # Interaction between company 1 and company 2
                    if time_travel.portfolio[company1]['action'] == None and \
                    time_travel.portfolio[company2]['action'] == None and \
                    max(time_travel.portfolio[company1]['moves'], time_travel.portfolio[company2]['moves'])<moves_per_company:

                        if time_travel.portfolio[company2]['number of stocks'] > 0 and\
                        ((time_travel.money + float(df_company2['Open'])*(time_travel.portfolio[company1]['number of stocks']+1))\
                           >(time_travel.portfolio[company1]['number of stocks']+1)*float(df_company1['Low'])):

                            time_travel.sell_open(current_day, company2, float(df_company2['Open']),
                                                 time_travel.portfolio[company1]['number of stocks']+1,
                                                 float(df_company2['Close']), int(df_company2['Volume']))

                            time_travel.buy_low(current_day, company1, float(df_company1['Low']),
                                               time_travel.portfolio[company1]['number of stocks']+1,
                                               float(df_company1['Close']), int(df_company1['Volume']))


            for company in companies:
                df_company = df_day[df_day['ID'] == company]
                time_travel.portfolio[company]['close price'] = float(df_company['Close'])

                if time_travel.portfolio[company]['action'] == None and \
                time_travel.portfolio[company]['moves']<moves_per_company and time_travel.mid_action == False:

                    sell_high(time_travel, df_company, current_day, company, life_span_factor_sell, early_sell_factor,
                             early_sell_volume, late_sell_factor, late_sell_volume)

                    buy_low(time_travel, df_company, current_day, company, life_span_factor_buy,
                           early_buy_factor, late_buy_factor)

                    intra_day(time_travel, df_company, current_day, company, intra_day_factor)


        elif current_day <=end_date - datetime.timedelta(days = len(companies)*sales_margin):

            for company in companies:
                df_company = df_day[df_day['ID'] == company]
                time_travel.portfolio[company]['close price'] = float(df_company['Close'])

                if time_travel.portfolio[company]['action'] == None and \
                time_travel.portfolio[company]['moves']<moves_per_company and time_travel.mid_action == False:
                    intra_day(time_travel, df_company, current_day, company, intra_day_factor)


        else: # sales period

            time_travel.sell_all_stocks(current_day)

        # Refresh all info in wallet just before the end of current day

        time_travel.cal_number_of_stocks(current_day)
        time_travel.cal_portfolio(current_day)
        time_travel.clear_daily_stock_info()

        current_day+=step
        
    return time_travel

    
