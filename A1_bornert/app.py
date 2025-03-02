from pyexpat.errors import messages

from flask import Flask, request, render_template, redirect, url_for, abort, flash


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                 # à modifier
            user="lbornert",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_lbornert",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
@app.route('/')

@app.route('/ordinateur/show')
def show_ordinateur():
    mycursor = get_db().cursor()
    sql = '''   SELECT id_ordinateur AS id, marque_ordinateur AS marque, nom_machine AS nom, ram, date_achat, nom_salle AS salle, prix , image
        FROM ordinateur
        LEFT JOIN salle_info
        ON ordinateur.salle_id = salle_info.id_salle
        ORDER BY id; '''
    mycursor.execute(sql)

    liste_ordinateurs = mycursor.fetchall()
    #print(ordinateurs)
    return render_template('ordinateurs/show_ordinateur.html', ordinateur=liste_ordinateurs)

@app.route('/ordinateur/add', methods=['GET'])
def add_ordinateur():
    print('''affichage du formulaire pour saisir un ordinateur''')
    mycursor = get_db().cursor()
    sql = '''   SELECT nom_salle AS nom, id_salle AS id
           FROM salle_info
           ORDER BY nom_salle ASC; '''
    mycursor.execute(sql)

    salle_info = mycursor.fetchall()

    return render_template('ordinateurs/add_ordinateur.html', salle_info=salle_info)

