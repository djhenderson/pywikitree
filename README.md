This package is a Python interface to the WikiTree Apps API

Currently, documentation is contained in docstrings in the source.
Documentation for the WikiTree API is found at the
http://apps.wikitree.com/apps/
page
which references the more detailed
http://www.wikitree.com/wiki/API_Documentation
page.

The following console session illustrates retrieving a public person
without logging on to WikiTree using Python 3. When using
Python 2, all returned strings are unicode.

Using python 3, get setup to use the API

    >>> import wt_apps, pprint
    >>> pp = pprint.PrettyPrinter(indent=2, width=120, depth=4)
    >>> apps = wt_apps.WT_Apps()
    >>>

We are not yet logged in, so we will only see public data.

Retrieve a well known person.

    >>> r = apps.getPerson("Côté-179", "*")
    >>> j = r.json()
    >>> pp.pprint(j)
    [ { 'person': { 'BirthDate': '1644-02-25',
                    'BirthDateDecade': '1640s',
                    'BirthLocation': 'Paroisse Notre Dame, Québec, Québec',
                    'BirthNamePrivate': 'Jean Côté',
                    'Children': { '3984864': {...},
                                  '4552796': {...},
                                  '4678737': {...},
                                  '4679329': {...},
                                  '6784208': {...},
                                  '6784701': {...},
                                  '7938357': {...},
                                  '7938361': {...},
                                  '7938364': {...},
                                  '7938371': {...},
                                  '7938381': {...},
                                  '7938420': {...},
                                  '7938428': {...},
                                  '7938434': {...},
                                  '7938443': {...},
                                  '7938540': {...},
                                  '7938547': {...},
                                  '7938555': {...},
                                  '7938575': {...},
                                  '8735045': {...}},
                    'Creator': 3833213,
                    'DeathDate': '1722-03-26',
                    'DeathDateDecade': '1720s',
                    'DeathLocation': "L'Ange-Gardien, Montmorency, Qc, Canada",
                    'Father': 4149374,
                    'FirstName': 'Jean',
                    'Gender': 'Male',
                    'Id': 4149371,
                    'IsLiving': 0,
                    'LastNameAtBirth': 'Côté',
                    'LastNameCurrent': 'Côté',
                    'LastNameOther': 'Cotte, Costé, dit Le Frisé Landroche',
                    'LongNamePrivate': 'Jean Côté',
                    'Manager': 2046555,
                    'MiddleName': '',
                    'Mother': 1232214,
                    'Name': 'Côté-179',
                    'Nicknames': '',
                    'Parents': {'1232214': {...}, '4149374': {...}},
                    'Photo': 'Cote-179.jpg',
                    'PhotoData': None,
                    'Prefix': '',
                    'Privacy': 60,
                    'Privacy_IsAtLeastPublic': True,
                    'Privacy_IsOpen': True,
                    'Privacy_IsPrivate': False,
                    'Privacy_IsPublic': False,
                    'Privacy_IsSemiPrivate': False,
                    'Privacy_IsSemiPrivateBio': False,
                    'RealName': 'Jean',
                    'ShortName': 'Jean Côté',
                    'Siblings': { '1232211': {...},
                                  '4359580': {...},
                                  '6228030': {...},
                                  '7695991': {...},
                                  '7938274': {...},
                                  '7938336': {...},
                                  '7938347': {...}},
                    'Spouses': {'2071958': {...}, '709705': {...}},
                    'Suffix': ''},
        'status': 0,
        'user_name': 'Côté-179'}]
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

    >>> r = apps.getBio("Côté-179")
    >>> j = r.json()
    >>> bio = j[0]["bio"]
    >>> j[0]["bio"] = "See below\nfor a few lines\nfrom the bio.\n"
    >>> pp.pprint(j)
    [{'bio': 'See below\nfor a few lines\nfrom the bio.\n', 'page_name': 'Côté-179', 'status': 0, 'user_id': 4149371}]
    >>>
    >>> print("\n".join([x.strip("\n") for x in bio.split("\n")][:2]))
    == Biographie ==
    '''Jean Côté dit le Frisé Landroche (1644 - 1722) aussi connu sous le nom de Costé et Cotte.'''
    >>>

