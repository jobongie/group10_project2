# Project 2 Group 10


## Dashboard Overview

![Dashboard_Index](images/Dashboard_Index.png)

Our project utilizes data that breaks down employment by industry, business size, and revenue. Notable transformations were conducted in the Analysis-Latest.ipynb to perform the ETL phase of the project. In addition to the libraries learned in class, we utilized a new Javascript grid layout library called Masonry to feature images that represents each member of the team. The project consists of the following visualizations:

1. **Group Bar Chart**- Uses the Flask routing @/linechart

2. **Scatterplot**- Uses the Flask routing @/scatterplot

![bubbles](images/bubbles.png)

3. **BubbleChart**- Uses the Flask routing @/bubble


![us_map_big_businesses](images/us_map_big_businesses.png)

4. **Large Business Map**- Uses the Flask routing @/map1


![us_map_small_businesses](images/us_map_small_businesses.png)

5. **Small Business Map**- Uses the Flask routing @/map2


![api_data](images/api_data.png)

6. **/api/data**- Shows the imported and jsonified Database Table_df



## POSTGRESQL DataBase

![ERD-US_Enterprises](images/ERD-US_Enterprises.png)

We utilize a Flask Server which connects locally to this DataBase. The raw data is imported from **.csv** files and joined into the table **Data** to be transformed into the Visualizations you viewed above.



## Presentation

![Pres](images/Pres.png)

Our story in a brief summary presentation.

- - -

### Instructions

To begin:

1. **PGAdmin4**- Open the Browser of your choice and begin running this program, you must keep it open throughout the operation of the Dashboard. Create a Database within your postgresql server named **Enterprises**, and open the query tool within this Database. Paste the code from the file **static\data\US_Enterprises-CreateTable.sql**, and follow the instructions outlined within, you will need to import the following 4 files after creating their tables.

    a. **static\data\2017_NAICS_Structure_Summary.csv**

    b. **static\data\Consolidated State_NAISC Sector 2008-2017. csv**

    c. **static\data\state_codes.csv**

    d. **static\data\data.csv**

2. **app.py**- Within the main directory of **Group10_PROJECT2** you will find this file, {dbuser} & {dbpassword} will need to match your postgresql server user credentials (save the changes).

3. **Group10_PROJECT2**- Navigate to this top level directory within your bash terminal.

4. **python app.py**- Input this in the command line to begin operating the Flask Server.

5. **LocalHost:5000**- Type this into a new tab of the browser you opened previously to begin viewing the Dashboard.

6. **/api/data**- If you wish to view the data in JSON format append this code to the preceding browser url.

7. **Navigation**- Simply use the Navbar at the top of the landing page to view the linked html pages, and the interactive sliders and filters to for the Data Visualizations.



### Copyright

Credit
Team 10, Google, and many other things.
