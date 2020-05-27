import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
#%matplotlib inline

to_date = lambda x: dt.strptime(x, '%m/%d/%y')

def convertToNum(s):
    if s[0] =='<':
        return int(s[1])
    else:
        return int(s)

past5 = pd.read_csv("animePast5Years.csv")
past5["Week"] = past5["Week"].apply(to_date)
past5['My Hero Academia: (United States)'] = past5['My Hero Academia: (United States)'].apply(convertToNum)


class Anime:
    def __init__(self, name, popular):
        self.title = name
        self.popularity = popular
        self.stock = 1000
    def getValue(self, date):
        return(self.popularity[date])
    def __str__(self):
        return self.title
    

class Player:
    def __init__(self, vc=150):
        self.balance = vc
        self.portfolio = {} # anime object: value
        self.purchase_history = {}
        
    def printPortfolio(self):
        for anime in self.portfolio:
            print(anime.title + ": " + str(self.portfolio[anime]))
    def buy(self, anime, number, time=Time):
        cost = number * anime.getValue(time)
        if (cost> self.balance):
            print("Not enough Virtual Currency to buy, try less")
            return None
        if(anime not in self.portfolio): # buying new stock
            print("new anime added")
            self.portfolio[anime] = number
        else: # has number of shares
            self.portfolio[anime] += number
        self.add_purchase(anime, number, time)
        self.balance -= cost
    
    def add_purchase(self, anime, num, time=Time):
        if anime not in self.purchase_history:
            self.purchase_history[anime] = []
        purchase = (num, time)
        self.purchase_history[anime].append(purchase)
    
    def sell(self, anime, number, time=Time):
        if(anime not in self.portfolio):
            print("You do not own this anime")
            return None
        elif (self.portfolio[anime] < number):
            print("Tried to sell more than owned")
            return None
        self.add_purchase(anime, -1*number, time)
        self.balance += number * anime.getValue(time)
        self.portfolio[anime] -= number  
    
    def get_net_worth(self, time=Time):
        result = self.balance
        for anime in self.portfolio:
            result += self.portfolio[anime] * anime.getValue(time)
        return(result)

    
def get_week_of(target):
    if isinstance(target, str):
        target = to_date(target)
    days = [date for date in past5["Week"] if (date.year==target.year and date.month == target.month and date.day<=target.day)]
    if (len(days)<1): # week in month before, recursively call on last day of previous month
        return get_week_of(target - timedelta(days=target.day)) # prev month
    return(max(days))