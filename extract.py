import requests
import re
import pandas as pd
from itertools import chain
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine

def extract_data(city, state):
    headers = requests.utils.default_headers()
    headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    URL = f"https://www.realtor.com/realestateandhomes-search/{city}_{state}"
    page = requests.get(URL, headers=headers, verify=False)
    soup = BeautifulSoup(page.content, "lxml")

    def get_city(list):
        extract_city = []
        for city in list:
            start = city.find('d"') + 3
            end = city.find("<!")
            test = city[start:end]
            extract_city.append(test)
        return (extract_city)

    def set_City():

        city = list()
        zip = list()

        for item in soup.select('.component_property-card'):
            for i in item.select('[data-label=pc-address]'):
                city.append(i.find_all("div"))

        extract_city = [(lambda x: str(x))(x) for x in city]
        return (extract_city)

    def get_address():
        address_list = []
        for item in soup.select('.component_property-card'):
            for i in item:
                value = str(i)
                start = value.find("pc-address")
                value = (str(i)[start:])

                start = value.find(">") + 1
                end = value.find("<")
                address_list.append(value[start:end])

        address_list = [i for i in address_list if i]
        return (address_list)

    def get_price():
        price_list = []

        for item in soup.select('.component_property-card'):
            for i in item.select('[data-label=pc-price]'):
                start = str(i).find("$")
                end = str(i).find("<") - 7
                price_list.append(str(i)[start:end])
        return (price_list)

    def get_bed():

        bed_list = []
        for item in soup.select('.component_property-card'):
            for i in item.select('[data-label=pc-meta-beds]'):
                test = re.findall(r">\d<", str(i))
                bed_list.append(test)

        val_list = []
        for i in bed_list:
            val_list.append(re.findall(r"\d", str(i)))

        return (list(chain.from_iterable(val_list)))

    def get_footage():
        foot_list = []

        for item in soup.select('.component_property-card'):
            for i in item.select('[data-label=pc-meta-sqft]'):
                start = str(i).find("meta-value")
                end = str(i).find("</")
                footage = str(i)[start: end]

                start = footage.find(">") + 1
                foot_list.append(footage[start:])
        return (foot_list)

    def get_bath():
        bath_list = []
        for item in soup.select('.component_property-card'):
            for i in item.select('[data-label=pc-meta-baths]'):
                start = str(i).find('data-label="meta-value">')
                value = str(i)[start:]

                start = value.find(">")
                value = value[start:]

                value = re.findall(r">\d<", value)
                bath_list.append(value)

        bath_list = list(chain.from_iterable(bath_list))
        val_list = []

        for i in bath_list:
            val_list.append(re.findall(r"\d", i))
        val_list = list(chain.from_iterable(val_list))
        return (val_list)

    def get_zip():
        city = list()
        zip = list()

        for item in soup.select('.component_property-card'):
            for i in item.select('[data-label=pc-address]'):
                city.append(i.find_all("div"))

        extract_city = [(lambda x: str(x))(x) for x in city]

        zip_list = []
        value = [(lambda x: re.findall(r">\d{1,5}", str(x)))(x) for x in extract_city]
        for i in value:
            zip_list.append(re.findall("\d{1,5}", str(i)))

        val_list = []
        zip_list = list(chain.from_iterable(zip_list))

        for i in zip_list:
            val_list.append(i)

        return (val_list)

    df = pd.DataFrame(zip(get_price(), get_address(), get_city(set_City()), get_zip(), get_bath(), get_bed()),
                 columns=['Price', 'Address', 'City', 'Zip_Code', 'Number of Bath', 'Number of Beds'])

    #df.to_csv("~/Downloads/extract_df.csv", index=False)

    def create_connection():
        """ create a database connection to a database that resides
            in the memory
        """
        conn = None;
        try:
            conn = sqlite3.connect('Housing.db')
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


    create_connection()

    engine = create_engine('sqlite:///Housing.db', echo=True)

    df.to_sql('mytable', con=engine, if_exists='append')

