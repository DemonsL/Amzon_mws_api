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
class AprFBAMangeInventory(Base):

    __tablename__ = 'Apr_FBA_Manage_Inventory'

    ID = Column(Integer)
    SnapDate = Column(DateTime, primary_key=True)
    Country = Column(String(10), primary_key=True)
    Sku = Column(String(50), primary_key=True)
    FnSku = Column(String(20))
    Asin = Column(String(20))
    ProductName = Column(String(300))
    Condition = Column(String(20))
    Price = Column(DECIMAL(6,2))
    PerUnitVolume = Column(DECIMAL(10,2))
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
        self.Price = json_report.get('your-price') or 0.00
        self.PerUnitVolume = json_report.get('per-unit-volume') or 0.00
        self.AfnTotal = json_report.get('afn-total-quantity') or 0
        self.MfnListingExists = json_report.get('mfn-listing-exists')
        self.MfnFulfillable = json_report.get('mfn-fulfillable-quantity') or 0
        self.AfnListingExists = json_report.get('afn-listing-exists')
        self.AfnWarehouse = json_report.get('afn-warehouse-quantity') or 0
        self.AfnFulfillable = json_report.get('afn-fulfillable-quantity') or 0
        self.AfnUnsellable = json_report.get('afn-unsellable-quantity') or 0
        self.AfnReserved = json_report.get('afn-reserved-quantity') or 0
        self.AfnInboundWorking = json_report.get('afn-inbound-working-quantity') or 0
        self.AfnInboundShipped = json_report.get('afn-inbound-shipped-quantity') or 0
        self.AfnInboundReceiving = json_report.get('afn-inbound-receiving-quantity') or 0


class AprFBAAllOrders(Base):

    __tablename__ = 'Apr_FBA_All_Orders'

    ID = Column(Integer, primary_key=True)
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
    Price = Column(DECIMAL(6,2))
    Tax = Column(DECIMAL(6,2))
    ShippingPrice = Column(DECIMAL(6,2))
    ShippingTax = Column(DECIMAL(6,2))
    GiftWrapPrice = Column(DECIMAL(6,2))
    GiftWrapTax = Column(DECIMAL(6,2))
    Promotion = Column(DECIMAL(6,2))
    ShippingPromotion = Column(DECIMAL(6,2))
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
        self.OrderDate = common.iso_time_to_dsttime(json_report.get('purchase-date'))
        self.LastUpdateDate = common.iso_time_to_dsttime(json_report.get('last-updated-date'))
        self.OrderStatus = json_report.get('order-status')
        self.SaleChannel = json_report.get('sales-channel')
        self.FulfillmentChannel = json_report.get('fulfillment-channel')
        self.FulfillmentLevel = json_report.get('ship-service-level')
        self.ProductName = json_report.get('product-name')
        self.ShipStatus = json_report.get('item-status')
        self.Quantity = json_report.get('quantity')
        self.Currency = json_report.get('currency')
        self.Price = json_report.get('item-price') or 0.00
        self.Tax = json_report.get('item-tax') or 0.00
        self.ShippingPrice = json_report.get('shipping-price') or 0.00
        self.ShippingTax = json_report.get('shipping-tax') or 0.00
        self.GiftWrapPrice = json_report.get('gift-wrap-price') or 0.00
        self.GiftWrapTax = json_report.get('gift-wrap-tax') or 0.00
        self.Promotion = json_report.get('item-promotion-discount') or 0.00
        self.ShippingPromotion = json_report.get('ship-promotion-discount') or 0.00
        self.ShipPostalCode = json_report.get('ship-postal-code')
        self.ShipCountry = json_report.get('ship-country')
        self.ShipState = json_report.get('ship-state')
        self.ShipCity = json_report.get('ship-city')
        self.PromotionIds = json_report.get('promotion-ids')


