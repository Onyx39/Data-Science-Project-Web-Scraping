import urllib.request
import requests
from api_insee import ApiInsee
import time
from bs4 import BeautifulSoup

api=ApiInsee(
    key="fWquistMMY4cCzPny5ik4ALnWZIa",
    secret="DcZXS9pINVftzS3OE0PQ8dzAjHQa"
)

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

print(create_dep_list())

def create_dic_pop () :
    tot_pop = 0
    dictionary = {}
    deplist = create_dep_list()
    for i in deplist :
        endpoint = "https://api.insee.fr/donnees-locales/V0.1/donnees/geo-SEXE-AGE15_15_90@GEO2021RP2018/DEP-"+i+".all.all"
        data = {"ip": "1.1.2.3"}
        headers = {"Authorization": "Bearer e60bbcb3-3ea8-36ad-aaa8-0553307b6876"}

        reponse=requests.get(endpoint, data=data, headers=headers)
        s = reponse.content.decode('utf-8')
        beautiful_s = BeautifulSoup(s, "html.parser")
        
        var=beautiful_s.find('valeur')
        total_pop=int(var.contents[0])
        tot_pop+=total_pop
        dictionary[i] = total_pop
        #print(i, total_pop)
        time.sleep(2)
    print(dictionary)
        
    print("La population totale de France est de : ",tot_pop, "habitants")
    print("Il y a ", len(dictionary), "départements")




if __name__ == "__main__" :
    create_dic_pop()