Get ancestors, depth=1 gives person and parents, depth=2 adds grandparents, etc.

    >>> r = apps.getAncestors("Côté-179", depth=1)
    >>> j = r.json()
    >>> pp.pprint(j)
    [ { 'ancestors': [ { 'BirthDate': '1644-02-25',
                         'BirthDateDecade': '1640s',
                         'BirthLocation': 'Paroisse Notre Dame, Québec, Québec',
                         'BirthNamePrivate': 'Jean Côté',
                         'Creator': 3833213,
                         'DeathDate': '1722-03-26',
                         'DeathDateDecade': '1720s',
                         'DeathLocation': "L'Ange-Gardien, Montmorency, Qc, Canada",
                         'Father': 4149374,
                         'FirstName': 'Jean',
                         'Gender': 'Male',
                         'Id': 4149371,
                         'IsLiving': 0,
                         'IsPerson': 1,
                         'LastNameAtBirth': 'Côté',
                         'LastNameCurrent': 'Côté',
                         'LastNameOther': 'Cotte, Costé, dit Le Frisé Landroche',
                         'LongNamePrivate': 'Jean Côté',
                         'Manager': 2046555,
                         'MiddleName': '',
                         'Mother': 1232214,
                         'Name': 'Côté-179',
                         'Nicknames': '',
                         'Photo': 'Cote-179.jpg',
                         'PhotoData': None,
                         'Prefix': '',
                         'Privacy': 60,
                         'Privacy_IsAtLeastPublic': True,
                         'Privacy_IsOpen': True,
                         'Privacy_IsPrivate': False,
                         'Privacy_IsPublic': False,
                         'Privacy_IsSemiPrivate': False,
                         'Privacy_IsSemiPrivateBio': False,
                         'RealName': 'Jean',
                         'ShortName': 'Jean Côté',
                         'Suffix': '',
                         'Touched': '20161106140612'},
                       { 'BirthDate': '1602-00-00',
                         'BirthDateDecade': '1600s',
                         'BirthLocation': None,
                         'BirthNamePrivate': 'Jean Côté',
                         'Creator': None,
                         'DeathDate': '1661-03-27',
                         'DeathDateDecade': '1660s',
                         'DeathLocation': None,
                         'Father': 8384551,
                         'FirstName': 'Jean',
                         'Gender': 'Male',
                         'Id': 4149374,
                         'IsLiving': None,
                         'IsPerson': 1,
                         'LastNameAtBirth': 'Côté',
                         'LastNameCurrent': 'Côté',
                         'LastNameOther': None,
                         'LongNamePrivate': 'Jean Côté',
                         'Manager': 2046555,
                         'MiddleName': '',
                         'Mother': 5182831,
                         'Name': 'Côté-180',
                         'Nicknames': None,
                         'Photo': 'Aubin-42-1.jpg',
                         'PhotoData': None,
                         'Prefix': None,
                         'Privacy': 60,
                         'Privacy_IsAtLeastPublic': True,
                         'Privacy_IsOpen': True,
                         'Privacy_IsPrivate': False,
                         'Privacy_IsPublic': False,
                         'Privacy_IsSemiPrivate': False,
                         'Privacy_IsSemiPrivateBio': False,
                         'RealName': 'Jean',
                         'ShortName': 'Jean Côté',
                         'Suffix': '',
                         'Touched': '20161124012931'},
                       { 'BirthDate': '1621-03-23',
                         'BirthDateDecade': '1620s',
                         'BirthLocation': None,
                         'BirthNamePrivate': 'Anne Martin',
                         'Creator': None,
                         'DeathDate': '1684-12-04',
                         'DeathDateDecade': '1680s',
                         'DeathLocation': None,
                         'Father': 0,
                         'FirstName': 'Anne',
                         'Gender': 'Female',
                         'Id': 1232214,
                         'IsLiving': None,
                         'IsPerson': 1,
                         'LastNameAtBirth': 'Martin',
                         'LastNameCurrent': 'Martin',
                         'LastNameOther': None,
                         'LongNamePrivate': 'Anne Martin',
                         'Manager': 1229367,
                         'MiddleName': '',
                         'Mother': None,
                         'Name': 'Martin-3448',
                         'Nicknames': None,
                         'Photo': 'Martin-3448.jpg',
                         'PhotoData': None,
                         'Prefix': None,
                         'Privacy': 60,
                         'Privacy_IsAtLeastPublic': True,
                         'Privacy_IsOpen': True,
                         'Privacy_IsPrivate': False,
                         'Privacy_IsPublic': False,
                         'Privacy_IsSemiPrivate': False,
                         'Privacy_IsSemiPrivateBio': False,
                         'RealName': 'Anne',
                         'ShortName': 'Anne Martin',
                         'Suffix': '',
                         'Touched': '20161124014736'}],
        'status': 0,
        'user_name': 'Côté-179'}]
    >>>

