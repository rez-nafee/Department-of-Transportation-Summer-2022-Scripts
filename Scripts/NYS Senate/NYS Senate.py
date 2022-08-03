from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl

nys_senate_URL = 'https://www.nysenate.gov/senators-committees'
senate_template_url = 'https://www.nysenate.gov'
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.0.0 Safari/537.36'}


def main():
    html_text = requests.get(nys_senate_URL, headers=user_agent).text
    soup = BeautifulSoup(html_text, 'lxml')
    nys_senators = soup.find_all('div', class_='u-odd')
    nys_senators.extend(soup.find_all('div', class_='u-even'))

    extracted_data = []

    for senator in nys_senators:
        # District Number, Name of Senator, Senator URL ,Party Affiliation(s), Email Address, and Addresses and Phone
        # Number(s)

        # Array to hold the data that we are trying to extract
        senate_data = []

        # Extract the senator's district number, party, and name
        district_party = senator.find(class_='nys-senator--party').text.strip()
        senator.find(class_='nys-senator--party').decompose()
        district_num = senator.find(class_="nys-senator--district").text.strip()
        senator_name = senator.find(class_="nys-senator--name").text.strip()

        # Extract the senator's page
        senator_url = senate_template_url + senator.find('a')['href']

        # Soupify the senator's contact info
        senate_contact_url = senator_url + '/contact'
        contact_text = requests.get(senate_contact_url, headers=user_agent).text
        senate_soup = BeautifulSoup(contact_text, 'lxml')

        # Extract the email address of the senator
        senator_email = senate_soup.find("div", class_='c-block--senator-email').find('a').text

        # Extract the Office Address(es) and Phone Number(s)
        contact_data = senate_soup.find_all("div", class_="vcard")
        address_lst = ''
        for address in contact_data:
            str = ''
            # Extract the Street Address
            if (address.find(itemprop="streetAddress") and address.find(itemprop="addressLocality") and address.find(
                    itemprop="addressRegion") and address.find(
                itemprop="postalCode")):
                str = str + address.find(itemprop="streetAddress").text.strip() + "\n"
                # Extract the City, Region, and Postal Code
                str = str + address.find(itemprop="addressLocality").text.strip() \
                      + ' ' + address.find(itemprop="addressRegion").text.strip() + ' ' + address.find(
                    itemprop="postalCode").text.strip() + '\n'
            else:
                str = str + "No Address found!"
            if address.find(itemprop="telephone"):
                # Extract the Telephone Number
                str = str + address.find(itemprop="telephone").text.strip() + '\n'
            else:
                str = str + "No Telephone No. Found!" + '\n'
            # Extract the Fax Number
            if address.find(itemprop="faxNumber"):
                str = str + address.find(itemprop="faxNumber").text.strip() + '\n'
            else:
                str = str + "No Fax No. Found!" + '\n'

            address_lst = address_lst + str + '\n'
        # Finished Extracting Data! Add values to the list in the specified format
        senate_data.append(district_num)
        senate_data.append(senator_name)
        senate_data.append(senator_url)
        senate_data.append(district_party)
        senate_data.append(senator_email)
        senate_data.append(address_lst)

        # Push the senate data into the extracted list
        extracted_data.append(senate_data)

    # Sort the extracted data by District Number
    extracted_data.sort(key=lambda x: get_district_num(x[0]))

    # Export the data to the spreadsheets
    export_data(extracted_data)


# Helper sort method to convert string into a number to sort extracted data numerically
def get_district_num(txt):
    num = 0
    for char in txt:
        if 48 <= ord(char) <= 57:
            num = num * 10 + int(char)
    return num


# Helper file method to export the extracted data to .csv file and a .xlsx file.
def export_data(lst):
    headers = ["District No.", "Name", "Senator's URL", "Party", "Email", "Addresses & Phone Number(s)"]
    datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")
    # Data filtered, extracted, and now need to be exported into .csv file.
    with open('NYS Senate ' + datetime_obj + ".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for district in lst:
            writer.writerow(district)
    # Data filtered, extracted, and now needs to be exported as .xlsx file
    wb = xl.Workbook()
    ws = wb.active
    ws.title = "Senators"
    ws.append(headers)
    for district in lst:
        ws.append(district)
    # Adjust column size by max length of cell length for readable convenience
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length
    # Save the file:
    wb.save(filename='NYS Senate ' + datetime_obj + ".xlsx")
    # Let the user know that the data has been exported
    print("Program complete!")
    print("Data outputted to (as a .csv) :", 'NYS Senate ' + datetime_obj + ".csv")
    print("Data outputted to (as a .xlsx) :", 'NYS Senate ' + datetime_obj + ".xlsx")


if __name__ == "__main__":
    main()
