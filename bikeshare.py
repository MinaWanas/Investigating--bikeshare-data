'''
Udacity Introduction to python lesson
Explore US Bikeshare project
Author: Mina Elia Wanas
Start Date: 06 May 2022
Finish Date: 09 May 2022
Project 1 for Professional Data Analysis track by udacity

#Project Description:

The following project reads three csv files 'washington.csv', 'new_york_city.csv', 'chicago.csv' and filter the csv according to user input
by month or day or both or no filters if the user chooses so.
The program then calculate the following parameters:

#1 Popular times of travel (i.e., occurs most often in the start time)
most common, least common month
most common, least common day of week
most common, least common hour of day

#2 Popular stations and trip
most common start station
most common end station
most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration
total travel time
average travel time

#4 User info
counts of each user type and display percentage
counts of each gender and display percentage
earliest, most recent, most common year of birth and display percentage
'''


import numpy as np
import pandas as pd
import time
from datetime import date

# Global dictionary that relate city name to the csv file 
CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv' 
    }

# Create 'MONTHS' dictionary that relate months 'String' to their number: for example, 'June' to '6' --> used in filtering user input
MONTHS = {
    1: ['january', 'jan.', 'jan', '1'],
    2: ['february', 'feb.', 'feb', '2'], 
    3: ['march', 'mar.', 'mar', '3'],
    4: ['april', 'apr.', 'apr', '4'],
    5: ['may', '5'],
    6: ['june', 'jun.', 'jun', '6'],
    }

# Create 'WEEKDAYS' dictionary that relate weekdays to their number: for example, 'Sunday' to '6' --> used in filtering user input
WEEKDAYS = {
    0: ['monday', 'mon', 'mo', 'mon.', 'mo.', '0'],
    1: ['tuesday', 'tue', 'tu', 'tue.', 'tu.', '1'],
    2: ['wednesday', 'wed', 'we', 'wed.', 'we.', '2'],
    3: ['thursday', 'thu', 'th', 'thu.', 'th.', '3'],
    4: ['friday','fri', 'fr','fri.', 'fr.', '4'],
    5: ['saturday', 'sat', 'sa', 'sat.', 'sa.', '5'],
    6: ['sunday', 'sun', 'su', 'sun.', 'su.', '6']
}

#Create 'CITIES dictionary that relate cities to their abbreviation for example, 'chi' to 'Chicago' --> used in filtering user input
CITIES = {
    'Chicago': ['chicago', 'chi'],
    'New York': ['ny', 'new york'],
    'Washington': ['washington', 'wa']
}

