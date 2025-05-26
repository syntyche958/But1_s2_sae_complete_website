#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_linge = Blueprint('client_linge', __name__,
                        template_folder='templates')

@client_linge.route('/client/index')
@client_linge.route('/client/linge/show')              # remplace /client
def client_linge_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT id_linge AS id_linge, nom_linge AS nom, prix_linge AS prix, image, stock
    FROM linge
    WHERE 1=1                             
    '''#ajouter stock
    params = []
    if 'filter_types' in session.keys() and session['filter_types']:
        sql += ' AND type_linge_id IN (%s)' % ','.join(['%s'] * len(session['filter_types']))
        params.extend(session['filter_types'])
    if 'filter_word' in session.keys() and session['filter_word']:
        sql += ' AND nom_linge LIKE %s'
        params.append('%' + session['filter_word'] + '%')
    if 'filter_prix_min' in session.keys() and session['filter_prix_min']:
        sql += ' AND prix_linge >= %s'
        params.append(session['filter_prix_min'])
    if 'filter_prix_max' in session.keys() and session['filter_prix_max']:
        sql += ' AND prix_linge <= %s'
        params.append(session['filter_prix_max'])
    mycursor.execute(sql,params)
    linges = mycursor.fetchall()

    sql = '''
        SELECT id_coloris  AS id_type_linge
                ,nom_coloris
                FROM coloris
                ORDER BY  nom_coloris
        '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    types_linge = couleurs

    sql = ''' #"SELECT * , 10 as prix , concat('nomlinge',linge_id) as nom FROM ligne_panier"
        SELECT linge.id_linge, linge.prix_linge as prix, linge.nom_linge AS nom, linge.stock, ligne_panier.quantite
        FROM linge
        JOIN ligne_panier
            ON ligne_panier.linge_id = linge.id_linge;
    '''

    mycursor.execute(sql)
    linges_panier = mycursor.fetchall()
    

    # pour le filtre
    sql="""
        SELECT * FROM type_linge
"""
    mycursor.execute(sql)
    types_linge = mycursor.fetchall()

    


    #linges_panier = []

    if len(linges_panier) >= 1:
        sql = ''' 
            SELECT SUM(linge.prix_linge * ligne_panier.quantite) as prix_total
            FROM linge
            JOIN ligne_panier
                ON linge.id_linge = ligne_panier.linge_id
            WHERE ligne_panier.utilisateur_id =%s;    
            '''
        mycursor.execute(sql,id_client)
        prix_total = mycursor.fetchone()['prix_total']
        print("prix_total : ",prix_total)
    else:
        prix_total = None
    return render_template('client/boutique/panier_linge.html'
                           , linges=linges
                           , linges_panier=linges_panier
                           , prix_total=prix_total
                           , items_filtre=types_linge
                           )
