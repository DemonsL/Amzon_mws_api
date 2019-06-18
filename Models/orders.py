# coding: utf-8
from Config import db
from Common import common
from sqlalchemy import Column, String, Integer, Float, DECIMAL, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)


Base = declarative_base()
class AprOrder(Base):

    __tablename__ = 'Apr_Order'

    AmazonOrderId = Column(String(20), primary_key=True)
    BuyerEmail = Column(String(50))
    BuyerName = Column(String(50))
    PurchaseDate = Column(DateTime)
    Status = Column(String(20))
    UnitsShipped = Column(Integer)
    UnitsUnshipped = Column(Integer)
    Revenue = Column(Float(10, 2))
    RevenueCurrency = Column(String(10))
    LastUpdateDate = Column(DateTime)
    MarketplaceId = Column(String(20))
    SalesChannel = Column(String(20))
    OrderType = Column(String(20))
    PaymentMethod = Column(String(10))
    PaymentMethodDetail = Column(String(15))
    IsBusiness = Column(String(10))
    IsPremium = Column(String(10))
    IsPrime = Column(String(10))
    IsReplacement = Column(String(10))
    FulfillmentChannel = Column(String(20))
    ShipServiceLevel = Column(String(20))
    AddrCountry = Column(String(10))
    AddrState = Column(String(100))
    AddrCity = Column(String(50))
    AddrPostal = Column(String(15))
    Addr1 = Column(String(200))
    Addr2 = Column(String(200))
    Addr3 = Column(String(200))
    AddrName = Column(String(100))
    EarliestShipDate = Column(DateTime)
    LatestShipDate = Column(DateTime)
    Flag = Column(Integer)
    # SellerOrderId = Column(String(30))
    # ShipmentServiceLevelCategory = Column(String(20))

    def __init__(self, json_order):
        self.AmazonOrderId = json_order.get('AmazonOrderId')
        self.BuyerEmail = json_order.get('BuyerEmail')
        self.BuyerName = json_order.get('BuyerName')
        self.PurchaseDate = common.utctime_to_dsttime(json_order.get('PurchaseDate'))
        self.Status = json_order.get('OrderStatus')
        self.UnitsShipped = json_order.get('NumberOfItemsShipped')
        self.UnitsUnshipped = json_order.get('NumberOfItemsUnshipped')
        self.Revenue = common.is_value('OrderTotal_Amount', json_order, 0)
        self.RevenueCurrency = common.is_value('OrderTotal_CurrencyCode', json_order, '')
        self.LastUpdateDate = common.utctime_to_dsttime(json_order.get('LastUpdateDate'))
        self.MarketplaceId = json_order.get('MarketplaceId')
        self.SalesChannel = json_order.get('SalesChannel')
        self.OrderType = json_order.get('OrderType')
        self.PaymentMethod = json_order.get('PaymentMethod')
        self.PaymentMethodDetail = common.is_value('PaymentMethodDetails_PaymentMethodDetail', json_order, '')
        self.IsBusiness = json_order.get('IsBusinessOrder')
        self.IsPremium = json_order.get('IsPremiumOrder')
        self.IsPrime = json_order.get('IsPrime')
        self.IsReplacement = json_order.get('IsReplacementOrder')
        self.FulfillmentChannel = json_order.get('FulfillmentChannel')
        self.ShipServiceLevel = json_order.get('ShipServiceLevel')
        self.AddrCountry = common.is_value('ShippingAddress_CountryCode', json_order, '')
        self.AddrState = common.is_value('ShippingAddress_StateOrRegion', json_order, '').upper() \
                                if json_order.get('ShippingAddress') else ''
        self.AddrCity = common.is_value('ShippingAddress_City', json_order, '')
        self.AddrPostal = common.is_value('ShippingAddress_PostalCode', json_order, '')
        self.Addr1 = common.is_value('ShippingAddress_AddressLine1', json_order, '')
        self.Addr2 = common.is_value('ShippingAddress_AddressLine2', json_order, '')
        self.Addr3 = common.is_value('ShippingAddress_AddressLine3', json_order, '')
        self.AddrName = common.is_value('ShippingAddress_Name', json_order, '')
        self.EarliestShipDate = common.utctime_to_dsttime(json_order.get('EarliestShipDate'))
        self.LatestShipDate = common.utctime_to_dsttime(json_order.get('LatestShipDate'))
        self.Flag = 0
        # self.SellerOrderId = json_order.get('SellerOrderId')
        # self.ShipmentServiceLevelCategory = json_order.get('ShipmentServiceLevelCategory')


