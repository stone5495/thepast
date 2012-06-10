#-*- coding:utf-8 -*-
import os
import re
import time
import datetime
import imghdr
import httplib2
import random
import string
import markdown2
from past import config

def randbytes(bytes_):
    return ''.join(random.sample(string.ascii_letters + string.digits, bytes_))

def httplib2_request(uri, method="GET", body='', headers=None, 
        redirections=httplib2.DEFAULT_MAX_REDIRECTS, 
        connection_type=None, disable_ssl_certificate_validation=True):

    DEFAULT_POST_CONTENT_TYPE = 'application/x-www-form-urlencoded'

    if not isinstance(headers, dict):
        headers = {}

    if method == "POST":
        headers['Content-Type'] = headers.get('Content-Type', 
            DEFAULT_POST_CONTENT_TYPE)

    return httplib2.Http(disable_ssl_certificate_validation=disable_ssl_certificate_validation).\
        request(uri, method=method, body=body,
        headers=headers, redirections=redirections,
        connection_type=connection_type)

def wrap_long_line(text, max_len=60):
    if len(text) <= max_len:
        return text
    out = ""
    parts = text.split("\n")
    parts_out = []
    for x in parts:
        parts_out.append( _wrap_long_line(x, max_len) )
    return "\n".join(parts_out)
    
def _wrap_long_line(text, max_len):
    out_text = ""
    times = len(text)*1.0 / max_len
    if times > int(times):
        times = int(times) + 1
    else:
        times = int(times)

    i = 0
    index = 0
    while i < times:
        s = text[index:index+max_len]
        out_text += s
        if not ('<' in s or '>' in s):
            out_text += "\n"
        index += max_len
        i += 1

    return out_text

def datetime2timestamp(datetime_):
    if not isinstance(datetime_, datetime.datetime):
        return 0

    return datetime_ and  int(time.mktime(datetime_.timetuple()))

EMAILRE = re.compile(r'^[_\.0-9a-zA-Z+-]+@([0-9a-zA-Z]+[0-9a-zA-Z-]*\.)+[a-zA-Z]{2,4}$')
def is_valid_email(email):
    if len(email) >= 6:
        return EMAILRE.match(email) != None 
    return False

def is_valid_image(content):
     return content and imghdr.what(content) in \
            [ 'rgb' ,'gif' ,'pbm' ,'pgm' ,
            'ppm' ,'tiff' ,'rast' ,'xbm' ,'jpeg' ,'bmp' ,'png']

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def markdownize(content):
    return markdown2.markdown(content)
    
