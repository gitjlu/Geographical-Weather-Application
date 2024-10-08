"""Retrieve data for temperatures for users to analyze."""

import pgeocode
import requests
import math
import csv
import json


class HistoricalTemps:
    """Represents historical temperatures with attributes and such."""

    def __init__(self, zip_code: str, start: str = "1950-08-13",
                 end: str = "2023-08-25"):
        """Constructs/initializes a new HistoricalTemps object."""
        self._zip_code = zip_code
        self._start = start
        self._end = end

        lat, lon, loc_name = HistoricalTemps.zip_to_loc_info(zip_code)

        if math.isnan(lat) or math.isnan(lon):
            raise LookupError("Invalid zip code, please try again.")

        self._lat = lat
        self._lon = lon
        self._loc_name = loc_name
        self._temp_list = None
        self._load_temps()

    def _load_temps(self):
        """Give temperature tuples list."""
        request_url = "https://archive-api.open-meteo.com/v1/archive"

        parameters = {
            "latitude": self._lat, "longitude": self._lon,
            "start_date": self._start, "end_date": self._end,
            "daily": "temperature_2m_max", "timezone": "America/Los_Angeles"
            }

        api_response = requests.get(request_url, params=parameters)
        self._temp_list = HistoricalTemps._convert_json_to_list(
            api_response.text)

    def average_temp(self):
        """Calculate and return the average temperature."""
        total_temp = 0.0
        for date, temp in self._temp_list:
            total_temp += temp
        average = total_temp / len(self._temp_list)
        return average

    def extreme_days(self, threshold: float):
        """Return dates where the temperature exceeds the threshold."""
        return [(date, temp) for date, temp in self._temp_list
                if temp > threshold]

    def top_x_days(self, num_days=5):
        """Return the days with highest temperatures."""
        sorted_temp_days_list = sorted(
            self._temp_list, key=lambda x: x[1], reverse=True)[:num_days]
        return sorted_temp_days_list

    @property
    def start(self):
        """Gets start date."""
        return self._start

    @property
    def end(self):
        """Get end date."""
        return self._end

    @property
    def zip_code(self):
        """Get zip code."""
        return self._zip_code

    @property
    def loc_name(self):
        """Get location name aka loc_name."""
        return self._loc_name

    @start.setter
    def start(self, start: str):
        """Set start date and reloads start date."""
        old_start = self._start
        self._start = start
        try:
            self._load_temps()
        except LookupError:
            self._start = old_start
            raise LookupError("Invalid start date, reloading.")

    @end.setter
    def end(self, end: str):
        """Set end date and reloads end date."""
        old_end = self._end
        self._end = end
        try:
            self._load_temps()
        except LookupError:
            self._end = old_end
            raise LookupError("invalid end date, reloading.")

    @staticmethod
    def zip_to_loc_info(zip_code):
        """Return latitude, longitude, and location name."""
        geocoder = pgeocode.Nominatim('us')
        location_demo = geocoder.query_postal_code(zip_code)

        lat = location_demo.latitude
        lon = location_demo.longitude
        loc_name = location_demo.place_name

        return lat, lon, loc_name

    @staticmethod
    def _convert_json_to_list(data):
        """Convert json string from web to dictionary and extraction."""
        meta_data = json.loads(data)
        dates = meta_data['daily']['time']
        temps = meta_data['daily']['temperature_2m_max']
        temp_list = []
        for date, temp in zip(dates, temps):
            temp_list.append((date, temp))
        return temp_list


def create_dataset():
    """Prompts user for a zip code and then creates new class object."""
    zip_code = input("Please enter a zip code: ")

    try:
        dataset = HistoricalTemps(zip_code)
        return dataset
    except LookupError:
        print("Invalid zipcode, please check validation and try again.")
        return None


