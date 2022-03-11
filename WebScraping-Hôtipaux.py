import urllib.request 
import bs4
import pandas as pd

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

def creer_liste_numero_depatemennt (liste_adresse) :
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


def creer_un_dictionnaire_hopital (h3_html_soup, tel, ad, ville, departement, cap, type_struct, cap_spe, equipements) :

    hopital =[]
    for i in range (len(h3_html_soup)) :
        hospital_entry = {
            "Nom" : h3_html_soup[i].text,
            "Téléphone" : tel[i],
            "Adresse" : ad[i],
            "Ville" : ville[i],
            "Département" : departement[i],
            "Capacité" : cap[i],
            "Type d'établissement" : type_struct[i],
            "Capacité médecine" : cap_spe[i][0],
            "Capacité chirurgie" : cap_spe[i][1],
            "Capacité obstétrique" : cap_spe[i][2],
            "Capacité psychiatrie" : cap_spe[i][3],
            "Capacité moyen séjour" : cap_spe[i][4],
            "Capacité long séjour" : cap_spe[i][5],
            "Capacité hébergement" : cap_spe[i][6],
            "Capacité hospitalisation à domicile" : cap_spe[i][7],
            "Capacité service de soins infirmiers à domicile" : cap_spe[i][8],
            "Equipement : scanner" : equipements[i][0],
            "Equipement : irm" : equipements[i][1],
            "Equipement : radiologie numérisée" : equipements[i][2],
            "Equipement : radiologie vasculaire" : equipements[i][3],
            "Equipement : caméras à scintillon" : equipements[i][4],
            "Equipement : tep (tomographe)" : equipements[i][5]
        }
        hopital.append(hospital_entry)
        print(hospital_entry)
    return hopital



def get_one_hospital (html_soup) :
    """Fonction qui recupère les données des hopitaux présents sur une page web"""
    liens = creer_liste_lien_hopitaux(html_soup)
    cap_spe=[]
    equipements = []
    for i in liens :
        lien_description_hop = "https://www.hopital.fr" + i 
        cap_spe.append(capacites_des_spe_d_un_hop(lien_description_hop))
        equipements.append(nombre_equipements_d_un_hop(lien_description_hop))



    ul_tag = html_soup.find_all(id = 'section_31')
    li_tag = []
    all_h3_in_html_page = html_soup.find_all("h3")

    for i in ul_tag :
      for child in i.descendants :
        if type(child) == bs4.element.NavigableString :
          li_tag.append(child)

    list_attributs = []
    for i in li_tag :
      if i != '\n':
        list_attributs.append(i)

    ville = creer_liste_ville(all_h3_in_html_page)

    tel, ad, cap, type_struct = creer_liste_telephone_adresse_capacite_type(list_attributs)

    departement = creer_liste_numero_depatemennt(ad)

    return creer_un_dictionnaire_hopital(all_h3_in_html_page, tel, ad, ville, departement, cap, type_struct, cap_spe, equipements)

def get_all_hospital () :

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
        departement = urllib.request.urlopen(urllib.request.quote(lien_dep, safe=':/'))
        departement_soup = bs4.BeautifulSoup(departement, 'html.parser')
        liste_hopitaux += get_one_hospital(departement_soup)
    
    return liste_hopitaux

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

if __name__ == '__main__' :

    #print(liste_hopitaux)
    
    res =pd.DataFrame(get_all_hospital())
    print(res)
    res.to_csv(r'C:/Users/val_p/Desktop/final_version.csv')
    '''

    l = capacites_des_spe_d_un_hop('https://www.hopital.fr/annuaire-etablissement/hopital-de-la-croix-rousse-hcl-lyon,5607')
    print(l)
    print(type(l))
    '''