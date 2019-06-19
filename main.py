# coding: utf-8
import xmltodict, json, datetime
from MwsApi.products import Products
from MwsApi.invertory import Invertory
from MwsApi.reports import Reports
from Config.mws_config import client, endpoint, marketplace


def main():
    access_key = client.get('access_key')
    secret_key = client.get('secret_key')
    seller_id = client.get('seller_id')
    auth_token = client.get('auth_token')
    host = endpoint.get('us')
    mkp_id = marketplace.get('us')

    return Reports(access_key, secret_key, seller_id, auth_token, host, mkp_id)


if __name__ == '__main__':

    params = {
        # "StartDate": datetime.datetime(2019, 5, 18),
        # "ReportType": "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_",
        # "ReportRequestIdList": "59432018036",
        "ReportId": "14943331231018036",
        # "ASINList": "B01MV2YGRR"
    }
    mws = main()
    resp = mws.get_report(params)
    print(resp.text)
    resp_dict = xmltodict.parse(resp.text)
    print(json.dumps(resp_dict))