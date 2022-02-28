# -*- coding: utf-8 -*-
"""
Entete à compléter
"""

import urllib.request 
import bs4

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

    ul_tag = html_soup.find_all(id = 'section_31')
    li_tag = []

    hospital = []
    all_h3_in_html_page = html_soup.findAll("h3")

    for i in ul_tag :
      for child in i.descendants :
        if type(child) == bs4.element.NavigableString :
          li_tag.append(child)

    list_attributs = []
    for i in li_tag :
      if i != '\n':
        list_attributs.append(i)

    tel = []
    ad = []
    cap = []
    type_struct = []
  
    for i in range(len(list_attributs)) :
        if list_attributs[i] == 'Téléphone :' :
            tel.append(list_attributs[i+1])
        elif list_attributs[i] == 'Adresse :' :
            ad.append(list_attributs[i+1])
        elif list_attributs[i] == 'Capacité :' : 
            cap.append(list_attributs[i+1])
        elif list_attributs[i] == 'Type de structure :' : 
            type_struct.append(list_attributs[i+1])

    for i in range (len(all_h3_in_html_page)) :
        hospital_entry = {
            "name" : all_h3_in_html_page[i].text,
            "telephone" : tel[i],
            "adress" : ad[i],
            "capacite" : cap[i],
            "type" : type_struct[i]
        }
        hospital.append(hospital_entry)
    return hospital




if __name__ == '__main__' :
    """
    html = urlopen("https://www.hopital.fr/annuaire/Haute-Savoie+Rh%C3%B4ne-Alpes+74/")
    html_soup = bs4.BeautifulSoup(html, 'html.parser')
    hospital_list = get_all_hospital(html_soup)
    print(hospital_list)
    #print(len(hospital_list))
    
    all_li_in_html_page = html_soup.findAll("li")
    print(all_li_in_html_page[-1])

    print(liste_choisie(all_li_in_html_page, 'Adresse :'))
    print(html_soup.get_text())
    print(html_soup.find('class="label"'))
    """

    html = urllib.request.urlopen("https://www.hopital.fr/annuaire-des-activites")
    html_soup = bs4.BeautifulSoup(html, 'html.parser')
    colonne_droite = html_soup.find("aside", {"class" : "col sidebar small"})
    options_departement = colonne_droite.find("ul")

    l = []
    for liens in options_departement.find_all("a") : 
        l.append(liens.get('href'))


    liste_hopitaux = []

    for i in l :
        lien_dep = "https://www.hopital.fr" + i + '/'
        urllib.parse.urlencode(lien_dep) 
        departement = urllib.request.urlopen(lien_dep)
        departement_soup = bs4.BeautifulSoup(html, 'html.parser')
        liste_hopitaux.append(get_all_hospital())

    print(l)


    

    
