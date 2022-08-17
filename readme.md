# Web-Scraping Scripts
###### By: Rezvan Nafee | Last Edited: 08/17/2022
The NYC DOT’s Asset Management Unit is responsible for the creation, collection, and maintenance of data on its millions
of assets across the city. NYC DOT has requested the creation of a script to aid in the automation of said 
data maintenance. A crucial dataset that is needed and changing is the information regarding public officials on a 
city, state, and federal level. 

The main goal of the project is to create a script in Python to extra the relevant contact information of the 
following:
* New York City Community Boards
* New York State Congressional Districts 
* New York City Council Members 
* New York State Senate 
* New York State Assembly

When extracting information of the web, we hope to collect information such as names, the boroughs the representatives 
represent, their email, their phone number, etc.

In this document, you will learn about the thought process and ideas applied to the scripts. 

## Before Running the Script!
We need to set up the necessary libraries needed to run the scripts found in the repository. We will be using the 
following: 
* [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
This library will be used scrape information from web pages. 
* [lxml](https://pypi.org/project/lxml/)
This library will be used for easy handling of XML and HTML files,
* [Requests](https://pypi.org/project/requests/)
This library will be used to send HTTP requests. 
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
This library will be used to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.

Run the following commands on your command console to install the libraries:
```
pip install beautifulsoup4
pip install lxml
pip install requests
pip install openpyxl
```
If you're running into issues setting up the libraries, please visit the website linked above for more information.

## Some Helpful Resources
1. [HTML Elements](https://www.w3schools.com/TAgs/default.asp)
2. [Example of Web Scraping](https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/)
3. [Python Cheat Sheet](https://perso.limsi.fr/pointal/_media/python:cours:mementopython3-english.pdf)


## Community Board
There are 59 community boards throughout the City, and each one consists of up to 50 nonsalaried members.
Each community board is led by a District Manager who establishes an office, hires staff, and implements procedures 
to improve the delivery of City services to the district. The main responsibility of the board office is to 
receive complaints from community residents, processing permits for block parties and street fairs,organizing tenants 
associations, coordinating neighborhood cleanup programs,and more.

You can find a list of the community boards in New York City by clicking
[here](https://www1.nyc.gov/site/cau/community-boards/community-boards.page) (organized by boroughs). 

Initially, the script aimed to use the borough links of the community boards to extract information from. Let's take a 
look at the composition of the HTML elements for the community boards in the Bronx:
```html
<h2>Community Board 1</h2>
<h3>Neighborhoods</h3>
<p>Mott Haven, Port Morris, Melrose</p>
<h3>CB Info</h3>
<p><strong>Address:</strong><br />Bronx Community Board 1<br />3024 Third Avenue<br />Bronx, NY 10455<br /><strong>Phone:</strong> 718-585-7117<br /><strong>Fax:</strong> 718-292-0558<br /><strong>Email:</strong> brxcb1@optonline.net<br /><a href="http://www.nyc.gov/html/bxcb1/html/home/home.shtml">Visit the Bronx CB 1 website</a></p>
<p><strong>Chair: </strong>Arlene Parks<br /><strong>District Manager:</strong> Vacant<br /><strong>Board Meeting:</strong> Last Thursday, 6:00pm<br /><strong>Cabinet Meeting:</strong> Second Tuesday, 10:00am</p>
<h3>Precinct(s)</h3>
<p>40</p>
<h3>Precinct Phone(s)</h3>
<p>718-402-2270</p>
```
The front end of displaying the Community Board is a simple one for each board in the Bronx. It's composed of many text 
formatting elements such as headers and paragraphs. However, it's missing information such as the class attribute. 
Without the elements being assigned class attribute(s), it makes it difficult and inefficient to extract the HTML 
elements using BeautifulSoup4. As you will need to iterate through each header to find the board number, each paragraph 
to find the address of the office, etc.

Instead, the data can be extracted form [NYC OpenData](https://opendata.cityofnewyork.us/). The NYC OpenData provides 
public data published by New York City agencies and other partners. One of the public datasets available is the 
[Community Board Contact List](https://data.cityofnewyork.us/City-Government/Community-Board-Contact-List/dy27-rrad). 
By using the requests library installed earlier and the 
[JSON object](https://data.cityofnewyork.us/resource/dy27-rrad.json), we can efficiently extract information. 

To access the data found in the JSON object, we will be iterating through each dictionary of Community Boards and extracting 
th following keys: 
* borough *_(Borough of Community Board)_*
* community_board *_(Community Board #)_*
* cb_website *_(URL to Community Board's Website)_*
* cb_office_email *_(Email address of Community Board)_*
* cb_chair *_(Name of Community Board's Chair)_*
* cb_district_manager *_(Name of Community Board's District Manager)_*
* cb_office_address *_(Address of Community Board's Office.)_*
* cb_office_phone *_(Phone Number of Community Board's Office)_*
* cb_office_fax *_(Fax Number of Community Board's Office)_*
* cb_precinct_s *_(Precinct(s) No. for Community Board)_*
* cb_precinct_phone_s *_(Precinct(s) Phone Number)_*

This data is then extracted, verified that the key returns a value, and transformed for each community board. Then the 
data is sorted by their borough and their board number. After that, it gets exported and saved as .csv file and 
a .xlsx file.

For the implementation of requesting, extracting, and exporting the data, please read the respective script found in the
repository.

## Congressional Districts 
Congressional districts are the 435 areas from which members are elected to the U.S. House of Representatives. 
After the apportionment of congressional seats among the states, each state with multiple seats is responsible for 
establishing congressional districts for the purpose of electing representatives. 

While researching ways to collect the relevant contact information regarding New York State's Congressional Districts, 
I came across with the 
[2022 Congressional and State Legislative District Finder](https://www.elections.ny.gov/district-map.html). The site 
provide a map of the congressional districts. This data set is waiting to be updated due to the pending election. 

The United States House of Representatives has a [directory](https://www.house.gov/representatives) containing the 
information regarding each congressman or congresswoman for each state. Each state can be represented as a table in HTML. 
Let's take a closer look at a snipper of the representative table for New York:
```html
<table class="table" id="housegov_reps_by_state-block_default-296414404">
<caption id="state-new-york">
              New York
                </caption>
<thead>
<tr>
<th class="views-field views-field-value-2" id="view-value-2-table-column--35" scope="col">District</th>
<th class="views-field views-field-value-4" id="view-value-4-table-column--35" scope="col">Name</th>
<th class="views-field views-field-value-7" id="view-value-7-table-column--35" scope="col">Party</th>
<th class="views-field views-field-value-9" id="view-value-9-table-column--35" scope="col">Office Room</th>
<th class="views-field views-field-value-10" id="view-value-10-table-column--35" scope="col">Phone</th>
<th class="views-field views-field-markup" id="view-markup-table-column--35" scope="col">Committee Assignment</th>
</tr>
</thead>
<tbody>
<tr>
<td class="views-field views-field-value-2" headers="view-value-2-table-column--35">1st        </td>
<td class="views-field views-field-value-4 views-field-value-5" headers="view-value-4-table-column--35"><a href="https://zeldin.house.gov/">Zeldin, Lee</a> </td>
<td class="views-field views-field-value-7" headers="view-value-7-table-column--35">R        </td>
<td class="views-field views-field-value-8 views-field-value-9" headers="view-value-9-table-column--35">2441 RHOB        </td>
<td class="views-field views-field-value-10" headers="view-value-10-table-column--35">(202) 225-3826        </td>
<td class="views-field views-field-markup" headers="view-markup-table-column--35">Financial Services|Foreign Affairs        </td>
</tr>
<tr>
<td class="views-field views-field-value-2" headers="view-value-2-table-column--35">2nd        </td>
<td class="views-field views-field-value-4 views-field-value-5" headers="view-value-4-table-column--35"><a href="https://garbarino.house.gov">Garbarino, Andrew R.</a> </td>
<td class="views-field views-field-value-7" headers="view-value-7-table-column--35">R        </td>
<td class="views-field views-field-value-8 views-field-value-9" headers="view-value-9-table-column--35">1516 LHOB        </td>
<td class="views-field views-field-value-10" headers="view-value-10-table-column--35">(202) 225-7896        </td>
<td class="views-field views-field-markup" headers="view-markup-table-column--35">Homeland Security|Small Business        </td>
</tr>
</tbody>
</table>
```
From this we learn that the New York table has two attribute of class and id. Theoretically, we could use BeautifulSoup
to find a table element and an id of "housegov_reps_by_state-block_default-296414404":
```python
soup.find_all('table', id='housegov_reps_by_state-block_default-296414404')
````
However, this would not work as the reloading of the request to access the site would cause the id of the New York table
to change. Instead, the solution is to look for the caption element that is attached to each table. For example, the 
caption element found within the New York table is:
```html
<caption id="state-new-york">New York</caption>
```
And using BeautifulSoup to find all table elements with a class name of table and checking the caption element of 
each table with the id value of "state-new-york", we can find the New York Representatives table. 

Now that we have our table, we can work on extracting the data we can collect from this site. Each row of the table 
holds the following data cells: 

* District Number
* Representative's Name 
* Representative's Website
* Representative's Party 
* Representative's Office 
* Representative's Phone Number
* Representative's Committee Assignment 

Each data cell corresponds to a class attribute found in the data cell. Refer to respective script for more information.

This data is then extracted, verified that a value is assigned, and transformed for each representative. After that, 
it gets exported and saved as .csv file and a .xlsx file.

For the implementation of requesting, extracting, and exporting the data, please read the respective script found in the
repository.

## Council Members

The New York City Council consists of 51 Council districts throughout the five boroughs are each represented by an 
elected Council Member. The New York City Council Introduce and vote on legislation having to do with all aspects of 
NYC life, negotiate the NYC’s budget with the Mayor, monitor NYC agencies such as the Department of Education and the 
NYPD to make sure they’re effectively serving New Yorkers, and more. 

The New York City Council has a [list](https://council.nyc.gov/districts/) of the council members and their districts.
Once on the website, you will find a table containing the data we would like to extract. Let's take a look at a snippet 
of the table: 
```html
<tbody class="list">
<tr>
<td class="sort-district"><a class="button small expanded" href="https://council.nyc.gov/district-1/"><strong>1</strong></a></td>
<td class="sort-member"><a data-member-name="Christopher Marte" href="https://council.nyc.gov/district-1/"><strong>Christopher Marte</strong></a></td>
<td style="text-align: right;"><a href="https://council.nyc.gov/district-1/"><img alt="Christopher Marte Head Shot" class="inline-icon large" src="https://raw.githubusercontent.com/NewYorkCityCouncil/districts/master/thumbnails/district-1.jpg"/></a></td>
<td class="sort-borough">Manhattan</td>
<td class="sort-party show-for-medium">Democrat</td>
<td class="sort-neighborhoods neighborhoods show-for-medium">Battery Park City, Civic Center, Chinatown, Financial District, Little Italy, the Lower East Side, NoHo, SoHo, South Street Seaport, South Village, TriBeCa &amp; Washington Square</td>
<td class="sort-email email" style="text-align:center;"><a aria-label="Send an email to Council Member Christopher Marte" href="mailto:District1@council.nyc.gov"><i aria-hidden="true" class="fa fa-share"></i><i aria-hidden="true" class="fa fa-envelope-o"></i></a><br/><span aria-label="Click to copy Council Member Christopher Marte's email address" data-email="District1@council.nyc.gov" onclick="copyToClipboard(jQuery(this))" style="cursor:pointer;">Copy</span></td>
</tr>
<tr>
<td class="sort-district"><a class="button small expanded" href="https://council.nyc.gov/district-2/"><strong>2</strong></a></td>
<td class="sort-member"><a data-member-name="Carlina Rivera" href="https://council.nyc.gov/district-2/"><strong>Carlina Rivera</strong></a></td>
<td style="text-align: right;"><a href="https://council.nyc.gov/district-2/"><img alt="Carlina Rivera Head Shot" class="inline-icon large" src="https://raw.githubusercontent.com/NewYorkCityCouncil/districts/master/thumbnails/district-2.jpg"/></a></td>
<td class="sort-borough">Manhattan</td>
<td class="sort-party show-for-medium">Democrat</td>
<td class="sort-neighborhoods neighborhoods show-for-medium">East Village, Gramercy Park, Kips Bay, Lower East Side, Murray Hill, Rose Hill</td>
<td class="sort-email email" style="text-align:center;"><a aria-label="Send an email to Council Member Carlina Rivera" href="mailto:District2@council.nyc.gov"><i aria-hidden="true" class="fa fa-share"></i><i aria-hidden="true" class="fa fa-envelope-o"></i></a><br/><span aria-label="Click to copy Council Member Carlina Rivera's email address" data-email="District2@council.nyc.gov" onclick="copyToClipboard(jQuery(this))" style="cursor:pointer;">Copy</span></td>
</tr>
<tr>
</tbody>
```
Each row on the table represents one of the 51 council districts we have. We can use BeautifulSoup4 to find all table
row elements to start extracting the information found in each data cell. 

Each row of the table holds the following data cells: 
* District Number
* Council Member's Name
* Council Member's Website 
  * Concil Member's Office Address and Phone Numbers
* Council Member's Borough
* Council Member's Party
* Council Member's Neighborhoods
* Council Member's Email 

Each data cell corresponds to a class attribute found in the data cell. Refer to respective script for more information.

This data is then extracted, verified that a value is assigned, and transformed for each representative. 
After that, it gets exported and saved as .csv file and a .xlsx file.

For the implementation of requesting, extracting, and exporting the data, please read the respective script found 
in the repository.

## NYS Senate

The New York State Senate is the upper chamber of the New York State Legislature. 
The NYS Senate forms the legislative branch of the New York state government and works alongside the governor of 
New York to create laws and establish a state budget. The responsibilities of the NYS Senate 
include passing bills on public policy matters, setting levels for state spending, raising and lowering taxes, 
and voting to uphold or override vetoes.

A [list](https://www.nysenate.gov/senators-committees) of senators can be found on The New York State Senate website.
Once on the site, you will find different blocks that represent the Senate's 63 members from across New York State. Let's
take a look at some blocks found on the website: 

```html
<div class="u-odd">
<a href="/senators/jamaal-t-bailey">
<div class="c-senator-block">
<div class="nys-senator--thumb">
<img alt="" height="160" src="https://www.nysenate.gov/sites/default/files/styles/160x160/public/bailey-hs-020_2.jpg?itok=LKcRq5kH" width="160"/> </div>
<div class="nys-senator--info">
<h4 class="nys-senator--name">Jamaal T. Bailey</h4>
<span class="nys-senator--district">
<span class="nys-senator--party">
				(D)				</span>
									36th District							</span>
</div>
</div>
</a>
</div>

<div class="u-even">
<a href="/senators/kevin-s-parker">
<div class="c-senator-block">
<div class="nys-senator--thumb">
<img alt="" height="160" src="https://www.nysenate.gov/sites/default/files/styles/160x160/public/2019kphs.jpg?itok=savOnro2" width="160"/> </div>
<div class="nys-senator--info">
<h4 class="nys-senator--name">Kevin S. Parker</h4>
<span class="nys-senator--district">
<span class="nys-senator--party">
				(D, WF)				</span>
									21st District							</span>
</div>
</div>
</a>
</div>
```
From this, we learn that each senator is divided into either div element with a class name of "u-even" or "u-odd". By
using BeautifulSoup we can collect both div elements and start extracting information as each div contains the same 
data.

Within the div element, we can collect the following information: 
* District Number
* Senator's Name 
* Senator's Website
  * Senator's Email Address
  * Senator's Address and Phone Number(s)
* Senator's Party

Each text formatting element within the div corresponds to the information outlined above. Refer to respective script for 
more information on the extraction process.

This data is then extracted, verified that a value is assigned, and transformed for each representative. 
After that, it gets exported and saved as .csv file and a .xlsx file.

For the implementation of requesting, extracting, and exporting the data, please read the respective script found 
in the repository.

## State Assembly
The New York State Assembly is the lower chamber of the New York State Legislature. The NYS Assembly is a legislative 
branch of the New York state government and works alongside the governor of New York to create laws and establish a 
state budget. The responsibilities of the New York State Assembly include passing bills on public policy matters, 
setting levels for state spending, raising and lowering taxes, and voting to uphold or override vetoes.

A [list](https://nyassembly.gov/mem/) of State Assembly members can be found on the New York State Assembly website. On 
this website, we will find section elements that contain text formatter elements that hold the information regarding the
State Assembly. Let's take a deeper lock at one of the section elements: 

```html
<section class="mem-item" id="049">
<div class="mem-pic">
<a href="Peter-J-Abbate-Jr" rel="noopener"><img alt=" Peter J. Abbate, Jr." src="/write/upload/member_files/049/headshot/049.jpg" width="100"/></a>
</div>
<div class="mem-info">
<h3 class="mem-name"><a href="/mem/Peter-J-Abbate-Jr" rel="noopener">
						 Peter J. Abbate, Jr.													<span>District 49</span>
</a></h3>
<div class="mem-email"><a href="mailto:abbatep@nyassembly.gov">abbatep@nyassembly.gov</a></div>
</div> <!-- /.mem-info -->
<div class="mem-address">
<div class="full-addr notranslate">6605 Fort Hamilton Parkway <br/> Brooklyn, NY 11219 <br/> 718-236-1764 <br/> Fax: 718-234-0986</div><div class="full-addr notranslate">LOB 839 <br/> Albany, NY 12248 <br/> 518-455-3053</div> </div> <!-- /.mem-address -->
</section>
```
From this element, we can use BeautifulSoup4 to find specified HTML elements and class names to extract the 
text that contains contact information. For example, we can use the following to extract the state assembly member's
name: 
```python
member.find('h3', class_='mem-name')
```
Within the section element, we can collect the following information:
* District Number
* State Assembly Member's Name 
* State Assembly Member's Email
* State Assembly Member's Office Address and Phone Numbers

This data is then extracted, verified that a value is assigned, and transformed for each member. 
After that, it gets exported and saved as .csv file and a .xlsx file.

For the implementation of requesting, extracting, and exporting the data, please read the respective script found 
in the repository.
