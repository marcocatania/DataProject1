# DataProject1: Details

	Code file:

- data_project1.py
 
	Technologies used:

- Python: Pandas, Numpy, Scipy

	Definitions:

- A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.

- A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.

- A recession bottom is the quarter within a recession which had the lowest GDP.

- A university town is a city which has a high percentage of university students compared to the total population of the city.

	Hypothesis: 
	
University towns have their mean housing prices less affected by recessions. The t-test compares  the ratio of the mean price of houses in university towns and non university towns the quarter before the recession starts compared to the recession bottom. (PriceRatio = quarter_before_recession/recession_bottom).

The function returns a tuple (different, p, better).

"different" returns True or False whether the alternative hypothesis (that the two groups are the same) is true or not (True if the t-test is True at a p<0.01 - We reject the null hypothesis).
(False if otherwise we cannot reject the null hypothesis - p>0.01).

The variable p is equal to the p value returned from the ttest.

The value for "better" is either "university town" or "non-university town" depending on which has a lower mean price ratio (which is equivalent to a reduced market loss).

	The following data files have been used:

- From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.

- From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.

- From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (used only the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. Only the GDP data from the first quarter of 2000 has been used.