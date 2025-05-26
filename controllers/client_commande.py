#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' selection des linges d'un panier 
    '''
    linges_panier = []
    if len(linges_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , linges_panier=linges_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    #selection du contenu du panier de l'utilisateur
    sql = ''' 
        SELECT * from ligne_panier WHERE utilisateur_id = %s;
    '''
    mycursor.execute(sql,id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'linges dans le ligne_panier', 'alert-warning')
         return redirect('/client/linge/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    
    a = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (a,1,id_client)
    sql = ''' INSERT INTO commande(id_commande, date_achat, etat_id, utilisateur_id) VALUES (null,%s,%s,%s) '''
    mycursor.execute(sql,tuple_insert)

    # numéro de la dernière commande
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()

    for item in items_ligne_panier:
        tuple_delete=(id_client,item['linge_id'])
        print(tuple_delete)

        #obtenir le prix de la ligne de panier
        tuple_select=(item['linge_id'])
        sql = '''
            SELECT linge.prix_linge AS prix
            FROM linge
            WHERE id_linge  = %s;
        '''
        mycursor.execute(sql,tuple_select)
        prix_ligne = mycursor.fetchone()

        # suppression d'une ligne de panier
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s AND linge_id  = %s '''
        mycursor.execute(sql,tuple_delete)

        
        tuple_insert=(id_commande['last_insert_id'],item['linge_id'],prix_ligne['prix'],item['quantite'])
        print(tuple_insert)
        sql = "  INSERT INTO ligne_commande (commande_id, linge_id, prix, quantite) VALUES(%s,%s,%s,%s)"
        mycursor.execute(sql,tuple_insert)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/linge/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''    
        SELECT c.id_commande, c.date_achat,c.etat_id, e.libelle,
        SUM(lc.quantite) AS nbr_linges,
        SUM(lc.prix * lc.quantite) AS prix_total
        FROM commande c
        JOIN etat e ON c.etat_id = e.id_etat
        LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        LEFT JOIN linge l ON lc.linge_id = l.id_linge
        WHERE c.utilisateur_id = %s 
        GROUP BY c.id_commande, c.date_achat, c.etat_id, e.libelle
        ORDER BY c.date_achat DESC
        '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()
    linges_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT l.nom_linge AS nom, lc.quantite, lc.prix, (lc.prix * lc.quantite) AS prix_ligne
             FROM ligne_commande lc
             JOIN linge l ON lc.linge_id = l.id_linge
             WHERE lc.commande_id = %s'''
        mycursor.execute(sql,(id_commande,))
        linges_commande = mycursor.fetchall()

        # partie 2 : selection de l'de l'adrde livraison et de facturation de la commande selectionnéeuration de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , linges_commande=linges_commande
                           , commande_adresses=commande_adresses
                           )

