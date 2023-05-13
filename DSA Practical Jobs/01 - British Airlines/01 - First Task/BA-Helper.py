### Developed by Renato Cezar, this script convert IATA codes
### to the name of city where the airport is located, throug 
### web scrapping and data handling.
### The airport data is provided by "aiportcodes.aero" 
### Last modification: May 12th 2023

def iata_converter():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import re as re
    from string import ascii_uppercase as letters_upper

    base_url = "https://airportcodes.aero"
    parsed_content = []
    # Loop to scrap content from each page:
    for i in letters_upper:
        #print(f"Scraping page with IATA codes starting with {i}")
        # Create URL to collect links from page
        url = f"{base_url}/iata/{i}"
        # Collect HTML data from this page
        response = requests.get(url)
        # Pre Parse content
        content = response.content
        pre_parsed_content = BeautifulSoup(content, 'html.parser') 
        # Split the articles from Pre Parsed Content and store them in a list of lists
        for iata in pre_parsed_content.find_all("tr"):
            parsed_content.append(iata)
    #print("Total of returned registers: " + str(len(parsed_content)))

    # Section to transform the data mass in parsed_content in a handsome dataset 
    iata = ""
    icao = ""
    airport_name = ""
    airport_data = []
    for i in range(0, len(parsed_content)):
        # Gathering and organizing the data from the scrap
        try:
            # IATA code
            iata = parsed_content[i].find_all("td")[0].string
            # ICAO code (extra information)
            icao = parsed_content[i].find_all("td")[1].string
            # Airport name
            airport_name = parsed_content[i].find_all("td")[2].string

            # Storing the organized data as list in a set of lists
            airport_data.append([iata, icao, airport_name])
        except Exception:
            pass
    #print("Final quantity of treated registers: " + str(len(airport_data)))

    # Removing the string " Aiport", "Municipal", "National", "Domestic", 
    # "Regional" and etc in airport_name to to keep only the airport name
    for i in range(0, len(airport_data)):
        try:
            airport_data[i][2] = airport_data[i][2].replace(" Airport", "")
            airport_data[i][2] = airport_data[i][2].replace(" Executive", "")
            airport_data[i][2] = airport_data[i][2].replace("Aeroporto ", "")
            airport_data[i][2] = airport_data[i][2].replace(" Metropolitan", "")
            airport_data[i][2] = airport_data[i][2].replace(" Aerodrome", "")
            airport_data[i][2] = airport_data[i][2].replace(" Domestic", "")
            airport_data[i][2] = airport_data[i][2].replace(" Regional", "")
            airport_data[i][2] = airport_data[i][2].replace(" Municipal", "")
            airport_data[i][2] = airport_data[i][2].replace(" National", "")
            airport_data[i][2] = airport_data[i][2].replace(" International", "")
        except Exception:
            pass

    # Creating and populating the data frame with the set of lists to handle 
    # the aiport data in a tabular way
    dataframe_airport = pd.DataFrame(airport_data, columns=['IATA', "ICAO", "Airport_Name"])

    # Return the airport data as tabular formated data
    return dataframe_airport