#Prblm valide add regarder par rapport au salle id qui est NULL dans la table + ajoute pas le nouvel ordinateur sur la page mais est présent dans la table
@app.route('/ordinateur/add', methods=['POST'])
def valid_add_ordinateur():
    mycursor = get_db().cursor()
    print('''ajout de l'ordinateur dans le tableau''')
    marque = request.form.get('marque_ordinateur','')
    nom = request.form.get('nom_machine','')
    ram = request.form.get('ram','')
    date_achat = request.form.get('date_achat')
    salle_id = request.form.get('id')
    prix = request.form.get('prix','')
    image = request.form.get('image', '')

    tuple_insert = (nom, marque, ram, date_achat, salle_id, prix, image)

    sql = '''
            INSERT INTO ordinateur(id_ordinateur,nom_machine, marque_ordinateur, ram, date_achat, salle_id, prix, image )
            VALUES (NULL,%s, %s, %s, %s, %s, %s, %s);
        '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()


    message = 'nom_machine :' + str(nom) + ' - marque_ordinateur :' + str(marque) + ' - ram :' + str(ram) + ' - date_achat :' + str(date_achat) + ' - salle :' + str(salle_id) + ' - prix :' + str(prix) + ' - image :' + str(image)
    print(message)
    flash(message, 'alert-success')
    return redirect('/ordinateur/show')

@app.route('/ordinateur/delete', methods=['GET'])
def delete_ordinateur():
    print('''suppression d'un ordinateur''')
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''
        DELETE FROM ordinateur where id_ordinateur=%s;
        '''
    tuple_del = (id)
    mycursor.execute(sql, tuple_del)

    get_db().commit()
    message= u'ordinateur supprimé, id : ' + id
    flash(message, 'alert-danger')
    return redirect('/ordinateur/show')


@app.route('/ordinateur/edit', methods=['GET'])
def edit_ordinateur():
    print('affichage du formulaire pour modifier un ordinateur')
    id = request.args.get('id')
    if id != None and id.isnumeric():
        mycursor = get_db().cursor()

        sql = '''
            SELECT id_ordinateur AS id, marque_ordinateur AS marque, nom_machine AS nom, ram, date_achat, salle_id, prix, image, nom_salle AS nom_salle
            FROM ordinateur
            LEFT JOIN salle_info ON ordinateur.salle_id = salle_info.id_salle
            WHERE ordinateur.id_ordinateur = %s;
        '''
        mycursor.execute(sql, (id,))
        ordinateur = mycursor.fetchone()

        sql_salles = '''
            SELECT id_salle AS id, nom_salle AS nom
            FROM salle_info
            ORDER BY nom_salle ASC;
        '''
        mycursor.execute(sql_salles)
        salles = mycursor.fetchall()

        return render_template('ordinateurs/edit_ordinateur.html',
                               ordinateurs=ordinateur,
                               salleInfo=salles)
    return redirect('/ordinateur/show')
@app.route('/ordinateur/edit', methods=['POST'])
def valid_edit_ordinateur():
    id = request.form.get('id')
    marque = request.form.get('marque')
    nom = request.form.get('nom')
    ram = request.form.get('ram')
    date_achat = request.form.get('date_achat')
    salle_id = request.form.get('salle_id')
    prix = request.form.get('prix')
    image = request.form.get('image')

    message = u'pour l ordinateur d identifiant : '+ id + '  marque_ordinateur :  ' + marque +  '  nom_machine :  ' + nom + '  ram :  ' + ram + '  date_achat :  ' + date_achat + '  salle_id :  ' + salle_id + '  prix :  ' + prix + '  image :  ' + image
    print(message)

    mycursor = get_db().cursor()
    sql = '''
        UPDATE ordinateur 
        SET marque_ordinateur = %s, nom_machine = %s, ram = %s, 
            date_achat = %s, salle_id = %s, prix = %s, image = %s 
        WHERE id_ordinateur = %s;
    '''
    tuple_update = (marque, nom, ram, date_achat, salle_id, prix, image, id)
    mycursor.execute(sql, tuple_update)

    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/ordinateur/show')


@app.route('/ordinateur/filtre', methods=['GET'])
def filtre_ordinateur():
    filtre_marque = request.args.get('marque', '') or session.get('marque', '')
    filtre_nom = request.args.get('nom', '') or session.get('nom', '')
    filtre_prix_min = request.args.get('prix_min', '') or session.get('prix_min', '')
    filtre_prix_max = request.args.get('prix_max', '') or session.get('prix_max', '')
    filtre_items_salle = request.args.getlist('nomSalle') or session.get('nomSalle', [])

    session['marque'] = filtre_marque
    session['nom'] = filtre_nom
    session['prix_min'] = filtre_prix_min
    session['prix_max'] = filtre_prix_max
    session['nomSalle'] = filtre_items_salle

    sql = '''SELECT *, nom_salle, etage
           FROM ordinateur
           JOIN salle_info ON ordinateur.salle_id = salle_info.id_salle'''

    list_param = []
    conditions = []

    if filtre_marque:
        conditions.append("ordinateur.marque_ordinateur LIKE %s")
        list_param.append(f"%{filtre_marque}%")
        flash(u'Filtre sur la marque : ' + filtre_marque, 'alert-success')

    if filtre_nom:
        conditions.append("ordinateur.nom_machine LIKE %s")
        list_param.append(f"%{filtre_nom}%")
        flash(u'Filtre sur le nom : ' + filtre_nom, 'alert-success')

    if filtre_prix_min and filtre_prix_max:
        if filtre_prix_min.isdigit() and filtre_prix_max.isdigit():
            conditions.append("ordinateur.prix BETWEEN %s AND %s")
            list_param.extend([filtre_prix_min, filtre_prix_max])
            flash(u'Filtre sur le prix entre : ' + filtre_prix_min + " et " + filtre_prix_max, 'alert-success')
        else:
            flash(u'Les prix doivent être des nombres', 'alert-warning')

    if filtre_items_salle:
        conditions.append("salle_info.nom_salle IN (" + ",".join(["%s"] * len(filtre_items_salle)) + ")")
        list_param.extend(filtre_items_salle)
        flash(u'Filtre sur les salles : ' + ', '.join(filtre_items_salle), 'alert-success')

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY ordinateur.id_ordinateur"

    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple(list_param))
    ordinateurs = mycursor.fetchall()

    sql_salles = "SELECT DISTINCT nom_salle, etage FROM salle_info ORDER BY nom_salle"
    mycursor.execute(sql_salles)
    salles_info = mycursor.fetchall()

    return render_template('ordinateurs/front_ordinateur_filtre_show.html',ordinateur=ordinateurs,salles_info=salles_info,filtres={'marque': filtre_marque,'nom': filtre_nom,
                               'prix_min': filtre_prix_min,
                               'prix_max': filtre_prix_max,
                               'salles': filtre_items_salle
                           })


@app.route('/ordinateur/filtre/suppr', methods=['GET'])
def suppr_filtre():
    session.pop('marque', None)
    session.pop('nom', None)
    session.pop('prix_min', None)
    session.pop('prix_max', None)
    session.pop('etage', None)
    session.pop('nomSalle', None)
    return redirect('/ordinateur/filtre')


@app.route('/salle-info/show')
def show_salle_info():
    mycursor = get_db().cursor()
    sql = '''   SELECT id_salle AS id, nom_salle AS nom, etage, COUNT(id_ordinateur) AS nb_ordi
        FROM salle_info
        LEFT JOIN ordinateur ON salle_info.id_salle = ordinateur.salle_id
        GROUP BY id_salle, nom_salle, etage
        ORDER BY id; '''
    mycursor.execute(sql)

    liste_salles = mycursor.fetchall()
    return render_template('sallesInfo/show_salle.html', sallesInfo=liste_salles)

@app.route('/salle-info/add', methods=['GET'])
def add_salle():
    print('''affichage du formulaire pour saisir une salle''')
    return render_template('sallesInfo/add_salle.html')

@app.route('/salle-info/add', methods=['POST'])
def valid_add_salle():
    print('''ajout de la salle dans le tableau''')

    nom = request.form.get('nom')
    etage = request.form.get('etage')
    print(nom, etage)
    mycursor = get_db().cursor()

    sql = '''
            INSERT INTO salle_info(id_salle, nom_salle, etage)
            VALUES (NULL, %s, %s);
        '''
    tuple_insert = (nom, etage)
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    message = 'nom_salle :' + str(nom) + ' - etage :' + str(etage)
    print(message)
    flash(message, 'alert-success')
    return redirect('/salle-info/show')

@app.route('/salle-info/delete', methods=['GET'])
def delete_salle():
    print('''suppression d'une salle''')
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id')
    mycursor = get_db().cursor()


    sql = '''
        DELETE FROM salle_info where id_salle =%s;
        '''
    tuple_del = (id)
    mycursor.execute(sql, tuple_del)

    get_db().commit()

    message = u'Salle supprimée, id :' + str(id)
    flash(message, 'alert-danger')
    return redirect('/salle-info/show')

