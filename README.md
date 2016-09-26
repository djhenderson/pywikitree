# pywikitree
Python interface to the WikiTree API

The following illustrates retrieving a public person
without logging on to WikiTree using Python 3. When using
Python 2, all returned strings are unicode.

    >>> import wt_apps, pprint
    >>> pp = pprint.PrettyPrinter(indent=2, width=120, depth=4)
    >>> apps = wt_apps.WT_Apps()
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
                    'DeathDate': '1722-03-26',
                    'DeathDateDecade': '1720s',
                    'DeathLocation': "L'Ange-Gardien, Montmorency, Qc, Canada",
                    'Father': '4149374',
                    'FirstName': 'Jean',
                    'Gender': 'Male',
                    'Id': 4149371,
                    'IsLiving': '0',
                    'LastNameAtBirth': 'Côté',
                    'LastNameCurrent': 'Côté',
                    'LastNameOther': 'Cotte, Costé, dit Le Frisé Landroche',
                    'LongNamePrivate': 'Jean Côté',
                    'MiddleName': '',
                    'Mother': '1232214',
                    'Name': 'Côté-179',
                    'Nicknames': '',
                    'Parents': {'1232214': {...}, '4149374': {...}},
                    'Photo': 'Cote-179.jpg',
                    'PhotoData': None,
                    'Prefix': '',
                    'Privacy': '60',
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

Currently, the only documentation is the in docstrings,
http://www.wikitree.com/wiki/API_Documentation
and
http://apps.wikitree.com/apps/
