# Projet de session


## Fonctionnalites :

### A1 :

>La liste des contrevenants est obtenue en format XML à l'aide d'une requête HTTP et son contenu est
>stocké dans une base de données SQLite. La modélisation de la base de données est à votre discrétion.
>Les données sont accessibles à partir de l'adresse suivante :
>http://donnees.ville.montreal.qc.ca/dataset/inspection-aliments-contrevenants/resource/92719d9b-8bf2-
>4dfd-b8e0-1021ffcaee2f
>À ce point-ci, vous ne devez faire qu’un script Python qui télécharge les données et insère les données
>dans la base de données. Vous pouvez assumer que la base de données existe déjà lors de l’exécution du
>script (le script ne doit pas créer la base de données, ni la vider). Vous devez également fournir le script
>SQL pour créer la base de données ainsi qu’une base de données déjà créée mais vide pour des fins de
>tests.

Fonctionnalite terminee, la base de donnee se remplit neanmoins en boucle.

Il suffit de faire 
>flask run

L'application validera la mise a jour de la base de donnee. 
Il est aussi possible de supprimer le fichier database.db et d'en recreer un avec 
>python3 reset.py

Il est possible de le remplir en lancant uniquement 
>python3 importation.py


### A2 :

>Construire une application Flask pour accéder aux données de la base de données. La page d’accueil
offre un outil de recherche qui permet de trouver les contrevenants par :
• nom d’établissement;
• propriétaire;
 • rue (par exemple, tous les restaurants sur le boulevard Rosemont).
Les résultats de la recherche doivent s’afficher sur une nouvelle page. Pour chaque contrevenant, on
affiche toutes les données disponibles sur une contravention. Il est possible qu’un restaurant apparaisse
plus d’une fois, s’il a eu plusieurs sanctions.

Fonctionnalite terminee.

Il suffit de faire 
>flask run

Puis d'aller sur 
* http://localhost:5000/

Tapez ensuite votre recherche dans une des deux barres de recherche (une globale au site et une pour la page plus grande et lisible), une nouvelle page s'ouvrira avec une liste de contrevenant contenant votre mot cle.


### A3 :

>Mettre en place un BackgroundScheduler dans l’application Flask afin d’extraire les données de la ville
de Montréal à chaque jour, à minuit, et mettre à jour les données de la base de données. Une fois par
jour, les données doivent être synchronisées avec celles de la ville.

Fonctionnalite terminee.

Attendez simplement minuit pour voir la base de donnee etre mise a jour dans les logs ou modifiez le scheduler a la ligne 38 du fichier "app.py"

>sched.add_job(dbrefresher, trigger='cron', hour = '00')

Vous pouvez modifier "hour" par l'heure de votre choix.


### A4 :

>Le système offre un service REST permettant d'obtenir la liste des contrevenants ayant commis une
infraction entre deux dates spécifiées en paramètre. Les dates sont spécifiées selon le format ISO 8601.
Les données retournées sont en format JSON.
Ex. GET /contrevenants?du=2018-05-08&au=2020-05-15
Une groupe /doc doit être disponible et afficher la représentation HTML de la document RAML du
service web.

Fonctionnalite terminee.

Vous pouvez essayer : 
* http://localhost:5000/contrevenants?du=2018-05-08&au=2020-05-15

Vous verrez alors un fichier Json contenant la liste des contrevenants ainsi que les proprietaires des etablissements durant la periode selectionnee.

La documentation est disponible sur : 
* http://localhost:5000/doc
### A5 :

>Sur la page d’accueil du site web, ajouter un petit formulaire de recherche rapide permettant de saisir
deux dates. Lorsque l'utilisateur lance la recherche, une requête Ajax contenant les deux dates saisies
est envoyée à la route définie en A4. Lorsque la réponse Ajax revient, l'application affiche la liste des 
contrevenants dans un tableau. Le tableau contient 2 colonnes :
• le nom de l’établissement;
• le nombre de contraventions obtenues durant cette période de temps.

Fonctionnalite terminee. 

Utilisez simplement les selecteurs de date presents sur la page daccueil puis le bouton "Valider" pour voir apparaitre le tableau.

