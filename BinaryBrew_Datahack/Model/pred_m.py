import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

train_dataset = pd.read_csv("train_data.csv")
test_dataset = pd.read_csv("test_data.csv")
train_dataset = train_dataset.iloc[:,0:]
train_dataset = train_dataset[train_dataset['Engine'].notna()]
train_dataset = train_dataset[train_dataset['Power'].notna()]
train_dataset = train_dataset[train_dataset['Seats'].notna()]
missing_indexes = train_dataset[train_dataset.isnull().any(axis=1)].index.tolist()
train_dataset = train_dataset.reset_index(drop=True)
for i in range(train_dataset.shape[0]):
    train_dataset.at[i, 'Company'] = train_dataset['Name'][i].split()[0]
    train_dataset.at[i, 'Mileage(km/kg)'] = str(train_dataset['Mileage'][i]).split()[0]
    train_dataset.at[i, 'Engine(CC)'] = str(train_dataset['Engine'][i]).split()[0]
    train_dataset.at[i, 'Power(bhp)'] = (train_dataset['Power'][i]).split()[0]
    
train_dataset['Mileage(km/kg)'] = train_dataset['Mileage(km/kg)'].astype(float)
train_dataset['Engine(CC)'] = train_dataset['Engine(CC)'].astype(float)

count = 0
missing_power_positions = []

for i, power in enumerate(train_dataset['Power(bhp)']):
    if power == 'null':
        count += 1
        missing_power_positions.append(i)
        
train_dataset = train_dataset[train_dataset['Power(bhp)'] != 'null']
train_dataset.reset_index(drop=True, inplace=True)
train_dataset['Power(bhp)'] = train_dataset['Power(bhp)'].astype(float)
train_dataset.loc[:, 'Power(bhp)'] = train_dataset['Power(bhp)'].astype(float)
train_dataset['New_Price'] = train_dataset['New_Price'].astype(str)
for i, row in train_dataset.iterrows():
    if not pd.isnull(row['New_Price']):
        train_dataset.at[i, 'New_car_Price'] = row['New_Price'].split()[0]
        
train_dataset.drop(["Name"],axis=1,inplace=True)
train_dataset.drop(["Mileage"],axis=1,inplace=True)
train_dataset.drop(["Engine"],axis=1,inplace=True)
train_dataset.drop(["Power"],axis=1,inplace=True)
train_dataset.drop(["New_Price"],axis=1,inplace=True)

Location = train_dataset[['Location']]
Location = pd.get_dummies(Location,drop_first=True)
ft = train_dataset[['Fuel_Type']]
Fuel_Type = pd.get_dummies(ft,drop_first=True)
train_dataset.replace({"First":1,"Second":2,"Third": 3,"Fourth & Above":4},inplace=True)
ot = train_dataset[['Owner_Type']]
Owner_Type = pd.get_dummies(ot,drop_first=True)
t = train_dataset[['Transmission']]
Transmission = pd.get_dummies(t,drop_first=True)
c = train_dataset[['Company']]
Company = pd.get_dummies(c,drop_first=True)
train_dataset.drop(["Company"],axis=1,inplace=True)
f_train_dataset= pd.concat([train_dataset,Location,Fuel_Type,Transmission],axis=1)
test_dataset = test_dataset.iloc[:,0:]

test_dataset = test_dataset[test_dataset['Mileage'].notna()]
test_dataset = test_dataset[test_dataset['Engine'].notna()]
test_dataset = test_dataset[test_dataset['Power'].notna()]
test_dataset = test_dataset[test_dataset['Seats'].notna()]

test_dataset = test_dataset.reset_index(drop=True)

for i in range(test_dataset.shape[0]):
    test_dataset.at[i, 'Mileage(km/kg)'] = test_dataset['Mileage'][i].split()[0]
    test_dataset.at[i, 'Engine(CC)'] = test_dataset['Engine'][i].split()[0]
    test_dataset.at[i, 'Power(bhp)'] = test_dataset['Power'][i].split()[0]

test_dataset['Mileage(km/kg)'] = test_dataset['Mileage(km/kg)'].astype(float)
test_dataset['Engine(CC)'] = test_dataset['Engine(CC)'].astype(float) 

position = []
for i in range(test_dataset.shape[0]):
    if test_dataset['Power(bhp)'][i]=='null':
        position.append(i)
        
test_dataset = test_dataset.drop(test_dataset.index[position])
test_dataset = test_dataset.reset_index(drop=True) 

test_dataset['Power(bhp)'] = test_dataset['Power(bhp)'].astype(float)

for i in range(test_dataset.shape[0]):
    if pd.isnull(test_dataset.loc[i,'New_Price']) == False:
        test_dataset.at[i,'New_car_Price'] = test_dataset['New_Price'][i].split()[0]

test_dataset['New_car_Price'] = test_dataset['New_car_Price'].astype(float)

test_dataset.drop(["Name"],axis=1,inplace=True)
test_dataset.drop(["Mileage"],axis=1,inplace=True)
test_dataset.drop(["Engine"],axis=1,inplace=True)
test_dataset.drop(["Power"],axis=1,inplace=True)
test_dataset.drop(["New_Price"],axis=1,inplace=True)

var = 'Location'
Location = test_dataset[[var]]
Location = pd.get_dummies(Location,drop_first=True)
Location.head()

var = 'Fuel_Type'
Fuel_t = test_dataset[[var]]
Fuel_t = pd.get_dummies(Fuel_t,drop_first=True)
Fuel_t.head()

var = 'Transmission'
Transmission = test_dataset[[var]]
Transmission = pd.get_dummies(Transmission,drop_first=True)
Transmission.head()

test_dataset.replace({"First":1,"Second":2,"Third": 3,"Fourth & Above":4},inplace=True)
test_dataset.head()

final_test= pd.concat([test_dataset,Location,Fuel_t,Transmission],axis=1)
final_test.head()

final_test.drop(["Location","Fuel_Type","Transmission","New_car_Price"],axis=1,inplace=True)
final_test.head()

x = f_train_dataset.loc[:,['Year', 'Kilometers_Driven', 'Owner_Type', 'Seats',
       'Mileage(km/kg)', 'Engine(CC)', 'Power(bhp)', 'Location_Bangalore',
       'Location_Chennai', 'Location_Coimbatore', 'Location_Delhi',
       'Location_Hyderabad', 'Location_Jaipur', 'Location_Kochi',
       'Location_Kolkata', 'Location_Mumbai', 'Location_Pune',
       'Fuel_Type_Diesel', 'Fuel_Type_LPG', 'Fuel_Type_Petrol',
       'Transmission_Manual']]
y = f_train_dataset.loc[:, ['Price']]
x.isnull().sum()

from sklearn.ensemble import ExtraTreesRegressor
selection= ExtraTreesRegressor()
selection.fit(x,y)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=25)

from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(x_train, y_train)
y_pred= rfr.predict(x_test)



def pred(x_test):
    sample = pd.DataFrame([x_test])
    return rfr.predict(sample)
