---
attachments: [Clipboard_2024-01-20 (2).png, Clipboard_2024-01-20 (3).png, Clipboard_2024-01-20 (4).png, Clipboard_2024-01-20 (5).png, Clipboard_2024-01-20 (6).png, Clipboard_2024-01-20 (7).png, Clipboard_2024-01-20 (8).png, Clipboard_2024-01-20 (9).png, Clipboard_2024-01-20 (10).png, Clipboard_2024-01-20 (11).png, Clipboard_2024-01-20 (12).png, Clipboard_2024-01-20.png]
title: report
created: '2024-01-20T09:13:42.433Z'
modified: '2024-01-20T10:21:51.938Z'
---

# report
## Python Final Project
> Data Engineering Campus
> Fanap & Filoger
> Author: Saleh Mohammad Gholamzadeh

# Project Description

## Notes:

1. Throughout all files, the `logging` module is used instead of `print`, and errors are stored in `error.log`.
2. Try-except is used for error handling.
3. Necessary inputs are taken from the user via `ArgParse` and the command line.

## File (PROGRAM) 1:

- In this file, two start and end dates are taken from the user, and after certain constraints are checked, such as ensuring the End date is not smaller than the Start date. Additionally, the type and format of the input data are validated.
  
- Then, a check is performed, and if absent, the temporary `stage` folder is created in the same directory.
  
- Using the `get_dates_between` function, all entered dates are checked and saved.
  
- The `etching_excel_files` function, using the format of the Iran Stock Organization link, downloads the Excel files related to stock transactions in the saved dates and stores them in the temporary `stage` folder.
  
- Checking for holidays (non-working days at the end of the week is done at this stage), and files related to these days are not downloaded with the help of the `is_iranian_weekend` function. However, it might be better to check for holidays in the `get_dates_between` function in future improvements.

### Test Case
![](@attachment/Clipboard_2024-01-20.png)
![](@attachment/Clipboard_2024-01-20 (2).png)
![](@attachment/Clipboard_2024-01-20 (3).png)

## File (PROGRAM) 2:
- In this program, the existence of the `dataLake` folder in the current directory is checked. If it does not exist, it is created using the `create_folder_if_not_exists` function.

- Using the `converting_to_csv` function, Excel files in the temporary `stage` folder are converted to CSV files and moved to the `dataLake` folder.

- Additionally, the `delete_files_in_folder` function, if desired by the user, deletes the Excel files in the temporary folder.

- The program prompts the user for two inputs: the address and name of the temporary folder, and their preference for deleting Excel files from the temporary folder after conversion and transfer.

### Test Case
![](@attachment/Clipboard_2024-01-20 (4).png)
![](@attachment/Clipboard_2024-01-20 (5).png)
![](@attachment/Clipboard_2024-01-20 (6).png)


## File (PROGRAM) 3:

In this program, we first create a `dataclass` that helps with quick work with CSV files in a key-oriented manner.

Then, a class named `StockAnalyzer` is created. This class includes methods for initializations, reading data, and analyzing CSV files.

1. **`analyze_price_change_percentage`**: In this method, the percentage of daily price changes is calculated for the top ten stocks with the highest price changes.

2. **`analyze_volume`**: Another key indicator, the trading volume of stocks, is examined, and the top ten stocks with the highest trading volume are displayed.

3. **`analyze_price_range`**: The price range of stocks, meaning the minimum and maximum traded prices in a day for a stock, is considered. It is expressed as a percentage change from the minimum price.

Additionally, the `prettytable` module is used for displaying all the information.

### Test Case
![](@attachment/Clipboard_2024-01-20 (7).png)
![](@attachment/Clipboard_2024-01-20 (8).png)
![](@attachment/Clipboard_2024-01-20 (9).png)
![](@attachment/Clipboard_2024-01-20 (10).png)
In this program, due to a small mistake in the `analyze_volume` method, an error is generated and logged in the `error.log` file.

![](@attachment/Clipboard_2024-01-20 (11).png)

In this program, in addition to printing tables as seen above, messages are also logged to a file.

![](@attachment/Clipboard_2024-01-20 (12).png)

### Pay Attention
def configure_logging():
    """
    Configure logging to save messages to a file and display in the terminal.

    - Messages with severity level ERROR and above will be saved in 'error.log'.
    - Messages with severity level INFO and above will be displayed in the terminal.

    """
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

    # Retrieve the file handler and set its level to a higher level than INFO
    file_handler = next((h for h in logging.getLogger('').handlers if isinstance(h, logging.FileHandler)), None)
    if file_handler:
        file_handler.setLevel(logging.WARNING)  # Set to WARNING or higher






