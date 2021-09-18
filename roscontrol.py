from response import response
import csv
from product import Product

class ProductRating(Product):
    def __init__(self):
        self.market_name = 'roscontrol'
        self.domain = 'https://roscontrol.com'
    
    def get_links(self):
        # собирает ссылки на продукты
        response.url = 'https://roscontrol.com/category/produkti/'
        soup = response.get_soup()
        catalog = soup.find('div', class_ = 'testlab-category').find_all('div', class_ = 'grid-padding')
        product_url_list = []
        for i in catalog:
            # сбор ссылок подкатегорий продуктов 'молоко, сыры, кифиры'
            url = i.find('a', class_ = 'catalog__category-item util-hover-shadow').attrs['href']
            response.url = 'https://roscontrol.com' + url
            soup = response.get_soup()
            all_subcategory = soup.find_all('a', class_ = 'catalog__category-item util-hover-shadow')
            for i in all_subcategory:
                # обработка пагинации
                subcategory_url = i['href']
                response.url = 'https://roscontrol.com' + subcategory_url
                soup = response.get_soup()
                try:
                    page = len(soup.find('div', class_='page-pagination').find_all('a')) - 1
                except:
                    page = 1
                for i in range(page):
                    # сбор ссылок на продукты
                    response.url = 'https://roscontrol.com' + subcategory_url + f'?page={page}'
                    all_products = soup.select('body > div.layout.testlab > div.layout-canvas > div.util-wrapper.util-box-shadow-default.clear > section > div > div.main-container__cont.group > div.grid-row > div.grid-padding.grid-column-9.grid-column-large-8.grid-column-middle-12.grid-column-small-12.grid-left > div > div.wrap-testlab-view.wrap-container-view.testlab-view-typecolumn > div')
                    urls = all_products[0].find_all('div', class_ ='wrap-product-catalog__item')
                    for i in urls:
                        product_url = i.find('a')['href']
                        print(i.find('a')['href'])
                        yield product_url
                    page-=1
    

    def get_product(self):
        # проходит по ссылкам и собирает информацию по товарам
        links = self.get_links()
        prod_id = 1
        for link in links:
            response.url = 'https://roscontrol.com' + link
            soup = response.get_soup()
            self.product_id = prod_id
            self.product_url = 'https://roscontrol.com' + link
            self.category_url = soup.find('ol').find_all('li')[1].find('a').attrs['href']
            self.category_name = soup.find('ol').find_all('li')[1].find('a').text
            self.subcategory_name = soup.find('ol').find_all('li')[2].find('a').text
            self.product_name = soup.find('h1', class_="main-title testlab-caption-products util-inline-block").text
            self.roscontrol_rating = soup.find('div', class_ = 'total green').text
            try:
                self.positive_reviews = soup.find('span', class_ = 'row-plus').text
                self.negativ_reviews = soup.find('span', class_ = 'row-minus').text
            except:
                pass
            self.vender_name = soup.find('a', class_ ="company__item-title company__item-title--desktop js-has_vivid_rows").text
            prod_id += 1
            yield self



    def writer_csv(self):
        file_name = self.market_name + '.csv'
        print(file_name)
        with open(file_name, mode='w', encoding='utf-8') as csv_file:
            fieldnames = ['product_id', 'market_name', 'domain', 'product_name', 'vender_name', 'roscontrol_rating',
                          'positive_reviews','negativ_reviews', 'product_url',
                          'category_name','subcategory_name', 'category_url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            products = self.get_product()
            writer.writeheader()
            for i in products:
                writer.writerow(i)