import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    frame = pd.read_table('university_towns.txt')

    frame = frame.T.reset_index().T.reset_index().drop(['index'],axis=1)
    frame = frame.rename(columns={frame.columns[0]: 'Data'})

    frame['State'] = None
    for string in frame['Data']:
        frame['State'] = frame[frame['Data'].str.endswith('[edit]')]
        frame['State'] = frame['State'].fillna(method='ffill')


    frame['Data'] = frame['Data'].str.split('(').str[0].str.rstrip()
    frame['State'] = frame['State'].str.split('[').str[0]
    frame = frame[['State', 'Data']]
    frame.columns = ['State', 'RegionName']
    frame = frame[frame.RegionName.str.endswith(']') == False]
    frame = frame.reset_index().drop(['index'], axis=1)

    return frame

frame1 = get_list_of_university_towns()
get_list_of_university_towns()


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''

    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly','GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index = int(file[file['Years Quarterly']=='2000q1'].index.values)
    file = file.iloc[index:].reset_index().drop('index', axis=1)

    result = None
    for i in range(len(file)):
        if(file['GDP'][i]> file['GDP'][i+1]> file['GDP'][i+2]):
            result = file['Years Quarterly'][i+1]
            break


    return result


start_recession = get_recession_start()
get_recession_start()


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''

    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly','GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index1 = int(file[file['Years Quarterly']=='2000q1'].index.values)
    file = file.iloc[index1:].reset_index().drop('index', axis=1)

    index2 = int(file[file['Years Quarterly']==start_recession].index.values)
    file = file.iloc[index2:].reset_index().drop('index', axis=1)

    result = None
    for i in range(len(file)):
        if(file['GDP'][i]<file['GDP'][i+1]<file['GDP'][i+2]):
        if file['GDP'][i]<file['GDP'][i+1]<file['GDP'][i+2]:
            result = file['Years Quarterly'][i+2]
            break

    return result
end_recession = get_recession_end()
get_recession_end()


def get_recession_bottom():

    file = pd.read_excel('gdplev.xls')
    file = file.rename(columns = {'Unnamed: 4':'Years Quarterly','Unnamed: 6':'GDP'})
    columns = ['Years Quarterly', 'GDP']
    file = file[columns]
    file = file.drop(file.index[0:7]).reset_index().drop('index', axis=1)
    index2 = int(file[file['Years Quarterly'] == start_recession].index.values)
    index3 = int(file[file['Years Quarterly'] == end_recession].index.values)
    file = file.iloc[index2:index3+1].reset_index().drop('index', axis=1)
    bottom = file['Years Quarterly'][(file['GDP'] == file['GDP'].min())].iloc[0]


    return bottom

bottom_recession = get_recession_bottom()
get_recession_bottom()



def convert_housing_data_to_quarters():
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    data['State'] = data['State'].map(states)
    data = data.set_index(['State','RegionName'])
    drop = ['RegionID', 'Metro', 'CountyName', 'SizeRank']
    data = data.drop(drop, axis=1)

    data = data.groupby(pd.PeriodIndex(data.columns, freq='Q'), axis=1).mean()
    data = data.loc[:,'2000Q1':'2016Q3']

    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    return data

hdf = convert_housing_data_to_quarters()
convert_housing_data_to_quarters()


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''



    Q5Frame = convert_housing_data_to_quarters()

    frame = pd.merge(convert_housing_data_to_quarters().reset_index(), get_list_of_university_towns(), on=get_list_of_university_towns().columns.tolist(), indicator ='_flag',how='outer')
    frame.columns = frame.columns.map(str)
    frame['2008Q3']=frame['2008Q3'].fillna(0)
    frame['2009Q4']=frame['2009Q4'].fillna(0)
    frame['PriceRatio'] = frame['2008Q3'].div(frame['2009Q4'])
    frame['PriceRatio'] = frame['PriceRatio'].fillna(0)
    columns = ['State', 'RegionName', '2008Q3', '2009Q2','PriceRatio', '_flag']
    frame = frame[columns]

    group1 = frame[frame['_flag']=='both']
    group2 = frame[frame['_flag']!='both']

    test = ttest_ind(group2['PriceRatio'], group1['PriceRatio'])
    pval = test[1]
    different = pval<1
    better=None
    if group1['PriceRatio'].mean()<group2['PriceRatio'].mean():
        better = 'university town'
    else:
        better = "non-university town"

    return (different, pval, better)

run_ttest()
