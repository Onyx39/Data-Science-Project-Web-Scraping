#Ce fichier utilise l'API de l'INSEE pour récupérer la populaton dans chaque départemet français

from fichier_a_completer import *
from bs4 import BeautifulSoup
import requests
import time

mon_api = api

def create_dep_list () :
    deplist = []
    for i in range (1, 10) :
        number = "0"+str(i)
        deplist.append(number)
    for i in range (10, 20) :
        deplist.append(str(i))
    deplist.append('2A')
    deplist.append('2B')
    for i in range (21, 96) :
        deplist.append(str(i))
    for i in range (971, 975) :
        deplist.append(str(i))
    return deplist


def create_dic_pop () :
    tot_pop = 0
    dictionary = {}
    deplist = create_dep_list()
    for i in deplist :
        endpoint = "https://api.insee.fr/donnees-locales/V0.1/donnees/geo-SEXE-AGE15_15_90@GEO2021RP2018/DEP-"+i+".all.all"
        data = {"ip": "1.1.2.3"}
        headers = {"Authorization": "Bearer " + bearer}

        reponse=requests.get(endpoint, data=data, headers=headers)
        s = reponse.content.decode('utf-8')
        beautiful_s = BeautifulSoup(s, "html.parser")
        
        var=beautiful_s.find('valeur')
        total_pop=int(var.contents[0])
        tot_pop+=total_pop
        dictionary[i] = total_pop
        print(i, total_pop)
        time.sleep(2)
    return dictionary