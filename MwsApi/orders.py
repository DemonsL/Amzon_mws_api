# coding: utf-8
from Common import common
from MwsApi.mws_client import MwsClient


class Orders(MwsClient):
    """
    订单接口
    """

    VERSION = '2013-09-01'
    URI = '/Orders/{}'.format(VERSION)

    def list_orders(self, params):
        http_method = 'GET'
        action = 'ListOrders'

        created_after = params.get('CreatedAfter')
        created_before = params.get('CreatedBefore')
        last_updated_after = params.get('LastUpdatedAfter')
        last_updated_before = params.get('LastUpdatedBefore')
        order_status = params.get('OrderStatus')
        channel = params.get('FulfillmentChannel')
        pay_method = params.get('PaymentMethod')
        buyer_email = params.get('BuyerEmail')
        seller_order_id = params.get('SellerOrderId')
        max_page = params.get('MaxResultsPerPage')
        tfm_ship_status = params.get('TFMShipmentStatus')
        easy_ship_status = params.get('EasyShipShipmentStatus')

        parameters = ''
        if created_after:
            parameters = '&CreatedAfter=' + self.params_encode(created_after)
        if last_updated_after:
            parameters = '&LastUpdatedAfter=' + self.params_encode(last_updated_after)
        if created_before:
            parameters += '&CreatedBefore=' + self.params_encode(created_before)
        if last_updated_before:
            parameters += '&LastUpdatedBefore=' + self.params_encode(last_updated_before)
        if order_status:
            if order_status.find(',') == -1:
                parameters += '&OrderStatus.Status.1=' + self.params_encode(order_status)
            else:
                parameters += common.set_param_list(order_status, 'OrderStatus.Status')
        if channel:
            if channel.find(',') == -1:
                parameters += '&FulfillmentChannel.Channel.1=' + self.params_encode(channel)
            else:
                parameters += common.set_param_list(channel, 'FulfillmentChannel.Channel')
        if pay_method:
            if pay_method.find(',') == -1:
                parameters += '&PaymentMethod.Method.1=' + self.params_encode(pay_method)
            else:
                parameters += common.set_param_list(pay_method, 'PaymentMethod.Method')
        if buyer_email:
            parameters += '&BuyerEmail=' + self.params_encode(buyer_email)
        if seller_order_id:
            parameters += '&SellerOrderId=' + self.params_encode(seller_order_id)
        if max_page:
            parameters += '&MaxResultsPerPage=' + self.params_encode(max_page)
        if tfm_ship_status:
            parameters += '&TFMShipmentStatus=' + self.params_encode(tfm_ship_status)
        if easy_ship_status:
            parameters += '&EasyShipShipmentStatus=' + self.params_encode(easy_ship_status)
        return self.req_handler(http_method, action, parameters)

    def list_orders_by_next_token(self, params):
        http_method = 'GET'
        action = 'ListOrdersByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def get_order(self, params):
        http_method = 'GET'
        action = 'GetOrder'

        order_id = params.get('AmazonOrderId')
        if order_id.find(',') == -1:
            parameters = '&AmazonOrderId.Id.1=' + self.params_encode(order_id)
        else:
            parameters = common.set_param_list(order_id, 'AmazonOrderId.Id')
        return self.req_handler(http_method, action, parameters)

    def list_order_items(self, params):
        http_method = 'GET'
        action = 'ListOrderItems'

        order_id = params.get('AmazonOrderId')
        if order_id.find(',') == -1:
            parameters = '&AmazonOrderId.Id.1=' + self.params_encode(order_id)
        else:
            parameters = common.set_param_list(order_id, 'AmazonOrderId.Id')
        return self.req_handler(http_method, action, parameters)

    def list_order_items_by_next_token(self, params):
        http_method = 'GET'
        action = 'ListOrderItemsByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def req_handler(self, http_method, action, params):
        query_string = self.get_query_string(action, params, self.VERSION)
        signature = self.string_to_sign(http_method, self.URI, query_string)
        url = self.get_url(self.host, self.URI, query_string, signature)
        return self.excute_req(url, http_method)

