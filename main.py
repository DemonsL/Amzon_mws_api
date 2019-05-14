# coding: utf-8
import xmltodict, json
from MwsApi.products import Products
from Config.mws_config import client, endpoint, marketplace


def main():
    access_key = client.get('access_key')
    secret_key = client.get('secret_key')
    seller_id = client.get('seller_id')
    auth_token = client.get('auth_token')
    host = endpoint.get('us')
    mkp_id = marketplace.get('us')

    return Products(access_key, secret_key, seller_id, auth_token, host, mkp_id)


if __name__ == '__main__':

    params = {
        'Query': 'iphone'
    }
    products = main()
    list_products = products.list_matching_products(params)
    resp_dict = xmltodict.parse(list_products.text)
    print(json.dumps(resp_dict))