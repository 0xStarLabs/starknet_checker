import json
import sys
import urllib3
from loguru import logger
import pandas as pd



def configuration():
    urllib3.disable_warnings()
    logger.remove()
    logger.add(sys.stdout, colorize=True,
               format="<light-cyan>{time:HH:mm:ss}</light-cyan> | <level> {level: <8}</level> | - <white>{"
                      "message}</white>")

def read_files():
    with open("./addresses.txt") as file:
        return [line.strip() for line in file if line.strip()]



def check(addresses):
    json_files = [
        "./db/0.json", "./db/1.json", "./db/2.json", "./db/3.json",
        "./db/4.json", "./db/5.json", "./db/6.json"
    ]

    # Store found addresses and amounts
    found_data = []

    # Track found addresses to identify which ones are not found
    found_addresses = set()

    # Initialize total amount
    total_amount = 0

    for file_name in json_files:
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                for eligible in data['eligibles']:
                    if eligible['identity'] in addresses:
                        logger.success(f"{eligible['identity']} amount: {eligible['amount']}")
                        found_addresses.add(eligible['identity'])
                        found_data.append({'Address': eligible['identity'], 'Amount': eligible['amount']})
                        # Update total amount, assuming 'amount' is a numeric value
                        if eligible['amount'] != 'Not Found':
                            total_amount += int(eligible['amount'])
        except FileNotFoundError:
            logger.error(f"{file_name} not found.")


       # Check for addresses that were not found in any file
    not_found_addresses = set(addresses) - found_addresses
    for address in not_found_addresses:
        logger.error(f"{address} not found in any file.")
        found_data.append({'Address': address, 'Amount': 'Not Found'})
    
    logger.info(f"Total amount: {total_amount}")

    # Create DataFrame
    df = pd.DataFrame(found_data)
    # Reorder df to place not found addresses at the end
    df['NotFound'] = df['Amount'] == 'Not Found'
    df.sort_values(by='NotFound', inplace=True)
    df.drop(columns=['NotFound'], inplace=True)
    # Insert blank column
    df.insert(2, 'Blank', '')

    # Add total amount row at the bottom using pd.concat
    total_row = pd.DataFrame([{'Address': 'Total', 'Amount': total_amount, 'Blank': ''}])
    df = pd.concat([df, total_row], ignore_index=True)

    # Save to Excel
    df.to_excel('addresses_and_amounts.xlsx', index=False)


def main():
    configuration()
    addresses = read_files()
    addresses_lower = []
    for address in addresses:
        addresses_lower.append(address.lower())
    check(addresses_lower)

if __name__ == "__main__":
    main()
