# coding: utf-8
from Config import db
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)


Base = declarative_base()
class AprFBAMangeInventory(Base):

    __tablename__ = 'Apr_FBA_Manage_Inventory'

    ID = Column(Integer)
    SnapDate = Column(DateTime)
    Country = Column(String(10))
    Sku = Column(String(50))
    FnSku = Column(String(20))
    Asin = Column(String(20))
    ProductName = Column(String(300))
    Condition = Column(String(20))
    Price = Column(Float(6,2))
    PerUnitVolume = Column(Float(10,2))
    AfnTotal = Column(Integer)
    MfnListingExists = Column(String(10))
    MfnFulfillable = Column(Integer)
    AfnListingExists = Column(String(10))
    AfnWarehouse = Column(Integer)
    AfnFulfillable = Column(Integer)
    AfnUnsellable = Column(Integer)
    AfnReserved = Column(Integer)
    AfnInboundWorking = Column(Integer)
    AfnInboundShipped = Column(Integer)
    AfnInboundReceiving = Column(Integer)

    def __init__(self, SnapDate, Country, json_report):
        self.SnapDate = SnapDate
        self.Country = Country
        self.Sku = json_report.get('sku')
        self.FnSku = json_report.get('fnsku')
        self.Asin = json_report.get('asin')
        self.ProductName = json_report.get('product-name')
        self.Condition = json_report.get('condition')
        self.Price = json_report.get('your-price')
        self.PerUnitVolume = json_report.get('per-unit-volume')
        self.AfnTotal = json_report.get('afn-total-quantity')
        self.MfnListingExists = json_report.get('mfn-listing-exists')
        self.MfnFulfillable = json_report.get('mfn-fulfillable-quantity')
        self.AfnListingExists = json_report.get('afn-listing-exists')
        self.AfnWarehouse = json_report.get('afn-warehouse-quantity')
        self.AfnFulfillable = json_report.get('afn-fulfillable-quantity')
        self.AfnUnsellable = json_report.get('afn-unsellable-quantity')
        self.AfnReserved = json_report.get('afn-reserved-quantity')
        self.AfnInboundWorking = json_report.get('afn-inbound-working-quantity')
        self.AfnInboundShipped = json_report.get('afn-inbound-shipped-quantity')
        self.AfnInboundReceiving = json_report.get('afn-inbound-receiving-quantity')


class AprFBAAllOrders(Base):

    __tablename__ = 'Apr_FBA_All_Orders'

    ID = Column(Integer)
    Country = Column(String(10))
    AmazonOrderId = Column(String(20))
    MerchantOrderId = Column(String(20))
    Sku = Column(String(50))
    Asin = Column(String(20))
    OrderDate = Column(DateTime)
    LastUpdateDate = Column(DateTime)
    OrderStatus = Column(String(20))
    SaleChannel = Column(String(50))
    FulfillmentChannel = Column(String(20))
    FulfillmentLevel = Column(String(40))
    ProductName = Column(String(300))
    ShipStatus = Column(String(20))
    Quantity = Column(Integer)
    Currency = Column(String(10))
    Price = Column(Float(6,2))
    Tax = Column(Float(6,2))
    ShippingPrice = Column(Float(6,2))
    ShippingTax = Column(Float(6,2))
    GiftWrapPrice = Column(Float(6,2))
    GiftWrapTax = Column(Float(6,2))
    Promotion = Column(Float(6,2))
    ShippingPromotion = Column(Float(6,2))
    ShipPostalCode = Column(String(20))
    ShipCountry = Column(String(10))
    ShipState = Column(String(20))
    ShipCity = Column(String(40))
    PromotionIds = Column(String(200))

    def __init__(self, Country, json_report):
        self.Country = Country
        self.AmazonOrderId = json_report.get('amazon-order-id')
        self.MerchantOrderId = json_report.get('merchant-order-id')
        self.Sku = json_report.get('sku')
        self.Asin = json_report.get('asin')
        self.OrderDate = json_report.get('purchase-date')
        self.LastUpdateDate = json_report.get('last-updated-date')
        self.OrderStatus = json_report.get('order-status')
        self.SaleChannel = json_report.get('sales-channel')
        self.FulfillmentChannel = json_report.get('fulfillment-channel')
        self.FulfillmentLevel = json_report.get('ship-service-level')
        self.ProductName = json_report.get('product-name')
        self.ShipStatus = json_report.get('item-status')
        self.Quantity = json_report.get('quantity')
        self.Currency = json_report.get('currency')
        self.Price = json_report.get('item-price')
        self.Tax = json_report.get('item-tax')
        self.ShippingPrice = json_report.get('shipping-price')
        self.ShippingTax = json_report.get('shipping-tax')
        self.GiftWrapPrice = json_report.get('gift-wrap-price')
        self.GiftWrapTax = json_report.get('gift-wrap-tax')
        self.Promotion = json_report.get('item-promotion-discount')
        self.ShippingPromotion = json_report.get('ship-promotion-discount')
        self.ShipPostalCode = json_report.get('ship-postal-code')
        self.ShipCountry = json_report.get('ship-country')
        self.ShipState = json_report.get('ship-state')
        self.ShipCity = json_report.get('ship-city')
        self.PromotionIds = json_report.get('promotion-ids')





