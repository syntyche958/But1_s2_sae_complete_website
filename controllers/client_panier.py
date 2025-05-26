#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_linge = request.form.get('id_linge')
    quantite = request.form.get('quantite')
    
    sql = "SELECT * FROM ligne_panier WHERE linge_id= %s AND utilisateur_id=%s"
    mycursor.execute(sql, (id_linge, id_client)) 
    linge_panier = mycursor.fetchone() 
    print(linge_panier)

    mycursor.execute("SELECT * FROM linge WHERE id_linge = %s", (id_linge)) 
    linge = mycursor.fetchone()
    print("linge : ",quantite,linge['stock'])
    if int(quantite) <= linge['stock'] :
        print("ca passe")
        if not (linge_panier is None) and linge_panier['quantite'] >= 1: 
            tuple_update =(quantite, id_client, id_linge) 
            sql = "UPDATE ligne_panier SET quantite = quantite+%s WHERE utilisateur_id = %s AND linge_id=%s" 
            mycursor.execute(sql, tuple_update) 
        else:
            print("aaaaaaa")
            tuple_insert =(id_client, id_linge, quantite) 
            sql = "INSERT INTO ligne_panier (utilisateur_id,linge_id, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)" 
            mycursor.execute(sql, tuple_insert) 
        tuple_update = (quantite,id_linge)
        sql = ''' # enlever 1 au stock quand un linge est ajouté
            UPDATE linge SET stock = stock - %s WHERE id_linge = %s
        '''
        mycursor.execute(sql,tuple_update)
        get_db().commit()
    else:
        print("test")

    return redirect('/client/linge/show')
    
    
    
    
    # ---------
    #id_declinaison_linge=request.form.get('id_declinaison_linge',None)
    id_declinaison_linge = 1

# ajout dans le panier d'une déclinaison d'un linge (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_linge))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_linge = declinaisons[0]['id_declinaison_linge']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_linge))
    #     linge = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_linge.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , linge=linge)

# ajout dans le panier d'un linge


    return redirect('/client/linge/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_linge = request.form.get('id_linge','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison du linge
    # id_declinaison_linge = request.form.get('id_declinaison_linge', None)

    tuple_sql = (id_client,id_linge)

    sql = ''' #selection de la ligne du panier pour le linge et l'utilisateur connecté
        SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND linge_id = %s;
    '''
    mycursor.execute(sql, tuple_sql)
    linge_panier= mycursor.fetchone()

    if not(linge_panier is None) and linge_panier['quantite'] > 1:
        sql = '''  #mise à jour de la quantité dans le panier => -1 linge
            UPDATE ligne_panier SET quantite = quantite -1 WHERE utilisateur_id = %s AND linge_id = %s;
        '''
    else:
        sql = ''' #suppression de la ligne de panier
            DELETE FROM ligne_panier WHERE utilisateur_id = %s AND linge_id = %s;
        '''
    mycursor.execute(sql, tuple_sql)


    sql = ''' # ajouter 1 au stock quand un linge est ajouté
            UPDATE linge SET stock = stock + 1 WHERE id_linge = %s
        '''
    mycursor.execute(sql,id_linge)


    # mise à jour du stock de l'linge disponible
    get_db().commit()
    return redirect('/client/linge/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    
    sql = ''' #sélection des lignes de panier
        SELECT * FROM ligne_panier WHERE utilisateur_id = %s;
    '''
    mycursor.execute(sql, client_id)
    items_panier= mycursor.fetchall()

    for item in items_panier:
        tuple_delete = (client_id,item['linge_id'])

        sql = ''' #suppression de la ligne de panier du linge pour l'utilisateur connecté
            DELETE FROM ligne_panier WHERE utilisateur_id = %s AND linge_id = %s;
        '''
        mycursor.execute(sql,tuple_delete)

        tuple_stock = (item['quantite'],item['linge_id'])
        sql2=''' #mise à jour du stock de l'linge : stock = stock + qté de la ligne pour l'linge
            UPDATE linge SET stock = stock + %s WHERE id_linge = %s;
        '''
        mycursor.execute(sql2,tuple_stock)

        get_db().commit()
    return redirect('/client/linge/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_linge = request.form.get('id_linge','')

    #id_declinaison_linge = request.form.get('id_declinaison_linge')

    tuple_sql = (id_client,id_linge)


    sql = ''' #selection de ligne du panier
        SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND linge_id = %s; 
    '''
    mycursor.execute(sql, tuple_sql)
    linge_panier= mycursor.fetchone()

    sql = ''' #suppression de la ligne du panier 
        DELETE FROM ligne_panier WHERE utilisateur_id = %s AND linge_id = %s;
    '''
    mycursor.execute(sql, tuple_sql)

    tuple_stock = (linge_panier['quantite'], id_linge)
    sql2=''' #mise à jour du stock de le linge : stock = stock + qté de la ligne pour le linge 
        UPDATE linge SET stock = stock + %s WHERE id_linge = %s;
    '''
    mycursor.execute(sql2,tuple_stock)

    get_db().commit()
    return redirect('/client/linge/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    session['filter_word'] = request.form.get('filter_word', None)
    session['filter_prix_min'] = request.form.get('filter_prix_min', None)
    session['filter_prix_max'] = request.form.get('filter_prix_max', None)
    session['filter_types'] = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/linge/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session['filter_word'] = None
    session['filter_prix_min'] = None
    session['filter_prix_max'] = None
    session['filter_types'] = []
    print("suppr filtre")
    return redirect('/client/linge/show')
