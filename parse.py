import requests
from bs4 import BeautifulSoup



def get_prop(soup, url):
    """
    get the needs properties of stuff
    """

    # result list
    about_suff = []

    # get html code of properties
    name_stuff_code = soup.find('div', class_='product__heading')
    code_stuff_code = soup.find('div', class_='product__rating').find('p', class_='product__code detail-code')
    seller_stuff_code = soup.find('div', class_='product-seller__info').find('strong', class_='ng-star-inserted')
    category_link = soup.find('ul', class_='breadcrumbs ng-star-inserted').find('li', class_='breadcrumbs__item ng-star-inserted').\
        find('a', class_='breadcrumbs__link').get('href')

    # result names
    name_stuff = name_stuff_code.text.strip()
    code_stuff = code_stuff_code.text[4:].strip()
    seller_stuff = seller_stuff_code.text.strip()
    print(f'Название: {name_stuff},\nКод товара: {code_stuff},\nПродавец товара: {seller_stuff}')
    print(category_link)


output_file = 'res.txt'
while True:
    url = input('Put the url:\n')
    if url == 'q':
        break
    else:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        get_prop(soup, url)

#print(r.text)

