from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl
import sys

nys_senate_URL = 'https://www.nysenate.gov/senators-committees'
senate_template_url = 'https://www.nysenate.gov'
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}


def main():
    # Test if we can access the site. If there are any errors being thrown, exit the program.
    try:
        request = requests.get(nys_senate_URL, headers=user_agent)
    except:
        sys.exit('Invalid URL. Verify the NYS Senate link!')

    # Go to the site and get the contents of the HTML.
    html_text = request.text
    soup = BeautifulSoup(html_text, 'lxml')

    # Grab all the senators' information.
    nys_senators = soup.find_all('div', class_='u-odd') + soup.find_all('div', class_='u-even')

    # Initialize am array that will hold arrays of extracted data for each Senator.
    extracted_data = []

    # For each senator in the list of senators:
    for senator in nys_senators:

        # Initialize an empty array to store the extracted information.
        # Data will be stored in the following format:
        # [District Number, Name of Senator, Senator URL ,Party Affiliation(s), Email Address, and Addresses and Phone
        # Number(s)]
        senate_data = []

        # Data we are looking to extract from the Website:
        district_party = ''  # Party Affiliation.
        district_num = ''  # Senator's District Number.
        senator_name = ''  # Senator's Name.
        senator_url = ''  # Senator's URL.
        senator_email = ''  # Senator's Email Address.
        address_lst = ''  # Senator's Address.

        # Extract the senator's party.
        if senator.find(class_='nys-senator--party'):
            district_party = senator.find(class_='nys-senator--party').text.strip()
        else:
            district_party = "No info found."  # If the element doesn't exist, default to no value found.

        # Remove the party from HTML Contents. This will make it easier to extract the name and district number.
        senator.find(class_='nys-senator--party').decompose()

        # If we can find the class that contains 'nys-senator--district', then extract the district number.
        if senator.find(class_='nys-senator--district'):
            district_num = senator.find(class_='nys-senator--district').text.strip()
        else:
            district_num = 'No info found.'  # If the element doesn't exist, default to no value found.

        # If we can find the class that contains 'nys-senator--name', then extract the senator's name.
        if senator.find(class_='nys-senator--name'):
            senator_name = senator.find(class_='nys-senator--name').text.strip()
        else:
            senator_name = 'No info found.'  # If the element doesn't exist, default to no value found.

        # Extract the senator's page.
        senator_url = senate_template_url + senator.find('a')['href']

        # Go to the site and get the contents of the HTML.
        senate_contact_url = senator_url + '/contact'
        contact_text = requests.get(senate_contact_url, headers=user_agent).text

        senate_soup = BeautifulSoup(contact_text, 'lxml')

        # If we can find the class that contains 'nys-senator--name', then extract the senator's email address.
        if senate_soup.find('div', class_='c-block--senator-email'):
            senator_email = senate_soup.find('div', class_='c-block--senator-email').find('a').text
        else:
            senator_email = 'No info found.'  # If the element doesn't exist, default to no value found.

        # Extract the Office Address(es) and Phone Number(s).
        if senate_soup.find_all('div', class_='vcard'):
            contact_data = senate_soup.find_all('div', class_='vcard')
        else:
            contact_data = []

        # Initialize string to concat the addresses and phone numbers to.
        address_lst = ''
        for address in contact_data:
            temp_str = ''
            # Extract the Street Address.
            if (address.find(itemprop='streetAddress') and address.find(itemprop='addressLocality') and address.find(
                    itemprop='addressRegion') and address.find(itemprop='postalCode')):
                temp_str = temp_str + address.find(itemprop="streetAddress").text.strip() + "\n"
                # Extract the City, Region, and Postal Code.
                temp_str = temp_str + address.find(itemprop="addressLocality").text.strip() \
                           + ' ' + address.find(itemprop="addressRegion").text.strip() + ' ' + address.find(
                    itemprop="postalCode").text.strip() + '\n'
            # Extract the Telephone Number.
            if address.find(itemprop="telephone"):
                temp_str = temp_str + address.find(itemprop="telephone").text.strip() + '\n'
            # Extract the Fax Number.
            if address.find(itemprop="faxNumber"):
                temp_str = temp_str + address.find(itemprop="faxNumber").text.strip() + '\n'
            if temp_str:
                address_lst = address_lst + temp_str + '\n'

        # If the address_lst is still empty, there was no address(es) or phone number(s) found.
        if not address_lst:
            address_lst = 'No info found.'  # If the element doesn't exist, default to no value found.

        # Finished Extracting Data! Add values to the list in the specified format
        senate_data.append(district_num.strip())
        senate_data.append(senator_name.strip())
        senate_data.append(senator_url.strip())
        senate_data.append(district_party.strip())
        senate_data.append(senator_email.strip())
        senate_data.append(address_lst.strip())

        # Push the senate data into the extracted list
        extracted_data.append(senate_data)

    # Sort the extracted data by District Number
    extracted_data.sort(key=lambda x: get_district_num(x[0]))

    # Export the data to the spreadsheets
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
    headers = ["District No.", "Name", "Senator's URL", "Party", "Email", "Addresses & Phone Number(s)"]

    # Datetime objects to grab both the data and time the script was executed.
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")  # Date is saved in YYYY/MM/DD HHMM format.

    # Data filtered and extracted. Export the info into .csv file.
    with open('NYS Senate ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for senator in lst:
            writer.writerow(senator)  # Append the data we extracted from earlier to .csv file.

    # Data filtered, extracted, and now needs to be exported as .xlsx file.
    wb = xl.Workbook()  # Create an Excel workbook.
    ws = wb.active  # Create a sheet within the workbook.
    ws.title = "Senators"  # Name the worksheet: Senators.
    ws.append(headers)  # Add the column names to the sheet.

    # For each community board we extracted, write to the Excel sheet.
    for senator in lst:
        ws.append(senator)

    # Adjust column size by max length of cell length for readable convenience.
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length

    # Save the file.
    wb.save(filename='NYS Senate ' + datetime_obj + ".xlsx")

    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'NYS Senate ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'NYS Senate ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