class AprFBAShipments(Base):

    __tablename__ = 'Apr_FBA_Shipments'

    ID = Column(Integer)
    Country = Column(String(10))
    AmazonOrderId = Column(String(20))
    MerchantOrderID = Column(String(50))
    ShipmentID = Column(String(40))
    ShipmentItemID = Column(String(40), primary_key=True)
    AmazonOrderItemID = Column(String(40))
    MerchantOrderItemID = Column(String(50))
    PurchaseDate = Column(DateTime)
    PaymentsDate = Column(DateTime)
    ShipmentDate = Column(DateTime)
    ReportingDate = Column(DateTime)
    BuyerEmail = Column(String(50))
    BuyerName = Column(String(100))
    BuyerPhoneNumber = Column(String(20))
    Sku = Column(String(50))
    ProductName = Column(String(300))
    ShippedQuantity = Column(Integer)
    FulfillmentLevel = Column(String(40))
    AddrCountry = Column(String(10))
    AddrState = Column(String(100))
    AddrCity = Column(String(100))
    AddrPostal = Column(String(15))
    Addr1 = Column(String(200))
    Addr2 = Column(String(200))
    Addr3 = Column(String(200))
    AddrName = Column(String(100))
    AddrTel = Column(String(30))
    BillCountry = Column(String(10))
    BillState = Column(String(100))
    BillCity = Column(String(100))
    BillPostal = Column(String(15))
    BillAddr1 = Column(String(200))
    BillAddr2 = Column(String(200))
    BillAddr3 = Column(String(200))
    Carrier = Column(String(30))
    TrackingNum = Column(String(50))
    EstimatedArrivalDate = Column(DateTime)
    FC = Column(String(20))

    def __init__(self, Country, json_report):
        self.Country = Country
        self.AmazonOrderId = json_report.get('amazon-order-id')
        self.MerchantOrderID = json_report.get('merchant-order-id')
        self.ShipmentID = json_report.get('shipment-id')
        self.ShipmentItemID = json_report.get('shipment-item-id')
        self.AmazonOrderItemID = json_report.get('amazon-order-item-id')
        self.MerchantOrderItemID = json_report.get('merchant-order-item-id')
        self.PurchaseDate = common.iso_time_to_dsttime(json_report.get('purchase-date'))
        self.PaymentsDate = common.iso_time_to_dsttime(json_report.get('payments-date'))
        self.ShipmentDate = common.iso_time_to_dsttime(json_report.get('shipment-date'))
        self.ReportingDate = common.iso_time_to_dsttime(json_report.get('reporting-date'))
        self.BuyerEmail = json_report.get('buyer-email')
        self.BuyerName = json_report.get('buyer-name')
        self.BuyerPhoneNumber = json_report.get('buyer-phone-number')
        self.Sku = json_report.get('sku')
        self.ProductName = json_report.get('product-name')
        self.ShippedQuantity = json_report.get('quantity-shipped')
        self.FulfillmentLevel = json_report.get('ship-service-level')
        self.AddrCountry = json_report.get('ship-country')
        self.AddrState = json_report.get('ship-state')
        self.AddrCity = json_report.get('ship-city')
        self.AddrPostal = json_report.get('ship-postal-code')
        self.Addr1 = json_report.get('ship-address-1')
        self.Addr2 = json_report.get('ship-address-2')
        self.Addr3 = json_report.get('ship-address-3')
        self.AddrName = json_report.get('recipient-name')
        self.AddrTel = json_report.get('ship-phone-number')
        self.BillCountry = json_report.get('bill-country')
        self.BillState = json_report.get('bill-state')
        self.BillCity = json_report.get('bill-city')
        self.BillPostal = json_report.get('bill-postal-code')
        self.BillAddr1 = json_report.get('bill-address-1')
        self.BillAddr2 = json_report.get('bill-address-2')
        self.BillAddr3 = json_report.get('bill-address-3')
        self.Carrier = json_report.get('carrier')
        self.TrackingNum = json_report.get('tracking-number')
        self.EstimatedArrivalDate = common.iso_time_to_dsttime(json_report.get('estimated-arrival-date'))
        self.FC = json_report.get('fulfillment-center-id')


