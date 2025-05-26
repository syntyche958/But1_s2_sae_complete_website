#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''  
        SELECT c.id_commande,u.login, c.date_achat,e.libelle,c.etat_id,
        SUM(lc.quantite) AS nbr_linges,
        SUM(lc.prix * lc.quantite) AS prix_total
        FROM commande c
        JOIN etat e ON c.etat_id = e.id_etat
        JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
        LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        WHERE c.utilisateur_id != %s
        GROUP BY c.id_commande '''
    mycursor.execute(sql, (admin_id,))
    commandes=mycursor.fetchall()


    linges_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = ''' SELECT l.nom_linge as nom, lc.prix, lc.quantite,(lc.prix* lc.quantite) AS prix_ligne
            FROM ligne_commande lc
            JOIN linge l ON lc.linge_id = l.id_linge
            WHERE lc.commande_id = %s'''
        mycursor.execute(sql,(id_commande,))
        linges_commande = mycursor.fetchall()


        sql_adresse = '''SELECT u.email
                         FROM utilisateur u
                         JOIN commande c ON u.id_utilisateur = c.utilisateur_id
                         WHERE c.id_commande = %s '''
        mycursor.execute(sql_adresse,(id_commande,))
        commande_adresses = mycursor.fetchall()

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , linges_commande=linges_commande
                           ,commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    etat_id = request.form.get('etat_id', None)
    if commande_id != None:
        if etat_id == "1":    
            sql = '''  UPDATE commande 
                        SET etat_id = 2 
                        WHERE id_commande = %s '''
            mycursor.execute(sql,(commande_id,))

            sql_update_stock = ''' UPDATE linge l
                                    JOIN ligne_commande lc ON l.id_linge = lc.linge_id
                                    SET l.stock = l.stock - lc.quantite
                                    WHERE lc.commande_id = %s'''
            mycursor.execute(sql_update_stock,(commande_id,))
    get_db().commit()

    return redirect('/admin/commande/show')


