from bs4 import BeautifulSoup
import requests
import csv
import datetime as dt
import openpyxl as xl

nyc_council_URL = "https://council.nyc.gov/districts/"
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/103.0.0.0 Safari/537.36'}

html_text = requests.get(nyc_council_URL, headers = user_agent).text
soup = BeautifulSoup (html_text, 'lxml')

district_table = soup.find('tbody', class_ = 'list')
district_rows = district_table.find_all('tr')

extracted_data = []

for district in district_rows:
    lst = []
    for data in district.findAll('td'):
        classLst = []
        try:
            classLst = data['class']
            # Found Elements that have the class Names
            if 'sort-district' in classLst:
                lst.append(data.text.strip())
                lst.append(data.find('a')['href'].strip())
                html_text = requests.get(data.find('a')['href'].strip(), headers= user_agent).text
                soup = BeautifulSoup(html_text, 'lxml')
                office_info = soup.find('p', class_ = 'text-small').text
                lst.append(office_info)
            if ('sort-member' in classLst) or ('sort-borough' in classLst) or ('sort-party' in classLst) or \
                    'neighborhoods' in classLst or 'neighborhoods' in classLst:
                lst.append(data.text.strip())
            if 'email' in classLst:
                lst.append(data.find('span')['data-email'].strip())
        except:
            continue
    #Printing data extracted from the site
    #[District, District Website, District Member Name, Borough , Party, Neighborhoods, Email]
    extracted_data.append(lst)


#Data filtered, extracted, and now need to be exported into .csv file.
headers = ['District No.', "District Website", "District Office Info", "Name", "Borough", "Party" ,"Neighborhoods",
          "Email"]
datetime_obj = dt.datetime.now().strftime("%Y-%m-%d %H%M")
with open (('Council Members & Districts ' + datetime_obj + ".csv"), 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for districtData in extracted_data:
        writer.writerow(districtData)

#Data filtered, extracted, and now needs to be exported as .xlsx file
wb = xl.Workbook()
ws = wb.active
ws.title = "Council Members Info"
ws.append(headers)
for districtData in extracted_data:
    ws.append(districtData)
for column_cells in ws.columns:
    length = max(len(str(cell.value)) for cell in column_cells)
    ws.column_dimensions[column_cells[0].column_letter].width = length
wb.save(filename = 'Council Members & Districts ' + datetime_obj + ".xlsx")

#Let the user know that program has been completed.
print("Program complete!")
print("Data outputted to (as a .csv) :",'Council Members & Districts ' + datetime_obj + ".csv")
print("Data outputted to (as a .xlsx) :",'Council Members & Districts ' + datetime_obj + ".xlsx")