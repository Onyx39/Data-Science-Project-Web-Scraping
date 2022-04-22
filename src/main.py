#Ce fichier est l'exécutable
#Pensez à remplir le fichier à compléter avnt de le lancer !

import Web_scraping_hospitals.enregistrement_des_donnees as ws
import INSEE_API.enregistrement_des_donnees_insee as api

def main() :
    ws.save_as_CSV_file()
    api.create_csv_file()

if __name__ == "__main__" :
    main()
