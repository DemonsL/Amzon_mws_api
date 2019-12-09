# coding: utf-8
import sys
sys.path.append('../')
import logging
import datetime
from Common import common
from Models import products
from MwsApi.products import Products


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/mws_products/static/{}.log'.format(datetime.date.today())
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

class DownloadProducts:

    def list_matching_products(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.list_matching_products(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('ListProductError: %s', e)
        return resp

    def get_product_for_asins(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.get_matching_product(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetProductError: %s', e)
        return resp

    def get_competitive_pricing_for_asins(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.get_competitive_pricing_for_asin(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetCompetitivePriceError: %s', e)
        return resp

    def get_lowest_offer_listings_for_asin(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.get_lowest_offer_listings_for_asin(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetLowestOfferListingsForASIN: %s', e)
        return resp

    def get_lowest_priced_offers_for_asin(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.get_lowest_priced_offers_for_asin(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetLowestPricedOffersForASIN: %s', e)
        return resp

    def get_myprice_for_asins(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.get_my_price_for_asin(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetMyPriceError: %s', e)
        return resp

    def get_product_categories_for_asin(self, pd_client, params):
        resp = []
        try:
            resp_xml = pd_client.get_product_categories_for_asin(params)
            resp = common.xml_to_json(resp_xml.text)
        except Exception as e:
            log.error('GetProductCategoriesError: %s', e)
        return resp


    # --------------数据库方法---------------
    # 从best_seller中获取asin
    def get_top_asins(self):
        session = products.DBSession()
        try:
            asin_list = session.query(products.ApbBestSeller,
                                      products.ApbBestSeller.Country,
                                      products.ApbBestSeller.Asin).distinct().all()
            return ((a[1], a[2]) for a in asin_list)
        except Exception as e:
            log.error('GetAsinsError: %s' % e)
        finally:
            session.close()

    def get_pub_all_asin(self):
        session = products.DBSession()
        try:
            all_asin = session.query(products.PubAllAsin, products.PubAllAsin.Country, products.PubAllAsin.Asin).all()
            return [(a[1], a[2]) for a in all_asin]
        except Exception as e:
            log.error('GetPubAllAsinError: %s' % e)
        finally:
            session.close()

    # 获取自行导入的asin
    def get_pub_all_asin_new(self):
        session = products.DBSession()
        try:
            asin_new = session.query(products.PubAllAsin, products.PubAllAsin.Country, products.PubAllAsin.Asin).filter_by(Brand='').all()
            return [(a[1], a[2]) for a in asin_new]
        except Exception as e:
            log.error('GetPubAllAsinNewError: %s' % e)
        finally:
            session.close()

    def add_pub_all_asin(self, country, p_asin, p_info):
        session = products.DBSession()
        try:
            session.add(products.PubAllAsin(country, p_asin, p_info))
            session.commit()
        except Exception as e:
            log.error('AddPubAllAsinError: %s, Asin: %s' % (e, p_asin))
            log.info(p_info)
        finally:
            session.close()

    def update_pub_all_asin(self, country, p_asin, p_info):
        session = products.DBSession()
        try:
            p = products.PubAllAsin(country, p_asin, p_info).to_dict()
            session.query(products.PubAllAsin).filter_by(Country=p.pop('Country'), Asin=p.pop('Asin')).update(p)
            session.commit()
        except Exception as e:
            log.error('UpdatePubAllAsinError: %s' % e)
        finally:
            session.close()



def download_start(client, p_asin):
    param = {
        'ASINList': p_asin
    }
    p_resp = dp.get_product_for_asins(client, param)
    try:
        pd_re = p_resp.get('GetMatchingProductResponse').get('GetMatchingProductResult')\
                      .get('Product').get('AttributeSets').get('ns2:ItemAttributes')
        # 文件备份
        file_pwd = '/home/develop/Mws_reports/DwProductStatic/' + str(datetime.datetime.today().date()) + '.txt'
        with open(file_pwd, 'a', encoding='utf-8') as f:
            f.write(str(p_resp) + '\n')
        return pd_re
    except Exception as e:
        log.error('FindPageError, Asin: %s' % p_asin)



if __name__ == '__main__':

    dp = DownloadProducts()
    client = common.get_client(Products, 'us')
    top_asins = dp.get_top_asins()
    new_asins = dp.get_pub_all_asin_new()
    all_asins = dp.get_pub_all_asin()

    log.info('Start download product info...')
    # best_seller中asin作为参数
    for asin in top_asins:
        if asin not in all_asins:
            pd_info = download_start(client, asin[1])
            dp.add_pub_all_asin(asin[0], asin[1], pd_info)
    # 自行导入asin作为参数
    for asin in new_asins:
        pd_info = download_start(client, asin[1])
        dp.update_pub_all_asin(asin[0], asin[1], pd_info)
    log.info('End download product info!')