create table contrevenants (
	id integer primary key,
	proprietaire varchar(100),
	categorie varchar(50),
	etablissement varchar(50),
	adresse varchar(100),
	ville varchar(50),
	descriptions varchar(500),
	date_infraction date,
	date_jugement date,
	montant decimal
);

