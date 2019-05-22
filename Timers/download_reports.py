# coding: utf-8
from Common import common
from MwsApi.reports import Reports
from Config.mws_config import client, endpoint, marketplace

class DownloadReports:

    def get_reports_client(self):
        access_key = client.get('access_key')
        secret_key = client.get('secret_key')
        seller_id = client.get('seller_id')
        auth_token = client.get('auth_token')
        host = endpoint.get('us')
        mkp_id = marketplace.get('us')
        return Reports(access_key, secret_key, seller_id, auth_token, host, mkp_id)

    def request_report(self, rp_client, params):
        resp = None
        try:
            resp_xml = rp_client.request_report(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            print('RequestReport Error: ', e)
        return resp

    def get_report_requests(self, rp_client, rpq_ids):
        params = {
            'ReportRequestIdList': rpq_ids
        }
        resp = None
        try:
            resp_xml = rp_client.get_report_request_list(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            print('GetReportRequestList Error: ', e)
        return resp

    def get_report(self, rp_client, rp_id):
        params = {
            'ReportId': rp_id
        }
        resp = None
        try:
            resp_flat = rp_client.get_report(params)
            resp = common.flat_to_json(resp_flat.text)
        except Exception as e:
            print('GetReport Error: ', e)
        return resp