def compare_average_temps(dataset_one: HistoricalTemps,
                          dataset_two: HistoricalTemps):
    """Compare average temperatures of HistoricalTemps objects.

    Call method average_temp and print out result of averages on
    both datasets.
    """
    # Check if any dataset is empty.
    if dataset_one is None or dataset_two is None:
        print("Error: Both datasets cannot be None, please try again.")
        return

    # Variable to store the instance variables for function call.
    avg_temp_one = dataset_one.average_temp()
    avg_temp_two = dataset_two.average_temp()

    # Print the results with one decimal precision.
    print(f"{dataset_one.loc_name}: Average Temperature = {avg_temp_one:.2f}")
    print(f"{dataset_two.loc_name}: Average Temperature = {avg_temp_two:.2f}")


def print_extreme_days(dataset: HistoricalTemps):
    """Allow user to set threshold temperature and print days."""
    if dataset is None:
        print("Dataset is empty, please load a dataset.")
    try:
        threshold = float(input("Please enter a threshold temperature: "))
    except ValueError:
        print("Invalid input. Please enter a numeric number for temperature.")
        return None

    extreme_days_list = dataset.extreme_days(threshold)

    total_extreme_days = len(extreme_days_list)
    print(
        f"Total number of days that exceeded threshold temperature: "
        f"{total_extreme_days}")

    for date, temp in extreme_days_list:
        print(date, " ", temp)  # Prints each tuple in list.


def print_top_five_days(dataset: HistoricalTemps):
    """Print top five days of the sorted temperature list."""
    if dataset is None:
        print("Dataset is empty, please load a dataset.")
        return

    top_days_list = dataset.top_x_days(5)
    print(f"Top five days with the highest temperatures"
          f" at {dataset.loc_name}:")

    for date, temp in top_days_list:
        print(date, " ", temp)


def change_dates(dataset: HistoricalTemps):
    """Take user input of start/end dates and loads them."""
    if dataset is None:
        print("Dataset is empty, please load dataset.")
        return

    try:
        new_start = input("Enter new start date (YYYY-MM-DD): ")
        new_end = input("Enter new end date (YYYY-MM-DD): ")
        dataset.start = new_start
        dataset.end = new_end
    except LookupError:
        print("Invalid date, please try again.")
        return


def print_menu(dataset_one, dataset_two):
    """Print out the options available for the user."""
    print("Main Menu")
    if dataset_one is None:
        print("1 - Load dataset one")
    else:
        print(f"1 - Replace {dataset_one.loc_name}")

    if dataset_two is None:
        print("2 - Load dataset two")
    else:
        print(f"2 - Replace {dataset_two.loc_name}")

    print("3 - Compare average temperatures")
    print("4 - Dates above threshold temperature")
    print("5 - Highest historical dates")
    print("6 - Change start and end dates for dataset one")
    print("7 - Change start and end dates for dataset two")
    print("9 - Quit")


def menu():
    """Load selected option and its function for user."""
    dataset_one = None
    dataset_two = None

    while True:
        print_menu(dataset_one, dataset_two)
        user_input = input("Please enter your choice: ")

        try:
            option = int(user_input)
        except ValueError:
            print("Invalid input, please enter a number.")
            continue

        match option:
            case 1:
                print("Option 1 is selected, dataset one loading...")
                dataset_one = create_dataset()
            case 2:
                print("Option 2 is selected, dataset two loading...")
                dataset_two = create_dataset()
            case 3:
                print("Option 3 is selected, displaying average temperatures.")
                compare_average_temps(dataset_one, dataset_two)
            case 4:
                print("Option 4 is selected... threshold temperature.")
                print_extreme_days(dataset_one)
            case 5:
                print(f"Option 5 is selected... displaying highest"
                      f" historical dates.")
                print_top_five_days(dataset_one)
            case 6:
                print(f"Option 6 is selected... changing start"
                      f" date and end date for dataset one.")
                change_dates(dataset_one)

            case 7:
                print(f"Option 7 is selected... changing start"
                      f" date and end date for dataset two.")
                change_dates(dataset_two)
            case 9:
                print("Goodbye!")
                break
            case _:
                print("Invalid option, please enter a number 1-7 or 9.")


def main():
    """Prompts user for their name and print a message."""
    name = input("Please enter your name: ")
    print(f"Hi {name}, let's explore some historical temperatures.")
    menu()


if __name__ == "__main__":
    main()
