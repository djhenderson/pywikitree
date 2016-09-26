#! python3
# -*- coding:utf-8 -*-

"""
wt_apps.py provides an interface to the WikiTree APPS API.

This code is intended to, and currently does work with Python 2.7 and
Python 3.4, 3.5 and 3.6.

It has been tested with 2.7.10 and 3.4.3 on cygwin
and Python 2.7.12, 3.5.2, and 3.6.0b1 on Windows 7.
"""
from __future__ import print_function, unicode_literals

import pprint
import requests
import logging
from simplejson.scanner import JSONDecodeError

# Enabling debugging at http.client level (requests->urllib3->http.client)
# you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# the only thing missing will be the response.body which is not logged.
#try: # for Python 3
    #from http.client import HTTPConnection
#except ImportError:
    #from httplib import HTTPConnection
#HTTPConnection.debuglevel = 1

logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

class WT_Apps(object):
    """WikiTree Apps interface
    """

    _url = "https://apps.wikitree.com/api.php"
    _format = "json"
    _session = None
    __Privacy2Levels = {}
    __LevelsPrivacy = {}
    _verbosity = 0

    def Privacy2Level(self, privacy):
        """Privacy2Level() translates a privacy level name
        to a numeric privacy level.
        """

        return self.__Privacy2Levels.get(privacy, 0)

    def Level2Privacy(self, level):
        """Level2Privacy*() translats a numeric privacy level to
        a privacy level name.
        """

        return self.__Levels2Privacy.get(level, "No description")

    __formats = ("json", "xmlfm")

    def __init__(self, url=None, default_format=None, verbosity=0):
        """__init__() initializes a WikiTree Apps interface instance.
        You may override the default WikiTree Apps URL.
        You can specify the default data format to be returned,
        either "json" or "xmlfm". "json" is the default.
        You can adjust the verbosity, default is 0.
        """

        if url:
            self._url = url

        if default_format:
            if default_format in self.__formats:
                self._format = default_format
            else:
                print("WARNING: invalid default_format ignored:"+repr(default_format))
                self._format = "json"

        s = self._session = requests.Session()

        s.headers['Accept-charset'] = "utf-8"

        if self._format == "json":
            pass
        elif self._format == 'xmlfm':
            s.headers['Accept'] = "application/xml"
            s.headers['Accept'] = "text/xml"
        else:
            raise RuntimeError("Invalid format: " + repr(self._format))

        r = self.getPrivacyLevels(_initialize=True)

    def _req(self, data, headers={}):
        """_req() is a private function to perform the
        https request to the WikiTree Apps API.
        It constructs and posts the request,
        and checks the status of the result.
        """

        if self._verbosity > 1:
            print("url:", self._url)
            print("data:", data)

        r = self._session.post(self._url, data=data)

        if r.status_code != requests.codes.ok:
            print("url:", self._url)
            print("data:", data)
            r.raise_for_status()

        return r

    def login(self, email, password):
        """login() logs you into WikiTree using your email address and password
        The email address and password are the same as you use to log into
        your WikiTree profile and private web pages."""

        data = {"action": "login", "email": email, "password": password}

        r = self._req(data)

        return r

    def logout(self):
        """logout() logs you out of WikiTree.
        No further requests can be performed (without a login ?).
        """

        self._session = None

    def getPerson(self, key, fields=None):
        """getPerson() gets a person from the WikiTree api.
        Provide the person key, either the LNAB-# or profile id.
        """

        if fields is None:
            fields = ""

        data = {"action": "getPerson", "key": key, "fields": fields,}

        r = self._req(data)

        return r

    def getPrivacyLevels(self, _initialize=False):
        """getPrivacyLevels() retrieves the name and number of the
        WikiTree privacy levels.
        The _initialize parameter is used during class initialization to
        retrieve privacy levels.
        """

        data = {"action": "getPrivacyLevels",}

        if _initialize:
            data["format"] = "json"  # force JSON request

        r = self._req(data)

        if _initialize:
            try:
                j = r.json()
                self.__Privacy2Levels = j[0].copy()
                self.__Levels2Privacy = {v:k for k,v in self.__Privacy2Levels.items()}

                if 35 not in self.__Levels2Privacy:
                    self.__Levels2Privacy[35] = "SEMIPRIVATE_TREE"
                    self.__Privacy2Levels["SEMIPRIVATE_TREE"] = 35
                    print("WARNING: added privacy level 35 SEMIPRIVATE_TREE")

            except JSONDecodeError as e:
                print("Exception:", e)
            except Exception as e:
                print("Exception:", e)
                raise

        return r

    __bioOptions = {"key",}

    def getBio(self, key=None, **kwargs):
        """getBio() retrieves the Biography for a WikiTree profile."""

        data = {"action": "getBio", "key": key,}

        for k, v in kwargs:
            if k not in self.__bioOptions:
                print("WARNING: invalid paramter to getBio:", repr(k))
                del kwargs[k]

        if len(kwargs) > 0:
            data.update(kwargs)

        r = self._req(data)

        return r

    __watchlistOptions = {
            'getPerson', 'getSpace',
            'onlyLiving', 'excludeLiving',
            'order', 'limit', 'offset',
        }

    __watchlistOrders = {
            'user_id', 'user_name', 'user_last_name_current',
            'user_birth_date', 'user_death_date',
            'page_touched',
        }

    def getWatchlist(self, **kwargs):
        """getWatchlist() retrieves your WikiTree watchlist."""

        data = {"action": "getWatchlist",}

        for k, v in list(kwargs.items()):
            if k not in self.__watchlistOptions:
                print("WARNING: invalid parameter to getWatchlist:", repr(k))
                del kwargs[k]
            elif k == 'order':
                if v not in self.__watchlistOrders:
                    print("WARNING: invalid value of getWatchlist order:", repr(v))
                    del kwargs[k]
            else:
                if isinstance(v, bool):
                    kwargs[k] = int(v)

        if len(kwargs) > 0:
            data.update(kwargs)

        r = self._req(data)

        return r

    def getProfile(self, key):
        """getProfile() retrieves a WikiTree profile."""

        data = {"action": "getProfile", "key": key,}

        r = self._req(data)

        return r

    def getAncestors(self, key, depth=None):
        """getAncestors() retrieves the ancestsors of a WikiTree person."""
        data = {"action": "getAncestors", "key": key,}

        if depth:
            data["depth"] = depth

        # fields is not recognized for ancestors
        # data["fields"] = "Name,LongName"

        r = self._req(data)

        return r

    __relativeChoices = ('getParents', 'getSpouses', 'getSiblings', 'getChildren',)

    def getRelatives(self, keys, **kwargs):
        """getRelatives() retrieves the relatives of a WikiTree person."""
        if not isinstance(keys, (list, tuple, set, frozenset,)):
            keys = [keys]
        data = {"action": "getRelatives", "keys": keys}

        for k in kwargs.keys():
            if k not in self.__relativeChoices:
                print("WARNING: invalid parameter to getRelatives:", k)
                del kwargs[k]
            else:
                kwargs[k] = int(kwargs[k])

        if len(kwargs) > 0:
            data.update(kwargs)

        r = self._req(data)

        return r

    def getPersonFSConnections(self, key):
        """getPersonFSConnections() retrieves the links between a WikiTree
        person and FamilySearch person(s).
        """

        data = {"action": "getPersonFSConnections", "key": key,}

        r = self._req(data)

        return r

if __name__ == "__main__":
    print("no unit tests")
