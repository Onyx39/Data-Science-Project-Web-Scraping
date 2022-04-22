#Ce fichier collecte les données et les stocke dans un dictionnaire

import fonctions_pour_le_traitement_des_donnees as f
import urllib.request 
import bs4


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
    liens = f.creer_liste_lien_hopitaux(html_soup)
    cap_spe=[]
    equipements = []
    for i in liens :
        lien_description_hop = "https://www.hopital.fr" + i 
        cap_spe.append(f.capacites_des_spe_d_un_hop(lien_description_hop))
        equipements.append(f.nombre_equipements_d_un_hop(lien_description_hop))

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

    ville = f.creer_liste_ville(all_h3_in_html_page)

    tel, ad, cap, type_struct = f.creer_liste_telephone_adresse_capacite_type(list_attributs)

    departement = f.creer_liste_numero_depatement(ad)

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