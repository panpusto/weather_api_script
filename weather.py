import argparse
import requests
import requests_cache
import csv
from datetime import date, datetime
import os
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(dir_path, 'events.log'))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

requests_cache.install_cache(
    cache_name=f'{dir_path}/weather_cache',
    backend='sqlite', 
    expire_after=300)

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location",
                    nargs="?",
                    const='Wrocław',
                    help="city name (default: Wrocław)")
parser.add_argument("-sd", "--start_date",
                    nargs="?",
                    const=date.today(),
                    type=date.fromisoformat,
                    help=f"start date in format: YYYY-MM-DD (default: {date.today()} )")
parser.add_argument("-ed", "--end_date",
                    nargs="?",
                    const='',
                    type=date.fromisoformat,
                    help="end date in format: YYYY-MM-DD (optional parameter)")
parser.add_argument("-d", "--display",
                    action="store_true",
                    help="display weather data in terminal")
parser.add_argument("-s", "--save",
                    help="save weather data as csv file, write 'filename' after argument")

args = parser.parse_args()


def fetch_data(city, date1, date2):
    """
    Fetches weather data from api.
    :param city: location name
    :param date1: start date
    :param date2: end date
    :return: selected weather (temperature and precipitation) data as a dictionary
    """
    try:
        api_key = "4YDED2R9B2UNLJ7VJ9DZU2J4K"
        api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        url_1_arg = api_url + city + "/" + str(date1) + "?" + "key=" + api_key + "&unitGroup=metric"
        url_2_args = (
                api_url + city + "/" + str(date1) + "/" + str(date2) + "?" + "key=" + api_key + "&unitGroup=metric"
        )
        response = requests.request("GET", url_2_args if args.end_date else url_1_arg)
        data_dict = response.json()
        location = data_dict.get("resolvedAddress")
        number_of_days = len(data_dict.get("days"))
        selected_data = {
            "location": location,
            "days": [
            ]
        }
        for day in range(number_of_days):
            selected_data['days'].append(
                {
                    "date": data_dict.get("days")[day].get("datetime"),
                    "avg_temp": data_dict.get("days")[day].get("temp"),
                    "avg_precip": data_dict.get("days")[day].get("precip")
                }
            )
        return selected_data

    except requests.exceptions.JSONDecodeError:
        parser.print_help()
        logger.error("Wrong parameters type or city isn't in database. Check parameters format and try again.")

    except requests.exceptions.ConnectionError as err:
        logger.error('Connection error')

def display_weather_data(data):
    """
    Displays weather information in terminal.
    :return: weather information as a string
    """
    try:
        location = data.get("location")
        break_line = 40 * "-"
        print(f"Location: {location}")
        print(break_line)
        number_of_days = len(data.get("days"))
        for day in range(number_of_days):
            date_obj = datetime.strptime(data.get("days")[day].get("date"), "%Y-%m-%d")
            info = (
                f"Date: {date_obj.strftime('%d %B, %Y')}\n"
                f"Temperature: {data.get('days')[day].get('avg_temp')}°C\n"
                f"Precipitation: {data.get('days')[day].get('avg_precip')}mm"
            )
            print(info)
            print(break_line)
        logger.info(f'Data displayed: {data}')

    except AttributeError:
        return


def write_data_as_csv_file(data, file_name):
    """
    Saves data as csv file.
    :param data: weather data to write
    :param file_name: name of file
    :return: csv file with weather data
    """
    if os.path.isfile(f"{dir_path}/{file_name}.csv"):
        with open(f"{dir_path}/{file_name}.csv", "a", newline='') as csv_file:
            field_names = ["location", "date", "avg_temp", "avg_precip"]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            for row in data.get("days"):
                writer.writerow({
                    "location": data.get("location"),
                    "date": row["date"],
                    "avg_temp": row["avg_temp"],
                    "avg_precip": row["avg_precip"]})
            csv_file.flush()
        
    else:
        with open(f"{dir_path}/{file_name}.csv", "w", newline='') as csv_file:
            field_names = ["location", "date", "avg_temp", "avg_precip"]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            for row in data.get("days"):
                writer.writerow({
                    "location": data.get("location"),
                    "date": row["date"],
                    "avg_temp": row["avg_temp"],
                    "avg_precip": row["avg_precip"]})
            csv_file.flush()


if __name__ == "__main__":
    if args.location and args.start_date and args.display:
        fetched_data = fetch_data(args.location, args.start_date, args.end_date)
        display_weather_data(fetched_data)

    elif args.location and args.start_date and args.save:
        fetched_data = fetch_data(args.location, args.start_date, args.end_date)
        write_data_as_csv_file(fetched_data, args.save)
        logger.info(f'Data saved: {fetched_data}')

    elif not args.display and not args.save:
        parser.print_help()
        logger.error("Missing mandatory arg: -d/--display or -s/--save")
        print("Choose whether you want to display data or save it as csv file.")

    else:
        parser.print_help()
