#Ce fichier enregistre les données collectées dans un fichier CVS en suivant le lien qui est à remplir en dessous.

import fichier_a_completer as d
import collecte_des_donnees as cd
import pandas as pd

def save_as_CSV_file () :
    res = pd.DataFrame(cd.get_all_hospital())
    res.to_csv(r'd.path')

if __name__ == "__main__" :
    save_as_CSV_file()
