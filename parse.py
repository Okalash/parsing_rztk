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


def get_prop(soup, url, correct_cat):
    """
    get the needs properties of stuff
    """

    # get html code of properties
    name_stuff_code = soup.find('div', class_='product__heading')
    code_stuff_code = soup.find('div', class_='product__rating').find('p', class_='product__code detail-code')
    seller_stuff_code = soup.find('div', class_='product-seller__info').find('strong', class_='ng-star-inserted')
    # not work normal, need the final category
    category_link = soup.find('ul', class_='breadcrumbs ng-star-inserted').\
        find('li', class_='breadcrumbs__item ng-star-inserted'). \
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
        'Ссылка на товар': url,
        'Продавец': seller_stuff,
        'Куратор': None,
        'Корректная категория': correct_cat
    }
    excel_writer(about_stuff_dict)


output_file = './res.xlsx'
input_file = './input_links.txt'
""""
In file input_links.txt need to push links format:
    link_stuff, correct_category_ulr
    
Each new transfer from new line
"""
with open(input_file, 'r') as file:
    for url_pair in file.readlines():
        url_line = url_pair.split(',')
        request_url_line = requests.get(url_line[0])
        soup = BeautifulSoup(request_url_line.text, 'lxml')
        get_prop(soup, url_line[0], url_line[1])
        print('Link is ready')

"""Manual input"""
# while True:
#     url = input('Put the url:\n')
#     if url == 'q':
#         break
#     else:
#         correct_cat = input('Correct category:\n')
#         r = requests.get(url)
#         soup = BeautifulSoup(r.text, 'lxml')
#         get_prop(soup, url, correct_cat)

# print(r.text)
