#! python3
# -*- coding:utf-8 -*-

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

pp = pprint.PrettyPrinter(indent=2, width=120, depth=4)

url = "https://apps.wikitree.com/api.php"

apps = WT_Apps(url=url, default_format="json", verbosity=2)  # json | xmlfm

try_key = "Henderson-6225"  # Thomas Henderson
#try_key = "Côté-179"  # Jean Côté

try_keys = [try_key]

blank_fields = [f.strip() for f in """\
BirthDate, BirthLocation, BirthNamePrivate,
Creator,
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

star_fields = [f.strip() for f in """\
BirthDate, BirthDateDecade, BirthLocation, BirthName, BirthNamePrivate,
Children, Creator,
DeathDate, DeathDateDecade, DeathLocation,
Father, FirstName,
Gender,
Id, IsLiving,
LastNameAtBirth, LastNameCurrent, LastNameOther, LongName, LongNamePrivate,
Manager, MiddleName, Mother,
Name, Nicknames,
Parents, Photo, PhotoData, Prefix,
Privacy, Privacy_IsAtLeastPublic, Privacy_IsOpen, Privacy_IsPrivate,
Privacy_IsPublic, Privacy_IsSemiPrivate, Privacy_IsSemiPrivateBio,
RealName,
ShortName, Siblings, Spouses, Suffix
""".split(",")]

all_fields = [f.strip() for f in """\
Id, Name, FirstName, MiddleName, LastNameAtBirth, LastNameCurrent,
Nicknames, LastNameOther, RealName, Prefix, Suffix,
Gender, BirthDate, DeathDate, BirthLocation, DeathLocation,
BirthDateDecade, DeathDateDecade, Photo, IsLiving, Privacy,
Mother, Father, Parents, Children, Siblings, Spouses,
Derived.ShortName, Derived.BirthNamePrivate, Derived.LongNamePrivate,
Creator, Manager, Touched
""".split(",")]

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
    wt_user = os.environ.get("WT_USER", "WT_USER")
    wt_pass = os.environ.get("WT_PASS", "WT_PASS")

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


def try_getPerson():

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
    except Exception as e:
        print("Exception:", e)
        raise

    # print("j:", type(j))
    # print("j[]:", [type(jj) for jj in j])
    print("j[0].keys()", list(j[0].keys()))
    print('j[0]["person"].keys()', sorted(j[0]["person"].keys()))
    pp.pprint(j)
    hr()


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
        try_login()  #
        try_getPerson()  # try_key
        # try_getPrivacyLevels()  #
        # try_getBio()  # try_key
        # try_getWatchlist()  #
        # try_getProfile()  # try_key
        # try_getAncestors()  # try_key
        # try_getAncestorsFields()  # try_key
        # try_getRelatives()  # try_keys
        # try_getPersonFSConnections()  # try_key
        try_logout()  #

    main()
