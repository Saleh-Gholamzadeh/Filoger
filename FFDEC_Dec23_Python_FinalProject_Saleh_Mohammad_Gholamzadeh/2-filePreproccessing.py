import os
import pandas as pd
import openpyxl
import argparse
import logging

def configure_logging():
    # Configure logging to save messages to a file and display in the terminal
    logging.basicConfig(filename='error.log', level=logging.ERROR,
                        format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logging.getLogger('').setLevel(logging.INFO)

    # Create a console handler and set the level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and attach it to the console handler
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger
    logging.getLogger('').addHandler(console_handler)

def create_folder_if_not_exists(folder_path):
    try:
        # Check if the folder exists; if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Folder created: {folder_path}")
    except Exception as e:
        logging.error(f"An error occurred while creating folder: {e}")

def converting_to_CSV(stageDirectory):
    try:
        files = os.listdir(stageDirectory)
        for file in files:
            file_path = os.path.join(stageDirectory, file)

            if os.path.isfile(file_path):
                # Load the Excel file into a Pandas DataFrame
                df = pd.read_excel(file_path, header=None, index_col=None)
                # Check if the DataFrame has at least 4 rows
                if len(df) <= 4:
                    logging.info(f"Processing file: {file_path}, which is empty")
                    os.remove(file_path)
                    logging.info(f'The file {file_path} has been deleted.')
                else:
                    # Remove the first two rows from the DataFrame
                    df = df.iloc[2:]

                    # Save the DataFrame to a CSV file in the destination directory
                    csv_file_name = f"{file.split('.')[0]}.csv"
                    csv_file_path = os.path.join(destination_directory, csv_file_name)
                    df.to_csv(csv_file_path, index=False, header=False)
                    logging.info(f"File {file} has been converted to {csv_file_name}")
    except Exception as e:
        logging.error(f"An error occurred during CSV conversion: {e}")

def delete_files_in_folder(folder_path, status):
    try:
        files = os.listdir(folder_path)
        if status == "Yes":
            # Iterate through the files and delete each one
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                logging.info(f"Deleted: {file_path}")

            logging.info("All files deleted successfully.")
        else:
            logging.info("According to your decision, Excel files in stage wouldn't be deleted.")
    except Exception as e:
        logging.error(f"An error occurred during file deletion: {e}")

configure_logging()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input the stage folder directory and choose deletion status for files after converting to CSV format and moving to dataLake")
    parser.add_argument('stageFolderDirectory', type=str, help="Specify the stage folder directory")
    parser.add_argument('deletionStatus', type=str, help="Specify deletion status. 'Yes' for deletion after format conversion, and 'No' for not deleting after format conversion")

    args = parser.parse_args()

    stageFolderDirectory = args.stageFolderDirectory
    deletionStatus = args.deletionStatus

# Specify the paths
current_path = os.getcwd()  # Get the current working directory
# Choose another folder within the parent directory
another_folder = 'dataLake'
destination_directory = os.path.join(current_path, another_folder)
create_folder_if_not_exists(destination_directory)

converting_to_CSV(stageFolderDirectory)

delete_files_in_folder(stageFolderDirectory, deletionStatus)
