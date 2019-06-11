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
class BkAmzOrder(Base):

    __tablename__ = 'Apr_Order'

    AmazonOrderId = Column(String(20), primary_key=True)
    BuyerEmail = Column(String(50))
    BuyerName = Column(String(50))
    EarliestShipDate = Column(DateTime)
    FulfillmentChannel = Column(String(10))
    IsBusinessOrder = Column(String(10))
    IsPremiumOrder = Column(String(10))
    IsPrime = Column(String(10))
    IsReplacementOrder = Column(String(10))
    LastUpdateDate = Column(DateTime)
    LatestShipDate = Column(DateTime)
    MarketplaceId = Column(String(40))
    NumberOfItemsShipped = Column(Integer)
    NumberOfItemsUnshipped = Column(Integer)
    OrderStatus = Column(String(20))
    OrderAmount = Column(Float(10,2))
    OrderCurrencyCode = Column(String(15))
    OrderType = Column(String(20))
    PaymentMethod = Column(String(20))
    PaymentMethodDetail = Column(String(20))
    PurchaseDate = Column(DateTime)
    SalesChannel = Column(String(30))
    ShipServiceLevel = Column(String(20))
    SellerOrderId = Column(String(30))
    ShipmentServiceLevelCategory = Column(String(20))
    CountryCode = Column(String(20))
    ShippingStateOrRegion = Column(String(30))
    City = Column(String(40))
    PostalCode = Column(String(25))
    AddressLine_1 = Column(String(200))
    AddressLine_2 = Column(String(200))
    AddressLine_3 = Column(String(200))
    AddresseeName = Column(String(200))
    EmailMark = Column(String(10))

    def __init__(self, json_order):
        self.AmazonOrderId = json_order.get('AmazonOrderId')
        self.BuyerEmail = json_order.get('BuyerEmail')
        self.BuyerName = json_order.get('BuyerName')
        self.EarliestShipDate = common.utctime_to_dsttime(json_order.get('EarliestShipDate'))
        self.FulfillmentChannel = json_order.get('FulfillmentChannel')
        self.IsBusinessOrder = json_order.get('IsBusinessOrder')
        self.IsPremiumOrder = json_order.get('IsPremiumOrder')
        self.IsPrime = json_order.get('IsPrime')
        self.IsReplacementOrder = json_order.get('IsReplacementOrder')
        self.LastUpdateDate = common.utctime_to_dsttime(json_order.get('LastUpdateDate'))
        self.LatestShipDate = common.utctime_to_dsttime(json_order.get('LatestShipDate'))
        self.MarketplaceId = json_order.get('MarketplaceId')
        self.NumberOfItemsShipped = json_order.get('NumberOfItemsShipped')
        self.NumberOfItemsUnshipped = json_order.get('NumberOfItemsUnshipped')
        self.OrderStatus = json_order.get('OrderStatus')
        self.OrderAmount = common.is_value('OrderTotal_Amount', json_order, 0)
        self.OrderCurrencyCode = common.is_value('OrderTotal_CurrencyCode', json_order, '')
        self.OrderType = json_order.get('OrderType')
        self.PaymentMethod = json_order.get('PaymentMethod')
        self.PaymentMethodDetail = json_order.get('PaymentMethodDetails').get('PaymentMethodDetail')
        self.PurchaseDate = common.utctime_to_dsttime(json_order.get('PurchaseDate'))
        self.SalesChannel = json_order.get('SalesChannel')
        self.ShipServiceLevel = json_order.get('ShipServiceLevel')
        self.SellerOrderId = json_order.get('SellerOrderId')
        self.ShipmentServiceLevelCategory = json_order.get('ShipmentServiceLevelCategory')
        self.CountryCode = common.is_value('ShippingAddress_CountryCode', json_order, '')
        self.ShippingStateOrRegion = common.is_value('ShippingAddress_StateOrRegion', json_order, '')
        self.City = common.is_value('ShippingAddress_City', json_order, '')
        self.PostalCode = common.is_value('ShippingAddress_PostalCode', json_order, '')
        self.AddressLine_1 = common.is_value('ShippingAddress_AddressLine1', json_order, '')
        self.AddressLine_2 = common.is_value('ShippingAddress_AddressLine2', json_order, '')
        self.AddressLine_3 = common.is_value('ShippingAddress_AddressLine3', json_order, '')
        self.AddresseeName = common.is_value('ShippingAddress_Name', json_order, '')