class AprOrderItem(Base):

    __tablename__ = 'Apr_Order_Item'

    OrderItemId = Column(String(20), primary_key=True)
    AmazonOrderId = Column(String(20))
    PurchaseDate = Column(DateTime)
    SKU = Column(String(50))
    ASIN = Column(String(20))
    ProductName = Column(String(300))
    UnitOrdered = Column(Integer)
    UnitShipped = Column(Integer)
    IsGift = Column(String(5))
    Rev = Column(DECIMAL(10,2))
    RevShipping = Column(DECIMAL(10, 2))
    DiscountShipping = Column(DECIMAL(10, 2))
    TaxShipping = Column(DECIMAL(10, 2))
    RevGiftWrap = Column(DECIMAL(10,2))
    TaxGiftWrap = Column(DECIMAL(10,2))
    DiscountPromotion = Column(DECIMAL(10,2))
    Tax = Column(DECIMAL(10,2))
    RevCOD = Column(DECIMAL(10,2))
    DiscountCOD = Column(DECIMAL(10,2))
    CurRev = Column(String(10))
    CurRevShipping = Column(String(10))
    CurDiscountShipping = Column(String(10))
    CurTaxShipping = Column(String(10))
    CurRevGiftWrap = Column(String(10))
    CurTaxGiftWrap = Column(String(10))
    CurDiscountPromotion = Column(String(10))
    CurTax = Column(String(10))
    CurRevCOD = Column(String(10))
    CurDiscountCOD = Column(String(10))
    PromotionIds = Column(String(200))
    GiftText = Column(String(400))

    def __init__(self, order_id, order_time, json_order_item):
        self.OrderItemId = json_order_item.get('OrderItemId')
        self.AmazonOrderId = order_id
        self.PurchaseDate = order_time
        self.SKU = json_order_item.get('SellerSKU')
        self.ASIN = json_order_item.get('ASIN')
        self.ProductName = json_order_item.get('Title')
        self.UnitOrdered = json_order_item.get('QuantityOrdered')
        self.UnitShipped = json_order_item.get('QuantityShipped')
        self.IsGift = json_order_item.get('IsGift')
        self.Rev = common.is_value('ItemPrice_Amount', json_order_item, 0)
        self.RevShipping = common.is_value('ShippingPrice_Amount', json_order_item, 0)
        self.DiscountShipping = common.is_value('ShippingDiscount_Amount', json_order_item, 0)
        self.TaxShipping = common.is_value('ShippingTax_Amount', json_order_item, 0)
        self.RevGiftWrap = common.is_value('GiftWrapPrice_Amount', json_order_item, 0)
        self.TaxGiftWrap = common.is_value('GiftWrapTax_Amount', json_order_item, 0)
        self.DiscountPromotion = common.is_value('PromotionDiscount_Amount', json_order_item, 0)
        self.Tax = common.is_value('ItemTax_Amount', json_order_item, 0)
        self.RevCOD = common.is_value('CODFee_Amount', json_order_item, 0)
        self.DiscountCOD = common.is_value('CODFeeDiscount_Amount', json_order_item, 0)
        self.CurRev = common.is_value('ItemPrice_CurrencyCode', json_order_item, '')
        self.CurRevShipping = common.is_value('ShippingPrice_CurrencyCode', json_order_item, '')
        self.CurDiscountShipping = common.is_value('ShippingDiscount_CurrencyCode', json_order_item, '')
        self.CurTaxShipping = common.is_value('ShippingTax_CurrencyCode', json_order_item, '')
        self.CurRevGiftWrap = common.is_value('GiftWrapPrice_CurrencyCode', json_order_item, '')
        self.CurTaxGiftWrap = common.is_value('GiftWrapTax_CurrencyCode', json_order_item, '')
        self.CurDiscountPromotion = common.is_value('PromotionDiscount_CurrencyCode', json_order_item, '')
        self.CurTax = common.is_value('ItemTax_CurrencyCode', json_order_item, '')
        self.CurRevCOD = common.is_value('CODFee_CurrencyCode', json_order_item, '')
        self.CurDiscountCOD = common.is_value('CODFeeDiscount_CurrencyCode', json_order_item, '')
        self.PromotionIds = str(common.is_value('PromotionIds_PromotionId', json_order_item, ''))
        self.GiftText = json_order_item.get('GiftMessageText')




