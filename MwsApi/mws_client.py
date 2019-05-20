# coding: utf-8
import hmac
import hashlib
import base64
import datetime
import requests
from urllib.parse import quote


class MwsClient:
    """
    Amazon mws api
    """

    signature_method = 'HmacSHA256'
    signature_version = '2'

    def __init__(self, access_key, secret_key, seller_id, auth_token, host, marketplace):
        self.access_key = access_key
        self.secret_key = secret_key
        self.seller_id = seller_id
        self.auth_token = auth_token
        self.host = host
        self.marketplace = marketplace

    def params_encode(self, params):
        return quote(params, safe='-_.~')

    def get_query_string(self, action, parameters, version):
        time_now = datetime.datetime.now()
        utc_time = time_now - datetime.timedelta(hours=8)
        iso_time = datetime.datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
        time_encode = self.params_encode(iso_time)

        query_string = 'AWSAccessKeyId=' + self.access_key + '&Action=' + action + parameters + \
                       '&MWSAuthToken=' + self.auth_token +  '&MarketplaceId=' + self.marketplace + \
                       '&SellerId=' + self.seller_id + '&SignatureMethod=' + self.signature_method + \
                       '&SignatureVersion=' + self.signature_version + '&Timestamp=' + time_encode + \
                       '&Version=' + version
        string_list = query_string.split('&')
        string_list.sort()
        string_sort = '&'.join(string_list)
        return string_sort

    def string_to_sign(self, http_method, uri, message):
        sig_string = http_method + '\n' + self.host + '\n' + uri + '\n' + message
        bytes_key = bytes(self.secret_key, 'utf-8')
        bytes_msg = bytes(sig_string, 'utf-8')
        h = hmac.new(bytes_key, bytes_msg, digestmod=hashlib.sha256)
        digest = h.digest()
        signature = base64.b64encode(digest)
        return self.params_encode(signature)

    def get_url(self, host, uri, query_string, signature):
        url = 'https://' + host + uri + '?' + query_string + '&Signature=' + signature
        return url

    def excute_req(self, url, method='POST'):
        headers = {
            "User_Agent": "Amzon_mws_api/1.0 (Language=Python)",
            "Host":"mws.amazonservices.com",
            "Content-Type": "text/xml"
        }
        resp = requests.post(url, headers=headers)
        if method == 'GET':
            resp = requests.get(url, headers=headers)
        return resp