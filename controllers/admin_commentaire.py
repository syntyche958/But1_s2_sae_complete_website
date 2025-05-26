#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/linge/commentaires', methods=['GET'])
def admin_linge_details():
    mycursor = get_db().cursor()
    id_linge =  request.args.get('id_linge', None)
    sql = '''    requête admin_type_linge_1    '''
    commentaires = {}
    sql = '''   requête admin_type_linge_1_bis   '''
    linge = []
    sql = '''   requête admin_type_linge_1_3   '''
    nb_commentaires = []
    return render_template('admin/linge/show_linge_commentaires.html'
                           , commentaires=commentaires
                           , linge=linge
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/linge/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_linge = request.form.get('id_linge', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_linge_2   '''
    tuple_delete=(id_utilisateur,id_linge,date_publication)
    get_db().commit()
    return redirect('/admin/linge/commentaires?id_linge='+id_linge)


@admin_commentaire.route('/admin/linge/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_linge = request.args.get('id_linge', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/linge/add_commentaire.html',id_utilisateur=id_utilisateur,id_linge=id_linge,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_linge = request.form.get('id_linge', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_linge_3   '''
    get_db().commit()
    return redirect('/admin/linge/commentaires?id_linge='+id_linge)


@admin_commentaire.route('/admin/linge/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_linge = request.args.get('id_linge', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_linge_4   '''
    get_db().commit()
    return redirect('/admin/linge/commentaires?id_linge='+id_linge)