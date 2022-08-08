from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}


def main():
    json = requests.get('https://data.cityofnewyork.us/resource/ruf7-3wgc.json', headers=user_agent).json()

    extracted_data = []

    for community_board in json:
        # [Borough, Community Board Number, Community Board Website, Community Board Email, Community Board Chair,
        # Community Board District Manager, Community Board Address and Phone Number(s), Precinct No.(s,
        # Precinct(s) Phone Number(s)]
        board_data = []

        cb_borough = ''
        cb_num = ''
        cb_website = ''
        cb_email = ''
        cb_chair = ''
        cb_district_manager = ''
        cb_office_full_address = ''
        cb_precincts = ''
        cb_precinct_phone_num = ''

        if 'borough' in community_board:
            cb_borough = community_board['borough']
        else:
            cb_borough = 'No Address Found!'
        board_data.append(cb_borough.strip())

        if 'community_board' in community_board:
            cb_num = community_board['community_board']
        else:
            cb_num = 'No Community Board Number found!'
        board_data.append(cb_num.strip())

        if 'cb_website' in community_board and community_board['cb_website']['url']:
            cb_website = community_board['cb_website']['url']
        else:
            cb_website = "No website URL found!"
        board_data.append(cb_website.strip())

        if 'cb_office_email' in community_board:
            cb_email = community_board['cb_office_email']
        else:
            cb_email = "No Email found!"
        board_data.append(cb_email.strip())

        if 'cb_chair' in community_board:
            cb_chair = community_board['cb_chair']
        else:
            cb_chair = "No info found!"
        board_data.append(cb_chair.strip())

        if 'cb_district_manager' in community_board:
            cb_district_manager = community_board['cb_district_manager']
        else:
            cb_district_manager = "No info found!"
        board_data.append(cb_district_manager.strip())

        # String Builder
        if 'cb_office_address' in community_board:
            cb_office_full_address = cb_office_full_address + community_board['cb_office_address'] + "\n"
        else:
            cb_office_full_address = cb_office_full_address + "No addresses found!" + "\n"

        if 'cb_office_phone' in community_board:
            cb_office_full_address = cb_office_full_address + "Phone: " + community_board['cb_office_phone'] + "\n"
        else:
            cb_office_full_address = cb_office_full_address + "No phone number found!" + "\n"

        if 'cb_office_fax' in community_board:
            cb_office_full_address = cb_office_full_address + "Fax: " + community_board['cb_office_fax'] + "\n"
        else:
            cb_office_full_address = cb_office_full_address + "No fax number found!" + "\n"
        board_data.append(cb_office_full_address.strip())

        if 'cb_precinct_s' in community_board:
            cb_precincts = community_board['cb_precinct_s']
        else:
            cb_precincts = "No precincts found!"
        board_data.append(cb_precincts.strip())

        if 'cb_precinct_phone_s' in community_board:
            cb_precinct_phone_num = community_board['cb_precinct_phone_s']
        else:
            cb_precinct_phone_num = "No precinct phone number found!"
        board_data.append(cb_precinct_phone_num.strip())
        extracted_data.append(board_data)
    extracted_data.sort(key=lambda x: (x[0], get_cb_num(x[1])))
    export_data(extracted_data)


# Helper sort method to convert string into a number to sort extracted data numerically
def get_cb_num(txt):
    num = 0
    for char in txt:
        if 48 <= ord(char) <= 57:
            num = num * 10 + int(char)
    return num


# Helper file method to export the extracted data to .csv file and a .xlsx file.
def export_data(lst):
    headers = ['Borough', 'Community Board Number', 'Community Board Website', 'Community Board Email',
               'Community Board Chair', 'Community Board District Manager',
               'Community Board Address and Phone Number(s)', 'Precinct No.(s)', 'Precinct(s) Phone Number(s)']

    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")
    # Data filtered, extracted, and now need to be exported into .csv file.
    with open('NYC Community Board ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for cb in lst:
            writer.writerow(cb)
    # Data filtered, extracted, and now needs to be exported as .xlsx file
    wb = xl.Workbook()
    ws = wb.active
    ws.title = "Community Board"
    ws.append(headers)
    for cb in lst:
        ws.append(cb)
    # Adjust column size by max length of cell length for readable convenience
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length
    # Save the file:
    wb.save(filename='NYC Community Board ' + datetime_obj + ".xlsx")
    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'NYC Community Board ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'NYC Community Board ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
