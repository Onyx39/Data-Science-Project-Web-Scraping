#Ce fichier est à compléter par l'utilisateur avant dxécuter le programme principal

from api_insee import ApiInsee


"""
Pour l'enregistrement des fichiers sur votre machine
"""
path ='C:/Users/val_p/Desktop/web_scraping_data07.csv'


"""
Pour avoir accès à l'API de l'INSEE
"""
insee_path_file = 'C:/Users/val_p/Desktop/insee_data07.csv'

api=ApiInsee(
    key="fWquistMMY4cCzPny5ik4ALnWZIa",
    secret="DcZXS9pINVftzS3OE0PQ8dzAjHQa"
)

bearer = "2d38905e-d95a-381d-b8ed-aae4e368fc43"