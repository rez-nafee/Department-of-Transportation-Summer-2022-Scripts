import requests
import csv
import datetime as dt
import openpyxl as xl
import sys

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}
nyc_community_board = 'https://data.cityofnewyork.us/resource/ruf7-3wgc.json'


def main():
    # Test if we can access the site. If there are any errors being thrown, exit the program.
    try:
        request = requests.get(nyc_community_board, headers=user_agent)
    except:
        sys.exit('Invalid URL. Verify the NYC Community Board link!')

    # Retrieve the json file that contains the information regarding NYC's Community Boards.
    json = request.json()

    # Initialize am array that will hold arrays of extracted data for each community board.
    extracted_data = []

    # For each community board found in the JSON file:
    for community_board in json:

        # The JSON file contains the following keys that represent different contact info:
        cb_borough = ''  # Borough of Community Board.
        cb_num = ''  # Community Board #.
        cb_website = ''  # URL to Community Board's Website.
        cb_email = ''  # Email address of Community Board.
        cb_chair = ''  # Name of Community Board's Chair.
        cb_district_manager = ''  # Name of Community Board's District Manager.
        cb_office_full_address = ''  # Address of Community Board's Office.
        cb_precincts = ''  # Precinct(s) No. for Community Board.
        cb_precinct_phone_num = ''  # Precinct(s) Phone Number.

        # Initialize an empty array to store the extracted information.
        # Data will be stored in the following format:
        # [Borough, Community Board Number, Community Board Website, Community Board Email, Community Board Chair,
        # Community Board District Manager, Community Board Address and Phone Number(s), Precinct No.(s,
        # Precinct(s) Phone Number(s)]
        board_data = []

        # If the community board has a key of 'borough', extract the name of the borough.
        if 'borough' in community_board:
            cb_borough = community_board['borough']
        else:
            cb_borough = 'No Borough Found!'  # If they key doesn't exist, default to no value found.
        board_data.append(cb_borough.strip())  # Add the data to the extracted data for the board.

        # If the community board has a key of 'community_board', extract the number of the community board.
        if 'community_board' in community_board:
            cb_num = community_board['community_board']
        else:
            cb_num = 'No Community Board Number found!'  # If they key doesn't exist, default to no value found.
        board_data.append(cb_num.strip())  # Add the data to the extracted data for the board.

        # If the community board has a key of 'cb_website', extract the website of the community board.
        if 'cb_website' in community_board and community_board['cb_website']['url']:
            cb_website = community_board['cb_website']['url']  # Get the URL to the community board.
        else:
            cb_website = "No website URL found!"  # If they key doesn't exist, default to no value found.
        board_data.append(cb_website.strip())  # Add the data to the extracted data for the board.

        # If the community board has a key of 'cb_office_email', extract the email address of the community board.
        if 'cb_office_email' in community_board:
            cb_email = community_board['cb_office_email']
        else:
            cb_email = "No Email found!"  # If they key doesn't exist, default to no value found.
        board_data.append(cb_email.strip())  # Add the data to the extracted data for the board.

        # If the community board has a key of 'cb_chair', extract the chairperson's name.
        if 'cb_chair' in community_board:
            cb_chair = community_board['cb_chair']
        else:
            cb_chair = "No info found!"  # If they key doesn't exist, default to no value found.
        board_data.append(cb_chair.strip())  # Add the data to the extracted data for the board.

        # If the community board has a key of 'cb_district_manager', extract the district manager's name.
        if 'cb_district_manager' in community_board:
            cb_district_manager = community_board['cb_district_manager']  # Grab the district manager's name.
        else:
            cb_district_manager = "No info found!"  # If they key doesn't exist, default to no value found.
        board_data.append(cb_district_manager.strip())  # Add the data to the extracted data for the board.

        # String Builder for the Community Board's Address:
        # If the community board has a key of 'cb_office_address', extract the street address.
        if 'cb_office_address' in community_board:
            cb_office_full_address = cb_office_full_address + community_board['cb_office_address'] + "\n"
        else:
            # If they key doesn't exist, default to no value found.
            cb_office_full_address = cb_office_full_address + "No addresses found!" + "\n"

        # If the community board has a key of 'cb_office_phone', extract the office phone number.
        if 'cb_office_phone' in community_board:
            cb_office_full_address = cb_office_full_address + "Phone: " + community_board['cb_office_phone'] + "\n"
        else:
            # If they key doesn't exist, default to no value found.
            cb_office_full_address = cb_office_full_address + "No phone number found!" + "\n"

        # If the community board has a key of 'cb_office_fax', extract the office fax number.
        if 'cb_office_fax' in community_board:
            cb_office_full_address = cb_office_full_address + "Fax: " + community_board['cb_office_fax'] + "\n"
        else:
            # If they key doesn't exist, default to no value found.
            cb_office_full_address = cb_office_full_address + "No fax number found!" + "\n"

        # Add the data to the extracted data for the board.
        board_data.append(cb_office_full_address.strip())

        # If the community board has a key of 'cb_precinct_s', extract the precinct number(s).
        if 'cb_precinct_s' in community_board:
            cb_precincts = community_board['cb_precinct_s']
        else:
            # If they key doesn't exist, default to no value found.
            cb_precincts = "No precincts found!"
        board_data.append(cb_precincts.strip())  # Add the data to the extracted data for the board.

        # If the community board has a key of 'cb_precinct_phone_s', extract the phone number(s) for the precinct(s).
        if 'cb_precinct_phone_s' in community_board:
            cb_precinct_phone_num = community_board['cb_precinct_phone_s']
        else:
            # If they key doesn't exist, default to no value found.
            cb_precinct_phone_num = "No precinct phone number found!"
        board_data.append(cb_precinct_phone_num.strip())  # Add the data to the extracted data for the board.

        # Extraction of data complete! Add the extracted data of the board to the list of extracted data.
        extracted_data.append(board_data)

    # Sort the community boards by the borough name and their number.
    extracted_data.sort(key=lambda x: (x[0], get_cb_num(x[1])))

    # Export the data.
    export_data(extracted_data)


