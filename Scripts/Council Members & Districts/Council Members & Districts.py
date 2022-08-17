from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl
import sys

nyc_council_URL = 'https://council.nyc.gov/districts/'
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}


def main():
    # Test if we can access the site. If there are any errors being thrown, exit the program.
    try:
        request = requests.get(nyc_council_URL, headers=user_agent)
    except:
        sys.exit('Invalid URL. Verify the Council Members link!')

    # Go to the site and get the contents of the HTML.
    html_text = request.text
    soup = BeautifulSoup(html_text, 'lxml')

    # Grab the table that contains all Council members.
    district_table = soup.find('tbody', class_='list')

    # Grab the rows that contain the information regarding the Council ,embers.
    district_rows = district_table.find_all('tr')

    # Initialize am array that will hold arrays of extracted data for each Council member.
    extracted_data = []

    # For each district in our rows of district:
    for district in district_rows:

        # Initialize an empty array to store the extracted information.
        # Data will be formatted as the following:
        # [District No., District Website, District Office Info, Name, Borough, Party, Neighborhoods, Email]
        cm_data = []

        # Data we are looking to extract from the Website:
        district_num = ''           # District number
        district_url = ''           # District's Website
        district_office = ''        # District office address.
        cm_name = ''                # Community member's name.
        cm_borough = ''             # Community member's borough.
        cm_party = ''               # Community member's party.
        cm_neighborhoods = ''       # Community member's neighborhoods.
        cm_email = ''               # Community member's email address.

        # If we find a data cell with a class of 'sort-district', extract the district number.
        if district.find('td', class_='sort-district'):
            district_num = district.find('td', class_='sort-district').text.strip()
        else:
            district_num = 'No info found.'     # If the element doesn't exist, then default to no value found.

        # If we find a data cell with a class of 'sort-member', then extract the council member's name.
        if district.find('td', class_='sort-member'):
            cm_name = district.find('td', class_='sort-member').text.strip()

            # If we find a data cell with a class of 'sort-member' and hyperlink, then extract the district's website.
            if district.find('td', class_='sort-member').find('a')['href']:
                district_url = district.find('td', class_='sort-member').find('a')['href'].strip()
                # Get the HTML contents of the district's website.
                request = requests.get(district_url, headers=user_agent)
                if not request.ok:
                    district_office = 'No info found! ' # If the element doesn't exist, then default to no value found.
                html_text = request.text
                cm_soup = BeautifulSoup(html_text, 'lxml')

                # If we find a paragraph with a class of 'text-small', then extract the address(es) and phone number(s).
                if cm_soup.find('p', class_='text-small'):
                    district_office = cm_soup.find('p', class_='text-small').text
                else:
                    district_office = 'No info found!'  # If the element doesn't exist, then default to no value found.
            else:
                district_url = 'No info found.'         # If the element doesn't exist, then default to no value found.
        else:
            # If the element doesn't exist, default to no value found.
            cm_name = 'No info found.'
            district_url = 'No info found.'
            district_office = 'No info found.'

        # If we find a data cell with a class of 'sort-borough', then extract the borough(s) the member represents.
        if district.find('td', class_='sort-borough'):
            cm_borough = district.find('td', class_='sort-borough').text.strip()
        else:
            cm_borough = 'No info found'            # If the element doesn't exist, then default to no value found.

        # If we find a data cell with a class of 'sort-party', then extract the part affiliation of the member.
        if district.find('td', class_='sort-party'):
            cm_party = district.find('td', class_='sort-party').text.strip()
        else:
            cm_party = 'No info found.'             # If the element doesn't exist, then default to no value found.

        # If we find a data cell with a class of 'sort-neighborhoods', then extract the neighborhoods.
        if district.find('td', class_='sort-neighborhoods'):
            cm_neighborhoods = district.find('td', class_='sort-neighborhoods').text.strip()
        else:
            cm_neighborhoods = 'No info found.'     # If the element doesn't exist, then default to no value found.

        # If we find a data cell with a class of 'sort-email', then check if they have email address listed.
        if district.find('td', class_='sort-email'):
            # If we find a span element with a value of 'data-email', then extract the email address.
            if district.find('td', class_='sort-email').find('span')['data-email']:
                cm_email = district.find('td', class_='sort-email').find('span')['data-email'].strip()
            else:
                cm_email = 'No info found.'          # If the element doesn't exist, then default to no value found.

        # Add all the extracted data into the array.
        cm_data = cm_data + [district_num, district_url, district_office, cm_name, cm_borough, cm_party,
                             cm_neighborhoods, cm_email]

        # Append the info extracted for the representative to list of extracted data.
        extracted_data.append(cm_data)

    # We have finished extracting the data for the council member, export the data into a .csv file and .xlsx file.
    export_data(extracted_data)


# Helper method to export the extracted data to .csv file and a .xlsx file.
def export_data(extracted_data):
    # Headers for the Excel file to describe the columns of the data.
    headers = ['District No.', 'District Website', 'District Office Info', 'Name', 'Borough', 'Party', 'Neighborhoods',
               'Email']

    # Datetime objects to grab both the data and time the script was executed.
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")  # Date is saved in YYYY/MM/DD HHMM format.

    # Data filtered and extracted. Export the info into .csv file.
    with open('Council Members & Districts ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for cb in extracted_data:
            writer.writerow(cb)  # Append the data we extracted from earlier to .csv file.

    # Data filtered, extracted, and now needs to be exported as .xlsx file.
    wb = xl.Workbook()                      # Create an Excel workbook.
    ws = wb.active                          # Create a sheet within the workbook.
    ws.title = "Council Members Info"       # Name the worksheet: Senators.
    ws.append(headers)                      # Add the column names to the sheet.

    # For each council member we extracted, write to the Excel sheet.
    for cm in extracted_data:
        ws.append(cm)

    # Adjust column size by max length of cell length for readable convenience.
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length

    # Save the file.
    wb.save(filename='Council Members ' + datetime_obj + ".xlsx")

    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'Council Members ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'Council Members ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
