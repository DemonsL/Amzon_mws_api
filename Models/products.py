# coding: utf-8
import datetime
from Config import db
from sqlalchemy import Column, String, Integer, Float, DECIMAL, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)


Base = declarative_base()
class AprProductInfo(Base):

    __tablename__ = 'Apr_Product_Info'

    ID = Column(Integer, primary_key=True)
    Country = Column(String(10))
    SnapDate = Column(DateTime)
    Asin = Column(String(20))
    Brand = Column(String(100))
    ListingDate = Column(DateTime)
    ParentAsin = Column(String(50))
    Color = Column(String(50))
    MaterialType = Column(String(100))
    Pack = Column(Integer)
    Size = Column(String(200))
    Title = Column(String(200))
    SmallImageUrl = Column(String(200))
    Length = Column(DECIMAL(6,1))
    Width = Column(DECIMAL(6,1))
    Height = Column(DECIMAL(6,1))
    Weight = Column(DECIMAL(6,2))
    PackageLength = Column(DECIMAL(6,1))
    PackageWidth = Column(DECIMAL(6,1))
    PackageHeight = Column(DECIMAL(6,1))
    PackageWeight = Column(DECIMAL(6,2))

    def __init__(self, country, snap_date, json_product):
        self.Country = country
        self.SnapDate = snap_date
        self.Asin = json_product.get('Identifiers').get('MarketplaceASIN').get('ASIN')
        self.Brand = json_product.get('AttributeSets').get('ns2:ItemAttributes').get('ns2:Brand')
        self.ListingDate = json_product.get('AttributeSets').get('ns2:ItemAttributes').get('ns2:ReleaseDate')
        self.ParentAsin = json_product.get('Relationships').get('VariationParent').get('Identifiers') \
                                      .get('MarketplaceASIN').get('ASIN') if not json_product.get('Relationships') else ''
        self.Color = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:Color')
        self.MaterialType = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:MaterialType')
        self.Pack = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:PackageQuantity')
        self.Size = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:Size')
        self.Title = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:Title')
        self.SmallImageUrl = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:SmallImage').get('ns2:URL')
        self.Length = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:ItemDimensions') \
                                  .get('ns2:Length').get('#text')
        self.Width = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:ItemDimensions') \
                                 .get('ns2:Width').get('#text')
        self.Height = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:ItemDimensions') \
                                  .get('ns2:Height').get('#text')
        self.Weight = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:ItemDimensions') \
                                  .get('ns2:Weight').get('#text')
        self.PackageLength = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:PackageDimensions') \
                                         .get('ns2:Length').get('#text')
        self.PackageWidth = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:PackageDimensions') \
                                        .get('ns2:Width').get('#text')
        self.PackageHeight = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:PackageDimensions') \
                                         .get('ns2:Height').get('#text')
        self.PackageWeight = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:PackageDimensions') \
                                         .get('ns2:Weight').get('#text')


class AprProductDaily(Base):

    __tablename__ = 'Apr_Product_Daily'

    ID = Column(Integer, primary_key=True)
    Country = Column(String(10))
    SnapDate = Column(DateTime)
    Asin = Column(String(20))
    Title = Column(String(200))
    ProductCategory = Column(String(60))
    Category1 = Column(String(100))
    Rank1 = Column(Integer)
    Category2 = Column(String(100))
    Rank2 = Column(Integer)
    Category3 = Column(String(100))
    Rank3 = Column(Integer)

    def __init__(self, country, snap_date, json_product):
        self.Country = country
        self.SnapDate = snap_date
        self.Asin = json_product.get('Identifiers').get('MarketplaceASIN').get('ASIN')
        self.Title = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:Title')
        self.ProductCategory = json_product.get('AttributeSets').get('ItemAttributes').get('ns2:ProductGroup')
        self.Category1 = json_product.get('SalesRankings').get('SalesRank')[0].get('ProductCategoryId')
        self.Rank1 = json_product.get('SalesRankings').get('SalesRank')[0].get('Rank')
        self.Category2 = json_product.get('SalesRankings').get('SalesRank')[1].get('ProductCategoryId')
        self.Rank2 = json_product.get('SalesRankings').get('SalesRank')[1].get('Rank')
        self.Category3 = json_product.get('SalesRankings').get('SalesRank')[2].get('ProductCategoryId') \
                                       if json_product.get('SalesRankings').get('SalesRank')[2] else ''
        self.Rank3 = json_product.get('SalesRankings').get('SalesRank')[2].get('Rank') \
                                       if json_product.get('SalesRankings').get('SalesRank')[2] else 0


class PubAsin(Base):

    __tablename__ = 'Pub_Asin'

    Asin = Column(String(20), primary_key=True)


class AprAsinRank(Base):

    __tablename__ = 'Apr_Asin_Rank'

    ID = Column(Integer)
    Country = Column(String(10), primary_key=True)
    SnapDate = Column(DateTime, primary_key=True)
    Asin = Column(String(20), primary_key=True)
    CategoryId = Column(String(100), primary_key=True)
    Rank = Column(Integer)
    LastUpdate = Column(DateTime)

    def __init__(self, country, snap_date, asin, json_rank):
        self.Country = country
        self.SnapDate = snap_date
        self.Asin = asin
        self.CategoryId = json_rank.get('ProductCategoryId')
        self.Rank = json_rank.get('Rank')
        self.LastUpdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
