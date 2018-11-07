# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:08:54 2018

@author: jp15101
"""

import requests
from requests_oauthlib import OAuth2Session

header = {"Accept": "application/json", 
          "Content-Type": "application/json",
          "username":"jp15101",
                                                                                                      "password": "Scr3wdr1v3r2"}

base_url = "https://api.hooktheory.com/v1/" 
post_url = "users/auth"
chord_prob_url = "trends/nodes"
r = requests.post(base_url+post_url,data=header)
activkey_value = r.json()['activkey']
client_id = r.json()['id']


#Authorization = ['Bearer' ] 

Authorization = {"Bearer": activkey_value}
#        "Header Value": "Bearer" + str(activkey_value)}
x = requests.get(base_url+chord_prob_url,params=Authorization)



print(r.json())