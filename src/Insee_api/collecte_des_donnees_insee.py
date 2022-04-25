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
    liste = []
    deplist = create_dep_list()
    for i in deplist :
        dictionary = {}
        endpoint = "https://api.insee.fr/donnees-locales/V0.1/donnees/geo-SEXE-AGE15_15_90@GEO2021RP2018/DEP-"+i+".all.all"
        data = {"ip": "1.1.2.3"}
        headers = {"Authorization": "Bearer " + bearer}

        reponse=requests.get(endpoint, data=data, headers=headers)
        s = reponse.content.decode('utf-8')
        beautiful_s = BeautifulSoup(s, "html.parser")
        var=beautiful_s.find_all('valeur')

        dictionary['departement'] = i

        total_pop_dep=int(var[0].contents[0])
        dictionary['Population totale département'] = total_pop_dep

        total_pop_hommes = int(round(float(var[1].contents[0])))
        dictionary['Population hommes département'] = total_pop_hommes

        total_pop_femmes = int(round(float(var[2].contents[0])))
        dictionary['Population femmes département'] = total_pop_femmes

        total_pop_0_14 = int(round(float(var[3].contents[0])))
        dictionary['Population entre 0 et 14 ans'] = total_pop_0_14

        total_pop_15_29 = int(round(float(var[6].contents[0])))
        dictionary['Population entre 15 et 29 ans'] = total_pop_15_29

        total_pop_30_44 = int(round(float(var[9].contents[0])))
        dictionary['Population entre 30 et 44 ans'] = total_pop_30_44

        total_pop_45_59 = int(round(float(var[12].contents[0])))
        dictionary['Population entre 45 et 59 ans'] = total_pop_45_59

        total_pop_60_74 = int(round(float(var[15].contents[0])))
        dictionary['Population entre 60 et 74 ans'] = total_pop_60_74

        total_pop_75_89 = int(round(float(var[18].contents[0])))
        dictionary['Population entre 74 et 89 ans'] = total_pop_75_89

        total_pop_90_plus = int(round(float(var[21].contents[0])))
        dictionary['Population de 90 ans et plus'] = total_pop_90_plus
        
        """
        print(i)
        print(dictionary)
        print(" ")
        """
        
        liste.append(dictionary)
        time.sleep(4)
    return liste
