
from urllib.request import urlopen
#from bs4 import BeautifulSoup
import bs4
from WebScraping-Hopitaux import get_all_hospital()


html = urlopen("https://www.hopital.fr/annuaire-des-activites")
html_soup = bs4.BeautifulSoup(html, 'html.parser')
colonne_droite = html_soup.find("aside", {"class" : "col sidebar small"})
options_departement = colonne_droite.find("ul")

l = []
for liens in options_departement.find_all("a") : 
    l.append(liens.get('href'))


liste_hopitaux = []

for i in l :
    departement = urlopen("https://www.hopital.fr" + i)
    departement_soup = bs4.BeautifulSoup(html, 'html.parser')
    liste_hopitaux.append(get_all_hospital)

print(l)