def update_order(json_order):
    update_field = {
        'BuyerEmail': json_order.get('BuyerEmail'),
        'BuyerName': json_order.get('BuyerName'),
        'PurchaseDate': common.utctime_to_dsttime(json_order.get('PurchaseDate')),
        'Status': json_order.get('OrderStatus'),
        'UnitsShipped': json_order.get('NumberOfItemsShipped'),
        'UnitsUnshipped': json_order.get('NumberOfItemsUnshipped'),
        'Revenue': common.is_value('OrderTotal_Amount', json_order, 0),
        'RevenueCurrency': common.is_value('OrderTotal_CurrencyCode', json_order, ''),
        'LastUpdateDate': common.utctime_to_dsttime(json_order.get('LastUpdateDate')),
        'MarketplaceId': json_order.get('MarketplaceId'),
        'SalesChannel': json_order.get('SalesChannel'),
        'OrderType': json_order.get('OrderType'),
        'PaymentMethod': json_order.get('PaymentMethod'),
        'PaymentMethodDetail': common.is_value('PaymentMethodDetails_PaymentMethodDetail', json_order, ''),
        'IsBusiness': json_order.get('IsBusinessOrder'),
        'IsPremium': json_order.get('IsPremiumOrder'),
        'IsPrime': json_order.get('IsPrime'),
        'IsReplacement': json_order.get('IsReplacementOrder'),
        'FulfillmentChannel': json_order.get('FulfillmentChannel'),
        'ShipServiceLevel': json_order.get('ShipServiceLevel'),
        'AddrCountry': common.is_value('ShippingAddress_CountryCode', json_order, ''),
        'AddrState': common.is_value('ShippingAddress_StateOrRegion', json_order, ''),
        'AddrCity': common.is_value('ShippingAddress_City', json_order, ''),
        'AddrPostal': common.is_value('ShippingAddress_PostalCode', json_order, ''),
        'Addr1': common.is_value('ShippingAddress_AddressLine1', json_order, ''),
        'Addr2': common.is_value('ShippingAddress_AddressLine2', json_order, ''),
        'Addr3': common.is_value('ShippingAddress_AddressLine3', json_order, ''),
        'AddrName': common.is_value('ShippingAddress_Name', json_order, ''),
        'EarliestShipDate': common.utctime_to_dsttime(json_order.get('EarliestShipDate')),
        'LatestShipDate': common.utctime_to_dsttime(json_order.get('LatestShipDate')),
        'Flag': 0
    }
    return update_field

def update_order_item(json_order_item):
    update_field = {
        'SKU': json_order_item.get('SellerSKU'),
        'ASIN': json_order_item.get('ASIN'),
        'ProductName': json_order_item.get('Title'),
        'UnitOrdered': json_order_item.get('QuantityOrdered'),
        'UnitShipped': json_order_item.get('QuantityShipped'),
        'IsGift': json_order_item.get('IsGift'),
        'Rev': common.is_value('ItemPrice_Amount', json_order_item, 0),
        'RevShipping': common.is_value('ShippingPrice_Amount', json_order_item, 0),
        'DiscountShipping': common.is_value('ShippingDiscount_Amount', json_order_item, 0),
        'TaxShipping': common.is_value('ShippingTax_Amount', json_order_item, 0),
        'RevGiftWrap': common.is_value('GiftWrapPrice_Amount', json_order_item, 0),
        'TaxGiftWrap': common.is_value('GiftWrapTax_Amount', json_order_item, 0),
        'DiscountPromotion': common.is_value('PromotionDiscount_Amount', json_order_item, 0),
        'Tax': common.is_value('ItemTax_Amount', json_order_item, 0),
        'RevCOD': common.is_value('CODFee_Amount', json_order_item, 0),
        'DiscountCOD': common.is_value('CODFeeDiscount_Amount', json_order_item, 0),
        'CurRev': common.is_value('ItemPrice_CurrencyCode', json_order_item, ''),
        'CurRevShipping': common.is_value('ShippingPrice_CurrencyCode', json_order_item, ''),
        'CurDiscountShipping': common.is_value('ShippingDiscount_CurrencyCode', json_order_item, ''),
        'CurTaxShipping': common.is_value('ShippingTax_CurrencyCode', json_order_item, ''),
        'CurRevGiftWrap': common.is_value('GiftWrapPrice_CurrencyCode', json_order_item, ''),
        'CurTaxGiftWrap': common.is_value('GiftWrapTax_CurrencyCode', json_order_item, ''),
        'CurDiscountPromotion': common.is_value('PromotionDiscount_CurrencyCode', json_order_item, ''),
        'CurTax': common.is_value('ItemTax_CurrencyCode', json_order_item, ''),
        'CurRevCOD': common.is_value('CODFee_CurrencyCode', json_order_item, ''),
        'CurDiscountCOD': common.is_value('CODFeeDiscount_CurrencyCode', json_order_item, ''),
        'PromotionIds': str(common.is_value('PromotionIds_PromotionId', json_order_item, '')),
        'GiftText': json_order_item.get('GiftMessageText')
    }
    return update_field