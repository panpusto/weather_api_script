# weather.py

## usage:
**weather.py [-h] [-l [LOCATION]] [-sd [START_DATE]] [-ed [END_DATE]] [-d] [-s SAVE]**

## optional arguments:
| Args                                        | Description                                                    |
|---------------------------------------------|----------------------------------------------------------------|
| -h, --help                                  | show this help message and exit                                |
| -l [LOCATION], --location [LOCATION]        | city name (default: Wrocław)                                   |
| -sd [START_DATE], --start_date [START_DATE] | start date in format: YYYY-MM-DD (default: 2023-02-05)         |
| -ed [END_DATE], --end_date [END_DATE]       | end date in format: YYYY-MM-DD (optional argument)             |
| -d, --display                               | display weather data in terminal                               |
| -s SAVE, --save SAVE                        | save weather data as csv file, write 'filename' after argument |

**for example:**
- ***if you want to display today's weather for default location***
  - `python3 weather.py -l -sd -d`
- ***if you want to display weather from today to selected date for selected location***
  - `python3 weather.py -l Cracow -sd -ed 2023-02-12 -d`
- ***if you want to save weather info to a file instead of displaying it***
  - `python3 weather.py -l Warsaw -sd 2023-02-08 -ed 2023-02-15 -s my_data`