def get_filters ():
    """
    This function takes no input and returns the city, month and day the user wants to filter by
    :return: city, month, day, True if is_month_filtered, True if is_day_filtered
    """
    # Print an intro hello
    print("Hello! Let's explore some US bikeshare data!")
    
    # First Filter: Promot the user to filter by city
    print('Would you like to see data for Chicago, New York, or Washington?\n')

    # While loop to keep prompting for user input till valid input (User must enter either chicago or washington or new york)
    while True:

        # User input is stored in city and is made case insensitive and leading and trailing whitespaces are removed
        city = input().casefold().strip()

        # If User input is valid city, break the loop, else prompts user to enter a valid city
        if get_dict_key(CITIES, city):
            break
        else:
            print("Sorry, only Chicago, New York, or Washington states are available! ")
            print('Kindly try again: \n')
    
    # Second Filter: Filter the data by month, day, both, or no filter
    print("""\nChoose how you want to filter the Bikeshare Data in {} city!
    \t1. Month 
    \t2. Day 
    \t3. Both 
    \t4. No filters, Type 'none' for no time filter""".format(get_dict_key(CITIES, city)))

    # Create month, day variables and set to None
    month, day = None, None

    # Create 2 boolean variable to keep track whether the user filtered by month or day
    # So that when displaying results, it won't show most common month is X, when the user filterd the month to show only X 
    is_month_filtered , is_day_filtered = False, False

    # While loop to keep prompting for user input till valid input (User must enter month or day or both or none)
    while True:
        # Boolean variable to keep track that the input is valid
        valid_input = False

        # User input is stored in date_filter variable and is made case insensitive and remove leading and trailing whitespaces
        date_filter = input().casefold().strip()

        # Filter by month
        if date_filter in ['month', 'months', 'both']:
            print("\nWhich month? kindly choose a month from January to June")
            
            # While loop to keep prompting for user input till valid input (User must enter a valid month)
            while True:
                # Take user input and make it case insensitive and remove leading and trailing whitespaces
                month = input().casefold().strip()

                # Check User input (month) is a valid month or not --> using the global dictionary MONTHS
                if get_dict_key(MONTHS, month) != None:
                    is_month_filtered = True
                    valid_input = True
                    break
                else:
                    print('Sorry! kindly enter a valid month!\n')
        
        # Filter by day
        if date_filter in ['day', 'days', 'both']:
            print("Which day? e.g. Sunday, Monday, etc")
            
            # While loop to keep prompting for user input till valid input (User must enter a valid day)
            while True:
                # Take user input and make it case insensitive and remove leading and trailing whitespaces
                day = input().casefold().strip()

                # Check User input (day) is a valid day or not using the global dictionary WEEKDAYS
                if get_dict_key(WEEKDAYS, day) != None:
                    is_day_filtered = True
                    valid_input = True
                    break
                else:
                    print('Sorry! kindly enter a valid day!\n')
        
        # No filter applied
        if date_filter in ['none', 'nope', 'no filters', 'no filter']:
            valid_input = True
        
        # Break the loop if input is valid
        if valid_input:
            break
        else:
            print("Sorry, not valid response, kindly enter 'month' or 'day' or 'both' or 'none'")
    
    # Print (Confirming) filters to the user
    if month and day:
        """
        Below is the comment to explain how the below code works:
        >>MONTHS.get(get_dict_key(MONTHS, month))[0].title()<<

        get_dict_key (MONTHS, month) --> takes the month variable and search in the dictionary (MONTHS) values, and return the key(month number)
        MONTHS.get() --> takes the (month number) from the get_dict_key() and return the value (list of string "list of months")
        [0] --> choose the first string in the list (which is the month name)
        .title() --> capitalize the first letter

        Result: month = jan, return = January
        """
        print("\nApplying {} and {} filters on {} Bikeshare data\n".format(MONTHS.get(get_dict_key(MONTHS, month))[0].title(), WEEKDAYS.get(get_dict_key(WEEKDAYS, day))[0].title(), get_dict_key(CITIES, city)))
    elif month:
        print("\nApplying {} filter on {} Bikeshare data\n".format(MONTHS.get(get_dict_key(MONTHS, month))[0].title(),get_dict_key(CITIES, city)))
    elif day:
        print("\nApplying {} filter on {} Bikeshare data\n".format(WEEKDAYS.get(get_dict_key(WEEKDAYS, day))[0].title(),get_dict_key(CITIES, city)))
    else:
        print("\nApplying No filters on {} Bikeshare data\n".format(get_dict_key(CITIES, city)))
    
    # Return city name, month, day, is_month_filtered, is_day_filtered
    return city, month, day, is_month_filtered, is_day_filtered

def load_data(city:str, month:str, day:str):
    """
    This function takes the city, month, and day as arguments and returns a new dataframe that contains
    the filtered data and a flag if washington.csv was loaded
    
    :param city: The name of the city to analyze
    :param month: Month from Jan to June to filter by, or 'None' to apply no month filter
    :param day: The day of the week (e.g., "Sunday", "Monday", etc.) to filter by, or 'None' to apply no day filter

    :return: A dataframe that is filtered by month and day of the week and a flag if washington.csv was loaded
    """

    # Read csv file for the city parameter
    """
        Below is the comment to explain how the below code works:
        >>CITY_DATA.get(get_dict_key(CITIES, city).casefold())<<

        get_dict_key (CITIES, city) --> takes the city variable and search in the dictionary (CITIES) values, and return the key(city name but first letter is capital)
        casefold() --> takes the city name with capitalized first letter and return caseless city
        CITY_DATA.get() --> takes the (city name) from the get_dict_key() and return the value (city name .csv)

        Result: month = ny, return = new_york_city.csv
        """
    path = './{}'.format(CITY_DATA.get(get_dict_key(CITIES, city).casefold()))
    city_df = pd.read_csv(path)
    
    # Create bool variable (flag) that becomes true if washington.csv is loaded, this variable to be used later when displaying gender and year
    is_washington = False
    if path == './washington.csv':
        is_washington = True

    # Convert Start Time to Datetime
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
    
    # Create a new column (month) and (day of the week) using (Start Time)
    city_df['Month'] = city_df['Start Time'].dt.month
    city_df['Weekday'] = city_df['Start Time'].dt.weekday #Monday = 0, Sunday = 6

    # Filter by month if applicable
    if month != None:
        # Use function (See function above) the get the key for month; takes the dictionary and the month as argumemnts
        month = get_dict_key(MONTHS, month.casefold())

        # Filter by month to create a new dataframe
        city_df = city_df[city_df['Month'] == month]

        # Delete month column to keep the data raw
        city_df.pop('Month')
    
    # Filter by Week of Day if applicable
    if day != None:
        # Use function (See function above) the get the key for month; takes the dictionary and the month as argumemnts
        day = get_dict_key(WEEKDAYS, day.casefold())

        # Filter by WeekDay if applicable
        city_df = city_df[city_df['Weekday'] == day]
    
    return city_df, is_washington

