#Ce fichier enregistre les données collectées grâce à l'api de l'INSEE

import collecte_des_donnees_insee as cd
import fichier_a_completer as d
import pandas as pd


def create_csv_file () :
    dictionary = cd.create_dic_pop()
    res = pd.DataFrame([dictionary])
    res.to_csv(r'd.insee_path_file')
