# © MARCO CATANIA

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

# Get the list of university towns

def get_list_of_university_towns():

    frame = pd.read_table('university_towns.txt')

    frame = frame.T.reset_index().T.reset_index().drop(['index'], axis=1)
    frame = frame.rename(columns={frame.columns[0]: 'Data'})

    # Creating column with State name (concatenated with Region Name in the file)
    frame['State'] = None
    frame['State'] = frame[frame['Data'].str.endswith('[edit]')]
    frame['State'] = frame['State'].fillna(method='ffill')

    # Cleaning State and Region names
    frame['Data'] = frame['Data'].str.split('(').str[0].str.rstrip()
    frame['State'] = frame['State'].str.split('[').str[0]
    frame = frame[['State', 'Data']]
    frame.columns = ['State', 'RegionName']

    # Deleting State name only rows
    frame = frame[frame.RegionName.str.endswith(']') == False]
    frame = frame.reset_index().drop(['index'], axis=1)
    return frame

print('\n')
print('University Towns Data Frame (head): ')    
print(get_list_of_university_towns().head())
print('\n')


# Get the recession start date

def get_recession_start():

    #Getting and cleaning data
    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly','GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index = int(file[file['Years Quarterly']=='2000q1'].index.values)
    file = file.iloc[index:].reset_index().drop('index', axis=1)

    #Getting recession start date 
    result = None
    for i in range(len(file)):
        if file['GDP'][i] > file['GDP'][i+1] > file['GDP'][i+2]:
            result = file['Years Quarterly'][i+1]
            break
    return result

print('The recession start is: ' + get_recession_start())
print('\n')


# Get the quarter before the recession's start

def get_quarter_before_recession():

    #Getting and cleaning data
    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly','GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index = int(file[file['Years Quarterly']=='2000q1'].index.values)
    file = file.iloc[index:].reset_index().drop('index', axis=1)

    #Getting the quarter before recession start
    result = None
    for i in range(len(file)):
        if file['GDP'][i] > file['GDP'][i+1] > file['GDP'][i+2]:
            result = file['Years Quarterly'][i]
            break
    return result

print('The Quarter before start of recession is: ' + get_quarter_before_recession())
print('\n')

# Get the recession end 

def get_recession_end():

    #Getting and cleaning data
    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly','GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index1 = int(file[file['Years Quarterly']=='2000q1'].index.values)
    file = file.iloc[index1:].reset_index().drop('index', axis=1)

    index2 = int(file[file['Years Quarterly']==get_recession_start()].index.values)
    file = file.iloc[index2:].reset_index().drop('index', axis=1)

    #Getting recession end quarter (Quarter after two consecutives GDP quarter rise)
    result = None
    for i in range(len(file)):
        if file['GDP'][i]<file['GDP'][i+1]<file['GDP'][i+2]:
            result = file['Years Quarterly'][i+2]
            break
    return result
    

print('The recession end is: ' + get_recession_end())
print('\n')


# Get the recession bottom quarter , within the recession period

def get_recession_bottom():

    #Getting and cleaning data
    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly', 'GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index2 = int(file[file['Years Quarterly'] == get_recession_start()].index.values)
    index3 = int(file[file['Years Quarterly'] == get_recession_end()].index.values)
    file = file.iloc[index2:index3+1].reset_index().drop('index', axis=1)
    bottom = file['Years Quarterly'][(file['GDP'] == file['GDP'].min())].iloc[0]

    return bottom
    

print('The recession bottom is: ' + get_recession_bottom())
print('\n')


#Get housing data and convert from years to quarters (mean value)

def convert_housing_data_to_quarters():

    # Getting and cleaning data
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    data['State'] = data['State'].map(states)
    data = data.set_index(['State','RegionName'])
    drop = ['RegionID', 'Metro', 'CountyName', 'SizeRank']
    data = data.drop(drop, axis=1)

    # Converting data period from year to quarter
    data = data.groupby(pd.PeriodIndex(data.columns, freq='Q'), axis=1).mean()
    data = data.loc[:,'2000Q1':'2016Q3']

    return data

print('Data Frame (header) representing the evolution of house prices (mean value per quarter): ')
print('\n')
print(convert_housing_data_to_quarters().head())
print('\n')


#   Creation of new data frame merging the two previous one, and showing the decline or growth of house prices between the recession start
#and the recession bottom.
#Then a ttest is run to compare the university town values to the non-university towns values (on the Price Ratio).
#The function returns a tuple (different, p, better).

#   "different" returns True or False whether the alternative hypothesis (that the two groups are the same) is true or not.
#(True if the t-test is True at a p<0.01 - We reject the null hypothesis).
#(False if otherwise we cannot reject the null hypothesis - p>0.01).

#The variable p is equal to the p value returned from the ttest.

#   The value for "better" is either "university town" or "non-university town" depending on which has a lower mean price ratio
#(which is equivalent to a reduced market loss).

def run_ttest():
    
    # Creation of the new dataframe creating a new column separating two groups: university towns and non university towns, and another one computing the mean price ratio (quarter before recession start/recession bottom)
    frame = pd.merge(convert_housing_data_to_quarters().reset_index(), get_list_of_university_towns(), on = get_list_of_university_towns().columns.tolist(), indicator = '_flag', how= 'outer')
    frame.columns = frame.columns.map(str)
    frame['2008Q3']=frame['2008Q3'].fillna(0)
    frame['2009Q4']=frame['2009Q4'].fillna(0)
    frame['PriceRatio'] = frame[get_quarter_before_recession().upper()].div(frame[get_recession_bottom().upper()])
    frame['PriceRatio'] = frame['PriceRatio'].fillna(0)
    columns = ['State', 'RegionName', get_quarter_before_recession().upper(), get_recession_bottom().upper(),'PriceRatio', '_flag']
    frame = frame[columns]

    group1 = frame[frame['_flag']=='both']
    group2 = frame[frame['_flag']!='both']

    #Ttest
    test = ttest_ind(group2['PriceRatio'], group1['PriceRatio'])
    pval = test[1]
    different = pval < 0.01
    better = None
    if group1['PriceRatio'].mean()<group2['PriceRatio'].mean():
        better = 'university town'
    else:
        better = "non-university town"

    return ('The two groups are the same (null hypothesis rejected): ' + str(different), 'The p value is: ' + str(pval), 'The group who has a lower mean price ratio (reduced market loss) is : ' + str(better))


print(run_ttest())
print('\n')
