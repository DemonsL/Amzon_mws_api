# coding: utf-8
import sys
sys.path.append('../')
import logging
import time
import datetime
from Common import common
from Models import orders
from MwsApi.orders import Orders
from sqlalchemy import desc , and_


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/mws_orders/{}.log'.format(datetime.date.today())
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

class DownloadOrders:

    def list_orders(self, od_client, params):
        resp = []
        try:
            resp_xml = od_client.list_orders(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('ListOrdersError: %s', e)
        return resp

    def list_orders_by_next_token(self, od_client, params):
        resp = []
        try:
            resp_xml = od_client.list_orders_by_next_token(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('ListOrdersByNextTokenError: %s', e)
        return resp

    def get_order(self, od_client, params):
        resp = []
        try:
            resp_xml = od_client.get_order(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetOrderError: %s', e)
        return resp

    def list_order_items(self, od_client, params):
        resp = []
        try:
            resp_xml = od_client.list_order_items(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('ListOrderItemsError: %s', e)
        return resp

    def list_order_items_by_next_token(self, od_client, params):
        resp = []
        try:
            resp_xml = od_client.list_order_items_by_next_token(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('ListOrderItemsByNextTokenError: %s', e)
        return resp

    # 数据库的操作
    def select_last_order_time(self):
        session = orders.DBSession()
        field_name = orders.AprOrder.LastUpdateDate
        last_order_time = session.query(orders.AprOrder, field_name).order_by(desc(field_name)).limit(1).one()
        session.close()
        return last_order_time[1]

    def select_order_ids(self, order_date):
        order_date_from = order_date - datetime.timedelta(days=30)  # 获取前30天订单，判断是否更新
        session = orders.DBSession()
        order_ids = session.query(orders.AprOrder, orders.AprOrder.AmazonOrderId)\
                           .filter(orders.AprOrder.LastUpdateDate>order_date_from).all()
        order_ids = [order_id[1] for order_id in order_ids]
        session.close()
        return order_ids

    def select_order_item_ids(self, order_id):
        session = orders.DBSession()
        item_ids = session.query(orders.AprOrderItem, orders.AprOrderItem.OrderItemId) \
                          .filter_by(AmazonOrderId=order_id).all()
        item_ids = [item_id[1] for item_id in item_ids]
        session.close()
        return item_ids

    def select_order_time(self, order_id):
        session = orders.DBSession()
        order_time = session.query(orders.AprOrder, orders.AprOrder.PurchaseDate) \
                            .filter_by(AmazonOrderId=order_id).one()
        session.close()
        return order_time[1]

    def add_order_to_sql(self, json_order):
        session = orders.DBSession()
        try:
            session.add(orders.AprOrder(json_order))
            session.commit()
        except Exception as e:
            log.error('AddOrderError: %s', e)
        finally:
            session.close()

    def add_order_item(self, order_id, order_time, json_order_item):
        session = orders.DBSession()
        try:
            session.add(orders.AprOrderItem(order_id, order_time, json_order_item)),
            session.commit()
        except Exception as e:
            log.error('AddOrderItemError: %s', e)
        finally:
            session.close()

    def update_order_to_sql(self, order_id, json_order):
        session = orders.DBSession()
        try:
            session.query(orders.AprOrder).filter_by(AmazonOrderId=order_id) \
                                          .update(orders.update_order(json_order))
            session.commit()
        except Exception as e:
            log.error('UpdateOrderError: %s', e)
        finally:
            session.close()

    def update_order_item(self, item_id, json_order_item):
        session = orders.DBSession()
        try:
            session.query(orders.AprOrderItem).filter_by(OrderItemId=item_id) \
                                              .update(orders.update_order_item(json_order_item))
            session.commit()
        except Exception as e:
            log.error('UpdateOrderItemError: %s', e)
        finally:
            session.close()







def order_item_to_sql(dw_meth, order_item, db_order_item, order_id, order_time):
    order_item_id = order_item.get('OrderItemId')
    if order_item_id in db_order_item:
        log.info('Update order item: %s', order_item_id)
        dw_meth.update_order_item(order_item_id, order_item)
    else:
        log.info('Add order item: %s', order_item_id)
        dw_meth.add_order_item(order_id, order_time, order_item)

def order_item_next_token(order_item_resp, dw_meth, db_order_item_ids, order_id, order_time, next=False):
    if not next:
        order_items = order_item_resp.get('ListOrderItemsResponse') \
                                     .get('ListOrderItemsResult') \
                                     .get('OrderItems') \
                                     .get('OrderItem')
        item_next_token = order_item_resp.get('ListOrderItemsResponse') \
                                     .get('ListOrderItemsResult') \
                                     .get('NextToken')
    else:
        order_items = order_item_resp.get('ListOrderItemsByNextTokenResponse ') \
                                     .get('ListOrderItemsByNextTokenResult') \
                                     .get('OrderItems') \
                                     .get('OrderItem')
        item_next_token = order_item_resp.get('ListOrderItemsByNextTokenResponse') \
                                         .get('ListOrderItemsByNextTokenResult') \
                                         .get('NextToken')
    if not isinstance(order_items, list):
        order_item_to_sql(dw_meth, order_items, db_order_item_ids, order_id, order_time)
    else:
        for order_item in order_items:
            order_item_to_sql(dw_meth, order_item, db_order_item_ids, order_id, order_time)
    return item_next_token


def download_order_item_start(order_id, dw_meth):
    order_item_params = {
        'AmazonOrderId': order_id
    }
    order_time = dw_meth.select_order_time(order_id)
    db_order_item_ids = dw_meth.select_order_item_ids(order_id)
    order_item_resp = dw_meth.list_order_items(od_client, order_item_params)

    item_next_token = order_item_next_token(order_item_resp, dw_meth, db_order_item_ids, order_id, order_time)
    while item_next_token:
        item_next_params = {
            'NextToken': item_next_token
        }
        log.info('ItemNextToken: %s', item_next_params)
        item_next_resp = dw_meth.list_order_items_by_next_token(od_client, item_next_params)
        item_next_token = order_item_next_token(item_next_resp, dw_meth, db_order_item_ids, order_id, order_time)
        time.sleep(3)

def order_to_sql(dw_meth, db_order, list_order, order_next_token):
    for order in list_order:
        order_id = order.get('AmazonOrderId')
        if order_id in db_order:
            log.info('Update order: %s', order_id)
            dw_meth.update_order_to_sql(order_id, order)
            time.sleep(3)
            download_order_item_start(order_id, dw_meth)
        else:
            log.info('Add order: %s', order_id)
            dw_meth.add_order_to_sql(order)
            time.sleep(3)
            download_order_item_start(order_id, dw_meth)
    return order_next_token

def download_order_start(dw_meth, order_resp, db_order, next=False):
    if not next:
        list_orders = order_resp.get('ListOrdersResponse').get('ListOrdersResult').get('Orders')
        if list_orders:
            list_order = list_orders.get('Order')
            order_next_token = order_resp.get('ListOrdersResponse').get('ListOrdersResult').get('NextToken', None)
            return order_to_sql(dw_meth, db_order, list_order, order_next_token)
        else:
            log.info('Now is no update orders')
    else:
        list_orders = order_resp.get('ListOrdersByNextTokenResponse').get('ListOrdersByNextTokenResult').get('Orders')
        if list_orders:
            list_order = list_orders.get('Order')
            order_next_token = order_resp.get('ListOrdersByNextTokenResponse').get('ListOrdersByNextTokenResult').get('NextToken', None)
            return order_to_sql(dw_meth, db_order, list_order, order_next_token)
        else:
            log.info('Now is no update orders')




if __name__ == '__main__':

    dw_orders = DownloadOrders()

    last_update = dw_orders.select_last_order_time()
    local_time = common.dsttime_to_utctime(str(last_update))
    order_params = {
        'LastUpdatedAfter': local_time
    }
    db_order_ids = dw_orders.select_order_ids(last_update)

    for mkp in ['us', 'ca']:
        od_client = common.get_client(Orders, mkp)
        log.info('%s, %s', order_params, mkp)

        order_resp = dw_orders.list_orders(od_client, order_params)
        next_token = download_order_start(dw_orders, order_resp, db_order_ids)
        while next_token:
            next_params = {
                'NextToken': next_token
            }
            log.info(next_params)
            next_resp = dw_orders.list_orders_by_next_token(od_client, next_params)
            next_token = download_order_start(dw_orders, next_resp, db_order_ids, True)
            time.sleep(60) # 每分钟请求一次
