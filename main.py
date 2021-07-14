import colorama
import requests
import time

from datetime import datetime as dt
from colorama import Fore

colorama.init()

authentication_url = 'https://authserver.mojang.com/authenticate'
challenges_url = 'https://api.mojang.com/user/security/challenges'
name_url = 'https://api.minecraftservices.com/minecraft/profile/name'

class Account:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None

    def authenticate(self):
        # print(self.email, ':', self.password)
        data = {
            'agent': {
                'name': 'Minecraft',
                'version': 1
            },

            'username': self.email,
            'password': self.password
        }
        
        r = requests.post(authentication_url, json=data)
        if r.status_code == 200:
            self.token = r.json()['accessToken']
        else:
            print(r.status_code, r.json()['errorMessage'])
            exit()

    

class Sniper:
    def __init__(self, data):
        self.release = data['release']
        self.target = data['target']
        self.email = data['email']
        self.password = data['password']
        self.wait = data['wait']
        
        self.account = Account(self.email, self.password)
        self.account.authenticate()

    def start(self):
        r = requests.get(name_url + '/' + self.target + '/available', headers={ 'Authorization': 'Bearer ' + self.account.token })
        status = r.json()['status']
        if status == 'AVAILABLE':
            print(status, '[OK]', f'Username: {self.target}')
            exit()

        elif status == 'DUPLICATE':
            print(status, '[POTENTIAL]', f'Username: {self.target}')

        else:
            print(status, '[BAD]', f'Username: {self.target}')
            exit()

        # Straight taken from https://github.com/cardbooard/Minecraft-NameSniper-Blocker/blob/master/NameSniper.py
        now = dt.now().strftime('%H:%M:%S')
        h = self.release.split(':')[0]
        m = self.release.split(':')[1]
        s = self.release.split(':')[2]

        if m == '00' and s == '00':
            if int(h) < 11:
                hh = int(h) - 1
                hh = '0' + str(hh)
            else:
                hh = int(h) - 1
                hh = str(hh)
            date = hh + ':59:59'
        elif s == '00':
            if int(m) < 11:
                mm = int(m) - 1
                mm = '0' +  str(mm)
            else:
                mm = int(m) - 1
                mm = str(mm)
            date = h + ':' + mm + ':59'
            
        else:
            if int(s) < 11:
                ss = int(s) - 1
                date = h + ':' + m + ':' + '0' + str(ss)
            else:
                ss = int(s) - 1
                date = h + ':' + m + ':' + str(ss)

        while True:
            now = dt.now().strftime('%H:%M:%S')
            if now == date:
                time.sleep(self.wait)
                for i in range(3):
                    r = requests.put(name_url + '/' + self.target, headers={ 'Authorization': 'Bearer ' + self.account.token })
                    print(r.status_code) # 200 means you got it!


if '__main__' == __name__:
    sniper = Sniper({
        'release': '00:00:00',
        'wait': 0.914,
        'target': '',
        'email': '',
        'password': ''
    })

    sniper.start()