# app/auth/routes.py
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies
from modules.auth.models import Personne
from modules import mysql
from datetime import datetime, timedelta
import bcrypt

auth_bp = Blueprint('auth', __name__)

# Route d'enregistrement
@auth_bp.route('/register', methods=['POST'])
def register():
    lastname = request.json.get('lastname')
    firstname = request.json.get('firstname')
    sexe = request.json.get('sexe')
    date_naissance = request.json.get('birthday')
    profession = request.json.get('work')
    username = request.json.get('user')
    email = request.json.get('email')
    password = request.json.get('password')
    active = True

    # Hachage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Enregistrement de l'utilisateur dans la base de données
    newUser = Personne(
        nom=lastname, 
        prenom=firstname, 
        sexe=sexe, 
        date_naissance=date_naissance, 
        profession=profession,
        username=username,
        email=email,
        password=hashed_password,
        active=active
    )
    
    newUser.save_to_db()
    
    return jsonify({'message': 'Personne registered successfully'}), 200


# Route de connexion
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Récupération de l'utilisateur depuis la base de données
    personne = Personne.login_query(email=email)
    identifiantGet = personne["id"]
    passwordGet = personne["password"]
 
    if personne and bcrypt.checkpw(password.encode('utf-8'), passwordGet.encode('utf-8')):
        # Génération du token JWT
        access_token = create_access_token(identity=identifiantGet)
        response = make_response(jsonify({'message': 'Login successful', 'access_token': access_token}), 200)
        response.set_cookie('access_token', access_token, httponly=True)
        
        return response, 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


# Route de profil utilisateur
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    personne = Personne.get_by_id(current_user_id)

    if personne:
        return jsonify({'profile':personne}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


#Route de modification de profile
@auth_bp.route('/update/profile', methods=['PUT'])
@jwt_required()
def update():
    current_user_id = get_jwt_identity()
    nom = request.json.get('lastname')
    prenom = request.json.get('firstname')
    sexe = request.json.get('sexe')
    date_naissance = request.json.get('birthday')
    profession = request.json.get('work')
    username = request.json.get('user')
    email = request.json.get('email')
    password = request.json.get('password')
    active = True
    
    personne = Personne.get_by_id(current_user_id)
    personne.update(
        nom=nom, 
        prenom=prenom, 
        sexe=sexe,
        date_naissance=date_naissance, 
        profession=profession, 
        email=email, 
        username=username, 
        password=password, 
        active=active
    )
    
    
    return jsonify({'message': 'Profile updated successfully', 'data': personne})


#Route d'activation/desactivation de profile
@auth_bp.route('/profile/desactive', methods=['PUT'])
@jwt_required()
def desactivate():
    username_id = request.json.get('user')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM personne WHERE id = %s", (username_id,))
    columns = [col[0] for col in cursor.description]
    users_details = dict(zip(columns, cursor.fetchone()))
    active = users_details["active"]
    message = ""
    if(active == True):
        active = False
        message = "Profile desactivated successfully"
    else:
        active = True
        message = "Profile activated successfully"
    
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE personne SET active=%s WHERE id=%s", (active, username_id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': message, 'data': users_details})

# Route de déconnexion (inutile pour les tokens JWT)
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jwt_token = get_jwt()
    jwt_token['exp'] = datetime.utcnow() - timedelta(seconds=1)
    response = make_response(jsonify({'message': 'Logout successful'}), 200)
    unset_jwt_cookies(response)
    return response
