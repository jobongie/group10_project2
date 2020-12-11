# Project 2 Group 10


## Dashboard Overview

![1-Index.html](images/w1.jpg)

Our project utilizes data that breaks down employment by industry, business size, and revenue. It consists of the following visualizations:

1. **Interactive Bubble Graph**- Uses this data

2. **Color Map**- Uses this Data 

3. **/api/data**- Uses this Data 

4. **other**- Uses this Data 


## Other Pages

![2-Map.html](images/w2.jpg)

This page focuses on the BLANK graph, it's interactivity utilizes a slider that displays the information based on year, the filters BLANK BLANK BLANK that allows the user to search by Industry, Business Size, and State.

## SQL DataBase

![2-static\data\US_Enterprises-CreateTable.sql](images/w3.jpg)

We utilize a Flask Server which connects locally to this DataBase. The raw data is imported from **.csv** files and joined into the table **Data** to be transformed into the Visualizations you viewed above.


## Presentation

![2-Project_2_Group_10.pptx](images/w3.jpg)

It tells the story.

- - -

### Instructions

To begin:

1. **PGAdmin4**- Open the Browser of your choice and begin running this program, you must keep it open throughout the operation of the Dashboard. Open the file **static\data\US_Enterprises-CreateTable.sql**, and follow the instructions outlined within, you will need to import the following 3 files after creating their tables.

    a. **static\data\2017_NAICS_Structure_Summary.csv**

    b. **static\data\Consolidated State_NAISC Sector 2008-2017.csv**

    c. **static\data\state_codes.csv**

2. **app.py**- Within the main directory of **Group10_PROJECT2** you will find this file, {dbuser} & {dbpassword} will need to match your postgresql server user credentials (save the changes).

3. **Group10_PROJECT2**- Navigate to this top level directory within your bash terminal.

4. **python app.py**- Input this in the command line to begin operating the Flask Server.

5. **LocalHost:5000**- Type this into a new tab of the browser you opened previously to begin viewing the Dashboard.

6. **/api/data**- If you wish to view the data in JSON format append this code to the preceding browser url.

7. **Navigation**- Simply use the Navbar at the top of the landing page to view the linked html pages, and the interactive sliders and filters to for the Data Visualizations.


### Copyright

Credit
Team 10 and other things
