# coding: utf-8
from Common import common
from MwsApi.mws_client import MwsClient


class Reports(MwsClient):
    """
    报告接口
    """

    VERSION = '2009-01-01'
    URI = '/Reports/{}'.format(VERSION)

    def request_report(self, params):
        http_method = 'POST'
        action = 'RequestReport'

        report_type = params.get('ReportType')
        start_date = params.get('StartDate')
        end_date = params.get('EndDate')
        report_options = params.get('ReportOptions')
        parameters = '&ReportType=' + self.params_encode(report_type)
        if start_date:
            iso_time = common.amz_iso_time(start_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&StartDate=' + time_encode
        if end_date:
            iso_time = common.amz_iso_time(end_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&EndDate=' + time_encode
        if report_options:
            parameters += '&ReportOptions=' + report_options
        return self.req_handler(http_method, action, parameters)

    def get_report_request_list(self, params):
        http_method = 'POST'
        action = 'GetReportRequestList'

        report_request_ids = params.get('ReportRequestIdList')
        report_types = params.get('ReportTypeList')
        report_status = params.get('ReportProcessingStatusList')
        max_count = params.get('MAXCOUNT')
        request_from_date = params.get('RequestedFromDate')
        request_to_date = params.get('RequestedToDate')
        parameters = ''
        if report_request_ids:
            if report_request_ids.find(',') == -1:
                parameters = '&ReportRequestIdList.Id.1=' + report_request_ids
            else:
                parameters = common.set_param_list(report_request_ids, 'ReportRequestIdList.Id')
        if report_types:
            if report_types.find(',') == -1:
                parameters += '&ReportTypeList.Type.1=' + report_types
            else:
                parameters += common.set_param_list(report_types, 'ReportTypeList.Type')
        if report_status:
            if report_status.find(',') == -1:
                parameters += '&ReportProcessingStatusList.Status.1=' + report_status
            else:
                parameters += common.set_param_list(report_status, 'ReportProcessingStatusList.Status')
        if max_count:
            parameters += '&MAXCOUNT=' + max_count
        if request_from_date:
            iso_time = common.amz_iso_time(request_from_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&RequestedFromDate=' + time_encode
        if request_to_date:
            iso_time = common.amz_iso_time(request_to_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&RequestedToDate=' + time_encode
        return self.req_handler(http_method, action, parameters)

    def get_report_request_list_by_next_token(self, params):
        http_method = 'POST'
        action = 'GetReportRequestListByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def get_report_request_count(self, params):
        http_method = 'POST'
        action = 'GetReportRequestCount'

        report_types = params.get('ReportTypeList')
        report_status = params.get('ReportProcessingStatusList')
        request_from_date = params.get('RequestedFromDate')
        request_to_date = params.get('RequestedToDate')
        parameters = ''
        if report_types:
            if report_types.find(',') == -1:
                parameters += '&ReportTypeList.Type.1=' + report_types
            else:
                parameters += common.set_param_list(report_types, 'ReportTypeList.Type')
        if report_status:
            if report_status.find(',') == -1:
                parameters += '&ReportProcessingStatusList.Status.1=' + report_status
            else:
                parameters += common.set_param_list(report_status, 'ReportProcessingStatusList.Status')
        if request_from_date:
            iso_time = common.amz_iso_time(request_from_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&RequestedFromDate=' + time_encode
        if request_to_date:
            iso_time = common.amz_iso_time(request_to_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&RequestedToDate=' + time_encode
        return self.req_handler(http_method, action, parameters)

    def cancel_report_requests(self, params):
        http_method = 'POST'
        action = 'CancelReportRequests'

        report_request_ids = params.get('ReportRequestIdList')
        report_types = params.get('ReportTypeList')
        report_status = params.get('ReportProcessingStatusList')
        request_from_date = params.get('RequestedFromDate')
        request_to_date = params.get('RequestedToDate')
        parameters = ''
        if report_request_ids:
            if report_request_ids.find(',') == -1:
                parameters += '&ReportRequestIdList.Id.1=' + report_request_ids
            else:
                parameters += common.set_param_list(report_request_ids, 'ReportRequestIdList.Id')
        if report_types:
            if report_types.find(',') == -1:
                parameters += '&ReportTypeList.Type.1=' + report_types
            else:
                parameters += common.set_param_list(report_types, 'ReportTypeList.Type')
        if report_status:
            if report_status.find(',') == -1:
                parameters += '&ReportProcessingStatusList.Status.1=' + report_status
            else:
                parameters += common.set_param_list(report_status, 'ReportProcessingStatusList.Status')
        if request_from_date:
            iso_time = common.amz_iso_time(request_from_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&RequestedFromDate=' + time_encode
        if request_to_date:
            iso_time = common.amz_iso_time(request_to_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&RequestedToDate=' + time_encode
        return self.req_handler(http_method, action, parameters)

    def get_report_list(self, params):
        http_method = 'POST'
        action = 'GetReportList'

        max_count = params.get('MaxCount')
        report_types = params.get('ReportTypeList')
        al = params.get('Acknowledged')
        report_request_ids = params.get('ReportRequestIdList')
        available_from_date = params.get('AvailableFromDate')
        available_to_date = params.get('AvailableToDate')
        parameters = ''
        if max_count:
            parameters += '&MaxCount=' + max_count
        if report_types:
            if report_types.find(',') == -1:
                parameters += '&ReportTypeList.Type.1=' + report_types
            else:
                parameters += common.set_param_list(report_types, 'ReportTypeList.Type')
        if al:
            parameters += '&Acknowledged=' + al
        if report_request_ids:
            if report_request_ids.find(',') == -1:
                parameters += '&ReportRequestIdList.Id.1=' + report_request_ids
            else:
                parameters += common.set_param_list(report_request_ids, 'ReportRequestIdList.Id')
        if available_from_date:
            iso_time = common.amz_iso_time(available_from_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&AvailableFromDate=' + time_encode
        if available_to_date:
            iso_time = common.amz_iso_time(available_to_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&AvailableToDate=' + time_encode
        return self.req_handler(http_method, action, parameters)

    def get_report_list_by_next_token(self, params):
        http_method = 'POST'
        action = 'GetReportListByNextToken'

        next_token = params.get('NextToken')
        parameters = '&NextToken=' + self.params_encode(next_token)
        return self.req_handler(http_method, action, parameters)

    def get_report_count(self, params):
        http_method = 'POST'
        action = 'GetReportCount'

        report_types = params.get('ReportTypeList')
        al = params.get('Acknowledged')
        available_from_date = params.get('AvailableFromDate')
        available_to_date = params.get('AvailableToDate')
        parameters = ''
        if report_types:
            if report_types.find(',') == -1:
                parameters += '&ReportTypeList.Type.1=' + report_types
            else:
                parameters += common.set_param_list(report_types, 'ReportTypeList.Type')
        if al:
            parameters += '&Acknowledged=' + al
        if available_from_date:
            iso_time = common.amz_iso_time(available_from_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&AvailableFromDate=' + time_encode
        if available_to_date:
            iso_time = common.amz_iso_time(available_to_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&AvailableToDate=' + time_encode
        return self.req_handler(http_method, action, parameters)

    def get_report(self, params):
        http_method = 'POST'
        action = 'GetReport'

        report_id = params.get('ReportId')
        parameters = '&ReportId=' + report_id
        return self.req_handler(http_method, action, parameters)

    def manage_report_schedule(self, params):
        http_method = 'POST'
        action = 'ManageReportSchedule'

        report_type = params.get('ReportType')
        schedule = params.get('Schedule')
        schedule_date = params.get('ScheduleDate')
        parameters = '&ReportType=' + report_type + '&Schedule=' + schedule
        if schedule_date:
            iso_time = common.amz_iso_time(schedule_date)
            time_encode = self.params_encode(iso_time)
            parameters += '&ScheduleDate=' + time_encode
        return self.req_handler(http_method, action, parameters)

    def get_report_schedule_list(self, params):
        http_method = 'POST'
        action = 'GetReportScheduleList'

        report_types = params.get('ReportTypeList')
        if report_types.find(',') == -1:
            parameters = '&ReportTypeList.Type.1=' + report_types
        else:
            parameters = common.set_param_list(report_types, 'ReportTypeList.Type')
        return self.req_handler(http_method, action, parameters)

    def get_report_schedule_count(self, params):
        http_method = 'POST'
        action = 'GetReportScheduleCount'

        report_types = params.get('ReportTypeList')
        if report_types.find(',') == -1:
            parameters = '&ReportTypeList.Type.1=' + report_types
        else:
            parameters = common.set_param_list(report_types, 'ReportTypeList.Type')
        return self.req_handler(http_method, action, parameters)

    def update_report_acknowledgements(self, params):
        http_method = 'POST'
        action = 'UpdateReportAcknowledgements'

        report_ids = params.get('ReportIdList')
        al = params.get('Acknowledged')
        if report_ids.find(',') == -1:
            parameters = '&ReportIdList.Id.1=' + report_ids
        else:
            parameters = common.set_param_list(report_ids, 'ReportIdList.Id')
        if al:
            parameters += '&Acknowledged=' + al
        return self.req_handler(http_method, action, parameters)

    def req_handler(self, http_method, action, params):
        query_string = self.get_query_string(action, params, self.VERSION)
        signature = self.string_to_sign(http_method, self.URI, query_string)
        url = self.get_url(self.host, self.URI, query_string, signature)
        return self.excute_req(url, http_method)


