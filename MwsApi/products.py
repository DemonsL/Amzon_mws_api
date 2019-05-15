# coding: utf-8

from MwsApi.mws_client import MwsClient


class Products(MwsClient):
    """
    产品接口
    """

    version = '2011-10-01'
    uri = '/Products/{}'.format(version)

    def list_matching_products(self, params):
        http_method = 'POST'
        action = 'ListMatchingProducts'

        query = params.get('Query')
        query_context_id = params.get('QueryContextId')
        parameters = '&Query=' + self.params_encode(query)
        if query_context_id:
            parameters += '&QueryContextId=' + self.params_encode(query_context_id)
        return self.req_handler(http_method, action, parameters)

    def get_matching_product(self, params):
        http_method = 'POST'
        action = 'GetMatchingProduct'

        asins = params.get('ASINList')
        if asins.find(',') == -1:
            parameters = '&ASINList.ASIN.1=' + asins
        else:
            parameters = self.set_param_list(asins, 'ASINList.ASIN')
        return self.req_handler(http_method, action, parameters)

    def get_matching_product_for_id(self, params):
        http_method = 'POST'
        action = 'GetMatchingProductForId'

        id_type = params.get('IdType')
        id_list = params.get('IDLIST')
        parameters = '&IdType=' + id_type
        if id_list.find(',') == -1:
            parameters += '&IdList.Id.1=' + id_list
        else:
            parameters += self.set_param_list(id_list, 'IdList.Id')
        return self.req_handler(http_method, action, parameters)

    def get_competitive_pricing_for_sku(self, params):
        http_method = 'POST'
        action = 'GetCompetitivePricingForSKU'

        seller_skus = params.get('SellerSKUList')
        if seller_skus.find(',') == -1:
            parameters = '&SellerSKUList.SellerSKU.1=' + seller_skus
        else:
            parameters = self.set_param_list(seller_skus, 'SellerSKUList.SellerSKU')
        return self.req_handler(http_method, action, parameters)

    def get_competitive_pricing_for_asin(self, params):
        http_method = 'POST'
        action = 'GetCompetitivePricingForASIN'

        asins = params.get('ASINList')
        if asins.find(',') == -1:
            parameters = '&ASINList.ASIN.1=' + asins
        else:
            parameters = self.set_param_list(asins, 'ASINList.ASIN')
        return self.req_handler(http_method, action, parameters)

    def get_lowest_offer_listings_for_sku(self, params):
        http_method = 'POST'
        action = 'GetLowestOfferListingsForSKU'

        seller_skus = params.get('SellerSKUList')
        item_condition = params.get('ItemCondition')
        if seller_skus.find(',') == -1:
            parameters = '&SellerSKUList.SellerSKU.1=' + seller_skus
        else:
            parameters = self.set_param_list(seller_skus, 'SellerSKUList.SellerSKU')
        if item_condition:
            parameters += '&ItemCondition=' + item_condition
        return self.req_handler(http_method, action, parameters)

    def get_lowest_offer_listings_for_asin(self, params):
        http_method = 'POST'
        action = 'GetLowestOfferListingsForASIN'

        asins = params.get('ASINList')
        item_condition = params.get('ItemCondition')
        if asins.find(',') == -1:
            parameters = '&ASINList.ASIN.1=' + asins
        else:
            parameters = self.set_param_list(asins, 'ASINList.ASIN')
        if item_condition:
            parameters += '&ItemCondition=' + item_condition
        return self.req_handler(http_method, action, parameters)

    def get_lowest_priced_offers_for_sku(self, params):
        http_method = 'POST'
        action = 'GetLowestPricedOffersForSKU'

        seller_sku = params.get('SellerSKU  ')
        item_condition = params.get('ItemCondition')
        parameters = '&SellerSKU=' + seller_sku + '&ItemCondition=' + item_condition
        return self.req_handler(http_method, action, parameters)

    def get_lowest_priced_offers_for_asin(self, params):
        http_method = 'POST'
        action = 'GetLowestPricedOffersForASIN'

        asin = params.get('ASIN')
        item_condition = params.get('ItemCondition')
        parameters = '&ASIN=' + asin + '&ItemCondition=' + item_condition
        return self.req_handler(http_method, action, parameters)

    def get_my_fees_estimate(self, params):
        http_method = 'POST'
        action = 'GetMyFeesEstimate'

        fees_estimate = params.get('FeesEstimateRequestList')
        parameters = '&FeesEstimateRequestList=' + fees_estimate
        return self.req_handler(http_method, action, parameters)

    def get_my_price_for_sku(self, params):
        http_method = 'POST'
        action = 'GetMyPriceForSKU'

        seller_skus = params.get('SellerSKUList')
        item_condition = params.get('ItemCondition')
        if seller_skus.find(',') == -1:
            parameters = '&SellerSKUList.SellerSKU.1=' + seller_skus
        else:
            parameters = self.set_param_list(seller_skus, 'SellerSKUList.SellerSKU')
        if item_condition:
            parameters += '&ItemCondition=' + item_condition
        return self.req_handler(http_method, action, parameters)

    def get_my_price_for_asin(self, params):
        http_method = 'POST'
        action = 'GetMyPriceForASIN'

        asins = params.get('ASINList')
        item_condition = params.get('ItemCondition')
        if asins.find(',') == -1:
            parameters = '&ASINList.ASIN.1=' + asins
        else:
            parameters = self.set_param_list(asins, 'ASINList.ASIN')
        if item_condition:
            parameters += '&ItemCondition=' + item_condition
        return self.req_handler(http_method, action, parameters)

    def get_product_categories_for_sku(self, params):
        http_method = 'POST'
        action = 'GetProductCategoriesForSKU'

        seller_sku = params.get('SellerSKU')
        parameters = '&SellerSKU=' + seller_sku
        return self.req_handler(http_method, action, parameters)

    def get_product_categories_for_asin(self, params):
        http_method = 'POST'
        action = 'GetProductCategoriesForASIN'

        asin = params.get('ASIN')
        parameters = '&ASIN=' + asin
        return self.req_handler(http_method, action, parameters)

    def set_param_list(self, param_list, param_name):
        i, resp= 1, ''
        for param in param_list.split(','):
            resp += '&{pn}.{i}='.format(pn=param_name, i=i) + param
            i += 1
        return resp

    def req_handler(self, http_method, action, params):
        query_string = self.get_query_string(action, params, self.version)
        signature = self.string_to_sign(http_method, self.uri, query_string)
        url = self.get_url(self.host, self.uri, query_string, signature)
        return self.excute_req(url, http_method)
