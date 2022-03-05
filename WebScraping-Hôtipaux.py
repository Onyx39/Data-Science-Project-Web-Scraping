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


def get_all_hospital (html_soup) :
    """Fonction qui recupère les donées des hopitaux présents sur une page web"""

    ul_tag = html_soup.find_all(id = 'section_31')
    li_tag = []
@@ -36,28 +48,57 @@ def get_all_hospital (html_soup) :
      if i != '\n':
        list_attributs.append(i)

    ville = []
    for i in all_h3_in_html_page :
        ville_courante = ""
        debut = i.text.rindex('(')
        fin = i.text.rindex(')')
        if i.text[debut+1] == "7" :
            debut = i.text.find('(')
            fin = i.text.rindex('(')
        for j in range(debut +1, fin) :
            ville_courante += i.text[j]
        ville.append(ville_courante)


    tel = []
    ad = []
    cap = []
    type_struct = []

    for i in range(len(list_attributs)) :
        if list_attributs[i] == 'Téléphone :' :
            if list_attributs[i+1] != 'Site internet :' :
                tel.append(list_attributs[i+1])
            else : tel.append('Pas de numéro')

        elif list_attributs[i] == 'Adresse :' :
            ad.append(list_attributs[i+1])

        elif list_attributs[i] == 'Capacité :' : 
            cap.append(list_attributs[i+1])
        elif list_attributs[i] == 'Type de structure :' : 
            type_struct.append(list_attributs[i+1])

    departement = []
    for i in ad :
        cp = trouver_liste_nombre_dans_string(i)
        if cp != "" :
            if cp[0] == '9' and cp[1] == '7' :
                departement.append(cp[0] + cp[1] + cp[2])
            else : departement.append(cp[0] + cp[1])
        else : departement.append("Pas de departement")


    for i in range (len(all_h3_in_html_page)) :
        hospital_entry = {
            "Nom" : all_h3_in_html_page[i].text,
            "Téléphone" : tel[i],
            "Adresse" : ad[i],
            "Ville" : ville[i],
            "Département" : departement[i],
            "Capacité" : cap[i],
            "Type d'établissement" : type_struct[i]
        }
        hospital.append(hospital_entry)
    return hospital
@@ -83,9 +124,13 @@ def get_all_hospital (html_soup) :
        lien_dep = "https://www.hopital.fr" + i + '/'
        departement = urllib.request.urlopen(urllib.request.quote(lien_dep, safe=':/'))
        departement_soup = bs4.BeautifulSoup(departement, 'html.parser')
        liste_hopitaux += get_all_hospital(departement_soup)

    #print(liste_hopitaux)
    res = pd.DataFrame(liste_hopitaux)
    print(res)
    res.to_csv(r'C:/Users/val_p/Desktop/onzième_essai_hopitaux.csv')
