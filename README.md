This package is a Python interface to the WikiTree Apps API

Currently, documentation is contained in docstrings in the source.
Documentation for the WikiTree API is found at the
http://apps.wikitree.com/apps/
page
which references the more detailed
http://www.wikitree.com/wiki/API_Documentation
page.

The following console session illustrates retrieving a public person
without logging on to WikiTree, and using Python 3.
When using Python 2, all returned strings are unicode.

Using python 3, get setup to use the API

    >>> import wt_apps, pprint, os
    >>> pp = pprint.PrettyPrinter(indent=2, width=120, depth=4)
    >>> apps = wt_apps.WT_Apps()
    >>> try:
    ...     from secrets import *
    ... except ImportError:
    ...     WT_USER = None
    ...     WT_PASS = None
    ...

We are not yet logged in, so we will only see public data.

Retrieve a well known person.

    >>> r = apps.getPerson("Churchill-4", "*")
    >>> j = r.json()
    >>> pp.pprint(j)
    [ { 'person': { 'BirthDate': '1874-11-30',
                    'BirthDateDecade': '1870s',
                    'BirthLocation': 'Blenheim, Oxfordshire, England',
                    'BirthNamePrivate': 'Winston Churchill KG OM CH',
                    'Children': {'5596': {...}, '5597': {...}, '5598': {...}, '5599': {...}, '5600': {...}},
                    'DeathDate': '1965-01-24',
                    'DeathDateDecade': '1960s',
                    'DeathLocation': 'Bladon, Oxfordshire, England',
                    'Father': 5584,
                    'FirstName': 'Winston',
                    'Gender': 'Male',
                    'Id': 5589,
                    'IsLiving': 0,
                    'LastNameAtBirth': 'Churchill',
                    'LastNameCurrent': 'Churchill',
                    'LastNameOther': '',
                    'LongNamePrivate': 'Winston L. Churchill KG OM CH',
                    'Manager': 4677796,
                    'MiddleName': 'Leonard Spencer',
                    'Mother': 5554,
                    'Name': 'Churchill-4',
                    'Nicknames': '',
                    'Parents': {'5554': {...}, '5584': {...}},
                    'Photo': 'Winston churchill.jpg',
                    'PhotoData': None,
                    'Prefix': 'Sir',
                    'Privacy': 60,
                    'Privacy_IsAtLeastPublic': True,
                    'Privacy_IsOpen': True,
                    'Privacy_IsPrivate': False,
                    'Privacy_IsPublic': False,
                    'Privacy_IsSemiPrivate': False,
                    'Privacy_IsSemiPrivateBio': False,
                    'RealName': 'Winston',
                    'ShortName': 'Winston Churchill KG OM CH',
                    'Siblings': {'5592': {...}},
                    'Spouses': {'5595': {...}},
                    'Suffix': 'KG OM CH'},
        'status': 0,
        'user_name': 'Churchill-4'}]
    >>>

Grab the privacy name/number translation data.

    >>> r = apps.getPrivacyLevels()
    >>> j = r.json()
    >>> pp.pprint(j)
    [ { 'OPEN': 60,
        'PRIVATE': 20,
        'PUBLIC': 50,
        'SEMIPRIVATE_BIO': 30,
        'SEMIPRIVATE_BIOTREE': 40,
        'SEMIPRIVATE_TREE': 35,
        'UNLISTED': 10}]
    >>>

Download the biography, and display the first two lines

    >>> r = apps.getBio("Churchill-4")
    >>> j = r.json()
    >>> bio = j[0]["bio"]
    >>> j[0]["bio"] = "See below\nfor a few lines\nfrom the bio.\n"
    >>> pp.pprint(j)
    [{'bio': 'See below\nfor a few lines\nfrom the bio.\n', 'page_name': 'Churchill-4', 'status': 0, 'user_id': 5589}]
    >>>
    >>> print("\n".join([x.strip("\n") for x in bio.split("\n")][:2]))
    [[Category:This Day In History April 24]]
    [[Category: This Day In History November 30]] [[Category: This Day In History January 24]] [[Category: British Prime Ministers]] [[Category: World War II Political Leaders]][[Category: Historians]] [[Category: Famous Politicians of the 20th Century]] [[Category: Knights Companion of the Garter]] {{Notables}}

    >>>

