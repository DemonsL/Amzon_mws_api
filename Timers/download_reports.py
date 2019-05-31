# coding: utf-8
import sys
sys.path.append('../')
import time
import datetime
from Models import reports
from Common import common
from MwsApi.reports import Reports
from Config import mws_config

class DownloadReports:
    """
    下载报告接口
    """

    time_fmt = '%Y-%m-%d %H:%M:%S'

    def request_report(self, rp_client, params):
        resp = []
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
        resp = []
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
        resp = []
        try:
            resp_flat = rp_client.get_report(params)
            resp = common.flat_to_json(resp_flat.text)
        except Exception as e:
            print('GetReport Error: ', e)
        return resp

    def add_report_to_sql(self, tb_name, country, report_json, snap_date=None):
        execute_sql = 'reports.{}'.format(tb_name)
        session = reports.DBSession()
        for report in report_json:
            if snap_date:
                report_to_sql = eval(execute_sql)(snap_date, country, report)
            else:
                report_to_sql = eval(execute_sql)(country, report)
            session.add(report_to_sql)
        session.commit()

    def get_report_id(self, rp_client, rpq_id):
        while True:
            time.sleep(20)                  # 等待报告生成成功
            rpq_resp = self.get_report_requests(rp_client, rpq_id)
            rpq_list = rpq_resp.get('GetReportRequestListResponse')
            if rpq_list:
                rpq_status = rpq_list.get('GetReportRequestListResult') \
                                     .get('ReportRequestInfo') \
                                     .get('ReportProcessingStatus')
                print(datetime.datetime.now().strftime(self.time_fmt), ' ReportStatus: ', rpq_status)
                if rpq_status == '_DONE_':
                    rp_id = rpq_list.get('GetReportRequestListResult') \
                                    .get('ReportRequestInfo') \
                                    .get('GeneratedReportId')
                    return rp_id
                if rpq_status == '_CANCELLED_':
                    print(datetime.datetime.now().strftime(self.time_fmt), ' Report is cancelled，please wait 30 minute.')
                    return False
            time.sleep(25)              # 请求报告列表每45秒一次

    def download_run(self, rp_client, params):
        while True:
            reports = self.request_report(rp_client, params)
            rpq_id = reports.get('RequestReportResponse') \
                            .get('RequestReportResult') \
                            .get('ReportRequestInfo') \
                            .get('ReportRequestId')
            rp_id = self.get_report_id(rp_client, rpq_id)
            if rp_id:
                rp = self.get_report(rp_client, rp_id)
                print(rp)

                print(datetime.datetime.now().strftime(self.time_fmt), ' Report add to sql...')
                mkp = params.get('mkp')
                tb_name = params.get('table_name')
                rp_date = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                if tb_name in ['AprFBAAllOrders', 'AprFBAShipments', 'AprFBAInventoryAge',
                               'AprFBAInventoryHealth', 'AprFBAInventoryAge']:
                    self.add_report_to_sql(tb_name, mkp.upper(), rp)
                else:
                    self.add_report_to_sql(tb_name, mkp.upper(), rp, rp_date)
                print(datetime.datetime.now().strftime(self.time_fmt), ' Report add success!')
                return
            time.sleep(1800)      # 请求报告取消状态时，每30分钟一次





def get_reports_client(mkp):
    access_key = mws_config.client.get('access_key')
    secret_key = mws_config.client.get('secret_key')
    seller_id = mws_config.client.get('seller_id')
    auth_token = mws_config.client.get('auth_token')
    host = mws_config.endpoint.get('us')
    mkp_id = mws_config.marketplace.get(mkp)
    return Reports(access_key, secret_key, seller_id, auth_token, host, mkp_id)

def download_report_start(rp_type, mkp):
    time_fmt = '%Y-%m-%d %H:%M:%S'
    print(datetime.datetime.now().strftime(time_fmt), ' Download report starting...')

    report_date = datetime.datetime.now()
    report_date -= datetime.timedelta(days=2)
    start_date = datetime.datetime.strptime(report_date.strftime('%Y-%m-%d 00:00:00'), time_fmt)
    end_date = datetime.datetime.strptime(report_date.strftime('%Y-%m-%d 23:59:59'), time_fmt)
    params = {
        "StartDate": start_date,
        "EndDate": end_date,
        "ReportType": rp_type,
        "table_name": mws_config.report_type.get(rp_type)
    }
    report_client = get_reports_client(mkp)
    params['mkp'] = mkp
    print(datetime.datetime.now().strftime(time_fmt), ' ReportDate: ', str(start_date) + ' - ' + str(end_date))
    print(datetime.datetime.now().strftime(time_fmt), ' ReportType: ', rp_type)
    print(datetime.datetime.now().strftime(time_fmt), ' Marketplace: ', mkp.upper())
    dw_report = DownloadReports()
    dw_report.download_run(report_client, params)

    print(datetime.datetime.now().strftime(time_fmt), ' Download report end!')


if __name__ == '__main__':

    dw_report_type = ['_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_',
                      '_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_',
                      '_GET_FBA_INVENTORY_AGED_DATA_',
                      '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_',
                      '_GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA_',
                      '_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_']

    for rp_type in dw_report_type:
        download_report_start(rp_type, 'us')

        time.sleep(60)  # 报告请求每分钟一次
