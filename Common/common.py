# coding: utf-8
import json
import pytz
import datetime
import xmltodict

def set_param_list(param_list, param_name):
    i, resp = 1, ''
    for param in param_list.split(','):
        resp += '&{pn}.{i}='.format(pn=param_name, i=i) + param
        i += 1
    return resp

def amz_iso_time(time):
    dt = datetime.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
    return dt

def iso_time_to_dsttime(time_str):
    time_date = datetime.datetime.fromisoformat(time_str)
    dst_zone = pytz.timezone('US/Pacific')
    dsttime = time_date.astimezone(dst_zone)
    return dsttime.strftime('%Y-%m-%d %H:%M:%S')

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