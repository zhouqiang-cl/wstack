# -*- coding: utf-8 -*-

import urllib2
import cookielib
import urllib
import json


DNS_HOST = "dns.internal.nosa.me"
DNS_AUTH_API = "api/v1/ldapauth"
DNS_AUTH_USERNAME = ""
DNS_AUTH_PASSWD = ''


class LoginException(Exception):
    def __init__(self, data):
        Exception.__init__(self, data)
        self.__data = data

    def __str__(self):
        return str(self.__data)


class Ldapapi(object):
    def __init__(self, host_url=DNS_HOST, username=DNS_AUTH_USERNAME,
                 password=DNS_AUTH_PASSWD, auth_uri=DNS_AUTH_API):
        self.is_login = False
        self.host_url = host_url
        self.username = username
        self.password = password
        self.auth_uri = auth_uri

        self.login()
        if not self.is_login:
            raise LoginException("asset auth fail")

    def login(self):
        auth_url = r"http://" + self.host_url + r"/" + self.auth_uri
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        data = urllib.urlencode({"username": self.username, 'password': self.password})
        login_response = urllib2.urlopen(auth_url, data)
        response = login_response.read()

        ret_dict = json.loads(response)

        # update to check the response content to check if passed
        # authentication
        if ret_dict["result"] == "success":
            self.is_login = True
        else:
            self.is_login = False

    def post_wrapper(self, url, data_dict):
        data = urllib.urlencode(data_dict)
        visit_url = r"http://" + self.host_url + r"/" + url
        login_response = urllib2.urlopen(visit_url, data)
        response = login_response.read()
        ret_dict = json.loads(response)

        return ret_dict

    def get_wrapper(self, url, data_dict):
        data = urllib.urlencode(data_dict)
        visit_url = r"http://" + self.host_url + r"/" + url
        login_response = urllib2.urlopen(visit_url + "?" + data)
        response = login_response.read()
        ret_dict = json.loads(response)

        return ret_dict


def add_record(hostname, ip):
    uri = "api/v1/add"
    data_dict = {
        "dnslist": json.dumps([{"hostname": hostname, "ip": ip}])
    }
    _object = Ldapapi()
    return _object.post_wrapper(uri, data_dict)
