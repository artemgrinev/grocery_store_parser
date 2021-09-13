from response import response
import csv
from product import Product

class ProductRating(Product):
    
    def get_links():
        response.url = 'https://roscontrol.com/category/produkti/'
        soup = response.get_soup()
        catalog = soup.find('div', class_ = 'testlab-category').find_all('div', class_ = 'grid-padding')
        product_url_list = []
        for i in catalog:
            url = i.find('a', class_ = 'catalog__category-item util-hover-shadow').attrs['href']
            response.url = 'https://roscontrol.com' + url
            soup = response.get_soup()
            all_subcategory = soup.find_all('a', class_ = 'catalog__category-item util-hover-shadow')
            for i in all_subcategory:
                subcategory_url = i['href']
                response.url = 'https://roscontrol.com' + subcategory_url
                soup = response.get_soup()
                try:
                    page = len(soup.find('div', class_='page-pagination').find_all('a')) - 1
                except:
                    page = 1
                for i in range(page):
                    response.url = 'https://roscontrol.com' + subcategory_url + f'?page={page}'
                    all_products = soup.select('body > div.layout.testlab > div.layout-canvas > div.util-wrapper.util-box-shadow-default.clear > section > div > div.main-container__cont.group > div.grid-row > div.grid-padding.grid-column-9.grid-column-large-8.grid-column-middle-12.grid-column-small-12.grid-left > div > div.wrap-testlab-view.wrap-container-view.testlab-view-typecolumn > div')
                    urls = all_products[0].find_all('div', class_ ='wrap-product-catalog__item')
                    for i in urls:
                        product_url_list.append(i.find('a')['href'])
                        print(i.find('a')['href'])
                    page-=1
        return product_url_list
    

    def get_product(self):
        links = self.get_links()
        for link in links:
            product = Product()
            response.url = 'https://roscontrol.com' + link
            soup = response.get_soup()
            product.product_url = 'https://roscontrol.com' + link
            product.category_url = soup.find('ol').find_all('li')[1].find('a').attrs['href']
            product.category_name = soup.find('ol').find_all('li')[1].find('a').text
            product.subcategory_url = soup.find('ol').find_all('li')[2].find('a').attrs['href']
            product.subcategory_name = soup.find('ol').find_all('li')[2].find('a').text
            product.product_name = soup.find('h1', class_="main-title testlab-caption-products util-inline-block").text
            product.rating = soup.find('div', class_ = 'total green').text
            try:
                product.positive_reviews = soup.find('span', class_ = 'row-plus').text
                product.negativ_reviews = soup.find('span', class_ = 'row-minus').text
            except:
                pass
            product.vender_name = soup.find('a', class_ ="company__item-title company__item-title--desktop js-has_vivid_rows").text
            yield product.__dict__


    def writer_csv(self):
        with open('okey.csv', mode='w', encoding='utf-8') as csv_file:
            fieldnames = ['market_name', 'domain', 'product_id', 'product_name', 'price',
                          'is_available', 'measure', 'product_url', 'vender_name',
                          'category_name','subcategory_name', 'category_url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            products = self.get_product()
            writer.writeheader()
            for i in products:
                writer.writerow(i.__dict__)