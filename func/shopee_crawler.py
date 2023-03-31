from seleniumwire.utils import decode
import json
import pandas as pd
import requests
import datetime, time
from .data_process import browser, get_json_data
from .character_process import flat_dict as flat_dict
from func.var.config import header_config
from typing import List

# Lấy thông tin sản phẩm theo từ khóa tìm kiếm theo số trang cần lấy
def search_get_items(url = f'https://shopee.vn/search?keyword=b%E1%BB%89m%20youli',
                     api = f'https://shopee.vn/api/v4/search/search_items?by=',
                     page_number = 1):
    # driver = browser()
    list_search = pd.DataFrame()
    for i in list(range(page_number)):
        try:
            # url = f'https://shopee.vn/search?keyword=s%E1%BB%AFa%20r%E1%BB%ADa%20m%E1%BA%B7t%20nuskin&page={i}'
            url = f'{url}&page={i}'
            driver = browser()
            time.sleep(1)
            driver.get(url)
            for request in driver.requests:
                if request.response:
                    if request.url.startswith(api):
                        response = request.response
                        body = decode(response.body, response.headers.get('Content-Encoding', 'Identify'))
                        decoded_body = body.decode('utf8')
                        json_data = json.loads(decoded_body)
                        r_list_search = pd.json_normalize(i['item_basic'] for i in json_data['items'])
                        r_list_search['page_number'] = i
                        list_search = pd.concat([list_search,r_list_search],axis=0)
            driver.close()
            time.sleep(1)
        except:
            pass
    list_search = list_search.reset_index().drop('index',axis=1)
    # driver.close()
    return list_search

# Lấy thông tin sản phẩm theo từ khóa tìm kiếm theo page chỉ định cụ thể
def search_get_items_with_selected_page(url = f'https://shopee.vn/search?keyword=b%E1%BB%89m%20youli',
                                        api = f'https://shopee.vn/api/v4/search/search_items?by=',
                                        page_number = 0):
    # driver = browser()
    list_search = pd.DataFrame()
    try:
        # url = f'https://shopee.vn/search?keyword=s%E1%BB%AFa%20r%E1%BB%ADa%20m%E1%BA%B7t%20nuskin&page={i}'
        url = f'{url}&page={page_number}'
        driver = browser()
        time.sleep(1)
        driver.get(url)
        # time.sleep(1)
        for request in driver.requests:
            if request.response:
                if request.url.startswith(api):
                    response = request.response
                    body = decode(response.body, response.headers.get('Content-Encoding', 'Identify'))
                    decoded_body = body.decode('utf8')
                    json_data = json.loads(decoded_body)
                    r_list_search = pd.json_normalize(i['item_basic'] for i in json_data['items'])
                    r_list_search['page_number'] = page_number
                    list_search = pd.concat([list_search,r_list_search],axis=0)
        driver.close()
        time.sleep(1)
    except:
        pass
    list_search = list_search.reset_index().drop('index',axis=1)
    # list_search = list_search.astype({'shopid':int,
    #                                   'itemid':int})
    return list_search

# Lấy danh sách sản phẩm phải có mã giảm giá
def search_only_voucher():
    final = search_get_items()
    final['shop_vouchers']= final['shop_vouchers'].fillna(value='')
    final['vouchers']= final['shop_vouchers'].apply(lambda x : [i['voucher_code'] for i in x] if i!= None else '' if len(i[0])<=1 else [])
    final['check'] = final['vouchers'].apply(lambda x: len(x))
    data = final[final['check']>0]
    # data = data.drop_duplicates()
    data['link'] = 'https://shopee.vn/abc-i'
    data['link'] = data['link'].str.cat(data[["shopid", "itemid"]].astype(str), sep=".")
    data = data.reset_index().drop('index',axis=1)
    return data

# Lấy mã ID ngành hàng mẹ
def get_industry_data(  url = f'https://shopee.vn/abc-cat.11036194?facet=100678',
                        api = f'https://shopee.vn/api/v4/pages/get_category_tree'
                        ):    
    # Lấy danh sách ngành
    # craw data
    json_raw = get_json_data(url,api)
    # transform
    cate_all = pd.json_normalize(json_raw['data']['category_list'])
    cat_details = pd.concat([pd.json_normalize(cate_all.iloc[[i]]['children'][i]) for i in range(len(cate_all))],axis=0)
    cat_details = cat_details.reset_index().drop('index',axis=1)[['catid','parent_catid','name','display_name','image']]
    # get final 
    sum_cate = cat_details.merge(cate_all[['catid','name','display_name']], how='left', left_on='parent_catid', right_on='catid')[['catid_x', 'parent_catid', 'name_x', 'display_name_x', 'image', 'name_y', 'display_name_y']]
    sum_cate.columns = ['catid', 'parent_catid', 'name', 'display_name', 'image','parent_name', 'parent_display_name']
    return sum_cate

# Lấy mã ID ngành hàng con
"""
url_file: File chứa thông tin ngành con từ ngành mẹ (tên "filter_facet")
e.g: D:\Python\Shopee-Crawler\output data\filter_facet.xlsx
"""
def get_facet(url_file: any,search_facet: dict):
    sub_facet = pd.DataFrame()
    for i in range(len(search_facet)):
        while True:
            try:
                cate = search_facet[i]['parent_catid']
                sub_cat_url = f'https://shopee.vn/abc-cat.{cate}'
                sub_cat_api= f'https://shopee.vn/api/v4/search/search_filter_config?match_id={cate}'
                r_sub_cat = get_json_data(sub_cat_url,sub_cat_api)
                raw_data = pd.json_normalize(r_sub_cat['data']['filter_configuration']['dynamic_filter_group_data']['facets'])
            except:
                pass
            if len(raw_data)>1:
                break
        list_sub_facet = raw_data[['catid','category.display_name']].rename(columns={'catid':'facetid','category.display_name': 'facet_name'}).drop_duplicates().reset_index().drop('index',axis=1)
        list_sub_facet['parent_facetid'] = cate
        list_sub_facet['parent_name'] = search_facet[i]['parent_display_name']
        sub_facet = pd.concat([sub_facet, list_sub_facet], axis=0)
        pd.concat([pd.read_excel(url_file).drop_duplicates(),sub_facet],axis=0).reset_index().drop('index',axis=1).to_excel(url_file,index=False)
    return sub_facet