Get ancestors, depth=1 gives person and parents, depth=2 adds grandparents, etc.

    >>> r = apps.getAncestors("Churchill-4", depth=1)
    >>> j = r.json()
    >>> for p in j[0]['ancestors']: del p['Touched'] # changes on read!
    >>> pp.pprint(j)
    [ { 'ancestors': [ { 'BirthDate': '1874-11-30',
                         'BirthDateDecade': '1870s',
                         'BirthLocation': 'Blenheim, Oxfordshire, England',
                         'BirthNamePrivate': 'Winston Churchill KG OM CH',
                         'DeathDate': '1965-01-24',
                         'DeathDateDecade': '1960s',
                         'DeathLocation': 'Bladon, Oxfordshire, England',
                         'Father': 5584,
                         'FirstName': 'Winston',
                         'Gender': 'Male',
                         'Id': 5589,
                         'IsLiving': 0,
                         'IsPerson': 1,
                         'LastNameAtBirth': 'Churchill',
                         'LastNameCurrent': 'Churchill',
                         'LastNameOther': '',
                         'LongNamePrivate': 'Winston L. Churchill KG OM CH',
                         'Manager': 4677796,
                         'MiddleName': 'Leonard Spencer',
                         'Mother': 5554,
                         'Name': 'Churchill-4',
                         'Nicknames': '',
                         'Photo': 'Winston churchill.jpg',
                         'PhotoData': None,
                         'Prefix': 'Sir',
                         'Privacy': 60,
                         'Privacy_IsAtLeastPublic': True,
                         'Privacy_IsOpen': True,
                         'Privacy_IsPrivate': False,
                         'Privacy_IsPublic': False,
                         'Privacy_IsSemiPrivate': False,
                         'Privacy_IsSemiPrivateBio': False,
                         'RealName': 'Winston',
                         'ShortName': 'Winston Churchill KG OM CH',
                         'Suffix': 'KG OM CH'},
                       { 'BirthDate': '1849-02-13',
                         'BirthDateDecade': '1840s',
                         'BirthLocation': None,
                         'BirthNamePrivate': 'Randolph Spencer-Churchill',
                         'DeathDate': '1895-01-24',
                         'DeathDateDecade': '1890s',
                         'DeathLocation': None,
                         'Father': 5586,
                         'FirstName': 'Randolph',
                         'Gender': 'Male',
                         'Id': 5584,
                         'IsLiving': None,
                         'IsPerson': 1,
                         'LastNameAtBirth': 'Spencer-Churchill',
                         'LastNameCurrent': 'Spencer-Churchill',
                         'LastNameOther': None,
                         'LongNamePrivate': 'Randolph H. Spencer-Churchill',
                         'Manager': 5932170,
                         'MiddleName': 'Henry',
                         'Mother': 5587,
                         'Name': 'Spencer-Churchill-1',
                         'Nicknames': None,
                         'Photo': 'Lord Randolph Churchill.jpg',
                         'PhotoData': None,
                         'Prefix': None,
                         'Privacy': 60,
                         'Privacy_IsAtLeastPublic': True,
                         'Privacy_IsOpen': True,
                         'Privacy_IsPrivate': False,
                         'Privacy_IsPublic': False,
                         'Privacy_IsSemiPrivate': False,
                         'Privacy_IsSemiPrivateBio': False,
                         'RealName': 'Randolph',
                         'ShortName': 'Randolph Spencer-Churchill',
                         'Suffix': ''},
                       { 'BirthDate': '1854-01-09',
                         'BirthDateDecade': '1850s',
                         'BirthLocation': None,
                         'BirthNamePrivate': 'Jennie Jerome CI',
                         'DeathDate': '1921-06-09',
                         'DeathDateDecade': '1920s',
                         'DeathLocation': None,
                         'Father': 5555,
                         'FirstName': 'Jeanette',
                         'Gender': 'Female',
                         'Id': 5554,
                         'IsLiving': None,
                         'IsPerson': 1,
                         'LastNameAtBirth': 'Jerome',
                         'LastNameCurrent': 'Churchill',
                         'LastNameOther': None,
                         'LongNamePrivate': 'Jennie (Jerome) Churchill CI',
                         'Manager': 4840833,
                         'MiddleName': '',
                         'Mother': 5575,
                         'Name': 'Jerome-1',
                         'Nicknames': None,
                         'Photo': 'Lady_Randolph.jpg',
                         'PhotoData': None,
                         'Prefix': None,
                         'Privacy': 60,
                         'Privacy_IsAtLeastPublic': True,
                         'Privacy_IsOpen': True,
                         'Privacy_IsPrivate': False,
                         'Privacy_IsPublic': False,
                         'Privacy_IsSemiPrivate': False,
                         'Privacy_IsSemiPrivateBio': False,
                         'RealName': 'Jennie',
                         'ShortName': 'Jennie (Jerome) Churchill CI',
                         'Suffix': 'CI'}],
        'status': 0,
        'user_name': 'Churchill-4'}]
    >>>

