from response import response
import csv


class Product:
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
        domain = 'https://www.vprok.ru'
        response.url = domain
        soup = response.get_soup()
        menu_urls = soup.find('nav', class_ = 'fo-catalog-menu__nav').find_all('a')
        products_list =[]
        for i in menu_urls:
            name_category = i.text.replace('\n', '').strip()
            links_category = i.attrs['href']
            try:
                response.url = domain + links_category
                soup = response.get_soup()
                catalog_items = soup.find('ul', id = 'catalogItems').find('li').find_all('div', class_ ='xf-product js-product')
                print(f'pars: {name_category} {links_category}')
            except:
                print(f'missed {name_category}')
            page = 1
            next_page = 2

            while page <= next_page:
                print(f'Парсинг страницы {page}')
                links_page = f'{ links_category }?page={page}'
                print(links_category)
                response.url = domain + links_page
                soup = response.get_soup()

                try:
                    next_page = int(soup.find('a', class_ = 'xf-paginator__item js-paginator__next').attrs['href'].split('=')[1])

                except AttributeError:
                    next_page = 1
                    print('В категории одна страница')

                try:
                    catalog_items = soup.find('ul', id = 'catalogItems').find_all('li') 
                    for i in catalog_items:
                        try:
                            product = i.find('div', class_ ='xf-product js-product').attrs
                            
                            self.market_name = 'vprok.ru'
                            self.domain = domain
                            self.product_id = product.get('data-owox-product-id')
                            self.product_name = product.get('data-owox-product-name')
                            self.price = product.get('data-owox-product-price')
                            self.is_available = product.get('data-owox-is-available')
                            self.measure = product.get('data-owox-fraction-text')
                            self.product_url = product.get('data-product-card-url')
                            self.vender_name = product.get('data-owox-product-vendor-name')
                            self.category_name = product.get('data-owox-portal-name')
                            self.subcategory_name = product.get('data-owox-category-name')
                            self.category_url = product.get('data-category-url')

                            print('product: ' + product.get('data-owox-product-name') + ' recorded')
                            yield self
                            
                        except AttributeError:
                            pass
                except AttributeError:
                    pass
                page += 1