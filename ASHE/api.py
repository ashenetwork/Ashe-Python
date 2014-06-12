#!/usr/bin/python

import urllib2
import json
import os
from error import ASHEError

class API:
  private_key = None
  merchant_id = None
  version = '1'
  mode = None
  base_url = 'https://www.ashepay.com'

  @classmethod
  def post_request(cls, data={}, method=None):
    cls.check_params(data, method)
    url = cls.build_url(method)
    headers = cls.build_headers()
    data = cls.build_private_data(data)
    data = json.dumps(data)
    try:
      request = urllib2.Request(url, data, headers)
      response = urllib2.urlopen(request).read()
      response = json.loads(response)
    except:
      raise ASHEError("Could not connect to the server. Please check your internet connection.", "E500")
    errors = response['errors']
    if isinstance(errors, list) and len(errors) > 0:
      error = errors[0]
      raise ASHEError(error['msg'], error['code'])
    return response

  @classmethod
  def build_private_data(cls, data):
    data['merchant_id'] = cls.merchant_id
    data['private_key'] = cls.private_key
    return data

  @classmethod
  def build_headers(cls):
    headers = {
                'Accept': 'application/json',
                'User-Agent': 'ASHE Corporation Python Payment API V%s' % cls.version,
                'Content-Type': 'application/JSON'
              }
    return headers

  @classmethod
  def check_params(cls, data, method):
    if method not in ['charge', 'refund']:
      raise Exception("Unknown method.")
    if not cls.merchant_id:
      raise ASHEError("Invalid merchant id.", "E402")
    if not cls.private_key:
      raise ASHEError("Invalid private key.", "E402")
    if cls.mode not in ['sandbox', 'production']:
      raise ASHEError("Invalid mode. Please specify either 'production' or 'sandbox'.", "E402")
    if 'amount' not in data.keys() or not data['amount']:
      raise ASHEError("Invalid amount.", "E401")
    if method == 'charge' and ('token' not in data.keys() or not data['token']):
      raise ASHEError("Invalid token.", "E401")
    if method == 'refund' and ('transaction_id' not in data.keys() or not data['transaction_id']):
      raise ASHEError("Invalid transaction id.", "E401")

  @classmethod
  def build_url(cls, method):
    if method == 'charge':
      if cls.mode == 'production':
        url = "%s/api/payment/v1/%s/" % (cls.base_url, cls.merchant_id)
      else:
        url = "%s/api/sandbox/%s/" % (cls.base_url, cls.merchant_id)
    elif method == 'refund':
      if cls.mode == 'production':
        url = "%s/api/refund/v1/%s/" % (cls.base_url, cls.merchant_id)
      else:
        url = "%s/api/sandbox/refund/%s/" % (cls.base_url, cls.merchant_id)

    return url

