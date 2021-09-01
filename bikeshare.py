""" DOCUMENTATION FILE """
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS_LIST = ["all", "january", "february", "march", "april", "may",
               "june", "july", "august", "september", "october", "november", "december"]

DAYS_LIST = ["all", "monday", "tuesday", "wednesday",
             "thursday", "friday", "saturday", "sunday"]


def get_hour_minutes_from_seconds(seconds_total):
    """
    Gets hours and minutes from seconds total

    Args:
        (int) seconds_total - our total amount of seconds we will get hours and minutes from

    Returns:
        (int) hours - total amount of hours
        (int) minutes - total amount of minutes
        (int) seconds - total amount of seconds

    """
    seconds = seconds_total % (24 * 3600)
    hours = seconds_total // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return hours, minutes, seconds


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    iscityvalid = False
    cities_abreviated = {"chg": "chicago",
                         "nyc": "new york city", "wa": "washington"}

    while not iscityvalid:
        city = input(
            "Please enter the city (Example: Chicago, New York City, Washington) : ")
        city = city.lower()

        if city in cities_abreviated.values():
            iscityvalid = True
        elif any(city in val for val in cities_abreviated):
            for value in cities_abreviated:
                if city in value:
                    city = cities_abreviated[value]
                    iscityvalid = True
        else:
            print(
                f"I'm sorry, please try entering another city as we weren't able to find {city}.\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    ismonthvalid = False
    while not ismonthvalid:
        month = input("Please enter the month: ")
        month = month.lower()

        if any(month in val for val in MONTHS_LIST):
            for value in MONTHS_LIST:
                if month in value:
                    month = value
                    ismonthvalid = True
        else:
            print(
                f"I'm sorry, please try entering another month as we weren't able to find {month}.\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    isdayvalid = False
    while not isdayvalid:
        day = input("Please enter the day: ")
        day = day.lower()

        if any(day in val for val in DAYS_LIST):
            for value in DAYS_LIST:
                if day in value:
                    day = value
                    isdayvalid = True
        else:
            print(
                f"I'm sorry, please try entering another day as we weren't able to find {day}.\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # Changing time to a datetime object for better usability
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Creating column for better usability for months
    df['Month'] = df['Start Time'].dt.month

    # Creating a new column for the day of the week
    df['Day Of Week'] = df['Start Time'].dt.dayofweek

    # Creating column for hour 
    df['Hour'] = df['Start Time'].dt.hour

    # Creating a column of start station to end station
    df['Start to End'] = "From: " + \
        df['Start Station'] + " To: " + df['End Station']

    # Filter for month and remove all months that don't match
    if month != "all":
        df = df[df['Start Time'].dt.month == MONTHS_LIST.index(month)]

    # Filter for day of week and remove all days that don't match
    if day != "all":
        df = df[df['Start Time'].dt.dayofweek == DAYS_LIST.index(day) - 1]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.


    Args:
        (Dataframe) df - The dataframe that we display our statistics from.

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is: " +
          str(MONTHS_LIST[df['Month'].mode()[0]]))

    # TO DO: display the most common day of week
    print("The most common day of week is: " +
          str(DAYS_LIST[df['Day Of Week'].mode()[0] + 1]))

    # TO DO: display the most common start hour
    common_hour = int(df['Hour'].mode()[0])
    hour_str = ""

    # Check if our hour is greater than 12 then change the string to PM otherwise AM
    if common_hour > 12:
        common_hour = common_hour - 12
        hour_str = f"{common_hour} P.M."
    else:
        hour_str = f"{common_hour} A.M."
    print("The most common hour is: " + hour_str)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (Dataframe) df - The dataframe that we display our statistics from.

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is: " +
          str(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most common end station is: " +
          str(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print("The most common end station is: " +
          str(df['Start to End'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (Dataframe) df - The dataframe that we display our statistics from.

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    # Taken from https://www.askpython.com/python/examples/convert-seconds-hours-minutes
    total_time = df['Trip Duration'].sum()
    hour, minute, second = get_hour_minutes_from_seconds(total_time)

    print(
        f"Total travel time is {int(hour)} hours, {int(minute)} minutes, {int(second)} seconds.")

    # TO DO: display mean travel time
    total_time = df['Trip Duration'].mean()
    hour, minute, second = get_hour_minutes_from_seconds(total_time)

    print(
        f"Mean travel time is {int(hour)} hours, {int(minute)} minutes, {int(second)} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (Dataframe) df - The dataframe that we display our statistics from.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The counts for user types is: " + "\n" +
          str(df['User Type'].dropna().value_counts()))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("\nThe counts for gender types is: " + "\n" +
              str(df['Gender'].dropna().value_counts()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nThe earliest birth year is: " +
              str(int(df['Birth Year'].dropna().min())))
        print("\nThe most recent birth year is: " +
              str(int(df['Birth Year'].dropna().max())))
        print("\nThe most common birth year is: " +
              str(int(df['Birth Year'].dropna().mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ 
    For displaying raw data 

    Args:
        (Dataframe) df - The dataframe that we display our statistics from.
    """
    i = 0
    # TO DO: convert the user input to lower case using lower() function
    raw = input("Please enter yes or no to display the raw data: ")
    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            # TO DO: appropriately subset/slice your dataframe to display next five rows
            print(df[i:i+5])
            # TO DO: convert the user input to lower case using lower() function
            raw = input(
                "\nPlease enter yes or no to continue to view the data")
            i += 5
        else:
            raw = input(
                "\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
