# coding: utf-8
from Common import common
from MwsApi.mws_client import MwsClient


class Finances(MwsClient):
    """
    财务接口
    """

    VERSION = '2015-05-01'
    URI = '/Finances/{}'.format(VERSION)

    def list_financial_event_groups(self, params):
        http_method = 'POST'
        action = 'ListFinancialEventGroups'

        max_num = params.get('MaxResultsPerPage')
        start_date = params.get('FinancialEventGroupStartedAfter')
        end_date = params.get('FinancialEventGroupStartedBefore')
        parameters = '&FinancialEventGroupStartedAfter=' + self.params_encode(common.amz_iso_time(start_date))
        if max_num:
            parameters += '&MaxResultsPerPage=' + max_num
        if end_date:
            parameters += '&FinancialEventGroupStartedBefore=' + self.params_encode(common.amz_iso_time(end_date))
        return self.req_handler(http_method, action, parameters)

    def list_financial_event_groups_by_nexttoken(self, params):
        http_method = 'POST'
        action = 'ListFinancialEventGroupsByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def list_financial_events(self, params):
        http_method = 'POST'
        action = 'ListFinancialEvents'

        max_num = params.get('MaxResultsPerPage')
        order_id = params.get('AmazonOrderId')
        event_group_id = params.get('FinancialEventGroupId')
        start_posted = params.get('PostedAfter')
        end_posted = params.get('PostedBefore')
        parameters = ''
        if order_id:
            parameters = '&AmazonOrderId=' + order_id
        elif event_group_id:
            parameters = '&FinancialEventGroupId=' + event_group_id
        elif start_posted:
            parameters = '&PostedAfter=' + self.params_encode(common.amz_iso_time(start_posted))
        if max_num:
            parameters += '&MaxResultsPerPage=' + max_num
        if end_posted:
            parameters += '&PostedBefore=' + self.params_encode(common.amz_iso_time(end_posted))
        return self.req_handler(http_method, action, parameters)

    def list_financial_events_by_nexttoken(self, params):
        http_method = 'POST'
        action = 'ListFinancialEventsByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def req_handler(self, http_method, action, params):
        query_string = self.get_query_string(action, params, self.VERSION)
        signature = self.string_to_sign(http_method, self.URI, query_string)
        url = self.get_url(self.host, self.URI, query_string, signature)
        return self.excute_req(url, http_method)