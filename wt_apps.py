#! python3
# -*- coding:utf-8 -*-

"""
wt_apps.py provides an interface to the WikiTree APPS API.

This code is designed to work with
Python 2.7
and
Python 3.4, 3.5, 3.6 and 3.7.

It has been tested
on cygwin
    with python2 2.7.13 and python3 3.6.1
and on Windows 7
    with python 2.7.13, and python 3.6.1
and on Ubuntu Linux 18.04LTS
    with python 3.7
"""

from __future__ import print_function, unicode_literals

__version__ = "0.1.3"

import logging
import pprint
import requests
from simplejson.scanner import JSONDecodeError

# Enabling debugging at http.client level (requests->urllib3->http.client)
# you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# the only thing missing will be the response.body which is not logged.
# try:  # for Python 3
#     from http.client import HTTPConnection
# except ImportError:
#     from httplib import HTTPConnection
# HTTPConnection.debuglevel = 1

# you need to initialize logging, otherwise you will not see anything from requests
logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

_pp = pprint.PrettyPrinter(indent=2, width=120, depth=4)


class WT_Apps(object):
    """WikiTree Apps interface
    """

    _url = "https://apps.wikitree.com/api.php"
    _default_format = "json"
    _format = _default_format
    _session = None
    _verbosity = 0

    # class members
    __privacy_init = False
    __Privacy2Levels = {}
    __Levels2Privacy = {}

    @classmethod
    def Privacy2Level(cls, privacy):
        """Privacy2Level() translates a privacy level name
        to a numeric privacy level.
        """

        if not cls.__privacy_init:
            raise RuntimeError("Privacy data not initialized.")

        return cls.__Privacy2Levels.get(privacy, 0)

    @classmethod
    def Level2Privacy(cls, level):
        """Level2Privacy() translats a numeric privacy level to
        a privacy level name.
        """

        if not cls.__privacy_init:
            raise RuntimeError("Privacy data not initialized.")

        return cls.__Levels2Privacy.get(level, "No description")

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
                self._format = self._default_format = default_format
            else:
                print("WARNING: invalid default_format ignored:" + repr(default_format))
                self._format = self._default_format = "json"

        if verbosity:
            self._verbosity = int(verbosity)

        self._init_session()

        if not type(self).__privacy_init:
            self.getPrivacyLevels(_initialize=True)

    def _init_session(self):
        """_init_session() is a private method to perfom command
        session initializaton actions.
        As this creates a session without a logged in user, only
        public profile content is available, until a login is
        performed on this session.
        """

        s = self._session = requests.Session()

        s.headers['Accept-charset'] = "utf-8"

        if self._format == "json":
            pass
        elif self._format == 'xmlfm':
            s.headers['Accept'] = "application/xml"
            s.headers['Accept'] = "text/xml"
        else:
            raise ValueError("Invalid format: " + repr(self._format))

    def _req(self, data, headers={}):
        """_req() is a private method to perform the
        https request to the WikiTree Apps API.
        It constructs and posts the request,
        and checks the status of the result.
        """

        if self._verbosity > 1:
            print("url:", self._url)
            print("data:", end=' ')
            _pp.pprint(data)

        if self._session is None:
            self._init_session()

        r = self._session.post(self._url, data=data)

        if r.status_code != requests.codes.ok:
            print("url:", self._url)
            print("data:", end=' ')
            _pp.pprint(data)
            r.raise_for_status()

        return r

    def getHelp(self):
        """getHelp()
        """

        data = {"action": "help", "format": self._format}

        r = self._req(data)

        return r

    def login(self, email, password):
        """login() logs you into WikiTree using your email address and password
        The email address and password are the same as you use to log into
        your WikiTree profile and private web pages.
        """

        data = {"action": "login", "format": self._format, "email": email, "password": password}

        r = self._req(data)

        return r

    def logout(self):
        """logout() logs you out of WikiTree.
        The API has no logout function. The only thing we can do
        is remove the session, which automatically retained our
        login credentials and authentication details.
        No further requests can be performed using the current
        login credentials. You will be an anonymous guest.
        """

        self._session = None

    def getPerson(self, key, fields=None):
        """getPerson() gets a person from the WikiTree api.
        Provide the person key, either the LNAB-# or numeric profile id.
        """

        if fields is None:
            fields = ""

        data = {"action": "getPerson", "format": self._format, "key": key, "fields": fields}

        r = self._req(data)

        return r

    __privacyLevelsOptions = ("format",)

    def getPrivacyLevels(self, _initialize=False, **kwargs):
        """getPrivacyLevels() retrieves the name and number of the
        WikiTree privacy levels.
        The _initialize parameter is used during class instance
        initialization to retrieve privacy levels used by the
        Privacy2Level() and Level2Privacy() class methods.
        """

        data = {"action": "getPrivacyLevels", "format": self._format}

        for k, v in kwargs:
            if k not in self.__privacyLevelsOptions:
                print("WARNING: invalid parameter to getPrivacyLevels:", repr(k))
                del kwargs[k]

        if len(kwargs) > 0:
            data.update(kwargs)

        if _initialize:
            data["format"] = "json"  # force JSON request

        r = self._req(data)

        if _initialize:
            try:
                # make sure to work with class data, not instance data
                type(self).__Privacy2Levels = {}
                type(self).__Levels2Privacy = ()
                j = r.json()
                type(self).__Privacy2Levels = j[0].copy()
                type(self).__Levels2Privacy = {v: k for k, v in type(self).__Privacy2Levels.items()}
                type(self).__privacy_init = True
            except JSONDecodeError as e:
                print("Exception(ignored):", e)
            except Exception as e:
                print("Exception:", e)
                raise

        return r

    __bioOptions = {"key"}

    def getBio(self, key=None, **kwargs):
        """getBio() retrieves the Biography for a WikiTree person profile.
        """

        data = {"action": "getBio", "format": self._format, "key": key}

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
        """getWatchlist() retrieves your WikiTree watchlist.
        See the WT app documentation for options to filter
        the watchlist, order it, and page through it.
        """

        data = {"action": "getWatchlist", "format": self._format}

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
                    # the API does not understand bool type values
                    # so convert False -> 0 and True -> 1
                    kwargs[k] = int(v)

        if len(kwargs) > 0:
            data.update(kwargs)

        r = self._req(data)

        return r

    def getProfile(self, key):
        """getProfile() retrieves a WikiTree profile.
        It will retrieve both person and space profiles.
        Provide a person key, either the LNAB-# or numeric id,
        or a numeric space id.
        """

        data = {"action": "getProfile", "format": self._format, "key": key}

        r = self._req(data)

        return r

    def getAncestors(self, key, depth=None):
        """getAncestors() retrieves the ancestors of a WikiTree person.
        Default depth is 5.
        """

        data = {"action": "getAncestors", "format": self._format, "key": key, "depth": 5}

        if depth:
            data["depth"] = depth

        # fields is not recognized for ancestors
        # data["fields"] = "Name,LongName"

        r = self._req(data)

        return r

    __relativeChoices = ('getParents', 'getSpouses', 'getSiblings', 'getChildren',)

    def getRelatives(self, keys, **kwargs):
        """getRelatives() retrieves the relatives of a WikiTree person.
        """

        # for ease of use, convert a single key into a list of keys
        if not isinstance(keys, (list, tuple, set, frozenset,)):
            keys = [keys]

        data = {"action": "getRelatives", "format": self._format, "keys": keys}

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
        """getPersonFSConnections() retrieves the links between
        a WikiTree person and FamilySearch person(s).
        """

        data = {"action": "getPersonFSConnections", "format": self._format, "key": key}

        r = self._req(data)

        return r


if __name__ == "__main__":
    print("no unit tests here. see ./tests")
