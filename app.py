from flask import Flask, render_template, url_for, flash, redirect, jsonify, request, Response
from flask_restful import Resource, Api, request
import flask_excel as excel
from jsonschema import validate
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import importation
import json
import datetime

app = Flask(__name__)
api = Api(app) 
app.config['SECRET_KEY'] = 'a3a9fb269885a66d27c3875e9d3b99bd'

# A sample schema, like what we'd get from json.load()
schema = {
    "type" : "object",
    "properties" : {
        "etablissement" : {"type" : "string"},
        "adresse" : {"type" : "string"},
        "ville" : {"type" : "string"},
        "date_visite" : {"type" : "string"},
        "nom_client" : {"type" : "string"},
        "prenom_client" : {"type" : "string"},
        "description" : {"type" : "string"},
    },
}


def dbrefresher():
    """Fuction to refresh the database once a day"""
    importation.importer()

#A3 : Mettre en place un BackgroundScheduler dans l’application Flask afin d’extraire les données de la ville 
# de Montréal à chaque jour, à minuit, et mettre à jour les données de la base de données
sched = BackgroundScheduler(daemon=True)
sched.add_job(dbrefresher, trigger='cron', hour = '00')
sched.start()

try:
	db = sqlite3.connect('database.db', check_same_thread=False)

	cursor = db.cursor()
	
except Exception as e:
    db.rollback()
    raise e

datas = [{}]
datasDup = [{}]

#A2 : Construire une application Flask pour accéder aux données de la base de données.
@app.route("/")
@app.route("/accueil")
def accueil():
    return render_template('accueil.html')

#documentation RAML sous format HTML
@app.route("/doc")
def doc():
    return render_template('documentation.html')


@app.route("/search/<recherche>")
def search(recherche):
    cursor.execute(
        "SELECT * FROM contrevenants WHERE (etablissement LIKE (?) OR adresse LIKE (?) OR proprietaire LIKE (?));",
        ("%" + recherche + "%",
         "%" + recherche + "%",
         "%" + recherche + "%"))
    del datas[:]
    del datasDup[:]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        data = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        if data not in datasDup:
            datas.append(data)
            datasDup.append(data)
    return render_template('visualisation.html', datas=datas)

#D1 : Le système offre un service REST permettant de faire une demande d’inspection à la ville.
@app.route("/inspection")
def inspection():
    return render_template('plainte.html')


#A4 : Le système offre un service REST permettant d'obtenir la liste des contrevenants 
# ayant commis une infraction entre deux dates spécifiées en paramètre
class contravention(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        args = request.args
        no1 =  datetime.datetime.strptime(args['du'], '%Y-%m-%d')
        no2 =  datetime.datetime.strptime(args['au'], '%Y-%m-%d')
        cursor.execute(
           "SELECT proprietaire, etablissement FROM contrevenants WHERE ( date_infraction >=(?) AND date_infraction <=(?));",
            (no1, no2))
        del datas[:]
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            data = (row[0], row[1])
            datas.append(data)
        return jsonify([dump for dump in datas])
  

#C1 Le système offre un service REST permettant d'obtenir la liste des établissements ayant commis une ou plusieurs infractions. 
class infractions(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        cursor.execute(
            "SELECT etablissement, COUNT(* ) FROM contrevenants GROUP BY etablissement ORDER BY COUNT(* ) DESC ;")
        del datas[:]
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            data = (row[0], row[1])
            datas.append(data)
        return jsonify([dump for dump in datas]) 


#C3 Le système offre un service REST permettant d'obtenir la liste des établissements ayant commis une ou plusieurs infractions en CSV. 
class infractionsCSV(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        cursor.execute(
            "SELECT etablissement, COUNT(* ) FROM contrevenants GROUP BY etablissement ORDER BY COUNT(* ) DESC ;")
        del datas[:]
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            data = (row[0], row[1])
            datas.append(data)
        r = Response(response=excel.make_response_from_array(datas, "csv"), status=200, mimetype="application/csv")
        r.headers["Content-Type"] = "text/csv; charset=utf-8"
        return r 

#C2 Le système offre un service REST permettant d'obtenir la liste des établissements ayant commis une ou plusieurs infractions en XML. 
class infractionsXML(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        cursor.execute(
            "SELECT etablissement, COUNT(* ) FROM contrevenants GROUP BY etablissement ORDER BY COUNT(* ) DESC ;")
        top  = Element('liste_contrevenants')
        comment = Comment('Generated for InfractionsXML')
        top.append(comment)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            child  = SubElement(top, 'contrevenant')
            etablissement = SubElement(child , 'etablissement')
            etablissement.text = row[0]
            nbinfractions = SubElement(child , 'nb_infraction')
            nbinfractions.text = str(row[1])
        r = Response(response=tostring(top), status=200, mimetype="application/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

#A6 L'application du point A5 offre un mode de recherche par nom du restaurant. La liste de tous les
#contrevenants est prédéterminée dans une liste déroulante et l'utilisateur choisira un restaurant parmi
#cette liste.
class restaurant(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        args = request.args
        name = args['resto']
        proprietaire = args['proprio']
        cursor.execute(
            "SELECT proprietaire, etablissement, descriptions  FROM contrevenants WHERE (etablissement LIKE (?) AND proprietaire LIKE (?));",
            ("%" + name + "%",
            "%" + proprietaire + "%"))
        del datas[:]
        del datasDup[:]
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            data = (row[0], row[1], row[2])
            if data not in datasDup:
                datas.append(data)
                datasDup.append(data)
        return jsonify([dump for dump in datas]) 

class plainte(Resource): 
  
    # corresponds to the post request. 
    # this function is called whenever there 
    # is a post request for this resource 
    def post(self): 
        args = request.args
        etablissement = args['etablissement']
        adresse = args['adresse']
        ville = args['ville']
        dateVisite = args['date_visite']
        nomClient = args['nom_client']
        prenomClient = args['prenom_client']
        description = args['description']
        data = {"etablissement" : etablissement, "adresse" : adresse, "ville" : ville, "date_visite" : dateVisite, "nom_client" : nomClient, "prenom_client" : prenomClient, "description" : description}
        jsonPlainte = jsonify(data)
        (validate(data, schema=schema))
        return jsonPlainte
        #if (validate(data, schema=schema)):
            #return jsonPlainte
        #else:
        #   return 'bad request!', 400
            

# adding the defined resources along with their corresponding urls 
api.add_resource(contravention, '/contrevenants') 
api.add_resource(infractions, '/infractions') 
api.add_resource(infractionsCSV, '/infractionsCSV') 
api.add_resource(infractionsXML, '/infractionsXML') 
api.add_resource(restaurant, '/restaurant') 
api.add_resource(plainte, '/plainte') 

if __name__ == '__main__':
    excel.init_excel(app)
    app.run()
