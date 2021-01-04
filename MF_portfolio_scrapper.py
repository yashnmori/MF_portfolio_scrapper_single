#author: YashnMori

#Importing necessary libs
import requests
import bs4
import csv
import pandas as pd
import matplotlib.pyplot as plt

res = requests.get('https://www.moneycontrol.com/mutual-funds/canara-robeco-blue-chip-equity-fund-regular-plan/portfolio-holdings/MCA174')

soup = bs4.BeautifulSoup(res.text,'lxml')


# # Method 1
file= open('axisltefportfolio.csv','w', newline='')
writer=csv.writer(file)

writer.writerow([soup.find('title').text])
writer.writerow(['Name','Sector','Value(Mn)','% of Total Holdings','Quantity','Mcap'])


eco_table = soup.find('table', id='equityCompleteHoldingTable')
for table in eco_table.find_all('tbody'):
    rows= table.find_all('tr')
    for row in rows:
        new_table=row.find_all('td')[0].text.strip()
        table_sector= row.find_all('td')[1].text.strip()
        table_value=row.find_all('td')[3].text.strip()
        table_holding=row.find_all('td')[4].text.strip()
        table_holdingquantity=row.find_all('td')[8].text.strip()
        table_size=row.find_all('td')[10].text.strip()
        print (new_table,',', table_sector,",",table_value,",",table_holding,",",table_holdingquantity,",",table_size)
        writer.writerow([new_table,table_sector,table_value,table_holding,table_holdingquantity,table_size])     
        
file.close()


#to check csv contents
csv_df = pd.read_csv('axisltefportfolio.csv',header=1,encoding='cp1252')
csv_df

#new_ df for pie chart
csv_pie_df = pd.DataFrame (csv_df, columns = ['Name','% of Total Holdings','Mcap'])
#renaming df
csv_pie_df = csv_pie_df.rename(columns={'Name': 'Stocks', '% of Total Holdings': 'Percentage_Holdings', 'Mcap':'Mcap'})
csv_pie_df.head()


#converting percentage into float datatype
csv_pie_df['Percentage_Holdings'] = csv_pie_df['Percentage_Holdings'].str.rstrip('%').astype('float') / 100.0
                                                                #^ use str funcs to elim '%'   ^ divide by 100



#Sum of all percentages after top 10 stocks
csv_others = csv_pie_df[10:]
csv_sum_others = csv_others.sum(axis = 0, skipna = True)
csv_sum_others


#slicing the dataframe
newcsv_pie_df = csv_pie_df
newcsv_pie_df = csv_pie_df.drop(csv_df.index[10:])
newcsv_pie_df



csvothers_row = {'Stocks':'Others', 'Percentage_Holdings': csv_sum_others.Percentage_Holdings }
#append row to the dataframe
newcsv_pie_df = newcsv_pie_df.append(csvothers_row, ignore_index=True)
newcsv_pie_df


explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.15)
plt.pie(newcsv_pie_df["Percentage_Holdings"], labels = newcsv_pie_df["Stocks"],radius = 1.2,autopct='%1.1f%%',pctdistance=0.85, explode = explode)
plt.title('Mutual Fund Portfolio')
plt.axis('equal')


#draw circle
centre_circle = plt.Circle((0,0),0.80,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
#ax1.axis('equal')  
#plt.tight_layout()
plt.show()


# # METHOD 2

table = soup.find_all('table', id='equityCompleteHoldingTable')
df = pd.read_html(str(table))[0]

#selection of variables
new_df = df[["Stock Invested in","Sector","Value(Mn)","% of Total Holdings","Quantity","M-Cap"]]

#saving new file
new_df.to_csv (r'F:\New folder\export_dataframe.csv', index = False, header=True)
new_df


#new_ df for pie chart
pie_df = pd.DataFrame (new_df, columns = ['Stock Invested in','% of Total Holdings','M-Cap'])
#renaming df
pie_df = pie_df.rename(columns={'Stock Invested in': 'Stocks', '% of Total Holdings': 'Percentage_Holdings', 'M-Cap':'Market Cap'})
pie_df.head()


#converting percentage into float datatype
pie_df['Percentage_Holdings'] = pie_df['Percentage_Holdings'].str.rstrip('%').astype('float') / 100.0
                                                                #^ use str funcs to elim '%'   ^ divide by 100


#Sum of all percentages after top 10 stocks
others = pie_df[10:]
sum_others = others.sum(axis = 0, skipna = True)
sum_others


#slicing the dataframe
new_pie_df = pie_df
new_pie_df = pie_df.drop(df.index[10:])
new_pie_df


others_row = {'Stocks':'Others', 'Percentage_Holdings': sum_others.Percentage_Holdings, 'Market Cap': 'Other' }
#append row to the dataframe
new_pie_df = new_pie_df.append(others_row, ignore_index=True)

new_pie_df


explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.15)
plt.pie(new_pie_df["Percentage_Holdings"], labels = new_pie_df["Stocks"],radius = 1.2,autopct='%1.1f%%',pctdistance=0.85, explode = explode)
plt.title('Mutual Fund Portfolio')
plt.axis('equal')


#draw circle
centre_circle = plt.Circle((0,0),0.80,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
#ax1.axis('equal')  
#plt.tight_layout()
plt.show()
