from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
jwt = JWTManager(app)


# Route d'enregistrement
@app.route('/register', methods=['POST'])
def register():
    nom = request.json.get('lastname')
    prenom = request.json.get('firstname')
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
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO personne (nom,prenom,sexe,date_naissance,profession,email,username,password,active)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nom, prenom, sexe, date_naissance, profession, email, username, hashed_password, active))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Personne registered successfully'})


# Route de connexion
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Récupération de l'utilisateur depuis la base de données
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, password FROM personne WHERE email = %s", (email,))
    user = cursor.fetchone()
    identifiantGet = user[0]
    passwordGet = user[1]
    cursor.close()


    if user and bcrypt.checkpw(password.encode('utf-8'), passwordGet.encode('utf-8')):
        # Génération du token JWT
        access_token = create_access_token(identity=identifiantGet)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


# Route de profil utilisateur
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM personne WHERE id = %s", (current_user_id,))
    columns = [col[0] for col in cursor.description]
    users_details = dict(zip(columns[:-2], cursor.fetchone()[:-2]))
    cursor.close()

    if users_details:
        return jsonify({'profile':users_details}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


#Route de modification de profile
@app.route('/update/profile', methods=['PUT'])
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
    
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE personne SET nom=%s, prenom=%s, sexe=%s, date_naissance=%s, profession=%s, email=%s, username=%s WHERE id=%s", (nom, prenom, sexe, date_naissance, profession, email, username, current_user_id))
    mysql.connection.commit()
    cursor.close()
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM personne WHERE id = %s", (current_user_id,))
    columns = [col[0] for col in cursor.description]
    users_details = dict(zip(columns[:-2], cursor.fetchone()[:-2]))
    
    return jsonify({'message': 'Profile updated successfully', 'data': users_details})


#Route d'activation/desactivation de profile
@app.route('/profile/desactive', methods=['PUT'])
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
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200
