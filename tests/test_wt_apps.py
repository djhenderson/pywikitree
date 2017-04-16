#! python3
# -*- coding:utf-8 -*-

# test the WikiTree apps interface

from __future__ import print_function, unicode_literals

import pprint
# import requests
# import simplejson as json
from simplejson.scanner import JSONDecodeError

try:
    from wt_apps import WT_Apps
except ImportError:
    print("Warning: modifing sys.path")
    import sys, os
    if os.path.exists("wt_apps.py"):
        sys.path.insert(0, ".")  # assume running in pywikitree
    else:
        sys.path.append("..")  # assume running in pywikitree/tests
    from wt_apps import WT_Apps

try:
    from secrets import *
except ImportError:
    WT_USER = None
    WT_PASS = None

pp = pprint.PrettyPrinter(indent=2, width=120, depth=4)

url = "https://apps.wikitree.com/api.php"

default_format = "json"
verbosity = 2
apps = WT_Apps(url=url, default_format=default_format, verbosity=verbosity)  # json | xmlfm

try_key = "Henderson-6225"  # Thomas Henderson (my grand father)
try_key = "Henderson-7140"  # James Henderson (my great grand father)
try_key = "Churchill-4"  #  Sir Winston Leonard Spencer Churchill KG OM CH

try_keys = [try_key]

blank_fields = [f.strip() for f in """\
BirthDate, BirthLocation, BirthNamePrivate,
DeathDate, DeathLocation,
Father, FirstName,
Gender,
Id, IsLiving,
LastNameAtBirth, LastNameCurrent, LastNameOther, LongNamePrivate,
Manager, MiddleName, Mother,
Name, Nicknames,
Photo, PhotoData, Prefix,
RealName,
ShortName, Suffix
""".split(",")]
blank_fields.sort()

star_fields = [f.strip() for f in """\
BirthDate, BirthDateDecade, BirthLocation, BirthNamePrivate,
Children,
DeathDate, DeathDateDecade, DeathLocation,
Father, FirstName,
Gender,
Id, IsLiving,
LastNameAtBirth, LastNameCurrent, LastNameOther, LongNamePrivate,
Manager, MiddleName, Mother,
Name, Nicknames,
Parents, Photo, PhotoData, Prefix,
Privacy, Privacy_IsAtLeastPublic, Privacy_IsOpen, Privacy_IsPrivate,
Privacy_IsPublic, Privacy_IsSemiPrivate, Privacy_IsSemiPrivateBio,
RealName,
ShortName, Siblings, Spouses, Suffix
""".split(",")]
star_fields.sort()

all_fields = [f.strip() for f in """\
BirthDate, BirthDateDecade, BirthLocation,
Children,
DeathDate, DeathDateDecade, DeathLocation,
Derived.BirthNamePrivate, Derived.LongNamePrivate, Derived.ShortName,
Father, FirstName,
Gender,
Id, IsLiving,
LastNameAtBirth, LastNameCurrent, LastNameOther,
Manager, MiddleName, Mother,
Name, Nicknames,
Parents, Photo, PhotoData, Prefix,
Privacy, Privacy_IsAtLeastPublic, Privacy_IsOpen, Privacy_IsPrivate,
Privacy_IsPublic, Privacy_IsSemiPrivate, Privacy_IsSemiPrivateBio,
RealName,
Siblings, Spouses, Suffix
""".split(",")]
all_fields.sort()

rel_fields = "Children,Parents,Siblings,Spouses".split(',')

space_fields = "Id,IsSpace,PageId,Privacy,Timestamp,Title".split(",")


def header(msg):
    print("\n%s %s %s\n" % ("*" * 20, msg, "*" * 20,))


def hr():
    print("\n%s\n" % ("=" * 80,))


def try_help():
    header("help")

    r = apps.getHelp()
    hr()

    print("r.headers:", type(r.headers))
    pp.pprint(dict(r.headers))
    pp.pprint(r.text)
    hr()

    try:
        j = r.json()
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", type(e), e)
        pp.pprint(r)
    except Exception as e:
        print("Exception:", type(e), e)
        raise
    hr()


def try_login():
    header("login")

    # provide your own WikiTree.com credentials
    wt_user = os.environ.get("WT_USER", WT_USER)
    wt_pass = os.environ.get("WT_PASS", WT_PASS)

    r = apps.login(wt_user, wt_pass)
    hr()

    print("r.headers:", type(r.headers))
    pp.pprint(dict(r.headers))
    hr()

    try:
        j = r.json()
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", type(e), e)
    except Exception as e:
        print("Exception:", type(e), e)
        raise
    hr()