# Helper sort method to convert string into a number to sort extracted data numerically.
def get_cb_num(txt):
    num = 0  # The numerical value found in the string.
    # For each character in the string
    for char in txt:
        # If the ASCII value of the character is between 48 and 57, it's a digit.
        if 48 <= ord(char) <= 57:
            num = num * 10 + int(char)  # Parse the character as a number and multiply the number by 10 and add it.
    return num  # Return the numerical value.


# Helper method to export the extracted data to .csv file and a .xlsx file.
def export_data(lst):
    # Headers for the Excel file to describe the columns of the data.
    headers = ['Borough', 'Community Board Number', 'Community Board Website', 'Community Board Email',
               'Community Board Chair', 'Community Board District Manager',
               'Community Board Address and Phone Number(s)', 'Precinct No.(s)', 'Precinct(s) Phone Number(s)']

    # Datetime objects to grab both the data and time the script was executed.
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")  # Date is saved in YYYY/MM/DD HHMM format.

    # Data filtered and extracted. Export the info into .csv file.
    with open('NYC Community Board ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for cb in lst:
            writer.writerow(cb)  # Append the data we extracted from earlier to .csv file.

    # Data filtered, extracted, and now needs to be exported as .xlsx file.
    wb = xl.Workbook()  # Create an Excel workbook.
    ws = wb.active  # Create a sheet within the workbook.
    ws.title = "Community Boards"  # Name the worksheet: Community Boards.
    ws.append(headers)  # Add the column names to the sheet.

    # For each community board we extracted, write to the Excel sheet.
    for cb in lst:
        ws.append(cb)

    # Adjust column size by max length of cell length for readable convenience.
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length

    # Save the file.
    wb.save(filename='NYC Community Board ' + datetime_obj + ".xlsx")

    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'NYC Community Board ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'NYC Community Board ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
