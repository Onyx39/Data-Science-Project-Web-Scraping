#Ce fichier enregistre les données collectées grâce à l'api de l'INSEE

from INSEE_API.collecte_des_donnees_insee import *
from fichier_a_completer import *
import pandas as pd


def create_csv_file () :
    liste_dictionnaires = create_dic_pop()
    res = pd.DataFrame.from_dict(liste_dictionnaires)
    res.to_csv(insee_path_file)