# coding: utf-8

from MwsApi.mws_client import MwsClient


class Products(MwsClient):
    """
    产品接口
    """

    version = '2011-10-01'
    uri = '/Products/{}'.format(version)

    def list_matching_products(self, params):
        action = 'ListMatchingProducts'
        query = params.get('Query')
        query_context_id = params.get('QueryContextId')
        parameters = '&Query=' + self.params_encode(query)
        if query_context_id:
            parameters += '&QueryContextId=' + self.params_encode(query_context_id)

        http_method = 'POST'
        query_string = self.get_query_string(action, parameters, self.version)
        signature = self.string_to_sign(http_method, self.uri, query_string)
        url = self.get_url(self.host, self.uri, query_string, signature)
        resp = self.excute_req(url, http_method)
        return resp