class AprFBAReturn(Base):

    __tablename__ = 'Apr_FBA_Return'

    ID = Column(Integer, primary_key=True)
    SnapDate = Column(DateTime)
    Country = Column(String(10))
    ReturnDate = Column(DateTime)
    LPN = Column(String(50))
    AmazonOrderId = Column(String(20))
    Sku = Column(String(50))
    Asin = Column(String(20))
    ProductName  = Column(String(300))
    ReturnQuantity = Column(Integer)
    FC = Column(String(20))
    ProductState = Column(String(20))
    Reason = Column(String(100))
    ReturnState = Column(String(40))
    Comments = Column(String(400))

    def __init__(self, SnapDate, Country, json_report):
        self.SnapDate = SnapDate
        self.Country = Country
        self.ReturnDate = common.iso_time_to_dsttime(json_report.get('return-date'))
        self.LPN = json_report.get('license-plate-number')
        self.AmazonOrderId = json_report.get('order-id')
        self.Sku = json_report.get('sku')
        self.Asin = json_report.get('asin')
        self.ProductName = json_report.get('product-name')
        self.ReturnQuantity = json_report.get('quantity')
        self.FC = json_report.get('fulfillment-center-id')
        self.ProductState = json_report.get('detailed-disposition')
        self.Reason = json_report.get('reason')
        self.ReturnState = json_report.get('status')
        self.Comments = json_report.get('customer-comments')


