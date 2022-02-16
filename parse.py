import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path
from openpyxl import load_workbook

def excel_writer(stuff_dict):
    # dataframe init
    df = pd.DataFrame(stuff_dict, index=[0])
    if not os.path.exists(output_file):
        # if file not found - create
        df.to_excel(output_file, index=False)
    else:
        # reuse file and add new line of data
        with pd.ExcelWriter(output_file, if_sheet_exists='overlay', mode='a', engine="openpyxl") as writer:
            df.to_excel(writer, index=False, startrow=writer.sheets['Sheet1'].max_row, header=False)


def get_prop(soup, url):
    """
    get the needs properties of stuff
    """

    # get html code of properties
    name_stuff_code = soup.find('div', class_='product__heading')
    code_stuff_code = soup.find('div', class_='product__rating').find('p', class_='product__code detail-code')
    seller_stuff_code = soup.find('div', class_='product-seller__info').find('strong', class_='ng-star-inserted')
    # not work normal, need the final category
    category_link = soup.find('ul', class_='breadcrumbs ng-star-inserted').find('li', class_='breadcrumbs__item ng-star-inserted').\
        find('a', class_='breadcrumbs__link').get('href')

    # result names
    name_stuff = name_stuff_code.text.strip()
    code_stuff = code_stuff_code.text[4:].strip()
    seller_stuff = seller_stuff_code.text.strip()

    # result dict
    about_stuff_dict = {
        'Код товара': code_stuff,
        'Название товара': name_stuff,
        'Ссылка на категорию': category_link,
        'Ссылка на товар' : url,
        'Продавец': seller_stuff
    }
    excel_writer(about_stuff_dict)


output_file = './res.xlsx'
while True:
    url = input('Put the url:\n')
    if url == 'q':
        break
    else:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        get_prop(soup, url)

# print(r.text)
