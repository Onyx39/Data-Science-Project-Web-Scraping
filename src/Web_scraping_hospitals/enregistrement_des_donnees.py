#Ce fichier enregistre les données collectées dans un fichier CVS en suivant le lien qui est à remplir en dessous.

from fichier_a_completer import *
from Web_scraping_hospitals.collecte_des_donnees import *
import pandas as pd

def save_as_CSV_file () :
    res = pd.DataFrame(get_all_hospital())
    res.to_csv(path)

if __name__ == "__main__" :
    save_as_CSV_file()
