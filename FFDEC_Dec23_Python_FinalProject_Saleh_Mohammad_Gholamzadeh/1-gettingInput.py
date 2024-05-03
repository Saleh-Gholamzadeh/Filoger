import argparse
from jdatetime import datetime, timedelta
import jdatetime
import requests
import os
import logging

def configure_logging():
    # Configure logging to save messages to a file and display in the terminal
    logging.basicConfig(filename='error.log', level=logging.ERROR,
                        format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

     # Set the logging level for the root logger to INFO
    logging.getLogger('').setLevel(logging.INFO)

    # Create a console handler and set the level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and attach it to the console handler
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger
    logging.getLogger('').addHandler(console_handler)

configure_logging()

def is_iranian_weekend(day):
    try:
        # Check if the day is Thursday or Friday (weekend in Iran)
        # Assuming the date is in the format "YYYY-MM-DD"
        holiday_date = jdatetime.date.fromisoformat(day)
        return holiday_date.weekday() in [5, 6]
    except Exception as e:
        logging.error(f"Error in is_iranian_weekend function: {e}")
        return False

def get_dates_between(start_date_str, end_date_str):
    try:
        # Convert input strings to jdatetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Create a list to store the dates
        global all_dates

        # Calculate the number of days between start and end dates
        delta = timedelta(days=1)

        # Iterate through the range of dates and append to the list
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += delta

        return all_dates
    except Exception as e:
        logging.error(f"Error in get_dates_between function: {e}")
        return []

def fetching_excel_files(dataRange, directory):
    try:
        for date in dataRange:
            if is_iranian_weekend(date):
                pass
            else:
                # Get the Excel file URL
                excel_file_url = 'http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d='+date
                file_name = f"{date}.xlsx"

                # Fetch the Excel file using requests
                response = requests.get(excel_file_url)
                # Combine the folder and file name to get the local file path
                local_file_path = os.path.join(directory, file_name)
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Save the Excel file locally
                    with open(local_file_path, 'wb') as excel_file:
                        excel_file.write(response.content)
                    logging.info(f"Excel file '{file_name}' saved to '{local_file_path}' successfully.")
                else:
                    logging.error(f"Failed to fetch Excel file for date {date}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error in fetching_excel_files function: {e}")

all_dates = []

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Enter your desired date. Pay attention to the format (YYYY-MM-DD)")
    parser.add_argument('startDate', type=str, help="Starting Date for downloading files")
    parser.add_argument('endDate', type=str, help="Ending Date for downloading files")

    args = parser.parse_args()

    startDate = args.startDate
    endDate = args.endDate

    try:
        start_date_obj = datetime.strptime(startDate, '%Y-%m-%d')
        end_date_obj = datetime.strptime(endDate, '%Y-%m-%d')

        # Check if startDate is greater than endDate
        if start_date_obj > end_date_obj:
            raise ValueError("Start date should be less than or equal to end date.")
    except ValueError as ve:
        logging.error(f"Error in date validation: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error in date format: {e}")
        raise ValueError("Incorrect date format. Use YYYY-MM-DD.")

# Define the local folder to save the Excel file
data_folder = 'stage'
os.makedirs(data_folder, exist_ok=True)
result = get_dates_between(startDate, endDate)
fetching_excel_files(result, data_folder)
