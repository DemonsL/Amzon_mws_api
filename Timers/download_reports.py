# coding: utf-8
import sys
sys.path.append('../')
import time
import logging
import datetime
from Models import reports, orders
from Common import common
from MwsApi.reports import Reports
from Config import mws_config

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/mws_reports/{}.log'.format(datetime.date.today())
log = logging.getLogger()
log.setLevel(logging.INFO)


fh = logging.FileHandler(file_name, mode='a+')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)

class DownloadReports:
    """
    下载报告接口
    """

    def request_report(self, rp_client, params):
        resp = []
        try:
            resp_xml = rp_client.request_report(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.info('RequestReport Error: %s', e)
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
            log.info('GetReportRequestList Error: %s', e)
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
            log.info('GetReport Error: %s', e)
        return resp

    # --Start-- 数据库操作
    def select_feedback_orderid(self):
        session = reports.DBSession()
        try:
            order_ids = session.query(reports.AprNegativeFeedback,
                                      reports.AprNegativeFeedback.FeedbackDate,
                                      reports.AprNegativeFeedback.AmazonOrderId).all()
            return order_ids
        except Exception as e:
            log.error('SelectFeedbackError: %s' % e)
        finally:
            session.close()

    def select_order_for_id(self, order_id):
        session = orders.DBSession()
        try:
            od_info = session.query(orders.AprOrder, orders.AprOrder.BuyerName,
                                    orders.AprOrder.BuyerEmail, orders.AprOrder.PurchaseDate) \
                             .filter(orders.AprOrder.AmazonOrderId == order_id).one()
            return od_info
        except Exception as e:
            log.error('SelectOrderError: %s, OrderId: %s' % (e, order_id))
        finally:
            session.close()

    def update_feedback_rating(self, order_id):
        session = reports.DBSession()
        try:
            session.query(reports.AprNegativeFeedback).filter(reports.AprNegativeFeedback.AmazonOrderId == order_id) \
                                                      .update({'RatingEnd': 0})
            session.commit()
        except Exception as e:
            log.error('UpdateFeedbackError: %s' % e)
        finally:
            session.close()

    def add_report_to_sql(self, tb_name, country, report_json, snap_date=None):
        execute_sql = 'reports.{}'.format(tb_name)
        session = reports.DBSession()
        for report in report_json:
            if tb_name == 'AprNegativeFeedback':    # feedback添加订单信息
                od_id = report.get('Order ID')
                od_info = self.select_order_for_id(od_id)
                if od_info:
                    report['BuyerName'] = od_info[1]
                    report['BuyerEmail'] = od_info[2]
                    report['PurchaseDate'] = od_info[3]
            if snap_date:
                report_to_sql = eval(execute_sql)(snap_date, country, report)
            else:
                report_to_sql = eval(execute_sql)(country, report)
            session.add(report_to_sql)
        session.commit()
    # --End-- 数据库操作

    def get_feedback_orderid(self, feedback):
        order_ids = []
        for feed in feedback:
            order_id = feed.get('Order ID')
            order_ids.append(order_id)
        return order_ids

    def get_report_id(self, rp_client, rpq_id):
        while True:
            time.sleep(20)                  # 等待报告生成成功
            rpq_resp = self.get_report_requests(rp_client, rpq_id)
            rpq_list = rpq_resp.get('GetReportRequestListResponse')
            if rpq_list:
                rpq_status = rpq_list.get('GetReportRequestListResult') \
                                     .get('ReportRequestInfo') \
                                     .get('ReportProcessingStatus')
                log.info('ReportStatus: %s', rpq_status)
                if rpq_status == '_DONE_':
                    rp_id = rpq_list.get('GetReportRequestListResult') \
                                    .get('ReportRequestInfo') \
                                    .get('GeneratedReportId')
                    return rp_id
                if rpq_status == '_CANCELLED_':
                    log.info('Report is cancelled，please wait 30 minute.')
                    return False
                if rpq_status == '_DONE_NO_DATA_':
                    return rpq_status
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
                if rp_id == '_DONE_NO_DATA_':
                    return
                rp = self.get_report(rp_client, rp_id)

                tb_name = params.get('table_name')
                log.info('Report fba_return bak')
                rp_return_name = '/home/develop/Mws_reports/{f_path}/{f_name}.json'.format(
                                 f_path=tb_name,
                                 f_name=str(params.get('StartDate')).split(' ')[0])
                with open(rp_return_name, 'w', encoding='utf-8') as f:
                    f.write(str(rp))

                log.info('Report add to sql...')
                mkp = params.get('mkp')

                rp_date = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                try:
                    if tb_name in ['AprFBAAllOrders', 'AprFBAShipments', 'AprFBAInventoryAge',
                                   'AprFBAInventoryHealth', 'AprFBAInventoryAge', 'AprFBALongFee']:
                        self.add_report_to_sql(tb_name, mkp.upper(), rp)
                    else:
                        self.add_report_to_sql(tb_name, mkp.upper(), rp, rp_date)
                    # 确认feedback数据有无被删除
                    if tb_name == 'AprNegativeFeedback':
                        feedback_od = self.select_feedback_orderid()
                        for fod in feedback_od:
                            feed_date = fod[1]
                            order_id = fod[2]
                            if (str(feed_date).split('-')[0] == datetime.datetime.now().year) \
                                               and (order_id not in self.get_feedback_orderid(rp)):
                                self.update_feedback_rating(order_id)
                except Exception as e:
                    log.info('AddSqlError: %s', e)
                log.info('Report add success!')
                return
            time.sleep(1800)      # 请求报告取消状态时，每30分钟一次



def download_report_start(rp_type, mkp):
    time_fmt = '%Y-%m-%d %H:%M:%S'
    log.info('Download report starting...')

    delay_day = 1
    if rp_type == '_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_':
        delay_day = 2
    if rp_type == '_GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA_':
        delay_day = 15
    if rp_type == '_GET_SELLER_FEEDBACK_DATA_':
        delay_day = 360
    report_date = datetime.datetime.now()
    report_date -= datetime.timedelta(days=delay_day)
    start_date = datetime.datetime.strptime(report_date.strftime('%Y-%m-%d 00:00:00'), time_fmt)
    end_date = datetime.datetime.strptime(report_date.strftime('%Y-%m-%d 23:59:59'), time_fmt)
    # FBA长期仓储费每月16号下载一次
    if rp_type == '_GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA_':
        if datetime.datetime.now().date().day != 16:
            return
        else:
            end_date = datetime.datetime.now()
    # Feedback 每日查看历史数据有无删除
    if rp_type == '_GET_SELLER_FEEDBACK_DATA_':
        end_date = datetime.datetime.now()
    params = {
        "StartDate": common.dsttime_to_localtime(start_date),
        "EndDate": common.dsttime_to_localtime(end_date),
        "ReportType": rp_type,
        "table_name": mws_config.report_type.get(rp_type)
    }
    report_client = common.get_client(Reports, mkp)
    params['mkp'] = mkp
    log.info('ReportDate: %s', str(start_date) + ' - ' + str(end_date))
    log.info(params)
    log.info('ReportType: %s', rp_type)
    log.info('Marketplace: %s', mkp.upper())
    dw_report = DownloadReports()
    dw_report.download_run(report_client, params)

    log.info('Download report end!')


if __name__ == '__main__':

    dw_report_type = ['_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_',
                      '_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_',
                      '_GET_FBA_INVENTORY_AGED_DATA_',
                      '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_',
                      '_GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA_',
                      '_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_',
                      '_GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA_',
                      '_GET_SELLER_FEEDBACK_DATA_']

    for rp_type in dw_report_type:
        download_report_start(rp_type, 'us')

        time.sleep(60)  # 报告请求每分钟一次




    # 添加数据库异常时，可直接从备份文件添加到数据库
    # with open('/home/develop/Mws_reports/AprFBAShipments/2019-08-28.json', 'r', encoding='utf-8') as f:
    #     rp = eval(f.read())
    #     dw = DownloadReports()
    #     dw.add_report_to_sql('AprFBAShipments', 'US', rp)


