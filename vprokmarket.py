from mysoup import Soup


def parser():
    URL = 'https://www.vprok.ru'
    soup = Soup(URL).get_soup()
    menu_urls = soup.find('nav', class_ = 'fo-catalog-menu__nav').find_all('a')
    products_list =[]
    for i in menu_urls:
        name_category = i.text.replace('\n', '').strip()
        links_category = i.attrs['href']
        try:
            soup = Soup(URL + links_category).get_soup()
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
            soup = Soup(URL + links_page).get_soup()

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
                            # cart_product_dict = {'product-card-url' : product.get('data-product-card-url'),
                            #                     'category-name' : product.get('data-owox-category-name'),
                            #                     'product-price' : product.get('data-owox-product-price'),
                            #                     'product-name' : product.get('data-owox-product-name'),
                            #                     'product-unit' : product.get('data-owox-fraction-text'),
                            #                     'is-available' : product.get('data-owox-is-available'),
                            #                     'product-vendor-name' : product.get('data-owox-product-vendor-name'),
                            #                         }
                        products_list.append(product) 
                        print('product: ' + product.get('data-owox-product-name') + ' recorded')
                    except AttributeError:
                        pass
            except AttributeError:
                pass
            page += 1
    return products_list