class BkAmzOrderItem(Base):

    __tablename__ = 'Apr_Order_Item'

    OrderItemId = Column(String(40), primary_key=True)
    ASIN = Column(String(40))
    SellerSKU = Column(String(40))
    Title = Column(String(300))
    NumberOfItems = Column(Integer)
    AmazonOrderId = Column(String(20))
    QuantityOrdered = Column(Integer)
    QuantityShipped = Column(Integer)
    IsGift = Column(String(5))
    ItemPrice_Amount = Column(Float(10,2))
    ItemPrice_CurrencyCode = Column(String(10))
    ItemTax_Amount = Column(Float(10))
    ItemTax_CurrencyCode = Column(String(10))
    PromotionDiscount_Amount = Column(Float(10,2))
    PromotionDiscount_CurrencyCode = Column(String(10))
    ShippingPrice_Amount = Column(Float(10,2))
    ShippingPrice_CurrencyCode = Column(String(10))
    ShippingTax_Amount = Column(Float(10,2))
    ShippingTax_CurrencyCode = Column(String(10))
    ShippingDiscount_Amount = Column(Float(10,2))
    ShippingDiscount_CurrencyCode = Column(String(10))
    PurchaseDate = Column(DateTime)

    def __init__(self, order_id, order_time, json_order_item):
        self.OrderItemId = json_order_item.get('OrderItemId')
        self.ASIN = json_order_item.get('ASIN')
        self.SellerSKU = json_order_item.get('SellerSKU')
        self.Title = json_order_item.get('Title')
        self.NumberOfItems = json_order_item.get('ProductInfo').get('NumberOfItems')
        self.AmazonOrderId = order_id
        self.QuantityOrdered = json_order_item.get('QuantityOrdered')
        self.QuantityShipped = json_order_item.get('QuantityShipped')
        self.IsGift = json_order_item.get('IsGift')
        self.ItemPrice_Amount = json_order_item.get('ItemPrice').get('Amount')
        self.ItemPrice_CurrencyCode = json_order_item.get('ItemPrice').get('CurrencyCode')
        self.ItemTax_Amount = json_order_item.get('ItemTax').get('Amount')
        self.ItemTax_CurrencyCode = json_order_item.get('ItemTax').get('CurrencyCode')
        self.PromotionDiscount_Amount = json_order_item.get('PromotionDiscount').get('Amount')
        self.PromotionDiscount_CurrencyCode = json_order_item.get('PromotionDiscount').get('CurrencyCode')
        self.ShippingPrice_Amount = common.is_value('ShippingPrice_Amount', json_order_item, 0)
        self.ShippingPrice_CurrencyCode = common.is_value('ShippingPrice_CurrencyCode', json_order_item, '')
        self.ShippingTax_Amount = common.is_value('ShippingTax_Amount', json_order_item, 0)
        self.ShippingTax_CurrencyCode = common.is_value('ShippingTax_CurrencyCode', json_order_item, '')
        self.ShippingDiscount_Amount = common.is_value('ShippingDiscount_Amount', json_order_item, 0)
        self.ShippingDiscount_CurrencyCode = common.is_value('ShippingDiscount_CurrencyCode', json_order_item, '')
        self.PurchaseDate = order_time





