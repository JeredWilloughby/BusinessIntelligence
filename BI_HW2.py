#Import the associative libraries.
import pandas as pd
import io
import requests as r
#Assign variables for the filepath, files, and url
url = 'http://drd.ba.ttu.edu/isqs6339/hw/hw2/'
path = '/Users/jeredwilloughby/Desktop/Business Intelligence/'
file1 = 'players.csv'
file2 = 'player_sessions.csv'
###I used this file to double check my dataframe after merging and creating new columns
testdf = 'pandastest.csv'
fileout2 = 'pdhw2a.csv'
fileout3 = 'pdhw2b.csv'
#Use requests library to get the csv file associated with the url
res1 = r.get(url + file1)
#Check the status of the page
res1.status_code
#Assign a dataframe and pass the file with correct delimiter
df1 = pd.read_csv(io.StringIO(res1.text), delimiter='|')
#Call the dataframe for content review
df1
#Use requests library to get the csv file associated with the url
res2 = r.get(url + file2)
#Check the status of the page
res2.status_code
#Assign a dataframe and pass the file with correct delimiter
df2 = pd.read_csv(io.StringIO(res2.text), delimiter=',')
#Check the first and last few rows for content
df2.head(5)
df2.tail(5)
#There are different columns in the two datasets. We will need to perform a left merge to not miss data.
#Perform a merge and check column values through describe, list, and count
df3 = df1.merge(df2, how="left", on="playerid")
df3.describe()
list(df3)
df3.count()

df3['damage_done'].fillna(0, inplace=True)
df3
#There are missing values in the damage_done column. This will need to be fixed/cleaned.
#Fill missing values as cleaning method. Reason: Assume the player didn't play specific session. This will keep dps quality from being skewed
df3['damage_done'].fillna(0, inplace=True)
#Check to ensure all column values are equal
df3.count()

#Define the performance function
def performance(row):
    return (row['damage_done']*2.5 + row['healing_done']*4.5)/4
#apply the function to our dataframe
df3['player_performance_metric'] = df3.apply(performance, axis = 1)
df3
#Defining new function for dps quality
def quality(damage_done):
    # this line assures that the value will be interpreted as an integer
    damage_done = int(damage_done)
    if damage_done > 700000:
        # now we are returning a value, instead of assigning it directly to the column
        return 'High'
    if damage_done < 300000:
        return 'Low'
    # removing the last check as it is not necessary
    return 'Medium'
# we are using the .apply method only on a series. This makes the reading easier
df3['dps_quality'] = df3['damage_done'].apply(quality)
df3

#Create groupby of the average damage and healing done per session
A = df3.groupby('session')['damage_done','healing_done'].mean()
A
#Create groupby of the average damage and healing done per position
B = df3.groupby('position')['damage_done','healing_done'].mean()
B
#Write the csv files based on the groupby preferences of session and position with the averages of damage and healing done. 
A.to_csv(path + fileout2)
B.to_csv(path + fileout3)

#*******************************************************************************
# Questions: 
#*******************************************************************************
# 1. What is the quality of your data?
#
#    We should remember from lecture that all data is dirty. To measure the quality, we need to inspect all values and attributes. 
#    The data pulled from the csv files only had the column 'playerid' in common. After merge the two files on playerid, we notice several missing values for damage_done from various playerids.
#
# 2. What steps did you take to clean you data and why did you choose those options?
#
#    After evaluating the two dataframes, one can deduce that the data is gaming stats and results. Since we're missing specific damage_done scores, we can assume the specific player
#    was not engaged during the session's battle/skirmish, or was killed before getting a chance to incur damage. By filling in the missing values with zeros, we will avoid skewing their performce (deleting otherwise, or just giving them an average). 
#
# 3. Who are the three best players based on: 
#
#    damage_done: Player 3 (Molbrew,dps) had an average of 772092.45
#
#    healing_done: Player 2 (Kalea, healer) had an average of 535271.37
#
#    player_performance_metric: Player 8 (Crystalline, healer) had an average of 618839.23