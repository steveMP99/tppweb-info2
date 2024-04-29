from flask_mysqldb import MySQL


# Configuration de Flask JWT Extended
secret_config['JWT_SECRET_KEY'] = 'info2-security'

# Configuration de la base de données MySQL
db_config['MYSQL_HOST'] = 'localhost'
db_config['MYSQL_USER'] = 'root'
db_config['MYSQL_PASSWORD'] = ''
db_config['MYSQL_DB'] = 'user_auth_db'
mysql = MySQL(app)


