# coding: utf-8
import os, sys
sys.path.append('../')
import logging
import datetime
from Common import common
from Models import products
from MwsApi.products import Products
from sqlalchemy import desc, and_


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/mws_products/{}.log'.format(datetime.date.today())
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

    # 数据库操作
    def add_product_to_sql(self, tb_name, country, snap_date, json_product):
        db_table = 'products.{}'.format(tb_name)
        session = products.DBSession()
        session.add(eval(db_table)(country, snap_date, json_product))
        session.commit()
        session.close()

    def get_asins(self):
        session = products.DBSession()
        asins = session.query(products.PubAsin, products.PubAsin.Asin).all()
        asins = [asin[1] for asin in asins]
        session.close()
        return asins

    def get_rank_date(self, asin):
        session = products.DBSession()
        field_name = products.AprAsinRank.SnapDate
        try:
            last_date = session.query(products.AprAsinRank, field_name).filter_by(Asin=asin) \
                                                                       .order_by(desc(field_name)) \
                                                                       .limit(1).one()
            return last_date[1]
        except Exception as e:
            log.info('GetRankDate: %s' % e)
            return ''
        finally:
            session.close()


    def add_ranks(self, country, snap_date, p_asin, json_rank):
        session = products.DBSession()
        for rank in json_rank:
            session.add(products.AprAsinRank(country, snap_date, p_asin, rank))
        session.commit()
        session.close()

    def update_rank(self, country, snap_date, p_asin, json_rank):
        session = products.DBSession()
        for rank in json_rank:
            p_id = rank.get('ProductCategoryId')
            p_rank = rank.get('Rank')
            session.query(products.AprAsinRank).filter(and_(and_(and_(
                                                        products.AprAsinRank.Country == country,
                                                        products.AprAsinRank.SnapDate == snap_date.split(' ')[0]),
                                                        products.AprAsinRank.Asin == p_asin),
                                                        products.AprAsinRank.CategoryId == p_id)) \
                                               .update({'Rank': p_rank,
                                                        'LastUpdate': snap_date})
        session.commit()
        session.close()





if __name__ == '__main__':

    now = datetime.datetime.now()
    us_time = common.iso_time_to_dsttime(str(now))
    us_date = us_time.split(' ')[0]
    pd_client = common.get_client(Products, 'us')

    dw_products = DownloadProducts()
    p_asins = dw_products.get_asins()
    log.info('Start download asin_rank... | Asins: %s' % len(p_asins))
    for asin in p_asins:
        params = {
            'ASINList': asin
        }
        pd_resp = dw_products.get_competitive_pricing_for_asins(pd_client, params)
        # 备份文件
        bak_file_name = '/home/develop/Mws_reports/{f_path}/{f_name}.json'.format(
                        f_path='GetCompetitivePricingForASIN',
                        f_name=us_date + '_' + asin)
        if not os.path.exists(bak_file_name):
            with open(bak_file_name, 'w', encoding='utf-8') as f:
                f.write(str(pd_resp))
            log.info('Baking today asin_rank file...')
        # 数据入库
        ranks = pd_resp.get('GetCompetitivePricingForASINResponse') \
                           .get('GetCompetitivePricingForASINResult') \
                           .get('Product').get('SalesRankings').get('SalesRank')
        list_rank = []
        if not isinstance(ranks, list):
            list_rank.append(ranks)
        else:
            list_rank = ranks
        last_rank_date = dw_products.get_rank_date(asin)
        if us_date != str(last_rank_date):
            log.info('Add asin_rank: %s to sql...' % asin)
            dw_products.add_ranks('US', us_time, asin, list_rank)
        else:
            log.info('Update asin_rank: %s to sql...' % asin)
            dw_products.update_rank('US', us_time, asin, list_rank)
    log.info('End download asin_rank!')