def get_dict_key (dictionary: dict, value):
    """
    Functions that takes a dictionary and a value to look for, and returns the key for the value if it exists in the dictionary,
    otherwise it returns None
    
    :param dictionary: dict = the dictionary you want to search in
    :param value: The value you want to find the key for, N.B. the dictionary value is list of strings
    :return: The key for the value in the dictionary if found, else return None.
    """
    for key, val in dictionary.items():
        if value in val:
            return key
    return None

def most_common_period (df:pd.DataFrame, time_column: str, period: str):
    """
    It takes a dataframe, a time column, and a period (e.g. hour, month, day) as input and returns the
    most common period (e.g. hour, month, day) as output.
    
    :param df: the dataframe you want to analyze
    :param time_column: the name of the column that contains the time
    :param period: str = period to be extracted from the time_column ('month' or 'day' or 'hour')

    :return _ str: The most common month (January to June) or hour (0 to 23) or day of the week (Monday to Sunday)
    """
    
    # Change start time or end time to be title case
    time_column = time_column.title()
    
    # Convert time column to Datetime
    df[time_column] = pd.to_datetime(df[time_column])

    if period == 'month':
        # Extract period (e.g. hour, month, day) from time column
        df['Month'] = df[time_column].dt.month

        # Return most common month number
        month_number = df['Month'].value_counts()
        month_number = month_number.index[0]

        # convert month number to month name e.g 6 --> June 
        month = MONTHS.get(month_number)[0].title()

        # Remove month column to keep the data raw
        df.pop('Month')

        #return month
        return month

    elif period == 'hour':
        # Extract period (e.g. hour, month, day) from time column
        df['Hour'] = df[time_column].dt.hour

        # Return most common hour number
        hour = df['Hour'].mode()[0]

        # Remove hour column to keep the data raw
        df.pop('Hour')

        #return most common hour
        return hour

    elif period == 'day':
        # Extract period (e.g. hour, month, day) from time column
        df['Day'] = df[time_column].dt.weekday

        # Return most common day number e.g Monday = 0, Sunday = 6
        day_number = df['Day'].mode()[0]

        # convert day number to day name e.g 6 --> Sunday 
        day = WEEKDAYS.get(day_number)[0].title()

        # Remove day column to keep the data raw
        df.pop('Day')

        #return day
        return day
    
    else:
        return None

def least_common_period (df:pd.DataFrame, time_column: str, period: str):
    """
    The function takes in a dataframe, a time column and a period (e.g. hour, month, day) and returns
    the least common period (e.g. hour, month, day)
    
    :param df: the dataframe you want to analyze
    :param time_column: The column in the dataframe that contains the time data
    :param period: str = period to be extracted from the time_column ('month' or 'day' or 'hour')

    :return _ str: The most common month (January to June) or hour (0 to 23) or day of the week (Monday to Sunday)
    """

    time_column = time_column.title()

    df[time_column] = pd.to_datetime(df[time_column])

    if period == 'month':
        # Extract period (e.g. hour, month, day) from time column
        df['Month'] = df[time_column].dt.month

        # Return least common month number
        month_number = df['Month'].value_counts()
        month_number = month_number.index[-1]

        # convert month number to month name e.g 6 --> June 
        month = MONTHS.get(month_number)[0].title()

        # Remove month column to keep the data raw
        df.pop('Month')

        #return month
        return month

    elif period == 'hour':
        # Extract period (e.g. hour, month, day) from time column
        df['Hour'] = df[time_column].dt.hour

        # Least common hour number
        hour = df['Hour'].value_counts()
        hour = hour.index[-1]
    
        # Remove hour column to keep the data raw
        df.pop('Hour')

        #return least common hour
        return hour

    elif period == 'day':
        # Extract period (e.g. hour, month, day) from time column
        df['Day'] = df[time_column].dt.weekday

        # Return least common day number e.g Monday = 0, Sunday = 6
        day_number = df['Day'].value_counts()
        day_number = day_number.index[-1]

        # convert day number to day name e.g 6 --> Sunday 
        day = WEEKDAYS.get(day_number)[0].title()
    
        # Remove day column to keep the data raw
        df.pop('Day')

        #return day
        return day
    
    else:
        return None 

