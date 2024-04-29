from datetime import datetime
from modules import mysql

model = mysql.Model

class Personne(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    nom = mysql.Column(mysql.String(50), nullable=False)
    prenom = mysql.Column(mysql.String(100), nullable=True)
    sexe = mysql.Column(mysql.String(1), nullable=False)
    date_naissance = mysql.Column(mysql.Date, nullable=True)
    profession = mysql.Column(mysql.String(255), nullable=True)
    email = mysql.Column(mysql.String(255), nullable=False)
    username = mysql.Column(mysql.String(30), nullable=False)
    password = mysql.Column(mysql.String(255), nullable=False)
    active = mysql.Column(mysql.Boolean, default=False)

    def __init__(self, nom, prenom, sexe, date_naissance, profession, email, username, password, active):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.date_naissance = date_naissance
        self.profession = profession
        self.email = email
        self.username = username
        self.password = password
        self.active = active

    def save_to_db(self):
        try:
            mysql.session.add(self)
            mysql.session.commit()
        except mysql.IntegrityError as e:
            mysql.session.rollback()
            print("Erreur : Données en double détectées lors de l'insertion dans la base de données.")

    @staticmethod
    def get_all():
        return Personne.query.all()

    @staticmethod
    def get_by_id(personne_id):
        personne = Personne.query.get(personne_id)
        return {
            "id": personne.id,
            "lastname": personne.nom,
            "fistname": personne.prenom,
            "sexe": personne.sexe,
            "profession": personne.profession,
            "email": personne.email,
            "username": personne.username
        }

    def update(self, nom, prenom, sexe, date_naissance, profession, email, username, password, active):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.date_naissance = date_naissance
        self.profession = profession
        self.email = email
        self.username = username
        self.password = password
        self.active = active
        mysql.session.commit()

    def delete(self):
        mysql.session.delete(self)
        mysql.session.commit()
        
    @staticmethod
    def login_query(email):
        personne = mysql.session.query(Personne).filter(Personne.email == email).first()
        return {
            'id': personne.id,
            'password': personne.password
        }