# Lấy danh sách sản phẩm từ web
"""
sub_facet: file chứa ID dữ liệu ngành mẹ + ngành con
e.g: D:\Python\Shopee-Crawler\output data\filter_facet.xlsx
"""
def get_items_from_industry (sub_facet: str, industry_list: List, page_number_to_crawl:int):
    selected_industry = sub_facet[sub_facet['parent_name'].isin(industry_list)]
    dict_menu= selected_industry.to_dict('records')
    list_item_by_menu = pd.DataFrame()
    for i in range(len(dict_menu)):
        for page_number in list(range(page_number_to_crawl)): #Lấy 4 trang đầu tiên tương ứng 240 sản phẩm
            try:
                parent_facetid = dict_menu[i]['parent_facetid']
                facetid = dict_menu[i]['facetid']
                menu_url = f'https://shopee.vn/abc-cat.{parent_facetid}?facet={facetid}&page={page_number}'
                menu_api = f'https://shopee.vn/api/v4/search/search_items?'
                raw = get_json_data(menu_url,menu_api)
                list_name = pd.json_normalize(raw['items'])[['item_basic.name']]
                list_name['parent_name'] = dict_menu[i]['parent_name']
                list_name['facet_name'] = dict_menu[i]['facet_name']
                list_item_by_menu = pd.concat([list_item_by_menu, list_name], axis=0)
            except:
                pass
    list_item_by_menu = list_item_by_menu.reset_index().drop('index',axis=1)
    return list_item_by_menu

# Lấy giá từ modelid, shopid, itemid
def get_item_price(df):
    item_url = f"https://shopee.vn/api/v4/product/get_purchase_quantities_for_selected_model?itemId={df['itemid']}&modelId={df['modelid']}&shopId={df['shopid']}"

    payload={
    }
    headers = header_config.headers
    response = requests.request("GET", item_url, headers=headers, data=payload)

    item_raw=response.json()
    price_r_data = pd.json_normalize(item_raw['available_price_and_stocks'])
    price_r_data = price_r_data[price_r_data.display_price >0]
    min_price = price_r_data[price_r_data.display_price == price_r_data.display_price.min()]
    price_data = pd.concat([pd.json_normalize(item_raw)[['price_before_discount']],min_price], axis = 1)
    price_data = price_data[['price_before_discount','display_stock','display_price']]
    return price_data


# Thông tin cơ bản sản phẩm
def get_in4_item(shopid: int, itemid: int):
    item_url = f"https://shopee.vn/api/v4/item/get?itemid={itemid}&shopid={shopid}"

    payload={
    }
    headers = header_config.headers
    response = requests.request("GET", item_url, headers=headers, data=payload)
    item_raw=response.json()
    # overview product infor
    product_data=pd.json_normalize(item_raw['data'])
    inf = product_data[['shopid','itemid','name','brand','categories','historical_sold','item_rating.rating_star','images']]#'price','stock','discount','historical_sold','sold','description','categories','shop_vouchers','global_sold'
    inf = pd.concat([inf,flat_dict(inf['categories'])],axis=1).rename(columns={'name':'parent_name'}).drop('categories',axis=1)    
    # Detail product infor
    model_data = pd.json_normalize(item_raw['data']['models'])[['itemid','name','modelid']].assign(shopid=shopid)
    get_price = pd.concat(model_data.apply(lambda x: get_item_price(x), axis=1).tolist(), ignore_index=True)
    price_data = pd.concat([model_data,get_price],axis=1).rename(columns={'itemid':'item','shopid':'shop'})
    # price_data = price_data.astype({'item':int,
    #                                 'shop':int})
    df = price_data.merge(inf, how='left', left_on=['item','shop'],right_on=['itemid','shopid'])
    df = df[df['itemid'].notnull()].reset_index().drop('index',axis=1)
    return df

# Thông tin chi tiết sản phẩm
def get_full_in4_item(shopid: int, itemid: int):
    item_url = f"https://shopee.vn/api/v4/item/get?itemid={itemid}&shopid={shopid}"

    payload={
    }
    headers = header_config.headers
    response = requests.request("GET", item_url, headers=headers, data=payload)
    item_raw=response.json()
    product_data=pd.json_normalize(item_raw['data'])
    # product_data = product_data.astype({'itemid':int,
    #                                     'shopid':int})
    model_data = pd.json_normalize(item_raw['data']['models'])[['itemid','name','modelid']].assign(shopid=shopid)
    get_price = pd.concat(model_data.apply(lambda x: get_item_price(x), axis=1).tolist(), ignore_index=True)
    price_data = pd.concat([model_data,get_price],axis=1).rename(columns={'itemid':'item','shopid':'shop'})
    # price_data = price_data.astype({'item':int,
    #                                 'shop':int})
    df = price_data.merge(product_data, how='left', left_on=['item','shop'],right_on=['itemid','shopid'])
    df = df[df['itemid'].notnull()].reset_index().drop('index',axis=1)
    return df