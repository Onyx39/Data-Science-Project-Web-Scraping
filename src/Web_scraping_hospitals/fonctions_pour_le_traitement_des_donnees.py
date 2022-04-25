#Ce fichier contient les fonctions utiles pour traiter les données récoletées

import urllib.request 
import bs4

def trouver_liste_nombre_dans_string(s) :
    candidat = ""
    for i in range (0, len(s) - 5) :
        a = 0
        for j in range(0, 5) :
            if s[i+j] == '0' or s[i+j] == '1' or s[i+j] == '2' or s[i+j] == '3' or s[i+j] == '4' or s[i+j] == '5' or s[i+j] == '6' or s[i+j] == '7' or s[i+j] == '8' or s[i+j] == '9' :
                a+=1  
        if a == 5 :
            candidat = s[i] + s[i+1] + s[i+2] + s[i+3] + s[i+4]
    if candidat != "" :
        return candidat
    else :
        for i in range (0, len(s) - 5) :
            a = 0
            for j in range(0, 5) :
                if s[i+j] == '0' or s[i+j] == '1' or s[i+j] == '2' or s[i+j] == '3' or s[i+j] == '4' or s[i+j] == '5' or s[i+j] == '6' or s[i+j] == '7' or s[i+j] == '8' or s[i+j] == '9' or s[i+j] == ' ':
                    a+=1  
            if a == 5 :
                candidat = s[i] + s[i+1] + s[i+2] + s[i+3] + s[i+4]
        return candidat

def creer_liste_numero_depatement (liste_adresse) :
    departement = []
    for i in liste_adresse :
        cp = trouver_liste_nombre_dans_string(i)
        if cp != "" :
            if cp[0] == '9' and cp[1] == '7' :
                departement.append(cp[0] + cp[1] + cp[2])
            else : departement.append(cp[0] + cp[1])
        else : departement.append("Pas de departement")
    return departement

def creer_liste_ville (h3_html_soup) :
    ville = []
    for i in h3_html_soup :
        ville_courante = ""
        debut = i.text.rindex('(')
        fin = i.text.rindex(')')
        if i.text[debut + 1] == "7" :
            debut = i.text.find('(')
            fin = i.text.rindex('(')
        for j in range(debut + 1, fin) :
            ville_courante += i.text[j]
        ville.append(ville_courante)
    return ville

def creer_liste_telephone_adresse_capacite_type (une_liste_attributs) :
    tel = []
    ad = []
    cap = []
    type_struct = []
    for i in range(len(une_liste_attributs)) :
        if une_liste_attributs[i] == 'Téléphone :' :
            if une_liste_attributs[i+1] != 'Site internet :' :
                tel.append(une_liste_attributs[i+1])
            else : tel.append('Pas de numéro')

        elif une_liste_attributs[i] == 'Adresse :' :
            ad.append(une_liste_attributs[i+1])

        elif une_liste_attributs[i] == 'Capacité :' : 
            cap.append(une_liste_attributs[i+1])
        elif une_liste_attributs[i] == 'Type de structure :' : 
            type_struct.append(une_liste_attributs[i+1])
    return tel, ad, cap, type_struct


def creer_liste_lien_hopitaux(lien) :

    all_h3_in_html_page = lien.find_all("h3")

    liste_lien = []
    
    for i in all_h3_in_html_page :
        liste_lien.append(i.contents[0].get("href"))
    
    return liste_lien

def recuperer_int_dans_string(s) :
    s1 = ""
    for i in range (s.find(':')+1, len(s)):
        s1+=s[i]
    return int(s1)


def capacites_des_spe_d_un_hop(lien_hopital):
    html = urllib.request.urlopen(lien_hopital)
    html_soup = bs4.BeautifulSoup(html, 'html.parser')
    l = html_soup.find_all("div", {"class" : "x2"})
    if len(l) == 2 :
        n = l[1].find_all("li")
    else :
        n = l[0].find_all("li")
    capacite_spe = []
    for i in n :
        capacite_spe.append(recuperer_int_dans_string(i.contents[0]))
    
    return capacite_spe

def recuperer_nom_equipement (s) :
    if s[0] == 'i' :
        return 1
    elif s[0] == 's' :
        return 0
    elif s[0] == 'c' :
        return 4
    elif s[0] == 't' :
        return 5
    elif s[11] == 'n' :
        return 2
    else : return 3


def nombre_equipements_d_un_hop(lien_hopital) :
    html = urllib.request.urlopen(lien_hopital)
    html_soup = bs4.BeautifulSoup(html, 'html.parser')
    l = html_soup.find_all("div", {"class" : "x2"})
    
    liste = [0, 0, 0, 0, 0, 0]

    if len(l) == 2 :
        n = l[0].find_all("li")
        for j in range (len(n)) :
            nom_equipement = recuperer_nom_equipement(n[j].text)
            nombre = recuperer_int_dans_string (n[j].text)
            if nom_equipement == 1 :
                liste[1] = nombre
            elif nom_equipement == 0 :
                liste[0] = nombre
            elif nom_equipement == 2 :
                liste[2] = nombre
            elif nom_equipement == 3 :
                liste[3] = nombre
            elif nom_equipement == 4 :
                liste[4] = nombre
            else : liste[5] = nombre
            print(liste)
    return liste

def recuperer_nom_equipements (s) :
    s1 = ""
    
    for i in range (0, s.find(':')):
        s1+=s[i]
    return s1

def creer_liste_equipements () :
    html = urllib.request.urlopen("https://www.hopital.fr/annuaire")
    html_soup = bs4.BeautifulSoup(html, 'html.parser')
    
    liste_equipements =[]
    
    colonne_droite = html_soup.find("aside", {"class" : "col sidebar small"})
    options_departement = colonne_droite.find("ul")

    l = []
    for liens in options_departement.find_all("a") : 
        l.append(liens.get('href'))

    for i in l :
        lien_dep = "https://www.hopital.fr" + i + '/'
        departement = urllib.request.urlopen(urllib.request.quote(lien_dep, safe=':/'))
        departement_soup = bs4.BeautifulSoup(departement, 'html.parser')
    
        liens = creer_liste_lien_hopitaux(departement_soup)
        for i in liens :
            lien_description_hop = "https://www.hopital.fr" + i 
            html2 = urllib.request.urlopen(lien_description_hop)
            html_soup2 = bs4.BeautifulSoup(html2, 'html.parser')
            l = html_soup2.find_all("div", {"class" : "x2"})
    
            if len(l) == 2 :
                n = l[0].find_all("li")
                for j in range (len(n)) :
                    candidat = recuperer_nom_equipements(n[j].text)
                    if candidat not in liste_equipements :
                        liste_equipements.append(candidat)  

    return liste_equipements