def update_order(json_order):
    update_field = {
        'BuyerEmail' : json_order.get('BuyerEmail'),
        'BuyerName' : json_order.get('BuyerName'),
        'EarliestShipDate' : common.utctime_to_dsttime(json_order.get('EarliestShipDate')),
        'FulfillmentChannel' : json_order.get('FulfillmentChannel'),
        'IsBusinessOrder' : json_order.get('IsBusinessOrder'),
        'IsPremiumOrder' : json_order.get('IsPremiumOrder'),
        'IsPrime' : json_order.get('IsPrime'),
        'IsReplacementOrder' : json_order.get('IsReplacementOrder'),
        'LastUpdateDate' : common.utctime_to_dsttime(json_order.get('LastUpdateDate')),
        'LatestShipDate' : common.utctime_to_dsttime(json_order.get('LatestShipDate')),
        'MarketplaceId' : json_order.get('MarketplaceId'),
        'NumberOfItemsShipped' : json_order.get('NumberOfItemsShipped'),
        'NumberOfItemsUnshipped' : json_order.get('NumberOfItemsUnshipped'),
        'OrderStatus' : json_order.get('OrderStatus'),
        'OrderAmount' : common.is_value('OrderTotal_Amount', json_order, 0),
        'OrderCurrencyCode' : common.is_value('OrderTotal_CurrencyCode', json_order, ''),
        'OrderType' : json_order.get('OrderType'),
        'PaymentMethod' : json_order.get('PaymentMethod'),
        'PaymentMethodDetail' : json_order.get('PaymentMethodDetails').get('PaymentMethodDetail'),
        'PurchaseDate' : common.utctime_to_dsttime(json_order.get('PurchaseDate')),
        'SalesChannel' : json_order.get('SalesChannel'),
        'ShipServiceLevel' : json_order.get('ShipServiceLevel'),
        'SellerOrderId' : json_order.get('SellerOrderId'),
        'ShipmentServiceLevelCategory' : json_order.get('ShipmentServiceLevelCategory'),
        'CountryCode' : common.is_value('ShippingAddress_CountryCode', json_order, ''),
        'ShippingStateOrRegion' : common.is_value('ShippingAddress_StateOrRegion', json_order, ''),
        'City' : common.is_value('ShippingAddress_City', json_order, ''),
        'PostalCode' : common.is_value('ShippingAddress_PostalCode', json_order, ''),
        'AddressLine_1' : common.is_value('ShippingAddress_AddressLine1', json_order, ''),
        'AddressLine_2' : common.is_value('ShippingAddress_AddressLine2', json_order, ''),
        'AddressLine_3' : common.is_value('ShippingAddress_AddressLine3', json_order, ''),
        'AddresseeName' : common.is_value('ShippingAddress_Name', json_order, '')
    }
    return update_field

def update_order_item(json_order_item):
    update_field = {
        'ASIN' : json_order_item.get('ASIN'),
        'SellerSKU' : json_order_item.get('SellerSKU'),
        'Title' : json_order_item.get('Title'),
        'NumberOfItems' : json_order_item.get('ProductInfo').get('NumberOfItems'),
        'QuantityOrdered' : json_order_item.get('QuantityOrdered'),
        'QuantityShipped' : json_order_item.get('QuantityShipped'),
        'IsGift' : json_order_item.get('IsGift'),
        'ItemPrice_Amount' : json_order_item.get('ItemPrice').get('Amount'),
        'ItemPrice_CurrencyCode' : json_order_item.get('ItemPrice').get('CurrencyCode'),
        'ItemTax_Amount' : json_order_item.get('ItemTax').get('Amount'),
        'ItemTax_CurrencyCode' : json_order_item.get('ItemTax').get('CurrencyCode'),
        'PromotionDiscount_Amount' : json_order_item.get('PromotionDiscount').get('Amount'),
        'PromotionDiscount_CurrencyCode' : json_order_item.get('PromotionDiscount').get('CurrencyCode'),
        'ShippingPrice_Amount' : common.is_value('ShippingPrice_Amount', json_order_item, 0),
        'ShippingPrice_CurrencyCode' : common.is_value('ShippingPrice_CurrencyCode', json_order_item, ''),
        'ShippingTax_Amount' : common.is_value('ShippingTax_Amount', json_order_item, 0),
        'ShippingTax_CurrencyCode' : common.is_value('ShippingTax_CurrencyCode', json_order_item, ''),
        'ShippingDiscount_Amount' : common.is_value('ShippingDiscount_Amount', json_order_item, 0),
        'ShippingDiscount_CurrencyCode' : common.is_value('ShippingDiscount_CurrencyCode', json_order_item, '')
    }
    return update_field