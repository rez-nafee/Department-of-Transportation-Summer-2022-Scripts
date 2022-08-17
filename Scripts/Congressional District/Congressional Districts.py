from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl
import sys

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}
congressional_districts_url = 'https://www.house.gov/representatives'


def main():
    # Test if we can access the site. If there are any errors being thrown, exit the program.
    try:
        request = requests.get(congressional_districts_url, headers=user_agent)
    except:
        sys.exit('Invalid URL. Verify the NYS Congressional link!')

    # Go to the site and get the HTML contents.
    html_text = request.text
    soup = BeautifulSoup(html_text, 'lxml')

    # Find all the state's representatives information that is stored in tables.
    reps_by_state = soup.find_all('table', class_='table')

    # Variable to store New York State's representative information.
    nys_rep_table = None

    # Iterate through all the tables by states and look for the table that has information on New York.
    for state in reps_by_state:
        if state.find("caption").text.strip() == 'New York':
            # Found the table! Set the variable to the table that has the information.
            nys_rep_table = state

    # Next find the rows within the NYS Table. Each row is a NYS House Representative.
    nys_reps = nys_rep_table.find_all("tr")[1::]

    # Initialize an array that will hold arrays of extracted data for each respective representative.
    extracted_data = []

    # For each representative in the table rows, extract the information.
    for rep in nys_reps:
        # Grab all the data cells in the row abot the representative.
        rep_info = rep.find_all('td')

        # Initialize an empty array to store the extracted information.
        # Data will be stored in the following format:
        # ["District No.", "Name", "Party", "Committee Assignment", "URL", "Office Room #", "Phone Number"]
        rep_data = []

        # Data we are looking to extract from the Website:
        district = ''  # Representative's District Number.
        rep_name = ''  # Representative's Name.
        rep_link = ''  # Representative's Website.
        rep_party = ''  # Representative's Party.
        rep_office = ''  # Representative's Office Number.
        rep_phone = ''  # Representative's Phone Number.
        rep_committee_assignment = ''  # Representative's Committee Assignments.

        # For each data cell in list of information, extract the data.
        for info in rep_info:
            # If the class name of data cell has 'views-field-value-2', extract the District Number.
            if 'views-field-value-2' in info['class']:
                district = info.text.strip()  # Grab the text and remove extra whitespaces.

            # If the class name of data cell has 'views-field-value-4', extract the Name and Link.
            if 'views-field-value-4' in info['class']:
                # The name is formatted with by Last Name, First Name.
                name = info.text.strip().split(',')[::-1]  # Split on the comma and reverse the list.
                rep_name = ' '.join(name).strip()  # Now the name is formatted as First Name and Last Name.

                # The link for the representative can be found in hyperlink.
                rep_link = info.find('a')['href'].strip()  # Get the href value for the link and strip the whitespace.

            # If the class name of data cell has 'views-field-value-7', extract the Party.
            if 'views-field-value-7' in info['class']:
                rep_party = info.text.strip()  # Get the party affiliation of the representative.

            # If the class name of data cell has 'views-field-value-8', extract the Rep Office.
            if 'views-field-value-8' in info['class']:
                rep_office = info.text.strip()  # Get the office number of the representative and strip the whitespace.

            # If the class name of date cell has views-field-value-10, extract the Phone Number.
            if 'views-field-value-10' in info['class']:
                rep_phone = info.text.strip()  # Get the phone number of the representative and strip the whitespace.

            # If the class name of the data cell has 'views-field-markup' --> Committee Assignment.
            if 'views-field-markup' in info['class']:
                committees = info.text.strip().split("|")
                rep_committee_assignment = ', '.join(committees).strip()

        # Add all the extracted data into the array.
        rep_data = rep_data + [district, rep_name, rep_party, rep_committee_assignment, rep_link, rep_office, rep_phone]

        # Go through the array and look for empty values. This means we were unable to find the info we are looking for.
        for n in range(len(rep_data)):
            # If the string is empty, set the string to display that no information was found.
            if not rep_data[n]:
                rep_data[n] = 'No info found.'

        # Append the info extracted for the representative to list of extracted data.
        extracted_data.append(rep_data)

    # We have finished extracting the data for the representatives, export the data into a .csv file and .xlsx file.
    export_data(extracted_data)


# Helper method to export the extracted data to .csv file and a .xlsx file.
def export_data(lst):
    # Headers for the Excel file to describe the columns of the data.
    headers = ["District No.", "Name", "Party", "Committee Assignment", "URL", "Office Room #", "Phone Number"]

    # Datetime objects to grab both the data and time the script was executed.
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")  # Date is saved in YYYY/MM/DD HHMM format.

    # Data filtered and extracted. Export the info into .csv file.
    with open('Congressional Districts ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for district in lst:
            writer.writerow(district)  # Append the data we extracted from earlier to .csv file.

    # Data filtered, extracted, and now needs to be exported as .xlsx file
    wb = xl.Workbook()  # Create an Excel workbook.
    ws = wb.active  # Create a sheet within the workbook.
    ws.title = "Congressional Districts"  # Name the worksheet: Congressional Districts.
    ws.append(headers)  # Add the column names to the sheet.

    # For each district we extracted, write to the Excel sheet.
    for district in lst:
        ws.append(district)

    # Adjust column size by max length of cell length for readable convenience.
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length

    # Save the file:
    wb.save(filename='Congressional Districts ' + datetime_obj + ".xlsx")

    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'Congressional Districts ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'Congressional Districts ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