Get relatives, just the spouses and siblings in this case.

    >>> pp = pprint.PrettyPrinter(indent=2, width=120, depth=5)
    >>> r = apps.getRelatives("Côté-179", getSpouses=1, getSiblings=1)
    >>> j = r.json()
    >>> pp.pprint(j)
    [ { 'items': [ { 'key': 'Côté-179',
                     'person': { 'BirthDate': '1644-02-25',
                                 'BirthDateDecade': '1640s',
                                 'BirthLocation': 'Paroisse Notre Dame, Québec, Québec',
                                 'BirthNamePrivate': 'Jean Côté',
                                 'Creator': 3833213,
                                 'DeathDate': '1722-03-26',
                                 'DeathDateDecade': '1720s',
                                 'DeathLocation': "L'Ange-Gardien, Montmorency, Qc, Canada",
                                 'Father': 4149374,
                                 'FirstName': 'Jean',
                                 'Gender': 'Male',
                                 'Id': 4149371,
                                 'IsLiving': 0,
                                 'IsPerson': 1,
                                 'LastNameAtBirth': 'Côté',
                                 'LastNameCurrent': 'Côté',
                                 'LastNameOther': 'Cotte, Costé, dit Le Frisé Landroche',
                                 'LongNamePrivate': 'Jean Côté',
                                 'Manager': 2046555,
                                 'MiddleName': '',
                                 'Mother': 1232214,
                                 'Name': 'Côté-179',
                                 'Nicknames': '',
                                 'Photo': 'Cote-179.jpg',
                                 'PhotoData': None,
                                 'Prefix': '',
                                 'Privacy': 60,
                                 'Privacy_IsAtLeastPublic': True,
                                 'Privacy_IsOpen': True,
                                 'Privacy_IsPrivate': False,
                                 'Privacy_IsPublic': False,
                                 'Privacy_IsSemiPrivate': False,
                                 'Privacy_IsSemiPrivateBio': False,
                                 'RealName': 'Jean',
                                 'ShortName': 'Jean Côté',
                                 'Siblings': {...},
                                 'Spouses': {...},
                                 'Suffix': '',
                                 'Touched': '20161106140612'},
                     'user_id': 4149371,
                     'user_name': 'Côté-179'}],
        'status': 0}]
    >>>

Try to retrieve the FamilySearch connections. This will fail because we are not logged in.

    >>> r = apps.getPersonFSConnections("Côté-179")
    >>> j = r.json()
    >>> pp.pprint(j)
    [{'status': 'Permission denied', 'user_name': 'Côté-179'}]
    >>>

Illustrate loggin on. Use an invalid password, so as to see the error result.

    >>> r = apps.login("Henderson-6191", "invalid password")
    >>> j = r.json()
    >>> pp.pprint(j)
    {'login': {'result': 'Illegal', 'wait': 1}}
    >>>

Illustrate logging off.

    >>> apps.logout()
    >>>

Our session is ended.
