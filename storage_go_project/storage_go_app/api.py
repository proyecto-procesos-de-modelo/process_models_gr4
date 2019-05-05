
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests
#from requests.exceptions import HTTPError


# Create your utilities here.
def query():
    """
    https://ourfarms.herokuapp.com/admin/
    https://ourfarms.herokuapp.com/apiRest/?format=api
    """

    url_base = 'https://ourfarms.herokuapp.com/apiRest/'

    user = 'GR4'
    password = 'gr4123567890'

    ref = 'REF/'
    product = 'product/'

    format = '?format='

    json = 'json'
    api = 'api'

    #response = requests.get(url_base + product + format + json, auth=(user, password))
    response = requests.get(url_base + ref + format + json, auth=(user, password))

    if response.status_code == 200:
        return response.json()
    else:
        return response.status




#
