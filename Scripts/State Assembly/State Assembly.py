from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl
import sys

state_assembly_url = 'https://nyassembly.gov/mem/'
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}


def main():
    # Test if we can access the site. If there are any errors being thrown, exit the program.
    try:
        request = requests.get(state_assembly_url, headers=user_agent)
    except:
        sys.exit('Invalid URL. Verify the State Assembly link!')

    # Go to the site and get the contents of the HTML.
    html_text = request.text
    soup = BeautifulSoup(html_text, 'lxml')

    # Start extracting from the HTML text.
    state_assembly_items = soup.find_all('section', class_='mem-item')

    # Initialize am array that will hold arrays of extracted data for each State assembly member.
    extracted_data = []

    # Each member in the list of State Assembly Members:
    for member in state_assembly_items:

        # Initialize an empty array to store the extracted information.
        # Data will be formatted as the following:
        # [District No., Name, Email, Address(es) & Phone Number(s)]
        sa_data = []

        # Data we are looking to extract from the Website:
        district_num = ''  # State Assembly's district number.
        sa_name = ''  # State Assembly member's name.
        sa_email = ''  # State Assembly member's email address.
        sa_office = ''  # State Assembly member's office address.

        # If we find a header element with the class name of 'mem-name', then extract the district number and name.
        if member.find('h3', class_='mem-name'):
            # The name and the district number is spaced out with tabs ('\t'). Split on the '\t'.
            lst = list(filter(None, member.find('h3', class_='mem-name').text.strip().split('\t')))[::-1]
            # For each string in the split string:
            for n in range(len(lst)):
                # If the word district is a substring of the string, then we found our district number.
                if 'district' in lst[n].lower():
                    district_num = lst[n]
                # If the word district is not a substring of the string, then we most likely found our member's name.
                if 'district' not in lst[n].lower():
                    sa_name = lst[n]

            # Check if we still have any empty strings after extracting district number and name
            if not sa_name:
                sa_name = 'No info found.'  # If the element doesn't exist, then default to no value found.
            if not district_num:
                district_num = 'No info found.'  # If the element doesn't exist, then default to no value found.
        else:
            sa_name = 'No info found.'  # If the element doesn't exist, then default to no value found.
            district_num = 'No info found.'  # If the element doesn't exist, then default to no value found.

        # If we find a div element with a class name of 'mem-email', then extract the email address.
        if member.find('div', class_='mem-email'):
            sa_email = member.find('div', class_='mem-email').text.strip()
        else:
            sa_email = 'No info found.'  # If the element doesn't exist, then default to no value found.

        # If we find div elements with a class name of 'full-addr', then extract the address(es) and phone number(s).
        if member.findAll('div', class_='full-addr'):
            # Temporary string we will use to concat the address and phone number to
            address = ''
            # For each address found:
            for addr in member.findAll('div', class_='full-addr'):
                # Concat the address to the temporary string.
                address = address + addr.text.strip() + '\n'
            # Once we have added all out address(es) and phone number(s), add the info to our respective data variable.
            sa_office = sa_office + address.strip()
        else:
            sa_office = 'No info found.'  # If the element doesn't exist, then default to no value found.

        # Add all the extracted data into the array.
        sa_data = sa_data + [district_num, sa_name, sa_email, sa_office]

        # Append the info extracted for the representative to list of extracted data.
        extracted_data.append(sa_data)

    # Sort the data by the first element in each array. In other words, sort by the district number.
    extracted_data.sort(key=lambda x: get_district_num(x[0]))

    # Export the data into a .csv file and also and .xlsx
    export_data(extracted_data)


# Helper sort method to convert string into a number to sort extracted data numerically.
def get_district_num(txt):
    num = 0  # The numerical value found in the string.
    # For each character in the string
    for char in txt:
        # If the ASCII value of the character is between 48 and 57, it's a digit.
        if 48 <= ord(char) <= 57:
            num = num * 10 + int(char)  # Parse the character as a number and multiply the number by 10 and add it.
    return num  # Return the numerical value.


# Helper file method to export the extracted data to .csv file and a .xlsx file.
def export_data(lst):
    # Headers for the Excel file to describe the columns of the data.
    headers = ["District No.", "Name", "Email", "Addresses & Phone Number(s)"]

    # Datetime objects to grab both the data and time the script was executed.
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")  # Date is saved in YYYY/MM/DD HHMM format.

    # Data filtered and extracted. Export the info into .csv file.
    with open('State Assembly ' + datetime_obj + '.csv', 'w', newline='', encoding='utf-8') \
            as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for district in lst:
            writer.writerow(district)  # Append the data we extracted from earlier to .csv file.

    # Data filtered, extracted, and now needs to be exported as .xlsx file.
    wb = xl.Workbook()  # Create an Excel workbook.
    ws = wb.active  # Create a sheet within the workbook.
    ws.title = "State Assembly"  # Name the worksheet: Senators.
    ws.append(headers)  # Add the column names to the sheet.

    # For each state assembly member we extracted, write to the Excel sheet.
    for district in lst:
        ws.append(district)

    # Adjust column size by max length of cell length for readable convenience
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length

    # Save the file:
    wb.save(filename='State Assembly ' + datetime_obj + ".xlsx")

    # Let the user know that the data has been exported
    print('Program complete!')
    print('Data outputted to (as a .csv) :', 'State Assembly ' + datetime_obj + '.csv')
    print('Data outputted to (as a .xlsx) :', 'State Assembly ' + datetime_obj + '.xlsx')


if __name__ == "__main__":
    main()
