# importing the libraries
from bs4 import BeautifulSoup #used for parsing the html code
import requests # used for implementing the http methods
import pandas as pd

# for storing the data
prod_list = []
sale_price_list = []
actual_price_list = []

for i in range(1,1000):
    # Website we are scraping in this project
    url = f'https://saamaan.pk/collections/accessories-and-gadgets?page={i}'

    # accessing the url html code
    content = requests.get(url)

    # checking the http method response
    print(content.status_code)

    # parsing the html code recieved
    soup = BeautifulSoup(content.content, 'html.parser')

    # printing all the text available in the url
    # print(soup.text)

    # filtering the html code to get only the required data
    divs = soup.find_all('div', class_ = 'product-item__info-inner')

    if len(divs)<=0:
        break
    
    for div in divs: 
        product_name = div.find('a', class_ = 'product-item__title text--strong link').text
        # print(product_name)
        prod_list.append(product_name)

        sale_price = div.find('span', class_ = 'price').text
        # cleaning sale_price
        sale_price = str(sale_price)
        sale_price = sale_price.replace('Regular priceRs.','').replace("Sale priceRs.", '').replace('Sale priceFrom Rs.', '').replace(' PKR', '').replace(',', '').strip()
        sale_price = float(sale_price)
        # print(sale_price)
        sale_price_list.append(sale_price)

        try:
            actual_price = div.find('span', class_ = 'price price--compare')
            actual_price = str(actual_price.text)
            actual_price = actual_price.replace('Regular priceRs.','').replace("Sale priceRs.", '').replace('Sale priceFrom Rs.', '').replace(' PKR', '').replace(',', '').strip()
            actual_price = float(actual_price)
            # print(actual_price)
        except AttributeError:
            actual_price = sale_price
            # print(actual_price)
        actual_price_list.append(actual_price)

# storing data into csv
data = {
    'product_names': prod_list,
    'sale_price': sale_price_list,
    'actual_price':actual_price_list
}
df = pd.DataFrame(data)
# saving data into csv
df.to_csv('product_data.csv', mode='w')

# saving data into json
df.to_json('product_data.json')

# saving data into excel
df.to_excel('product_data.xlsx')

    # for product_name in product_names:
    #     print(product_name.text)

    # cleaning the data
    # for reg_price in reg_prices:
    #     reg_price = str(reg_price.text)
    #     reg_price = reg_price.replace('Regular priceRs.','').replace("Sale priceRs.", '').replace('Sale priceFrom Rs.', '').replace(' PKR', '').replace(',', '').strip()
    #     reg_price = float(reg_price)
    #     print(reg_price)


        