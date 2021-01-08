import json
import pandas as pd
import datetime as dt
import calendar
import matplotlib.pyplot as plt


with open('message.json', encoding = 'utf8') as f:
    data = json.load(f)

# keep only created at as we aren't
# analyzing the text or who sent them
ids = []
for p_id in data:
    ids.append([p_id['created_at']])

df = pd.DataFrame(ids[1:])
df.columns = ['time']
df['time'] = pd.to_datetime(df['time'], unit = 's')

# convert year data to pandas df, clean_data

def df_creator(df, year):
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df = df[(df['time'] >= '%s-01-01 00:00:00' % year)
    & (df['time'] <= '%s-12-31 23:59:59' % year)]
    df['month'] = df['time'].dt.month
    return(df)

df_2020 = df_creator(df, '2020')
df_2019 = df_creator(df, '2019')

# Get num of messages per month in a vector
def get_total(df):
    values = []
    for i in range(1,13):
        values.append(len(df[df['month'] == i]))
    return(values)

data_2020 = get_total(df_2020)
data_2019 = get_total(df_2019)

# get list of months for x - axis
df_months = pd.Series([1,2,3,4,5,6,7,8,9,10,11,12])
df_months = df_months.apply(lambda x: calendar.month_abbr[x])
months = df_months.values.tolist()

clean_df = pd.DataFrame({'2019': data_2019,
    '2020': data_2020}, 
    index = months)

ax = clean_df.plot.bar(rot = 0, title = "Covid-19 Effect on Fraternity Groupchat",
    color = ['#dc5538','#3cbabd'])
ax.set_xlabel('Month')
ax.set_ylabel('# of Messages')
plt.show()