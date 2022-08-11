from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}
congressional_districts_url = 'https://www.house.gov/representatives'


def main():
    # Go to the site and get the contents of the HTML
    html_text = requests.get(congressional_districts_url, headers=user_agent).text
    soup = BeautifulSoup(html_text, 'lxml')

    reps_by_state = soup.find_all('table', class_='table')
    nys_rep_table = None

    for state in reps_by_state:
        if state.find("caption").text.strip() == 'New York':
            nys_rep_table = state

    nys_reps = nys_rep_table.find_all("tr")[1::]

    extracted_data = []

    for rep in nys_reps:

        rep_info = rep.find_all('td')
        rep_data = []

        # Data we are looking to extract from the Website
        district = ''
        rep_name = ''
        rep_link = ''
        rep_party = ''
        rep_office = ''
        rep_phone = ''
        rep_committee_assignment = 'No info found!'

        for info in rep_info:
            # views-field-value-2 --> District Number
            if 'views-field-value-2' in info['class']:
                district = info.text.strip()

            # views-field-value-4 --> Name and Link
            if 'views-field-value-4' in info['class']:
                # Extract the name
                name = info.text.strip().split(',')[::-1]
                rep_name = ' '.join(name).strip()
                # Extract the link
                rep_link = info.find('a')['href'].strip()

            # views-field-value-7 --> Party
            if 'views-field-value-7' in info['class']:
                rep_party = info.text.strip()

            # views-field-value-8 --> Rep Office
            if 'views-field-value-8' in info['class']:
                rep_office = info.text.strip()

            # views-field-value-10 --> Phone Number
            if 'views-field-value-10' in info['class']:
                rep_phone = info.text.strip()

            # views-field-markup --> Committee Assignment
            if 'views-field-markup' in info['class']:
                committees = info.text.strip().split("|")
                rep_committee_assignment = ', '.join(committees).strip()

        rep_data = rep_data + [district, rep_name, rep_party, rep_committee_assignment, rep_link, rep_office, rep_phone]
        for n in range(len(rep_data)):
            if not rep_data[n]:
                rep_data[n] = 'No info found.'
        extracted_data.append(rep_data)
    export_data(extracted_data)


# Helper file method to export the extracted data to .csv file and a .xlsx file.
def export_data(lst):
    # Headers for the Excel file to describe the columns of the data
    headers = ["District No.", "Name", "Party", "Committee Assignment", "URL", "Office Room #", "Phone Number"]
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")

    # Data filtered, extracted, and now need to be exported into .csv file.
    with open('Congressional Districts ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for district in lst:
            writer.writerow(district)

    # Data filtered, extracted, and now needs to be exported as .xlsx file
    wb = xl.Workbook()
    ws = wb.active
    ws.title = "Congressional Districts"
    ws.append(headers)
    for district in lst:
        ws.append(district)

    # Adjust column size by max length of cell length for readable convenience
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
