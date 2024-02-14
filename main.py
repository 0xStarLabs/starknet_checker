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
    with open("./stark_addresses.txt") as file:
        stark_addresses = [line.strip() for line in file if line.strip()]
    
    with open("./evm_addresses.txt") as file:
        evm_addresses = [line.strip() for line in file if line.strip()]

    return stark_addresses, evm_addresses


def check_stark(addresses):
    json_files = [
        "./db/stark/0.json", "./db/stark/1.json", "./db/stark/2.json", "./db/stark/3.json",
        "./db/stark/4.json", "./db/stark/5.json", "./db/stark/6.json", "./db/stark/key0.json",
        "./db/stark/key1.json",
    ]

    # Store found addresses and amounts
    found_data = []

    # Track found addresses to identify which ones are not found
    found_addresses = set()

    # Initialize total amount
    total_amount = 0
    print("inside")
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
    df.to_excel('stark_amount.xlsx', index=False)


def check_evm(addresses):
    json_files = [
        "./db/eth/0.json", "./db/eth/1.json", "./db/eth/2.json", "./db/eth/3.json",
        "./db/eth/4.json", "./db/eth/5.json", "./db/eth/6.json",
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
    df.to_excel('evm_amount.xlsx', index=False)


def main():
    configuration()
    stark_addresses, evm_addresses = read_files()
    
    print("Choose an option:")
    print("1. Stark checker")
    print("2. Eth checker")
    choice = int(input("Enter your choice: "))

    
    if choice == 1:
        stark_addresses_lower = []
        for address in stark_addresses:
            stark_addresses_lower.append(address.lower())
        check_stark(stark_addresses_lower)
    elif choice == 2:
        evm_addresses_lower = []
        for address in evm_addresses:
            evm_addresses_lower.append(address.lower())
        check_stark(evm_addresses_lower)
    else:
        logger.error("Inccorect choice")

if __name__ == "__main__":
    main()
