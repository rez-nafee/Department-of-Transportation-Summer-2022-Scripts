from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl

state_assembly_url = "https://nyassembly.gov/mem/"
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}
def main():
    html_text = requests.get(state_assembly_url, headers=user_agent).text
    soup = BeautifulSoup(html_text, 'lxml')

    state_assembly_items = soup.find_all('section', class_='mem-item')
    extracted_data = []
    for member in state_assembly_items:
        data = []
        for tag in member.findChildren():
            try:
                if 'mem-info' in tag['class']:
                    name_n_district = tag.find('h3', class_='mem-name')
                    if name_n_district:
                        # Have District Number and Name
                        lst = list(filter(None, name_n_district.text.strip().strip().split('\t')))[::-1]
                        for item in lst:
                            data.append(item)
                    else:
                        # Don't have District Number and Name
                        data.append("No data found!")
                        data.append("No data found!")
                    email = tag.find('div', class_='mem-email')
                    if email:
                        # Has an email address
                        data.append(email.text)
                    else:
                        # Does not have email address
                        data.append("No data found!")
                if 'mem-address' in tag['class']:
                    children = tag.findChildren('div', recursive=False)
                    addresses = ""
                    for child in children:
                        addresses = addresses + child.text + "\n"
                    data.append(addresses.strip())
            except:
                continue
        extracted_data.append(data)
    extracted_data.sort(key=lambda x: get_district_num(x[0]))
    export_data(extracted_data)


def get_district_num(str):
    num = 0
    for char in str:
        if 48 <= ord(char) <= 57:
            num = num * 10 + int(char)
    return num


def export_data(lst):
    headers = ["District No.", "Name", "Email", "Addresses & Phone Number(s)"]
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")
    # Data filtered, extracted, and now need to be exported into .csv file.
    with open('State Assembly ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') \
            as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for district in lst:
            writer.writerow(district)
    # Data filtered, extracted, and now needs to be exported as .xlsx file
    wb = xl.Workbook()
    ws = wb.active
    ws.title = "State Assembly"
    ws.append(headers)
    for district in lst:
        ws.append(district)
    # Adjust column size by max length of cell length for readable convenience
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length
    # Save the file:
    wb.save(filename='State Assembly ' + datetime_obj + ".xlsx")
    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'State Assembly ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'State Assembly ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
