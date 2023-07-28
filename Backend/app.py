import os
from vector import is_vectoriel
from flask import Flask, render_template, request, session, redirect, url_for
import uuid
app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Assurez-vous de définir une clé secrète appropriée.

id_serveur = str(uuid.uuid4())
print(f"ID du serveur : {id_serveur}")

connected_users = set()


import mysql.connector


mydb = mysql.connector.connect(host="localhost", user="dev", password="", database="table")


@app.before_request
def before_request():
    if 'username' in session:

        if session['id_serveur'] != id_serveur:
            session.clear()
            return redirect(url_for('index'))



@app.route('/')
def index():

    print(connected_users)
    if 'username' in session:

        if session['id_serveur'] != id_serveur:
            session.clear()  # Supprimez toutes les données de session pour l'utilisateur.

        return render_template('dashboard.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        mycursor.execute(f"SELECT * FROM user WHERE name='{username}' AND password='{password}'")
        myresult = mycursor.fetchall()

        if len(myresult) == 0:
            return "Identifiants incorrects"

        # Ici, vous pourriez effectuer une vérification du nom d'utilisateur et du mot de passe,
        # puis stocker les informations dans la session.
        session['username'] = username
        session['id_serveur'] = id_serveur

        # Générez un identifiant de session unique (uuid) et ajoutez-le à la session.
        session['uuid'] = str(uuid.uuid4())
        connected_users.add(session['uuid'])  # Vous pouvez utiliser un identifiant de session unique comme 'uuid'.
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Supprimez les données de la session lors de la déconnexion.
    session.pop('username', None)
    connected_users.discard(session['uuid'])
    return redirect(url_for('index'))

@app.route('/users_count')
def users_count():
    print(connected_users)
    return f"Nombre de personnes connectées : {len(connected_users)}"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Aucun fichier sélectionné."

    file = request.files['file']

    if file.filename == '':
        return "Aucun fichier sélectionné."

    file.save(file.filename)

    # Traitez le fichier selon vos besoins, par exemple, vous pouvez le sauvegarder.
    if is_vectoriel(f"{file.filename}"):
        os.remove(file.filename)
        return "Le fichier est vectoriel !"
    else:
        os.remove(file.filename)
        return "Le fichier n'est pas vectoriel !"




if __name__ == '__main__':
    mydb = mysql.connector.connect(host="localhost", user="dev", password="", database="table")
    mycursor = mydb.cursor()

    app.run()
