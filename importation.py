import requests
import xml.etree.ElementTree as ET
import sqlite3
import datetime
import locale

#A1 :La liste des contrevenants est obtenue en format XML à l'aide d'une requête HTTP 
#et son contenu est stocké dans une base de données SQLite.
def importer():
    try:
	    db = sqlite3.connect('database.db', check_same_thread=False)

	    cursor = db.cursor()
	
    except Exception as e:
        db.rollback()
        raise e

    


    locale.setlocale(locale.LC_ALL, 'fr_CA.utf8')

    url = 'http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml'
    headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
    response = requests.get(url, headers=headers)

    tree = ET.fromstring(response.text)

    for child in tree.findall('contrevenant'):
        proprietaire = child.find('proprietaire').text
        categorie = child.find('categorie').text
        etablissement = child.find('etablissement').text
        adresse = child.find('adresse').text
        ville = child.find('ville').text
        description = child.find('description').text

        date_tempo=child.find('date_infraction').text

        date_infraction = datetime.datetime.strptime(date_tempo, '%d %B %Y') 

        date_tempo=child.find('date_jugement').text

        date_jugement = datetime.datetime.strptime(date_tempo, '%d %B %Y') 
        montant = child.find('montant').text
        params = (proprietaire, categorie, etablissement, adresse, ville, description, date_infraction, date_jugement, montant)

        cursor.execute("INSERT INTO contrevenants(proprietaire, categorie, etablissement, adresse, "
                            "ville, descriptions, date_infraction, date_jugement, montant) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            params)

    db.commit()
    now = datetime.datetime.now()
    print("Base de donnees mise a jour le: " + now.strftime("%Y-%m-%d a %H:%M:%S"))


importer()

