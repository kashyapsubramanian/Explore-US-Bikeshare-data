import time
import calendar as cal
import pandas as pd
import numpy as np

#-----------------------------------------------------------------------------------------#
#
#  Initialize variables
#
#-----------------------------------------------------------------------------------------#

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {'All':0,'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,
              'August':8,'September':9,'October':10,'November':11,'December':12}

DAY_DATA = {'All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'}

#-----------------------------------------------------------------------------------------#
#
# Function: get_filters
#
#   Asks user to specify a city, month, and day to analyze.
#
#   Returns:
#        (str) city - name of the city to analyze
#       (str) month - name of the month to filter by, or "all" to apply no month filter
#       (str) day - name of the day of week to filter by, or "all" to apply no day filter
#
#-----------------------------------------------------------------------------------------#
def get_filters():
    
    try:
        print('Hello! Let\'s explore some US bikeshare data!')

        #*************************************************#
        #   GET CITY: get user input for month (all, january, february, ... , june)
        #*************************************************#

        city = input('Bikeshare data is available for the cities \n\t1.Chicago\n\t2.New York City\n\
        3.Washington\n\nWhich city do you want to explore?\n').lower()

        while city not in CITY_DATA:
            print('\nThe entered City value is invalid.')
            city = input('Bikeshare data is available for the cities \n\t1.Chicago\n\t2.New York City\n\
        3.Washington\n\nWhich city do you want to explore?\n').lower()

        #*************************************************#
        #    GET MONTH: get user input for month (all, january, february, ... , june)
        #*************************************************#
        
        month = input('Would you like to filter by a particular month?\n(type month name like may..etc)\
        \n(type "all"if you dont want to filter by month)\n').title()

        while month not in MONTH_DATA:
            print('\nThe entered Month value is invalid.')
            month = input('Would you like to filter by a particular month?\n(type month name like may..etc)\
            \n(type "all" if you dont want to filter by month)\n').title()

        #*************************************************#
        #    GET DAY: get user input for day of week (all, monday, tuesday, ... sunday)
        #*************************************************#
        
        day = input('Would you like to filter by a particular day?\n(type weekday name like monday..etc)\
        \n(type "all" if you dont want to filter by day)\n').title()

        while day not in DAY_DATA:
            print('\nThe entered Day value is invalid.')
            day = input('Would you like to filter by a particular day?\n(type weekday name like monday..etc)\
            \n(type "all" if you dont want to filter by day)\n').title()

        print('-'*40)
        return city, month, day

    except:
        print('Some error occured')
        return None,None,None

#-----------------------------------------------------------------------------------------#
#
# Function: load_data
# 
#    Loads data for the specified city and filters by month and day if applicable.
#
#    Args:
#        (str) city - name of the city to analyze
#        (str) month - name of the month to filter by, or "all" to apply no month filter
#        (str) day - name of the day of week to filter by, or "all" to apply no day filter
#    Returns:
#        df - Pandas DataFrame containing city data filtered by month and day
#
#-----------------------------------------------------------------------------------------#
def load_data(city, month, day):

    #*************************************************#
    #   LOAD: load the data for the given City
    #*************************************************#
    df = pd.read_csv(CITY_DATA[city])

    #*************************************************#
    #   CONVERT: convert columns to datetime data type
    #            (helps date/time calculations)
    #*************************************************#
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #*************************************************#
    #   EXTRACT: Extract and Store the data in required format
    #            from existing columns
    #*************************************************#
    df['months']=df['Start Time'].dt.month
    df['weekday']=df['Start Time'].dt.weekday_name
    df['time']=df['Start Time'].dt.hour

    #*************************************************#
    #   FILTER MONTH: filter the dataframe by given Month
    #*************************************************#
    if month != 'All':
        df = df[df['months']==MONTH_DATA[month]]

    #*************************************************#
    #   FILTER DAY: filter the dataframe by given Day
    #*************************************************#
    if day != 'All':
        df = df[df['weekday']==day]

    return df