def column_value_count(df:pd.DataFrame, column: str):
    """
    It takes a dataframe and a column name as input and returns the value counts of the column
    
    :param df _ DataFrame: The dataframe you want to use
    :param column _ str: The column you want to count the values of
    :return: The number of times each value appears in the column.
    """
    return df[column.title()].value_counts()

def most_common_trip (df:pd.DataFrame):
    """
    It loops over all start stations and counts trips from each start station to each end station. If
    the end station count is higher than the previous highest, it changes the highest, start station,
    and end station variables
    
    :param df: DataFrame to be analyzed
    
    :return: A string describing the start station, end station, and the count of the most occured trip
    """
    # groupby the start station and end station.size() --> takes every start station and sort it descending, then for every start station it sorts the end station
    # and sort it also descending. the size() function shows the values or number of occurance for each pair of start station to end station.
    # max () --> show the highest or maximum value / 'number of occurance for each pair from start station to end station' i.e. "most popular trip count"
    # idxmax() --> index max show a list of the index [Start Station, End Station] that have the highest number of occurance i.e. "most popular trip"
    start_station = df.groupby(['Start Station', 'End Station']).size().idxmax()[0]
    end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()[1]
    trip_count = df.groupby(['Start Station', 'End Station']).size().max()

    # Create a string message to be returned describing the start station, end station, and the count of the most occured trip
    message = """The most common trip:\n\tStart Station: '{}'\n\tEnd Station: '{}'\n\tTotal count for the most common trip: {}""".format(start_station,end_station,trip_count)
    
    # Return message string
    return message        

def prompt_user_raw_data (df:pd.DataFrame):
    """
    The function prompts the user to see the first 5 rows of the dataframe, and if the user inputed
    "yes", the function displays the first 5 rows, and then prompts the user again to see the next 5
    rows, and so on, until the user inputed "no" or until the user reached the end of the rows
    
    :param df: the dataframe to be displayed
    """
    #  Display all columns when printing
    pd.set_option('display.max_columns', 200)

    # Delete 'Weekday' and column from the load_data function()
    df.pop('Weekday')

    print()
    # Create 2 variables to keep track of the raw data displayed
    start_index = 0
    end_index = 5
    
    while True:

        print()
        print('Do you want to see the rows from {} to {} of raw data'.format(start_index,end_index-1)) # Prompt user

        # record user input in input_message variable
        input_message = input("Press 'Y' to continue or anything else to exit\n")
        if input_message in ['Y', 'y', 'yes', 'Yes']:
            # if user inputed "yes", display the rows starting from row at index= start_index, and ending at index = end_index -1
            print(df.iloc[start_index:end_index,:])
            # Change the values of start, and end index as follows
            start_index = end_index
            end_index += 5
            
            # Break the loop in case the user inputed 'yes' until the user reached the end of the rows
            rows_count = df.value_counts().shape[0]
            if start_index > rows_count:
                break
        else:
            # if the user inputed "no", just break the loop
            break

