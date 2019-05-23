# coding: utf-8
import sys
sys.path.append('../')
import time
import datetime
from Models import reports
from Timers.download_reports import DownloadReports


class DownloadFbaInventory(DownloadReports):

    def add_report_to_sql(self, snap_date, country, report_json):
        session = reports.DBSession()
        for report in report_json:
            report_to_sql = reports.AprFBAMangeInventory(snap_date, country, report)
            session.add(report_to_sql)
        session.commit()

    def get_report_id(self, rp_client, rpq_id):
        while True:
            time.sleep(20)                  # 等待报告生成成功
            rpq_resp = self.get_report_requests(rp_client, rpq_id)
            print(rpq_resp)
            rpq_list = rpq_resp.get('GetReportRequestListResponse')
            if rpq_list:
                rpq_status = rpq_list.get('GetReportRequestListResult') \
                                     .get('ReportRequestInfo') \
                                     .get('ReportProcessingStatus')
                if rpq_status == '_DONE_':
                    rp_id = rpq_list.get('GetReportRequestListResult') \
                                    .get('ReportRequestInfo') \
                                    .get('GeneratedReportId')
                    return rp_id
            time.sleep(25)              # 请求报告列表每45秒一次

    def download_run(self, rp_client, params):
        reports = self.request_report(rp_client, params)
        rpq_id = reports.get('RequestReportResponse') \
                        .get('RequestReportResult') \
                        .get('ReportRequestInfo') \
                        .get('ReportRequestId')
        rp_id = self.get_report_id(rp_client, rpq_id)
        rp = self.get_report(rp_client, rp_id)

        rp_date = datetime.datetime.strptime(params.get('StartDate').strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.add_report_to_sql(rp_date, 'US', rp)


if __name__ == '__main__':

    day = 2
    while day <= 92:
        report_date = datetime.datetime.now()
        report_date -= datetime.timedelta(days=day)
        params = {
            "StartDate": report_date,
            "ReportType": "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_"#_GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA_"#
        }
        fba_inventory = DownloadFbaInventory()
        report_client = fba_inventory.get_reports_client()
        fba_inventory.download_run(report_client, params)

        time.sleep(60)    # 报告请求每分钟一个
        day += 1


