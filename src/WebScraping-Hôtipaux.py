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

def creer_un_dictionnaire_hopital (h3_html_soup, tel, ad, ville, departement, cap, type_struct) :
    hopital =[]
    for i in range (len(h3_html_soup)) :
        hospital_entry = {
            "Nom" : h3_html_soup[i].text,
            "Téléphone" : tel[i],
            "Adresse" : ad[i],
            "Ville" : ville[i],
            "Département" : departement[i],
            "Capacité" : cap[i],
            "Type d'établissement" : type_struct[i]
        }
        hopital.append(hospital_entry)
    return hopital



def get_one_hospital (html_soup) :
    """Fonction qui recupère les donées des hopitaux présents sur une page web"""

    ul_tag = html_soup.find_all(id = 'section_31')
    li_tag = []

    hopital = []
    all_h3_in_html_page = html_soup.findAll("h3")

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

    return creer_un_dictionnaire_hopital(all_h3_in_html_page, tel, ad, ville, departement, cap, type_struct)

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



if __name__ == '__main__' :

    #print(liste_hopitaux)
    res = pd.DataFrame(get_all_hospital())
    print(res)
    res.to_csv(r'C:/Users/val_p/Desktop/hopitaux_propres_test_bof.csv')