#! python3
# -*- coding:utf-8 -*-

from __future__ import print_function, unicode_literals

import pprint
import requests
import simplejson as json
from simplejson.scanner import JSONDecodeError


try:
    import wt_apps
except ImportError:
    print("Warning: modifing sys.path")
    import sys
    sys.path.append("..") # assume running in pywikitree/tests
    import wt_apps

from wt_apps import WT_Apps

pp = pprint.PrettyPrinter(indent=4, width=120, depth=4)
url = "https://apps.wikitree.com/api.php"

apps = WT_Apps(url=url, default_format="json")  # json | xmlfm

# 6
try_key = "Côté-179"  # [Jean Côté]
try_keys = ["Côté-179",]  # [Jean Côté]

def header(msg):
    print("\n%s %s %s\n" % ("*"*20, msg, "*"*20,))

def hr():
    print("\n%s\n" % ("="*80,))

def try_login():
    header("login")

    # provide your own WikiTree.com credentials
    email = "WikiTreeUser"
    password = "WikiTreePassword"

    r = apps.login(email, password)
    hr()

    print("r.headers:", type(r.headers))
    pp.pprint(dict(r.headers))
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", type(e), e)
    except Exception as e:
        print("Exception:", type(e), e)
        raise
    hr()

def try_getPerson():

    header("getPerson")
    fields = "*"

    r = apps.getPerson(try_key, fields)
    #hr()

    try:
        j = r.json()
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
        print("r.text:", type(r.text))
        print("v"*80)
        print(r.text)
        print("^"*80)
    except Exception as e:
        print("Exception:", e)
        raise

    #print("j:", type(j))
    #print("j[]:", [type(jj) for jj in j])
    #print("j[0].keys()", list(j[0].keys()))
    #print("type(j[0].values())", [type(jj) for jj in j[0].values()])
    pp.pprint(j)
    hr()

def try_getPrivacyLevels():
    header("getPrivacyLevels")

    r = apps.getPrivacyLevels()
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getBio():
    header("getBio")
    params = {
        }

    r = apps.getBio(try_key, **params)
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getWatchlist():
    header("getWatchlist")
    params = {
        'getPerson': True,
        'getSpace': False,
        'onlyLiving': False,
        'excludeLiving': False,
        'order': '',
        'offset': 0,
        'limit': 10,
        }

    r = apps.getWatchlist(**params)
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getProfile():
    header("getProfile")

    r = apps.getProfile(try_key)
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getAncestors():
    header("getAncestors")
    depth = 2

    r = apps.getAncestors(try_key, depth)
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getAncestorsFields(fields=None):
    header("getAncestors")
    depth = None

    r = apps.getAncestors(try_key, depth)
    hr()

    try:
        j = r.json()

        for jj in j:
            k = jj["ancestors"]
            for kk in k:
                wid = kk["Id"]
                name = kk["Name"]
                longname = kk.get("LongName", kk.get("LongNamePrivate","[no name]"))
                longname = longname.replace("  ", " ")
                print("%-8s %-16s %s" % (wid, name, longname,))
        hr()

        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getRelatives():
    header("getRelatives")

    x_try_keys = ",".join(try_keys)
    r = apps.getRelatives(x_try_keys, getParents=True, getSpouses=False, getSiblings=False, getChildren=False)
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp = pprint.PrettyPrinter(indent=4, width=120, depth=7) # note depth
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_getPersonFSConnections():
    header("getPersonFSConnections")

    r = apps.getPersonFSConnectio(try_key)
    hr()

    try:
        j = r.json()
        #print("r.json():", type(j))
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()

def try_logout():
    r = apps.logout()

if __name__ == '__main__':

    def main():
        #try_login()  #
        try_getPerson() # try_key
        #try_getPrivacyLevels()  #
        #try_getBio()  # try_key
        #try_getWatchlist()  #
        #try_getProfile()  # try_key
        #try_getAncestors()  # try_key
        #try_getAncestorsFields()  # try_key
        #try_getRelatives()  # try_keys
        #try_getPersonFSConnections()  # try_key
        #try_logout()  #

    main()