def main_function ():
    city, month, day, is_month_filtered, is_day_filtered = get_filters()
    city_df, is_washington = load_data(city, month, day)
    
    print()
    print("#1 Popular times of travel")
    
    if not is_month_filtered:
        # If user filtered by month, don't display those 2 lines, as the the most common and least common month will be the month filtered
        # Create 2 variables to hold the most, and the least common month
        most_common_month = most_common_period(city_df, 'Start Time', 'month')
        least_common_month = least_common_period(city_df, 'Start Time', 'month')
        
        # Print the most, and the least common month
        print("Most common Month is: {}".format(most_common_month))
        print("Least common Month is: {}".format(least_common_month))
    if not is_day_filtered:
        # If user filtered by day, don't display those 2 lines, as the the most common and least common day will be the day filtered
        # Create 2 variables to hold the most, and the least common day of the week
        most_common_day = most_common_period(city_df,'Start Time', 'day')
        least_common_day = least_common_period(city_df, 'Start Time', 'day')
        
        # Print the most common day, and the least common day
        print("Most common Day of the week is: {}".format(most_common_day))
        print("Least common Day of the week is: {}".format(least_common_day))
    
    # Print those 2 lines in any case, as there is no 'hour filter' applied
    # Create 2 variables that hold the most, and the least common hour of the day
    most_common_hour = most_common_period(city_df, 'Start Time', 'hour')
    least_common_hour = least_common_period(city_df, 'Start Time', 'hour')
    
    # Print the most, and the least common hour
    print("Most common Hour of the day is: {}".format(most_common_hour))
    print("Least common Hour of the day is: {}".format(least_common_hour))
    
    print()
    print("#2 Popular stations and trip")
    
    # Create 2 variables to hold the name of the most common start station and the total count
    common_start_station = city_df['Start Station'].value_counts().index[0]
    count_start_station = city_df['Start Station'].value_counts().iloc[0]

    # Print the most common start station and the total count for the most common start station
    print("Most Common Start Station: {} with total count {}".format(common_start_station, count_start_station))

    # Create 2 variables to hold the name of the most common end station and the total count
    common_end_station = city_df['End Station'].value_counts().index[0]
    count_end_station = city_df['End Station'].value_counts().iloc[0]
    
    # Print the most common end station and the total count for the most common end station
    print("Most Common End Station: {} with total count {}".format(common_end_station, count_end_station))
    
    # Print the most common trip from start to end, also print the total count for the most common trip
    print()
    print(most_common_trip(city_df)) 

    print()
    print("#3 Trip duration")
    # Variables that hold total trip duration (in hours), and the average trip duration
    total_trip_duration = city_df['Trip Duration'].sum() / 3600
    average_trip_duration = city_df['Trip Duration'].mean()

    # Print total and average trip duration rounded to 2 decimel places
    print("Total trip duration: {} hours".format(round(total_trip_duration, 2)))
    print("Average trip duration: {} seconds".format(round(average_trip_duration, 2)))

    print()
    print("#4 User info")
    
    # Variables that hold subscribers, customers, and total users count
    sub_count = city_df['User Type'].value_counts().loc['Subscriber']
    customer_count = city_df['User Type'].value_counts().loc['Customer']
    total_users = sub_count + customer_count
    
    # Variables that hold percentage of subscribers and customers
    sub_percent = (sub_count/total_users) * 100
    customer_percent = 100 - sub_percent

    print("Subscribers no#: {}, who constitute {}%  of the users".format(sub_count, round(sub_percent,2)))
    print("Customers no#: {}, who constitute {}%  of the users".format(customer_count, round(customer_percent, 2)))
    print()

    if not is_washington:
        # Variables that hold male and female count
        male_count = city_df['Gender'].value_counts().loc['Male']
        female_count = city_df['Gender'].value_counts().loc['Female']
        total_gender = male_count + female_count
        
        # Calculate the male and female percentage
        male_percent = male_count / total_gender * 100
        female_count = 100 - male_percent

        # Print Male and Female count and their percentage
        print("Males count: {}, who constitute: {}%  of the users".format(male_count, round(male_percent,2)))
        print("Females count: {}, who constitute: {}%  of the users".format(female_count, round(female_count, 2)))
        print()
        
        # Variables that calculate the oldest user birth year, youngest user birth year, youngest user age, most common birth year
        oldest_user_bd = int(city_df['Birth Year'].min())
        youngest_user_bd = int(city_df['Birth Year'].max())
        current_year = date.today().year
        youngest_user_age = current_year - youngest_user_bd
        most_common_bd = int(city_df['Birth Year'].mode()[0])
        most_common_age = current_year - most_common_bd

        # Print oldest user birth year, youngest user birth year, youngest user age, most common birth year
        print("Oldest Users born in: {}".format(oldest_user_bd))
        print("youngest Users born in: {} and are {} years old.".format(youngest_user_bd, youngest_user_age))
        print("Most common year of birth: {}".format(most_common_bd))
        print("Peak age for people using the Bikeshare app is: {}".format(most_common_age))
    
    # prompt the user to display the raw data
    prompt_user_raw_data(city_df)

if __name__ == "__main__":
    main_function()
    while True:
        print()
        print('Analysis finished!')
        input_message = input("Press 'Y' to continue and 'N' to exit\n")
        if input_message in ['Y', 'y', 'yes', 'Yes']:
            main_function()
        elif input_message in ['N','n','no','No','nope','Nope']:
            print ('Exiting...')
            break
        else:
            print('Invalid input!')
            print('Exiting...')
            break