# -*- coding: utf-8 -*-
"""
Entete à compléter
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
#import pandas as pd
import re

"""def is_hospital_entry (table_row) :
    Fonction qui permet de déterminer si une ligne de la table HTML
    que nous allons récupérer est bien un hopital
    row_cells = table_row.findAll("a")
    hospital_name = get_hospital_name(row_cells[0].text)
    return (hospital_name)

def get_hostipal_name (cell_value) :
    r = re.match("^[a-zA-Z.-.(.)]*(AP.-HP)[a-zA-Z.-.(.)]*]$", cell_value)
    if r :
        hospital_name = r.group(1)
        return hospital_name
    else:
        return None
    
    
def get_hospital_adress (cell_value) :
    if cell_value[0] == "Adresse :" :
        return cell_value[1]
    else : return None
"""


def liste_choisie (liste, chaine):
    """Prend une liste en entrée et ne garde que les éléments qui correspondent à l'information voulue"""
    l =[]
    #long_chaine = len(chaine)
    for i in range (len(liste)) :
        if liste[i] == chaine :
            print(liste[i].find('label').contents)
            l.append(liste[i])
    return l



def get_all_hospital (html_soup) :
    
    hospital = []
    all_h3_in_html_page = html_soup.findAll("h3")
    all_li_in_html_page = html_soup.findAll("li")
    adress = liste_choisie(all_li_in_html_page, 'label')

    for i in range (len(all_h3_in_html_page)) :
        hospital_entry = {
            "name" : all_h3_in_html_page[i].text,
            "Adress" : adress[i].text
        }
        hospital.append(hospital_entry)
    return hospital




if __name__ == '__main__' :
    
    html = urlopen("https://www.hopital.fr/annuaire/Haute-Savoie+Rh%C3%B4ne-Alpes+74/")
    html_soup = BeautifulSoup(html, 'html.parser')
    """hospital_list = get_all_hospital(html_soup)
    print(hospital_list)
    print(len(hospital_list))"""
    
    all_li_in_html_page = html_soup.findAll("li")
    print(all_li_in_html_page[-1])

    print(liste_choisie(all_li_in_html_page, 'Adresse :'))

    
    