@app.route('/salle-info/edit', methods=['GET'])
def edit_salle():
    print('''affichage du formulaire pour modifier une salle''')
    print(request.args.get('id'))
    id = request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = '''
                SELECT id_salle AS id, nom_salle AS nom, etage
                FROM salle_info
                WHERE id_salle = %s;
                '''
        mycursor.execute(sql, (id))
        salle_info = mycursor.fetchone()
    else:
        salle_info = []
    return render_template('sallesInfo/edit_salle.html', salleinfo=salle_info)

@app.route('/salle-info/edit', methods=['POST'])
def valid_edit_salle():
    print('''modification de la salle dans le tableau''')
    id = request.form.get('id')
    nom = request.form.get('nom')
    etage = request.form.get('etage')
    message = 'nom_salle :' + str(nom) + ' - etage :' + etage + ' pour la salle d identifiant :' + id
    print(message)
    mycursor = get_db().cursor()
    sql = '''
        UPDATE salle_info SET nom_salle = %s, etage =%s WHERE id_salle = %s;
        '''
    tuple_update = (nom, etage, id)
    mycursor.execute(sql, tuple_update)

    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/salle-info/show')


@app.route('/etat/show')
def show_etat():
    mycursor = get_db().cursor()
    sql_etat1 = '''
    SELECT nom_salle AS salle, etage AS etage, COUNT(id_ordinateur) AS nombre_ordinateurs,AVG(ram) AS moyenne_ram,MIN(prix) AS prix_minimum,MAX(prix) AS prix_maximum,SUM(prix) AS valeur_totale,GROUP_CONCAT(DISTINCT marque_ordinateur ORDER BY marque_ordinateur) AS marques
    FROM salle_info LEFT JOIN ordinateur ON salle_info.id_salle = ordinateur.salle_id
    GROUP BY 
    salle_info.id_salle, salle_info.nom_salle, salle_info.etage
    ORDER BY salle_info.etage, Nombre_Ordinateurs DESC;
     '''
    mycursor.execute(sql_etat1)
    liste_ordinateur = mycursor.fetchall()


    # sql_etat2 = '''
    #     SELECT cdt.Nom_centreDeTri AS Centre_De_Tri,COUNT(r.id_tournee) AS Nombre_Tournees
    #     FROM Centre_de_Tri cdt
    #     JOIN recupere r ON cdt.id_centreDeTri = r.id_centreDeTri
    #     GROUP BY cdt.Nom_centreDeTri
    #     ORDER BY Nombre_Tournees DESC;
    #     '''
    #
    # mycursor.execute(sql_etat2)
    # liste_dechets = mycursor.fetchall()

    return render_template('ordinateurs/etat_ordinateur.html', ordi=liste_ordinateur)






if __name__ == '__main__':
    app.run()
