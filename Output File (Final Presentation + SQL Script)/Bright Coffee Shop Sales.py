
# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt           
import seaborn as sns                     
import plotly.express as px   


# Importing Data
df=pd.read_excel("/content/drive/MyDrive/Data Analytics/Bright Coffee Shop/Bright Coffee Shop Sales.xlsx")
display(df)


# Exploratory Data Analysis
df.shape
df.columns
df.duplicated().sum()
df.info()
df.describe()
df.isnull().sum()


##____________________________________________________________________________________________________________________________________

# ANALYSIS


## Calculating Revenue
df['total_amount']=df['transaction_qty']*df['unit_price']


## Bucketing Time

#### Defining time buckets
def time_bucket(t):
  hour = t.hour
  if 5 <= hour < 12:
    return 'Morning'
  elif 12 <= hour < 17:
    return 'Afternoon'
  elif 17 <= hour < 22:
    return 'Evening'
  else:
    return 'Night'

### Applying the time_bucket function on transaction time
df['time_bucket'] = df['transaction_time'].apply(time_bucket)



## Creating Month Name and Day Name
df['day_of_week'] = pd.to_datetime(df['transaction_date']).dt.day_name()
df['day_of_week_num'] = pd.to_datetime(df['transaction_date']).dt.dayofweek
df['Month'] = pd.to_datetime(df['transaction_date']).dt.month_name()
df['Month_num'] = pd.to_datetime(df['transaction_date']).dt.month


##____________________________________________________________________________________________________________________________________


# VITUALIZING


## Revenue per Month

### Group revenue by month
grouped = df.groupby(['Month_num','Month'])['total_amount'].sum().reset_index()

plt.figure(figsize=(10, 5))
bars = plt.bar(grouped['Month'], grouped['total_amount'])

### Add data label
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'R{height:.0f}', ha='center', va='bottom', fontsize = 10)

### Labels and formatting
plt.xlabel('Month')
plt.ylabel('Revenue (R)')
plt.title('Total Revenue by Month')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



## Revenue per Day of Week

### Group revenue by day name
grouped = df.groupby(['day_of_week_num','day_of_week'])['total_amount'].sum().reset_index()

### Calculate percentage of total
grouped['percentage'] = grouped['total_amount'] / grouped['total_amount'].sum() * 100

### Plot the graph
plt.figure(figsize=(10, 5))
bars = plt.bar(grouped['day_of_week'], grouped['percentage'], color = 'mediumseagreen')

### Add % label on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}%', ha='center', va='bottom', fontsize = 10)

### Labels and formatting
plt.xlabel('day of week')
plt.ylabel('% of Total Revenue')
plt.title('Total Revenue by day of week')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



## Revenue per Product Category

### Group by Product Category
grouped = df.groupby(['product_category'])['total_amount'].sum().reset_index()

### Calculate percentage of total
grouped['percentage'] = grouped['total_amount'] / grouped['total_amount'].sum() * 100

### Sort by percentage
grouped = grouped.sort_values('percentage', ascending=False)

### Plot the graph
plt.figure(figsize=(10, 5))
bars = plt.bar(grouped['product_category'], grouped['percentage'], color = 'mediumseagreen')

### Add % label on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}%', ha='center', va='bottom', fontsize = 10)

### Labels and formatting
plt.xlabel('product category')
plt.ylabel('% of Total Revenue')
plt.title('Total Revenue by product category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



## Revenue per Product Type for the Top 2 product categories

### Find the top 2 product caregories
 top_categories = df.groupby(['product_category'])['total_amount'].sum().sort_values(ascending=False).head(2).index
 
### Filter for only top 2 categories
 Filtered_df = df[df['product_category'].isin(top_categories)]

### Group product type within filtered data - This gives product type for the only top 2 product categories
 grouped = Filtered_df.groupby(['product_type'])['total_amount'].sum().reset_index()

### Calculate percentage of total
grouped['percentage'] = grouped['total_amount'] / grouped['total_amount'].sum() * 100

### Sort by percentage
grouped = grouped.sort_values('percentage', ascending=False)

### Plot the graph
plt.figure(figsize=(10, 5))
bars = plt.bar(grouped['product_type'], grouped['percentage'], color = 'mediumseagreen')

### Add % label on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}%', ha='center', va='bottom', fontsize = 10)

### Labels and formatting
plt.xlabel('product type')
plt.ylabel('% of Total Revenue')
plt.title('Total Revenue by product type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



## % Revenue per Store per Time
 
### Group by store location and time bucket, and then pivot
pivot_df = df.groupby(['store_location', 'time_bucket'])['total_amount'].sum().unstack(fill_value=0)  # makes time_bucket values into columns

### Covert to % of the total per location
percent_df = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

    
### Plot
fig, ax = plt.subplots(figsize=(10, 6))
bottom = pd.Series([0] * len(percent_df), index=percent_df.index)

colors = plt.get_cmap('tab10').colors
for i, col in enumerate(percent_df.columns):
    bars = ax.bar(percent_df.index, percent_df[col], bottom=bottom, label=col, color=colors[i % len(colors)])
    
    # Add % labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:  # Only label non-zero
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2,
                    f"{height:.1f}%", ha='center', va='center', fontsize=9, color='white')
    
    bottom += percent_df[col]

### Format
plt.xlabel('Store Location')
plt.ylabel('Revenue')
plt.title('Sales by Store Location and Time Bucket')
plt.legend(title='Time Bucket')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



## %Revenue Breakdown per Location

### Group revenue by location
revenue_by_location = df.groupby('store_location')['total_amount'].sum()

### Plot pie chart
plt.figure(figsize=(8, 6))
plt.pie(revenue_by_location, labels=revenue_by_location.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
plt.title('Revenue Distribution by Store Location')
plt.axis('equal')  # Ensures pie is a circle
plt.tight_layout()
plt.show()



## Total Revenue per Location

### Group revenue by location
grouped = df.groupby(['store_location'])['total_amount'].sum().reset_index()

### Sort by percentage
grouped = grouped.sort_values('total_amount', ascending=False)

### Plot the graph
plt.figure(figsize=(10, 5))
bars = plt.bar(grouped['store_location'], grouped['total_amount'], color = 'mediumseagreen')

### Add % label on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'R{height:.0f}', ha='center', va='bottom', fontsize = 10)

### Labels and formatting
plt.xlabel('Store Location')
plt.ylabel('Total Revenue (R)')
plt.title('Total Revenue by Store Location')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