def try_getPersonJSON():

    header("getPerson")

    # fields = ''
    # fields = "*"
    fields = ','.join(all_fields)

    r = apps.getPerson(try_key, fields)
    hr()

    try:
        j = r.json()
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
        print("r.text:", type(r.text))
        print("v" * 80)
        print(r.text)
        print("^" * 80)
        raise
    except Exception as e:
        print("Exception:", e)
        raise

    # print("j:", type(j))
    # print("j[]:", [type(jj) for jj in j])
    print("j[0].keys()", list(j[0].keys()))
    print('j[0]["person"].keys()', sorted(j[0]["person"].keys()))
    pp.pprint(j)
    hr()

    if fields == '':
        s_fields = s_blank_fields = set(blank_fields)
    elif fields == '*':
        s_fields = s_star_fields = set(star_fields)
    else:
        s_fields = s_all_fields = set(all_fields)

    r_fields = set(j[0]['person'].keys())

    common = r_fields.intersection(s_fields)
    not_rcvd = s_fields.difference(r_fields)
    not_rqst= r_fields.difference(s_fields)

    print("\n   fields:", fields)
    print("\n s_fields:", sorted(list(s_fields)))
    print("\n   common:", sorted(list(common)))
    print("\n not_rcvd:", sorted(list(not_rcvd)))
    print("\n not_rqst:", sorted(list(not_rqst)))
    hr()

def try_getPersonXML():

    header("getPerson")

    try_key = 5589 # Churchill-4

    fields = ''
    # fields = "*"
    # fields = ','.join(all_fields)

    r = apps.getPerson(try_key, fields)
    hr()

    print("type(r):", type(r))
    print("r:", r)

    try:
        j = r.text
    except Exception as e:
        print("Exception:", e)
        raise

    print("type(j):", type(j))
    print("j:", j)
    # print("j[]:", [type(jj) for jj in j])
    # print("j[0].keys()", list(j[0].keys()))
    # print('j[0]["person"].keys()', sorted(j[0]["person"].keys()))
    pp.pprint(j)
    hr()


def try_getPerson():
    if default_format == "json":
        try_getPersonJSON()
    else:
        try_getPersonXML()


def try_getPrivacyLevels():
    header("getPrivacyLevels")

    r = apps.getPrivacyLevels()
    hr()

    try:
        j = r.json()
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
        'order': 'page_touched',
        'offset': 0,
        'limit': 4,
    }

    r = apps.getWatchlist(**params)
    hr()

    try:
        j = r.json()
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
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()


def try_getAncestors():
    header("getAncestors")
    depth = 1  # 0=self(1), 1+=parent(3), 2+=grandparents(7), 3+=great-grandparents

    r = apps.getAncestors(try_key, depth)
    hr()

    try:
        j = r.json()
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()


def try_getAncestorsFields(fields=None):
    header("getAncestors")
    depth = 3

    r = apps.getAncestors(try_key, depth)
    hr()

    try:
        j = r.json()

        for jj in j:
            k = jj["ancestors"]
            for kk in k:
                wid = kk["Id"]
                name = kk["Name"]
                longname = kk.get("LongName", kk.get("LongNamePrivate", "[no name]"))
                longname = longname.replace("  ", " ")
                print("%9s %-16s %s" % (wid, name, longname,))

        # hr()
        # pp.pprint(j)
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
        pp = pprint.PrettyPrinter(indent=2, width=120, depth=7)  # note depth
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()


def try_getPersonFSConnections():
    header("getPersonFSConnections")

    r = apps.getPersonFSConnections(try_key)
    hr()

    try:
        j = r.json()
        pp.pprint(j)
    except JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("Exception:", e)
        raise
    hr()


def try_logout():
    header("logout")
    apps.logout()
    hr()


if __name__ == '__main__':

    def main():
        # hr()
        # print("session headers")
        # pp.pprint(apps._session.headers)
        # hr()
        # try_help()  #
        # try_login()  #
        # try_getPerson()  # try_key
        # try_getPrivacyLevels()  #
        # try_getBio()  # try_key
        # try_getWatchlist()  #
        # try_getProfile()  # try_key
        try_getAncestors()  # try_key
        # try_getAncestorsFields()  # try_key
        # try_getRelatives()  # try_keys
        # try_getPersonFSConnections()  # try_key
        # try_logout()  #

    main()
