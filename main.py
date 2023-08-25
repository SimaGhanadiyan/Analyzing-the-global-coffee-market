import pandas as pd
import matplotlib as plt
import numpy as np

coffee_production = pd.read_csv("coffee/total-production.csv").T
coffee_production.columns = coffee_production.iloc[0]
coffee_production = coffee_production.drop("total_production")
coffee_production.head()

# Get top 10 producers
top10_producers = coffee_production.sum().sort_values(ascending=False).iloc[:10]
top10_producers.head()

# Barplot for top ten producers
fig , ax = plt.subplots(figsize=(8,8))
position = list(range(10))
labels = ['BR','VN','CO','ID','ET','MX','GT','HN','UG']
ax.bar(top10_producers.index , height = top10_producers / 1000000)
ax.set_title('Top Coffee Producing Nations 1990-2018')
ax.set_ylabel('Production (Millions 60kg Bags)" ,fontsize = 14')
ax.set_xticks(position)
ax.set_xticklabels(labels)
plt.show()


# Top 5 nation overtime
top5 = coffee_production.loc[:,['Brazil','Viet Nam','Colombia','Indonesia','Ethiopia']]
top5.index = top5.index.astype('datetime64[ns]')
top5.head()

# line chart with top 5 producers overtime
fig , ax = plt.subplots()
ax.plot(top5.index, coffee_production['Brazil'] / 1000 , label = 'Brazil')
ax.plot(top5.index, coffee_production['Viet Nam'] / 1000 , label = 'Viet Nam')
ax.plot(top5.index, coffee_production['Colombia'] / 1000 , label = 'Colombia')
ax.plot(top5.index, coffee_production['Indonesia'] / 1000 , label = 'Indonesia')
ax.plot(top5.index, coffee_production['Ethiopia'] / 1000 , label = 'Ethiopia')
fig.suptitle('Top Coffee Producing Nation 1990-2018')
ax.set_title('Viet Nam Surges to Number 2 Spot')
ax.set_ylabel('Production (Thousand 60kg Bags)')
ax.legend()
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
plt.show()

# Global total production as well as brazil's contribution to global production ovetime
brazil_vs_others = (coffee_production.assign(rest_of_world = coffee_production.drop("Brazil", axis=1).sum(axis=1)).loc[:, ["Brazil", "rest_of_world"]].astype({"Brazil": "float64"}))
brazil_vs_others

# Stacked plot
fig , ax = plt.subplots()
ax.stackplot(brazil_vs_others.index.astype('datetime64[ns]'),brazil_vs_others['Brazil'],brazil_vs_others['rest_of_world'],labels=['Brazil','World Total'])
ax.fig.suptitle("Brazil's Share of Global Coffee Production 1990-2018")
ax.set_title('Brazil Increases share of Growing Market')
ax.set_ylabel('Production (60kg Bags)', fontsize=14)
ax.legend(loc='upper left')
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
plt.show()

# Comparing Brazil's vs Veitnam's 
fig, ax = plt.subplots()
ax.scatter(coffee_production["Brazil"],coffee_production["Viet Nam"])
ax.set_title("Vietnam and Brazil Production Trend Up Together")
ax.set_ylabel("Vietnam Production (Millions 60kg Bags)")
ax.set_xlabel("Brazil Production (Millions 60kg Bags)")
plt.show()

# Compare Brazil's vs Venezuela
fig, ax = plt.subplots()
ax.scatter(coffee_production["Brazil"], coffee_production["Venezuela"])
ax.set_title("Venezuela Production Declines as Brazil Expands")
ax.set_ylabel("Venezuela Production (Millions 60kg Bags)")
ax.set_xlabel("Brazil Production (Millions 60kg Bags)")
plt.show()

# Create a pie chart with top5 producers as well as the sum for the rest of countries
coffee_production["Rest of World"] = coffee_production.drop(["Brazil","Viet Nam","Colombia", "Indonesia","Ethiopia",], axis=1).sum(axis=1)
coffee_production_top5_2018 = coffee_production.loc['2018', ["Brazil", "Viet Nam","Colombia", "Indonesia","Ethiopia","Rest of World"]]
coffee_production_top5_2018

fig , ax = plt.subplots()
ax.pie(coffee_production_top5_2018[::-1],autopct='%.0f%%',labels=list(coffee_production_top5_2018.index[::-1]),startangle=90)
fig.suptitle("share of global coffee production 2018")
plt.show()

brazil_vs_others = (coffee_production.assign(rest_of_world = coffee_production.drop("Brazil", axis=1).sum(axis=1)).loc[:, ["Brazil", "rest_of_world"]].astype({"Brazil": "float64"}))
brazil_vs_others

fig , ax = plt.subplots()
ax.pie(brazil_vs_others.iloc[0].sort_values(ascending=False),startangle=90,labels=['',''],pctdistance=.85,colors=['red','blue'])
hole=plt.Circle((0,0),0.70,fc='white')
fig=plt.gcf()

# Adding circle in pie chart
fig.gca().add_artist(hole)
plt.text(0,0,f"{round((brazil_vs_others.loc['1990', 'Brazil'] / brazil_vs_others.loc['1990'].sum()*100))}%",ha="center",va='center',fontsize=42)
ax.set_title('Brazil share of global production in 1990',fontsize=14)
plt.show()


# Grouped bar chart 
imports = pd.read_csv("coffee/imports.csv")
imports.head()

consumption = pd.read_csv("coffee/imports.csv").set_index("imports").mean(axis=1)
consumption.name = "imports"
consumption.head()

prices = pd.read_csv("coffee/retail-prices.csv")
prices.head()

prices = pd.read_csv("coffee/retail-prices.csv").set_index("retail_prices").mean(axis=1)
prices.head()

price_cons = (pd.DataFrame(prices).merge(consumption,left_on=prices.index,right_on=consumption.index,how="inner").sort_values(["imports"], ascending=False))
price_cons.columns= ["country", "Price", "Imports"]
price_cons["country"] = price_cons["country"].str.strip(" ")
price_cons

fig , ax =plt.subplots()
width =.35
x = np.arange(0,len(price_cons['country']))
# Bar1
bar1 = ax.bar(x-width/2 , price_cons['Imports'],width=width)
ax.set_title('Prices Paid Vs. Consumption of Select Importing Nations',fontsize=18,fontweight='bold')
ax.set_ylabel('Consumption (k 60kg bags)',fontsize=12)

# Bar2
ax2 = ax.twinx()
bar2 = ax2.bar(x+width/2,price_cons['Price'],width=width,color='orange')
ax2.set_ylabel('Average Price Paid Per Bag (USD)',fontsize=12)

plt.xticks(x, price_cons["country"], fontsize=7)
ax.legend([bar1, bar2], ["Consumption", "Price"])
plt.show()

