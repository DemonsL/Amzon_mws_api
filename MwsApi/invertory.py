# coding: utf-8
import datetime
from MwsApi.mws_client import MwsClient
from Common import common


class Invertory(MwsClient):
    """
    库存接口
    """

    VERSION = '2010-10-01'
    URI = '/FulfillmentInventory/{}'.format(VERSION)

    def list_invertory_supply(self, params):
        http_method = 'GET'
        action = 'ListInventorySupply'

        seller_skus = params.get('SellerSkus')
        start_time = params.get('QueryStartDateTime')
        response_group = params.get('ResponseGroup')
        parameters = ''
        if seller_skus:
            if seller_skus.find(',') == -1:
                parameters = '&SellerSkus.member.1=' + seller_skus
            else:
                parameters = common.set_param_list(seller_skus, 'SellerSkus.member')
        if start_time:
            start_time_iso = datetime.datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            parameters = '&QueryStartDateTime=' + self.params_encode(start_time_iso)
        if response_group:
            parameters += '&ResponseGroup=' + response_group
        return self.req_handler(http_method, action, parameters)

    def list_invertory_supply_by_next_token(self, params):
        http_method = 'GET'
        action = 'ListInventorySupplyByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def req_handler(self, http_method, action, params):
        query_string = self.get_query_string(action, params, self.VERSION)
        signature = self.string_to_sign(http_method, self.URI, query_string)
        url = self.get_url(self.host, self.URI, query_string, signature)
        return self.excute_req(url, http_method)