Get relatives, just the spouses and siblings in this case.

    >>> pp = pprint.PrettyPrinter(indent=2, width=120, depth=5)
    >>> r = apps.getRelatives("Churchill-4", getSpouses=1, getSiblings=1)
    >>> j = r.json()
    >>> # for p in j[0]['items']: del p['Touched'] # changes on read!
    >>> pp.pprint(j)
    [ { 'items': [ { 'key': 'Churchill-4',
                     'person': { 'BirthDate': '1874-11-30',
                                 'BirthDateDecade': '1870s',
                                 'BirthLocation': 'Blenheim, Oxfordshire, England',
                                 'BirthNamePrivate': 'Winston Churchill KG OM CH',
                                 'DeathDate': '1965-01-24',
                                 'DeathDateDecade': '1960s',
                                 'DeathLocation': 'Bladon, Oxfordshire, England',
                                 'Father': 5584,
                                 'FirstName': 'Winston',
                                 'Gender': 'Male',
                                 'Id': 5589,
                                 'IsLiving': 0,
                                 'IsPerson': 1,
                                 'LastNameAtBirth': 'Churchill',
                                 'LastNameCurrent': 'Churchill',
                                 'LastNameOther': '',
                                 'LongNamePrivate': 'Winston L. Churchill KG OM CH',
                                 'Manager': 4677796,
                                 'MiddleName': 'Leonard Spencer',
                                 'Mother': 5554,
                                 'Name': 'Churchill-4',
                                 'Nicknames': '',
                                 'Photo': 'Winston churchill.jpg',
                                 'PhotoData': None,
                                 'Prefix': 'Sir',
                                 'Privacy': 60,
                                 'Privacy_IsAtLeastPublic': True,
                                 'Privacy_IsOpen': True,
                                 'Privacy_IsPrivate': False,
                                 'Privacy_IsPublic': False,
                                 'Privacy_IsSemiPrivate': False,
                                 'Privacy_IsSemiPrivateBio': False,
                                 'RealName': 'Winston',
                                 'ShortName': 'Winston Churchill KG OM CH',
                                 'Siblings': {...},
                                 'Spouses': {...},
                                 'Suffix': 'KG OM CH',
                                 'Touched': '20170211033528'},
                     'user_id': 5589,
                     'user_name': 'Churchill-4'}],
        'status': 0}]
    >>>

Try to retrieve the FamilySearch connections. This will fail because we are not logged in.

    >>> r = apps.getPersonFSConnections("Churchill-4")
    >>> j = r.json()
    >>> pp.pprint(j)
    [{'status': 'Permission denied', 'user_name': 'Churchill-4'}]
    >>>

Illustrate login failure.
Use an invalid password, so as to see the error result.

    >>> r = apps.login("MissingSurname-1", "InvalidPassword")
    >>> j = r.json()
    >>> pp.pprint(j)
    {'login': {'result': 'Illegal', 'wait': 1}}
    >>>

Try logging in with user and password from environment.
Provide your own WikiTree.com credentials.
Use "SET WT_USER=your_user_id" or "export WT_USER=your_user_id", etc.
Or create a "secrets.py" file with lines with WT_USER=your_user_id, etc.

    >>> wt_user = os.environ.get("WT_USER", WT_USER)
    >>> wt_pass = os.environ.get("WT_PASS", WT_PASS)
    >>> r = apps.login(wt_user, wt_pass)
    >>> j = r.json()
    >>> del j['login']['token']  # hide the token (it won't match)
    >>> del j['login']['userid'] # hide the userid (it won't match)
    >>> del j['login']['username'] # hide the userid (it won't match)
    >>> pp.pprint(j)
    {'login': {'result': 'Success'}}
    >>>

Try to retrieve the FamilySearch connections while logged in.

    >>> r = apps.getPersonFSConnections("Churchill-4")
    >>> j = r.json()
    >>> pp.pprint(j)
    [{'status': 'Permission denied', 'user_name': 'Churchill-4'}]
    >>>

Illustrate logging off.

    >>> apps.logout()
    >>>

Our session is ended.
