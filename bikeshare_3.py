import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': '/Users/jbreu/Downloads/bikeshare-2/chicago.csv',
              'new york city': '/Users/jbreu/Downloads/bikeshare-2/new_york_city.csv',
              'washington': '/Users/jbreu/Downloads/bikeshare-2/washington.csv' }


def intro():
    print("Hello! Looking forward to exploring bike share data with you!")
    print("We are reviewing data between three cities and thier bike share programs.")
    print('-'*40)
    print("The three cities are Chicago, New York City, and Washington")
     # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Please select a city. Or, enter 'all' to choose all three --->  ")
        if city.lower() in ['chicago', 'new york city', 'washington', 'all']:
            break
        else:
            print("\nSorry... please enter an acceptable input!")
    while True:
        month = input("Please enter the month you would like to review "
                              "(January through June). Or, choose 'all' to select all --->  ") 
        if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("\nSorry... please enter an acceptable input!")        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day of the week you would like to review "
                            "(Monday through Sunday). Or, choose 'all' to select all --->  ")
        if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("\nSorry... please enter an acceptable input!")
            
    print("\nThank you! You have made the following selections: \n")
    print("City: {}".format(city.title()))
    print("Month: {}".format(month.title()))
    print("Day: {}".format(day.title()))
    print("\nLet's get started!\n")
    print('-'*40)
    
    return city, month, day
    
    
def load_data(city, month, day):
     #loading data file into a dataframe
    df = []
    if city == 'all':
       for file in CITY_DATA:
            data = pd.read_csv(CITY_DATA[file])
            df.append(data)
       df = pd.concat(df)
    else:
        df = pd.read_csv(CITY_DATA[city])
        
    #converting the start time colum to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #extracting month and day from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    
        
    #filtering by month to create a new dataframe
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
        
    if day != 'all':
        df = df[df['Day_of_Week'] == day.title()]
    
    return df


def initial_stats(df):
    print("Calculating the most frequent time of travel... \n")
    start_time = time.time()
    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    pop_month = months[int((df['Month'].mode())) - 1]
    print("The most popular month for rentals is: {}".format(pop_month))
    
    # display the most common day of week
    print("The most popular day for rentals is: {}".format(df['Day_of_Week'].mode().values))

    # display the most common start hour
    print("The most popular hour for rentals to begin is: {}".format(df['Start Time'].dt.hour.mode().values))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # display most commonly used start station / creating a new dataframe counting the most used start stations 
    s_station = df.groupby(['Start Station']).size().reset_index(name="total trips")
    print("The top five start stations are: \n")
    print((s_station.sort_values(by=['total trips'], ascending=False)[:5]))

    # display most commonly used end station / / creating a new dataframe counting the most used end stations
    e_station = df.groupby(['End Station']).size().reset_index(name="total trips")
    print("\nThe top five ending stations are: \n")
    print((e_station.sort_values(by=['total trips'], ascending=False)[:5]))

    # display most frequent combination of start station and end station trip
    print("\nThe top five combination of start/end stations are: \n")
    df['combined'] = df['Start Station'] + df['End Station']
    combined = df.groupby(['combined']).size().reset_index(name='combined totals')
    print((combined.sort_values(by=['combined totals'], ascending=False)[:5]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Durations...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: {}".format(int(df['Trip Duration'].sum())))

    # display mean travel time
    print("Average travel time: {}".format(int(df['Trip Duration'].mean())))
    
    #display longest trip
    print("Longest travel time: {}".format(int(df['Trip Duration'].max())))
    
    #display shortest trip
    print("Shortest travel time: {}".format(int(df['Trip Duration'].min())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Total User Counts")
    print(df.groupby(['User Type']).size().reset_index(name="total"))


    # Display counts of gender
    print("\nTotal Gender Counts")
    try:
        df['Gender'] = df['Gender'].fillna("unknown")
        print(df.groupby(['Gender']).size().reset_index(name="total"))
    except KeyError:
        print("There is no gender data to review.")

    # Display earliest, most recent, and most common year of birth
    print("\nReview of Renters Ages")
    try:
        print("\nThe youngest renter was born in: {}".format(int(df['Birth Year'].min())))
        print("\nThe oldest renter was born in: {}".format(int(df['Birth Year'].max())))
        print("\nThe most common renters were born in: {}".format(int(df['Birth Year'].mode())))
    except KeyError:
        print("There is no birth year data to review.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def full_frame(df):
    print("Generating the first five rows from the data set you selected, "
          "sorted in ascending order by trip duration... ")
    #setting display option to show all columns
    pd.set_option("display.max_columns", None)
    df = df.sort_values(by=['Trip Duration', 'Day_of_Week'], ascending = False)
    next_5 = 'y'
    i = 0
    while next_5.lower() == 'y':
        print(df[i:i+5])
        i += 5
        next_5 = input("Would you like to see the next five rows of data?  Enter y or n ---> ")
        

def main():
    while True:
        city, month, day = intro()
        df = load_data(city, month, day)
        
        initial_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        full_frame(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