class AprFBAInventoryHealth(Base):

    __tablename__ = 'Apr_FBA_Inventory_Health'

    ID = Column(Integer, primary_key=True)
    Country = Column(String(10))
    SnapDate = Column(DateTime)
    Sku = Column(String(50))
    FnSku = Column(String(20))
    Asin = Column(String(20))
    ProductName = Column(String(300))
    Condition = Column(String(50))
    Category = Column(String(100))
    CategoryRank = Column(Integer)
    IsHazmat = Column(String(10))
    AmzTheoryUnit = Column(Integer)
    TotalUnits = Column(Integer)
    SellableUnits = Column(Integer)
    UnsellableUnits = Column(Integer)
    InBoundUnit = Column(Integer)
    IsLimit = Column(Integer)
    Quarter1Units = Column(Integer)
    Quarter2Units = Column(Integer)
    Quarter3Units = Column(Integer)
    Quarter4Units = Column(Integer)
    Quarter5Units = Column(Integer)
    Ship1DayUnits = Column(Integer)
    Ship7DayUnits = Column(Integer)
    Ship30DayUnits = Column(Integer)
    Ship90DayUnits = Column(Integer)
    Ship180DayUnits = Column(Integer)
    Ship365DayUnits = Column(Integer)
    DOS7 = Column(DECIMAL(10,4))
    DOS30 = Column(DECIMAL(10, 4))
    DOS90 = Column(DECIMAL(10, 4))
    DOS180 = Column(DECIMAL(10, 4))
    DOS365 = Column(DECIMAL(10, 4))
    AfnUnitsNew = Column(Integer)
    AfnUnitsUsed = Column(Integer)
    Currency = Column(String(10))
    YourPrice = Column(DECIMAL(10,2))
    SalesPrice = Column(DECIMAL(10,2))
    LowestAfnPriceNew =Column(DECIMAL(10,2))
    LowestAfnPriceUsed = Column(DECIMAL(10,2))
    LowestMfnPriceNew = Column(DECIMAL(10,2))
    LowestMfnPriceUsed = Column(DECIMAL(10,2))
    RemovalUnit = Column(Integer)
    Month6Unit = Column(Integer)
    Month6Fee = Column(DECIMAL(10,2))
    Month12Unit = Column(Integer)
    Month12Fee = Column(DECIMAL(10,2))
    LongTermUnit = Column(Integer)
    FeePerUnit = Column(DECIMAL(10,2))

    def __init__(self, Country, json_report):
        self.Country = Country
        self.SnapDate = common.iso_time_to_dsttime(json_report.get('snapshot-date'))
        self.Sku = json_report.get('sku')
        self.FnSku = json_report.get('fnsku')
        self.Asin = json_report.get('asin')
        self.ProductName = json_report.get('product-name')
        self.Condition = json_report.get('condition')
        self.Category = json_report.get('product-group')
        self.CategoryRank = json_report.get('sales-rank')
        self.IsHazmat = json_report.get('is-hazmat')
        self.AmzTheoryUnit = json_report.get('inbound-recommend-quantity')
        self.TotalUnits = json_report.get('total-quantity')
        self.SellableUnits = json_report.get('sellable-quantity')
        self.UnsellableUnits = json_report.get('unsellable-quantity')
        self.InBoundUnit = json_report.get('in-bound-quantity')
        self.IsLimit = json_report.get('asin-limit')
        self.Quarter1Units = json_report.get('inv-age-0-to-90-days')
        self.Quarter2Units = json_report.get('inv-age-91-to-180-days')
        self.Quarter3Units = json_report.get('inv-age-181-to-270-days')
        self.Quarter4Units = json_report.get('inv-age-271-to-365-days')
        self.Quarter5Units = json_report.get('inv-age-365-plus-days')
        self.Ship1DayUnits = json_report.get('units-shipped-last-24-hrs')
        self.Ship7DayUnits = json_report.get('units-shipped-last-7-days')
        self.Ship30DayUnits = json_report.get('units-shipped-last-30-days')
        self.Ship90DayUnits = json_report.get('units-shipped-last-90-days')
        self.Ship180DayUnits = json_report.get('units-shipped-last-180-days')
        self.Ship365DayUnits = json_report.get('units-shipped-last-365-days')
        self.DOS7 = common.set_param_value(json_report.get('weeks-of-cover-t7'))
        self.DOS30 = common.set_param_value(json_report.get('weeks-of-cover-t30'))
        self.DOS90 = common.set_param_value(json_report.get('weeks-of-cover-t90'))
        self.DOS180 = common.set_param_value(json_report.get('weeks-of-cover-t180'))
        self.DOS365 = common.set_param_value(json_report.get('weeks-of-cover-t365'))
        self.AfnUnitsNew = json_report.get('num-afn-new-sellers')
        self.AfnUnitsUsed = json_report.get('num-afn-used-sellers')
        self.Currency = json_report.get('currency')
        self.YourPrice = json_report.get('your-price')
        self.SalesPrice = json_report.get('sales_price')
        self.LowestAfnPriceNew = json_report.get('lowest-afn-new-price')
        self.LowestAfnPriceUsed = json_report.get('lowest-afn-used-price')
        self.LowestMfnPriceNew = json_report.get('lowest-mfn-new-price')
        self.LowestMfnPriceUsed = json_report.get('lowest-mfn-used-price')
        self.RemovalUnit = json_report.get('qty-with-removals-in-progress') or 0
        self.Month6Unit = json_report.get('qty-to-be-charged-ltsf-6-mo')
        self.Month6Fee = json_report.get('projected-ltsf-6-mo')
        self.Month12Unit = json_report.get('qty-to-be-charged-ltsf-12-mo')
        self.Month12Fee = json_report.get('projected-ltsf-12-mo')
        self.LongTermUnit = json_report.get('qty-in-long-term-storage-program')
        self.FeePerUnit = json_report.get('per-unit-volume')


