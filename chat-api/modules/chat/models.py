from datetime import datetime
from modules import mysql

class Converssation(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    code = mysql.Column(mysql.String(50), nullable=False)
    type = mysql.Column(mysql.String(100), nullable=True)
    created_at = mysql.Column(mysql.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, code, type):
        self.code = code
        self.type = type

    def save_to_db(self):
        try:
            mysql.session.add(self)
            mysql.session.commit()
        except mysql.IntegrityError as e:
            mysql.session.rollback()
            print("Erreur : Données en double détectées lors de l'insertion dans la base de données.")

    @staticmethod
    def get_all():
        return Converssation.query.all()

    @staticmethod
    def get_by_id(converssation_id):
        converssation = Converssation.query.get(converssation_id)
        return {
            "id": converssation.id,
            "code": converssation.code,
            "type": converssation.type,
            "created_at": converssation.created_at
        }

    def update(self, code, type):
        self.code = code
        self.type = type
        mysql.session.commit()

    def delete(self):
        mysql.session.delete(self)
        mysql.session.commit()


class Participant(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    converssation_id = mysql.Column(mysql.Integer, nullable=False)
    personne_id = mysql.Column(mysql.Integer, nullable=False)
    created_at = mysql.Column(mysql.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, converssation_id, personne_id):
        self.converssation_id = converssation_id
        self.personne_id = personne_id

    def save_to_db(self):
        try:
            mysql.session.add(self)
            mysql.session.commit()
        except mysql.IntegrityError as e:
            mysql.session.rollback()
            print("Erreur : Données en double détectées lors de l'insertion dans la base de données.")

    @staticmethod
    def get_all():
        return Participant.query.all()

    @staticmethod
    def get_by_converssation_id(converssation_id):
        participant =  mysql.session.query(Participant).filter(Participant.converssation_id == converssation_id).all()
        data = [
            {
                'id': item.id,
                'personne_id': item.personne_id
            }
            for item in participant
        ]
        
        return data

    def update(self, converssation_id, participant_id):
        self.converssation_id = converssation_id
        self.participant_id = participant_id
        mysql.session.commit()

    def delete(self):
        mysql.session.delete(self)
        mysql.session.commit()
        

class Message(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    converssation_id = mysql.Column(mysql.Integer, nullable=False)
    personne_id = mysql.Column(mysql.Integer, nullable=False)
    content = mysql.Column(mysql.String(100), nullable=True)
    created_at = mysql.Column(mysql.DateTime, default=datetime.utcnow, nullable=True)

    def __init__(self, converssation_id, personnel_id, content):
        self.converssation_id = converssation_id
        self.personne_id = personnel_id
        self.content = content

    def save_to_db(self):
        try:
            mysql.session.add(self)
            mysql.session.commit()
        except mysql.IntegrityError as e:
            mysql.session.rollback()
            print("Erreur : Données en double détectées lors de l'insertion dans la base de données.")


    def delete(self):
        mysql.session.delete(self)
        mysql.session.commit()
        
    @staticmethod
    def get_all(converssation_id):
        message = mysql.session.query(Message).filter(Message.converssation_id == converssation_id).all()
        data = [
            {
                'id': item.id,
                'converssation': item.converssation_id,
                'sender': item.personne_id,
                'content': item.content,
                'created_at': item.created_at
            }
            for item in message
        ]
        
        return data