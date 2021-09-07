from response import GetSoup
import csv


response = GetSoup()

class Category:
    name = ''
    sub_name = ''
    url = ''
    response.url = 'https://www.okeydostavka.ru/spb/catalog'

    def parser(self):
        soup = response.get_soup()
        all_menu = soup.find('ul', id = 'allDepartmentsMenu').find_all('li', class_ ='catalog-menu__department')
        
        for i in all_menu:
            self.name = i.find('div', class_="menu-label").text.replace("\n","").replace("\t","")
            url_list = i.find('ul', class_ = 'categoryList catalog-menu__category-list')
            if url_list is not None:
                subcategory_list = url_list.find_all('li')
                for i in subcategory_list:
                    self.url = i.find('a', class_='menuLink').attrs['href']
                    self.sub_name = i.find('a', class_='menuLink').text.strip()
                    print(self.sub_name)
                    yield self


class Product(Category):
    market_name = ''
    domain = ''
    product_id = ''
    product_name = ''
    price = ''
    is_available = ''
    measure = ''
    product_url = ''
    vender_name = ''
    portal_name = ''
    category_name = ''
    category_url = ''
    
    
    def parser(self):
        for category in Category().parser():
            domain = 'https://www.okeydostavka.ru'
            response.url = domain + category.url
            soup = response.get_soup()
            try:
                products = soup.find('ul', class_ = 'grid_mode grid rows').find_all('li')
                for i in products:
                    if products is not None:
                        product_weight = i.find('div', class_ = 'product-weight').text.split()
                        response.url = domain + i.find('a').attrs['href']
                        product_soup = response.get_soup()
                        
                        self.market_name = 'okey'
                        self.domain = domain
                        self.product_id = i.find('div', class_='product-cart').find('a').attrs['data-entry-id']
                        self.product_name = i.find('a').attrs['title']
                        self.price = i.find('div', class_='product-cart').find('a').attrs['data-price']
                        self.is_available = product_weight[0]
                        self.measure = product_weight[1]
                        self.product_url = i.find('a').attrs['href']
                        self.vender_name = product_soup.find('div', class_='tab-container-bordered').find('div', class_='attributes__value').text.strip()
                        self.category_name = category.name
                        self.subcategory_name = category.sub_name
                        self.category_url = category.url
                        print(f'        {self.product_name}')
                        yield self
            except:
                pass


    def writer_csv(self):
        file_name = self.market_name
        with open('file_name.csv', mode='w', encoding='utf-8') as csv_file:
            fieldnames = ['market_name', 'domain', 'product_id', 'product_name', 'price',
                          'is_available', 'measure', 'product_url', 'vender_name',
                          'category_name','subcategory_name', 'category_url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            products = self.parser()
            writer.writeheader()
            for i in products:
                writer.writerow(i.__dict__)