DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS est_de_couleur;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS linge;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS coloris;
DROP TABLE IF EXISTS type_linge;


CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   est_actif TINYINT(1),
   PRIMARY KEY(id_utilisateur)
   
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_etat)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE coloris(
   id_coloris INT AUTO_INCREMENT,
   nom_coloris VARCHAR(50),
   PRIMARY KEY(id_coloris)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE type_linge(
   id_type_linge INT AUTO_INCREMENT,
   libelle_type_linge VARCHAR(50),
   PRIMARY KEY(id_type_linge)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   etat_id INT NOT NULL,
   utilisateur_id INT NOT NULL,
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   PRIMARY KEY(id_commande)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE linge(
   id_linge INT AUTO_INCREMENT,
   nom_linge VARCHAR(50),
   prix_linge DECIMAL(15,2),
   dimension VARCHAR(50),
   description VARCHAR(50),
   fournisseur VARCHAR(50),
   marque VARCHAR(50),
   type_linge_id INT NOT NULL,
   coloris_id INT,
   stock INT,
   image VARCHAR(50),
   
   PRIMARY KEY(id_linge),
   FOREIGN KEY(type_linge_id) REFERENCES type_linge(id_type_linge),
   FOREIGN KEY(coloris_id) REFERENCES coloris(id_coloris)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ligne_commande(
   commande_id INT AUTO_INCREMENT,
   linge_id INT,
   prix DECIMAL(15,2),
   quantite INT,
   
   PRIMARY KEY(commande_id, linge_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(linge_id) REFERENCES linge(id_linge)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ligne_panier(
   utilisateur_id INT AUTO_INCREMENT,
   linge_id INT,
   quantite INT,
   date_ajout DATE,
   
   PRIMARY KEY(utilisateur_id, linge_id), 
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(linge_id) REFERENCES linge(id_linge)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




-- INSERTS : 

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');

INSERT INTO etat(id_etat, libelle) VALUES
(1, 'En cours de traitement'),
(2, 'Expédiée'),
(3, 'Livrée');

INSERT INTO coloris(id_coloris, nom_coloris) VALUES
(1, 'Gris'),
(2, 'Marron'),
(3, 'Rouge'),
(4, 'Bleu'),
(5, 'Vert'),
(6, 'Orange'),
(7, 'Blanc'),
(8, 'Jaune');

INSERT INTO type_linge(id_type_linge, libelle_type_linge) VALUES
(1, 'Nappe'),
(2, 'Serviette'),
(3, 'Kimono'),
(4, 'Plaid'),
(5, 'Tablier'),
(6, 'Chemin de table');

INSERT INTO commande(id_commande, date_achat, etat_id, utilisateur_id) VALUES
(1, '2025-01-20', 1, 1),
(2, '2025-01-21', 2, 2),
(3, '2025-01-22', 3, 3);

INSERT INTO linge(id_linge, nom_linge, prix_linge, dimension, description, fournisseur, marque, type_linge_id, coloris_id, stock, image) VALUES
(1, 'Nappe Farandole', 59.00, '150x150', 'Nappe en coton', 'Fournisseur A', 'Marque A', 1, 4, 10, 'nappe_1.jpg'),
(2, 'Nappe 2', 19.99, '150x200', 'Nappe en lin', 'Fournisseur B', 'Marque B', 1, 5, 15, 'nappe_2.jpg'),
(3, 'Nappe 3', 24.99, '200x200', 'Nappe en soie', 'Fournisseur C', 'Marque C', 1, 7, 5, 'nappe_3.jpg'),
(4, 'Serviette 1', 4.99, '50x100', 'Serviette en coton', 'Fournisseur D', 'Marque D', 2, 4, 50, 'serviette_blue_1.jpg'),
(5, 'Serviette 2', 5.99, '60x120', 'Serviette en lin', 'Fournisseur E', 'Marque E', 2, 8, 40, 'serviette_jaune_2.jpg'),
(6, 'Serviette 3', 6.99, '70x140', 'Serviette en microfibre', 'Fournisseur F', 'Marque F', 2, 1, 30, 'serviette_3.jpg'),
(7, 'Kimono 1', 39.99, 'M', 'Kimono en soie', 'Fournisseur G', 'Marque G', 3, 3, 20, 'kimono_1.jpg'),
(8, 'Kimono 2', 49.99, 'L', 'Kimono en coton', 'Fournisseur H', 'Marque H', 3, 4, 25, 'kimono_2.jpg'),
(9, 'Kimono 3', 59.99, 'XL', 'Kimono en lin', 'Fournisseur I', 'Marque I', 3, 5, 10, 'kimono_3.jpg'),
(10, 'Plaid 1', 24.99, '150x200', 'Plaid en polaire', 'Fournisseur J', 'Marque J', 4, 6, 12, 'Plaid_arange_1.jpg'),
(11, 'Plaid 2', 29.99, '200x220', 'Plaid en laine', 'Fournisseur K', 'Marque K', 4, 7, 8, 'Plaid_blanc_2.jpg'),
(12, 'Plaid 3', 34.99, '220x240', 'Plaid en cachemire', 'Fournisseur L', 'Marque L', 4, 8, 5, 'Plaid_jaune_3.jpg'),
(13, 'Tablier 1', 9.99, 'Unique', 'Tablier en coton', 'Fournisseur M', 'Marque M', 5, 7, 50, 'tablier_1.jpg'),
(14, 'Tablier 2', 11.99, 'Unique', 'Tablier en lin', 'Fournisseur N', 'Marque N', 5, 5, 45, 'Tablier_2.jpg'),
(15, 'Tablier 3', 14.99, 'Unique', 'Tablier en jean', 'Fournisseur O', 'Marque O', 5, 3, 30, 'tablier_3.jpg'),
(16, 'Chemin de table 1', 12.99, '50x150', 'Chemin de table en coton', 'Fournisseur P', 'Marque P', 6, 1, 20, 'chemin_de_table_1.jpg'),
(17, 'Chemin de table 2', 15.99, '50x200', 'Chemin de table en lin', 'Fournisseur Q', 'Marque Q', 6, 2, 18, 'chemin_de_table_2.jpg'),
(18, 'Chemin de table 3', 18.99, '50x250', 'Chemin de table en soie', 'Fournisseur R', 'Marque R', 6, 3, 15, 'chemin_de_table_3.jpg');

INSERT INTO ligne_commande(commande_id, linge_id, prix, quantite) VALUES
(1, 1, 14.99, 2),
(1, 4, 4.99, 10),
(2, 3, 24.99, 1),
(2, 5, 5.99, 5),
(3, 2, 19.99, 1),
(3, 6, 6.99, 7);

-- INSERT INTO ligne_panier(utilisateur_id, linge_id, quantite, date_ajout) VALUES
-- (1, 4, 10, '2025-01-20'),
-- (2, 3, 1, '2025-01-21'),
-- (2, 5, 5, '2025-01-21'),
-- (3, 2, 1, '2025-01-22'),
-- (3, 6, 7, '2025-01-22'),
-- (1, 1, 2, '2025-01-24');


