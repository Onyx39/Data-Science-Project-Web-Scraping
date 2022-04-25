#Ce fichier enregistre les données collectées grâce à l'api de l'INSEE

from INSEE_API.collecte_des_donnees_insee import *
from fichier_a_completer import *
import pandas as pd


def create_csv_file () :
    dictionary = create_dic_pop()
    res = pd.DataFrame.from_dict(dictionary)
    res.to_csv(r'C:/Users/val_p/Desktop/test2.csv')
