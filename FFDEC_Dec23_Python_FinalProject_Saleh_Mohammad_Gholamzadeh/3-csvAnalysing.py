import csv
from dataclasses import dataclass
import logging
from prettytable import PrettyTable
import locale
import argparse

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

locale.setlocale(locale.LC_ALL, '')

@dataclass
class Stock:
    symbol: str
    name: str
    quantity: int
    volume: int
    value: int
    yesterday: int
    first_trade: int
    last_trade_quantity: int
    last_trade_change: int
    last_trade_percent: float
    final_price_quantity: int
    final_price_change: int
    final_price_percent: float
    min_price: int
    max_price: int

class StockAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.stocks = []

    def read_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    stock = Stock(
                        symbol=row.get('نماد', ''),
                        name=row.get('نام', ''),
                        quantity=int(row.get('تعداد', 0)),
                        volume=int(row.get('حجم', 0)),
                        value=int(row.get('ارزش', 0)),
                        yesterday=int(row.get('دیروز', 0)),
                        first_trade=int(row.get('اولین', 0)),
                        last_trade_quantity=int(row.get('آخرین معامله - مقدار', 0)),
                        last_trade_change=int(row.get('آخرین معامله - تغییر', 0)),
                        last_trade_percent=float(row.get('آخرین معامله - درصد', 0)),
                        final_price_quantity=int(row.get('قیمت پایانی - مقدار', 0)),
                        final_price_change=int(row.get('قیمت پایانی - تغییر', 0)),
                        final_price_percent=float(row.get('قیمت پایانی - درصد', 0)),
                        min_price=int(row.get('کمترین', 0)),
                        max_price=int(row.get('بیشترین', 0)),
                    )
                    self.stocks.append(stock)
        except Exception as e:
            logging.error(f"Error reading data from {self.file_path}: {str(e)}")
            raise  # Raise an exception to stop further execution

    def analyze_price_change_percentage(self):
        logging.info("Analysis 1: Daily Price Change Percentage")
        try:
            top_ten_stocks = sorted(self.stocks, key=lambda x: ((x.final_price_quantity - x.yesterday)/x.yesterday) * 100, reverse=True)[:10]

            table = PrettyTable()
            table.field_names = ["Symbol", "Name", "Price Change Percentage"]
            for stock in top_ten_stocks:
                price_change_percentage = ((stock.final_price_quantity - stock.yesterday)/stock.yesterday) * 100
                formatted_percentage = "{:,.2f}%".format(price_change_percentage)
                table.add_row([stock.symbol, stock.name, formatted_percentage])

            print(table)

        except Exception as e:
            logging.error(f"Error analyzing price change percentage: {str(e)}")

    def analyze_volume(self):
        logging.info("Analysis 2: Trading Volume")
        try:
            top_ten_stocks = sorted(self.stocks, key=lambda x: x.volume, reverse=True)[:10]

            table = PrettyTable()
            table.field_names = ["Symbol", "Name", "Volume"]

            for stock in top_ten_stocks:
                formatted_volume = "{:,d}".format(stock.volume)
                table.add_row([stock.symbol, stock.name, formatted_volume])
            print(table)

        except Exception as e:
            logging.error(f"Error analyzing volume and trends: {str(e)}")

    def analyze_price_range(self):
        logging.info("Analysis 3: Price Range Analysis")
        try:
            top_ten_stocks = sorted(self.stocks, key=lambda x: (x.max_price - x.min_price), reverse=True)[:10]

            table = PrettyTable()
            table.field_names = ["Symbol", "Name", "Price Range", "Price Range Percentage"]
            for stock in top_ten_stocks:
                price_range = (stock.max_price - stock.min_price)
                price_range_percentage = ((stock.max_price - stock.min_price) / stock.min_price) * 100
                formatted_price_range = "{:,d}".format(price_range)
                formatted_percentage =  "{:,.2f}%".format(price_range_percentage)
                table.add_row([stock.symbol, stock.name, formatted_price_range, formatted_percentage])
            print(table)

        except Exception as e:
            logging.error(f"Error analyzing price range: {str(e)}")
            
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Input your desired csv file directory. In the format folder/csv_name.csv")
    parser.add_argument('csv_path', type=str, help="Enter the csv file path.")

    args = parser.parse_args()

    csv_file_path = args.csv_path
    
if __name__ == "__main__":
    file_path =csv_file_path
    analyzer = StockAnalyzer(file_path)
    
    try:
        analyzer.read_data()
        analyzer.analyze_price_change_percentage()
        analyzer.analyze_volume()
        analyzer.analyze_price_range()
    except Exception as e:
        # Handle the exception, if any, raised during the execution
        logging.error(f"Error during analysis: {str(e)}")