#-----------------------------------------------------------------------------------------#
#
# Function: time_stats
# 
#    Displays statistics on the most frequent times of travel.
#
#    Args:
#        df - Pandas DataFrame containing city data filtered by month and day
#    Returns:
#        The function does not return anything
#
#-----------------------------------------------------------------------------------------#
def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #*************************************************#
    #   COMMON MONTH: display the most common month
    #*************************************************#
    common_month = cal.month_name[df['months'].mode()[0]]
    print('\nThe month when bikes are most frequently used: ',common_month)

    #*************************************************#
    #   COMMON DAY: display the most common day of week
    #*************************************************#
    common_day = df['weekday'].mode()[0]
    print('\nThe weekday when bikes are most frequently used: ',common_day)

    #*************************************************#
    #   COMMON TIME: display the most common start hour
    #*************************************************#
    common_time = str(df['time'].mode()[0])
    print('\nThe most common hour of bike usage: ',common_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#-----------------------------------------------------------------------------------------#
#
# Function: station_stats
# 
#    Displays statistics on the most popular stations and trip.
#
#    Args:
#        df - Pandas DataFrame containing city data filtered by month and day
#    Returns:
#        The function does not return anything
#
#-----------------------------------------------------------------------------------------#
def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #*************************************************#
    #   COMMON START STATION: display most commonly used start station
    #*************************************************#
    common_st_station = df['Start Station'].describe()[2]
    print('\nThe Station from where most of the rides begin: ',common_st_station)

    #*************************************************#
    #   COMMON END STATION: display most commonly used end station
    #*************************************************#
    common_end_station = df['End Station'].describe()[2]
    print('\nThe Station where most of the rides end: ',common_st_station)

    #*************************************************#
    #   COMMON ROUTE: display most frequent combination of start station and end station trip
    #*************************************************#
    df_gby=df.groupby(['Start Station','End Station'],as_index=False)['Start Time'].count()
    common_route = df_gby[df_gby['Start Time']==df_gby['Start Time'].max()][['Start Station','End Station']]
    print('\nThe most common route of travel: \n From: %s\n To:   %s'%(common_route['Start Station'].values[0],common_route['End Station'].values[0]))

    print("\nThis took %s seconds." %(time.time() - start_time))
    print('-'*40)

#-----------------------------------------------------------------------------------------#
#
# Function: trip_duration_stats
# 
#    Displays statistics on the total and average trip duration.
#
#    Args:
#        df - Pandas DataFrame containing city data filtered by month and day
#       (str) month - name of the month
#    Returns:
#        The function does not return anything
#
#-----------------------------------------------------------------------------------------#
def trip_duration_stats(df,month):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #*************************************************#
    #   TOTAL TRAVEL TIME: display total travel time
    #*************************************************#
    tot_time = pd.Timedelta(df['Trip Duration'].sum(),unit='s')

    if month and month!='all':
        print('\nTotal travelling done in 2017, in {} is: {}'.format(month,tot_time))
    else:
        print('\nTotal travelling done in 2017 through June is: {}'.format(tot_time))

    #*************************************************#
    #   AVERAGE TRIP DURATION: display average trip duration
    #*************************************************#
    mn_time = pd.Timedelta(df['Trip Duration'].mean(),unit='s')
    print('\nThe average travelling time is: %s'%(mn_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#-----------------------------------------------------------------------------------------#
#
# Function: user_stats
# 
#    Displays statistics on bikeshare users.
#
#    Args:
#        df - Pandas DataFrame containing city data filtered by month and day
#       (str) city - name of the city
#    Returns:
#        The function does not return anything
#
#-----------------------------------------------------------------------------------------#
def user_stats(df,city):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #*************************************************#
    #   USER TYPES: Display counts of user types
    #*************************************************#
    user = df['User Type'].dropna()
    print('\nThe breakdown on User Types\n',user.groupby(user).count())

    if city != 'washington':
        #*************************************************#
        #   GENDER STATS: Display counts of gender
        #*************************************************#
        gender = df['Gender'].dropna()
        print('\nThe breakdown on gender\n',gender.groupby(gender).count())

        #*************************************************#
        #   BIRTH YEAR STATS: Display earliest, most recent, and most common year of birth
        #*************************************************#
        birth_yr = df['Birth Year'].dropna()
        min_yr = int(birth_yr.min())
        max_yr = int(birth_yr.max())
        mode_yr = int(birth_yr.mode())

        print('\nWhat is the oldest, youngest and most popular year of birth?')
        print('oldest: {}\nyoungest: {}\npopular: {}\n'.format(min_yr,max_yr,mode_yr))

    else:
        print('\nThe breakdown on "Gender" and "Year of birth" is not available \
for',city)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#-----------------------------------------------------------------------------------------#
#
# Function: main
# 
#    Main function of the program. Acts as controller of program execution
#
#    Args:
#        No arguments taken by the function
#    Returns:
#        The function does not return anything
#
#-----------------------------------------------------------------------------------------#
def main():
    while True:
        city, month, day = get_filters()
        if city:
            df = load_data(city, month, day)
            
            if not df.empty:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df,month)
                user_stats(df,city)
            else:
                print('-'*40,'\n There is no data available for the given inputs\n'+'-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
