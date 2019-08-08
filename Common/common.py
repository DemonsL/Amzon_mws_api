# coding: utf-8
import json
import pytz
import datetime
import logging
import xmltodict
from Config import mws_config

log = logging.getLogger()

def get_client(client_obj, mkp):
    access_key = mws_config.client.get('access_key')
    secret_key = mws_config.client.get('secret_key')
    seller_id = mws_config.client.get('seller_id')
    auth_token = mws_config.client.get('auth_token')
    host = mws_config.endpoint.get('us')
    mkp_id = mws_config.marketplace.get(mkp)
    return client_obj(access_key, secret_key, seller_id, auth_token, host, mkp_id)

def set_param_list(param_list, param_name):
    i, resp = 1, ''
    for param in param_list.split(','):
        resp += '&{pn}.{i}='.format(pn=param_name, i=i) + param
        i += 1
    return resp

def amz_iso_time(time):
    dt = datetime.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
    return dt

def iso_time_to_date(time_str):
    if time_str:
        time_date = datetime.datetime.fromisoformat(time_str[:-1])
        return time_date

def iso_time_to_dsttime(time_str):
    if time_str:
        time_date = datetime.datetime.fromisoformat(time_str)
        dst_zone = pytz.timezone('US/Pacific')
        dsttime = time_date.astimezone(dst_zone)
        return dsttime.strftime('%Y-%m-%d %H:%M:%S')

def dsttime_to_utctime(time_str):
    if time_str:
        time_date = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        us_date = pytz.timezone('US/Pacific').localize(time_date)
        utc_zone = pytz.timezone('UTC')
        utctime = us_date.astimezone(utc_zone)
        return utctime

def utctime_to_dsttime(time_str):
    if time_str:
        time_date = iso_time_to_date(time_str)
        utc_date = pytz.timezone('UTC').localize(time_date)
        us_zone = pytz.timezone('US/Pacific')
        us_time = utc_date.astimezone(us_zone)
        return us_time

def dsttime_to_localtime(time_date):
    if time_date:
        us_date = pytz.timezone('US/Pacific').localize(time_date)
        utc_zone = pytz.timezone('Asia/Shanghai')
        utctime = us_date.astimezone(utc_zone)
        return utctime

def xml_to_json(data):
    data_dict = xmltodict.parse(data)
    json_str = json.dumps(data_dict)
    data_json = json.loads(json_str)
    return data_json

def flat_to_json(data):
    resp_list = [flat.strip().split('\t') for flat in data.strip().split('\r\n')]
    d_key = resp_list[0]
    datas = []
    for d_value in resp_list[1:]:
        datas.append(dict(zip(d_key, d_value)))
    json_str = json.dumps(datas)
    data_json = json.loads(json_str)
    return data_json

def set_param_value(param):
    resp = param
    if param == 'Infinite':
        resp = 99999.9999
    return resp

def is_value(field_keys, field_dict, default_value):
    resp = default_value
    field_key1 = field_keys.split('_')[0]
    field_key2 = field_keys.split('_')[1]
    if field_key1 in field_dict.keys():
        resp = field_dict.get(field_key1).get(field_key2)
    return resp

