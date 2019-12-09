# coding: utf-8
import datetime
from Config import db
from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)


Base = declarative_base()
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




#-------------------------------------------------------------------------------

def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict


class ApbBestSeller(Base):

    __tablename__ = 'Apb_Best_Seller'

    Country = Column(String(10), primary_key=True)
    Asin = Column(String(20))


class PubAllAsin(Base):

    __tablename__ = 'Pub_All_Asin'

    Country = Column(String(10), primary_key=True)
    Brand = Column(String(100))
    Manufacturer = Column(String(600))
    Publisher = Column(String(600))
    Studio = Column(String(600))
    PN = Column(String(50))
    Asin = Column(String(20), primary_key=True)
    PartNumber = Column(String(100))
    Title = Column(String(400))
    ReleaseDate = Column(DateTime)
    AmzBinding = Column(String(100))
    AmzGroup = Column(String(100))
    AmzType = Column(String(100))
    Length = Column(DECIMAL(8, 1))
    Width = Column(DECIMAL(8, 1))
    Height = Column(DECIMAL(8, 1))
    Weight = Column(DECIMAL(8, 1))
    PLength = Column(DECIMAL(8, 1))
    PWidth = Column(DECIMAL(8, 1))
    PHeight = Column(DECIMAL(8, 1))
    PWeight = Column(DECIMAL(8, 1))
    UnitLength = Column(String(10))
    UnitWeight = Column(String(10))
    Color = Column(String(50))
    Size = Column(String(50))
    ListPrice = Column(DECIMAL(8, 2))
    CurrencyCode = Column(String(10))
    ImageUrl = Column(String(100))
    MaterialType = Column(String(800))
    Warranty = Column(String(800))

    def __init__(self, country, asin, product):
        self.Country = country
        self.Asin = asin
        self.Brand = self.str_up(product.get('ns2:Brand'))
        self.Manufacturer = self.str_up(product.get('ns2:Manufacturer'))
        self.Publisher = self.str_up(product.get('ns2:Publisher'))
        self.Studio = self.str_up(product.get('ns2:Studio'))
        self.PN = product.get('ns2:Model')
        self.PartNumber = product.get('ns2:PartNumber')
        self.Title = product.get('ns2:Title')
        self.ReleaseDate = product.get('ns2:ReleaseDate')
        self.AmzBinding = product.get('ns2:Binding')
        self.AmzGroup = product.get('ns2:ProductGroup')
        self.AmzType = product.get('ns2:ProductTypeName')
        self.Length = self.is_value(product, 'ns2:ItemDimensions', 'ns2:Length', '#text', 0.0)
        self.Width = self.is_value(product, 'ns2:ItemDimensions', 'ns2:Width', '#text', 0.0)
        self.Height = self.is_value(product, 'ns2:ItemDimensions', 'ns2:Height', '#text', 0.0)
        self.Weight = self.is_value(product, 'ns2:ItemDimensions', 'ns2:Weight', '#text', 0.0)
        self.PLength = self.is_value(product, 'ns2:PackageDimensions', 'ns2:Length', '#text', 0.0)
        self.PWidth = self.is_value(product, 'ns2:PackageDimensions', 'ns2:Width', '#text', 0.0)
        self.PHeight = self.is_value(product, 'ns2:PackageDimensions', 'ns2:Height', '#text', 0.0)
        self.PWeight = self.is_value(product, 'ns2:PackageDimensions', 'ns2:Weight', '#text', 0.0)
        self.UnitLength = self.is_value(product, 'ns2:PackageDimensions', 'ns2:Length', '@Units', 0.0)
        self.UnitWeight = self.is_value(product, 'ns2:PackageDimensions', 'ns2:Weight', '@Units', 0.0)
        self.Color = self.str_trunc(product.get('ns2:Color'), 50)
        self.Size = product.get('ns2:Size')
        self.ListPrice = product.get('ns2:ListPrice').get('ns2:Amount') if product.get('ns2:ListPrice') else 0.0
        self.CurrencyCode = product.get('ns2:ListPrice').get('ns2:CurrencyCode') if product.get('ns2:ListPrice') else ''
        self.ImageUrl = product.get('ns2:SmallImage').get('ns2:URL')
        self.MaterialType = str(product.get('ns2:MaterialType'))
        self.Warranty = self.str_trunc(product.get('ns2:Warranty'), 800)

    def str_up(self, value):
        if value:
            return str(value).upper()
        else:
            return value

    def is_value(self, p, field1, field2, field3, value):
        if p.get(field1) and p.get(field1).get(field2):
            return p.get(field1).get(field2).get(field3)
        else:
            return value

    def str_trunc(self, value, trunc_num):
        if len(str(value)) > trunc_num:
            return value[:trunc_num]
        else:
            return value

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class AprAllAsinRank(Base):

    __tablename__ = 'Apr_All_Asin_Rank'

    ID = Column(Integer)
    Country = Column(String(10), primary_key=True)
    SnapDate = Column(DateTime, primary_key=True)
    SnapHour = Column(String(2), primary_key=True)
    Asin = Column(String(20), primary_key=True)
    CategoryId = Column(String(100))
    Rank = Column(Integer)
    LastUpdate = Column(DateTime)

    def __init__(self, rank, param):
        self.Country = param.get('Country')
        self.SnapDate = param.get('SnapDate')
        self.SnapHour = param.get('SnapHour')
        self.Asin = param.get('Asin')
        self.CategoryId = rank.get('ProductCategoryId')
        self.Rank = rank.get('Rank')
        self.LastUpdate = param.get('LastUpdate')