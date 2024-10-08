[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=15489670)
# Objective

Demonstrate an understanding of:

* Unpacking JSON strings
* zip() function

# Specification

This is the second part of our API assignment, and completes our project for the class.  When you have completed this assignment you will be able to collect and compare temperature data from two locations for any time period in the past 70+ years.

Start with your code from Assignment Ten.

## Changes to the HistoricalTemps Class

### new static method: _convert_json_to_list(data)
This method will take a json string from open-meteo.com, convert the string to a dictionary using the appropriate json function, and then extract dates and temperatures for use in our projects.

The method will return a list of tuples, with each tuple containing a date and the corresponding maximum temperature.

As a requirement for this assignment, you should elegantly use the zip() function to create your list of tuples. Do note that the zip function does not produce a list, it produces a "zip object." We need to convert that to a list before returning.

### modification to _load_temps()
It is time to remove all the fake data from _load_temps(). We've already written code to get real data from open-meteo.com, we just need to pass the json string to our new method, _convert_json_to_list(), and then assign the result to self._temp_list.

Be sure you are passing a json string, not a requests object, to _convert_json_to_list().  Remember that we use the .text attribute to extract the json string from the requests object.

### modifications to start() and end() setters
We have coded setters for self._start and self._end, but up to this point they have not had any functionality. Rewrite these functions so that the data is reloaded every time the start or end date is changed.

Carefully note, if the new start or end date is invalid, then self._start or self._end should revert to the original date and a LookupError should be raised. There is no need to check whether the dates are valid, just "try" to load the new temperatures with the dates given.

Use _load_temps(), do not duplicate that code inside the setter. It might take a bit of thought to figure out how to "try" to load data using _load_temps() with the new date, while still reverting to the old date if the attempt fails. Remember, all of this should happen inside the setter, not at the module level.

## Module Level Changes

### new function change_dates(dataset: HistoricalTemps)

This function will allow the user to change the start and end dates of a dataset.

First check whether the dataset is loaded. If not, print a friendly message and return.

Ask the user to enter a start date. "Try" to change the start date using the setter. If it fails, print a friendly message and return. Otherwise ask the user to enter an end date.  "Try" to change the end data using the setter.  If it fails, print a friendly message and return.

Note that we are using the setters separately to change the start and end dates. This means that if the user enters a valid start date but an invalid end date, the start date will still be changed. This might seem a bit unsatisfactory, but it keeps our code simple.

### modification to menu() function

Modify items six and seven to call change_dates() with the appropriate dataset.

# Other Requirements

Any issues from prior assignments must be fixed in this assignment.

Your assignment will be submitted on GitHub. You should check to make sure
that all autograder tests have passed. Do not modify any of the testing code.

Your code should use the `if __name__ == "__main__"` pattern shown in the
modules.

There should be a module level docstring, a docstring for the class, and a
docstring for each function and method.

Follow the PEP-8 conventions you have learned so far.

# Instructor Sample Run

    Please enter your name: Eric
    Hi Eric, let's explore historical temperatures.
    
    Main Menu
    1 - Load dataset one
    2 - Load dataset two
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 1
    Please enter a zip code: 94065
    Main Menu
    1 - Replace Redwood City
    2 - Load dataset two
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 2
    Please enter a zip code: 94022
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 3
    The average maximum temperature for Redwood City was 19.29 degrees Celsius
    The average maximum temperature for Los Altos was 20.06 degrees Celsius
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 4
    List days above what temperature? 36
    There are 37 days above 36.0 degrees in Redwood City
    1954-06-20: 37.6
    1959-07-10: 36.8
    1961-06-14: 38.1
    1971-09-13: 38.0
    1971-09-14: 40.2
    1971-09-15: 36.6
    1973-06-20: 37.3
    1973-06-21: 36.3
    1976-06-24: 37.0
    1976-06-27: 36.8
    1979-09-11: 36.3
    1979-09-12: 36.2
    1980-10-01: 36.2
    1980-10-02: 36.4
    1980-10-03: 36.6
    1983-07-11: 36.3
    1984-09-08: 36.6
    1985-07-01: 36.5
    1987-10-05: 37.2
    1988-07-17: 38.4
    1993-08-01: 36.4
    2000-06-14: 39.1
    2003-06-26: 36.5
    2006-07-22: 36.5
    2008-06-20: 36.3
    2010-08-24: 36.1
    2017-09-01: 39.9
    2017-09-02: 40.8
    2019-06-10: 36.8
    2020-08-14: 36.5
    2020-09-06: 38.7
    2020-09-07: 38.9
    2020-09-28: 37.1
    2020-10-01: 37.0
    2022-09-05: 38.4
    2022-09-06: 41.8
    2022-09-08: 36.5
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 6
    Please enter a new start date (YYYY-MM-DD): 2022-11-10
    Please enter a new end date (YYYY-MM-DD): 2022-10-10
    End date could not be changed.  Please check that the end date is in the correct format and is after the current start date of 2022-11-10
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 4
    List days above what temperature? 36
    There are 0 days above 36.0 degrees in Redwood City
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 6
    Please enter a new start date (YYYY-MM-DD): 2000-10-10
    Please enter a new end date (YYYY-MM-DD): 2010-10-10
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 5
    Following are the hottest five days in Redwood City on record from
    2000-10-10 to 2010-10-10
    Date 2003-06-26: 36.5
    Date 2006-07-22: 36.5
    Date 2008-06-20: 36.3
    Date 2010-08-24: 36.1
    Date 2006-07-23: 35.4
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 6
    Please enter a new start date (YYYY-MM-DD): 2009-10-10
    Please enter a new end date (YYYY-MM-DD): 2020-10-10
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 5
    Following are the hottest five days in Redwood City on record from
    2009-10-10 to 2020-10-10
    Date 2017-09-02: 40.8
    Date 2017-09-01: 39.9
    Date 2020-09-07: 38.9
    Date 2020-09-06: 38.7
    Date 2020-09-28: 37.1
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 6
    Please enter a new start date (YYYY-MM-DD): e
    Start date could not be changed.  Please check that the start date is in the correct format and is before the current end date of 2020-10-10
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 5
    Following are the hottest five days in Redwood City on record from
    2009-10-10 to 2020-10-10
    Date 2017-09-02: 40.8
    Date 2017-09-01: 39.9
    Date 2020-09-07: 38.9
    Date 2020-09-06: 38.7
    Date 2020-09-28: 37.1
    Main Menu
    1 - Replace Redwood City
    2 - Replace Los Altos
    3 - Compare average temperatures
    4 - Dates above threshold temperature
    5 - Highest historical dates
    6 - Change start and end dates for dataset one
    7 - Change start and end dates for dataset two
    9 - Quit
    What is your choice? 
