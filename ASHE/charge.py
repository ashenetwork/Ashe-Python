#!/usr/bin/python

from api import API

class Charge:

  @classmethod
  def charge(cls, data):
    response = API.post_request(data, 'charge')
    return response

  @classmethod
  def refund(cls, data):
    response = API.post_request(data, 'refund')
    return response