class AprFBAInventoryAge(Base):

    __tablename__ = 'Apr_FBA_Inventory_Age'

    ID = Column(Integer)
    Country = Column(String(10), primary_key=True)
    SnapDate = Column(DateTime, primary_key=True)
    Sku = Column(String(50), primary_key=True)
    FnSku = Column(String(20))
    Asin = Column(String(20))
    ProductName = Column(String(300))
    Condition = Column(String(50))
    SellableUnits = Column(Integer)
    UnsellableUnits = Column(Integer)
    Quarter1Units = Column(Integer)
    Quarter2Units = Column(Integer)
    Quarter3Units = Column(Integer)
    Quarter4Units = Column(Integer)
    Quarter5Units = Column(Integer)
    Currency = Column(String(10))
    Units6 = Column(Integer)
    ProjectedUnits6 = Column(Integer)
    Units12 = Column(Integer)
    ProjectedUnits12 = Column(Integer)
    Ship7DayUnits = Column(Integer)
    Ship30DayUnits = Column(Integer)
    Ship60DayUnits = Column(Integer)
    Ship90DayUnits = Column(Integer)
    Alert = Column(String(20))
    YourPrice = Column(DECIMAL(6, 2))
    SalesPrice = Column(DECIMAL(6, 2))
    LowestPriceNew = Column(DECIMAL(6, 2))
    LowestPriceUsed = Column(DECIMAL(6, 2))
    RecommendedAction = Column(String(50))
    TargetUnits = Column(Integer)
    TargetPirce = Column(DECIMAL(6, 2))
    TargetDos = Column(Integer)
    TagetClearUnits = Column(Integer)
    TargetCost = Column(DECIMAL(10, 2))
    Dos = Column(DECIMAL(10, 2))
    Volume = Column(DECIMAL(12, 6))

    def __init__(self, Country, json_report):
        self.Country = Country
        self.SnapDate = common.iso_time_to_dsttime(json_report.get('snapshot-date'))
        self.Sku = json_report.get('sku')
        self.FnSku = json_report.get('fnsku')
        self.Asin = json_report.get('asin')
        self.ProductName = json_report.get('product-name')
        self.Condition = json_report.get('condition')
        self.SellableUnits = json_report.get('avaliable-quantity(sellable)')
        self.UnsellableUnits = json_report.get('qty-with-removals-in-progress')
        self.Quarter1Units = json_report.get('inv-age-0-to-90-days')
        self.Quarter2Units = json_report.get('inv-age-91-to-180-days')
        self.Quarter3Units = json_report.get('inv-age-181-to-270-days')
        self.Quarter4Units = json_report.get('inv-age-271-to-365-days')
        self.Quarter5Units = json_report.get('inv-age-365-plus-days')
        self.Currency = json_report.get('currency')
        self.Units6 = json_report.get('qty-to-be-charged-ltsf-6-mo')
        self.ProjectedUnits6 = json_report.get('projected-ltsf-6-mo')
        self.Units12 = json_report.get('qty-to-be-charged-ltsf-12-mo')
        self.ProjectedUnits12 = json_report.get('projected-ltsf-12-mo')
        self.Ship7DayUnits = json_report.get('units-shipped-last-7-days')
        self.Ship30DayUnits = json_report.get('units-shipped-last-30-days')
        self.Ship60DayUnits = json_report.get('units-shipped-last-60-days')
        self.Ship90DayUnits = json_report.get('units-shipped-last-90-days')
        self.Alert = json_report.get('alert')
        self.YourPrice = json_report.get('your-price') or 0.0
        self.SalesPrice = json_report.get('sales_price') or 0.0
        self.LowestPriceNew = json_report.get('lowest_price_new')
        self.LowestPriceUsed = json_report.get('lowest_price_used')
        self.RecommendedAction = json_report.get('Recommended action')
        self.TargetUnits = json_report.get('Healthy Inventory Level')
        self.TargetPirce = json_report.get('Recommended sales price')
        self.TargetDos = json_report.get('Recommended sale duration (days)')
        self.TagetClearUnits = json_report.get('Recommended Removal Quantity')
        self.TargetCost = json_report.get('Estimated cost savings of removal')
        self.Dos = json_report.get('sell-through')
        self.Volume = json_report.get('cubic-feet')