### A6 :

>L'application du point A5 offre un mode de recherche par nom du restaurant. La liste de tous les
contrevenants est prédéterminée dans une liste déroulante et l'utilisateur choisira un restaurant parmi
cette liste. Lorsque l'utilisateur lance la recherche, une requête Ajax est envoyée à un service REST que
vous devez créer à cet effet. Lorsque la réponse Ajax revient, l'application affiche l'information des
différentes infractions du restaurant.

Fonctionnalite terminee.

Apres avoir fait apparaitre le tableau du point A5 vous aurez un selecteur de restaurant, selectionnez l'un d'entre eux puis faites "Valider" (un nouveau bouton apparu a gauche du selecteur).

### C1 :

>Le système offre un service REST permettant d'obtenir la liste des établissements ayant commis une ou
plusieurs infractions. Pour chaque établissement, on indique le nombre d'infractions connues. La liste
est triée en ordre décroissant du nombre d'infractions. Le service doit être documenté avec RAML sur /
doc.

Fonctionnalite terminee.

Vous pouvez essayer : 
* http://localhost:5000/infractions

Vous verrez alors un fichier Json contenant la liste des etablissement ayant commis des infractions ainsi aue le nombre d'infractions commises.

La documentation est disponible sur : 
* http://localhost:5000/doc


### C2 :

>Le système offre un service permettant d'obtenir exactement les mêmes données que le point C1 mais
en format XML. L'encodage de caractères doit être UTF-8. Le service doit être documenté avec RAML
sur /doc.

Fonctionnalite terminee.

Vous pouvez essayer : 
* http://localhost:5000/infractionsXML

Vous verrez alors un fichier XML contenant la liste des etablissement ayant commis des infractions ainsi aue le nombre d'infractions commises.

La documentation est disponible sur : 
* http://localhost:5000/doc

### C3:

>Le système offre un service permettant d'obtenir exactement les mêmes données que le point C1 mais
en format CSV. L'encodage de caractères doit être UTF-8. Le service doit être documenté avec RAML
sur /doc.

Fonctionnalite terminee.

Vous pouvez essayer : 
* http://localhost:5000/infractionsCSV

Vous verrez alors un fichier CSV contenant la liste des etablissement ayant commis des infractions ainsi aue le nombre d'infractions commises.

La documentation est disponible sur : 
* http://localhost:5000/doc

### D1:

>Le système offre un service REST permettant de faire une demande d’inspection à la ville. Le
document JSON doit être validé avec json-schema. Le service doit permettre de recevoir les données
suivantes :
• le nom de l’établissement;
• l’adresse;
• la ville;
• la date de la visite du client;
• le nom et prénom du client faisant la plainte;
• une description du problème observé.
Le service doit être documenté avec RAML sur /doc.
Ensuite, une page de plainte doit permettre à un visiteur sur le site web de faire une plainte à propos
d’un restaurant. La page de plainte doit offrir un formulaire et la page doit invoquer le service REST de
création d’une demande d’inspection. Indice : la requête doit être envoyée au backend par du
Javascript.

Fonctionnalite terminee.

Depuis la page d'accueil vous avez acces a un bouton permettant de demander une inspection. Vous pouvez aussi essayer 
* http://localhost:5000/inspection

Une fois le formulaire rempli, envoyez le pour voir le Json cree.

La documentation est disponible sur : 
* http://localhost:5000/doc


### F1:

>Le système est entièrement déployé sur la plateforme infonuagique Heroku. Pour compléter ce point,
vous pouvez transformer votre projet pour utiliser la base de données PostgreSQL. Il est possible de le
faire avec SQLite, c’est donc à votre discrétion.

Fonctionnalite terminee. (toujours sous SQLite)
Il suffit de suivre le lien 
* [ProjetHeroku](https://tpweb2x067.herokuapp.com)


## Installation

Vous aurez besoin des dependances suivantes :


```sh
$ pip3 install flask
$ pip3 install flask-excel
$ pip3 install flask-restful
$ pip3 install jsonschema
$ pip3 install apscheduler
$ pip3 install sqlite3
$ pip3 install requests
```


