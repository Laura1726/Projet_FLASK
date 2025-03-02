DROP TABLE IF EXISTS ordinateur;
DROP TABLE IF EXISTS salle_info;


CREATE TABLE salle_info (
    id_salle INT AUTO_INCREMENT
    , nom_salle VARCHAR(255)
    , etage INT
    , PRIMARY KEY(id_salle)
);
CREATE TABLE ordinateur
(
    id_ordinateur INT AUTO_INCREMENT
    ,marque_ordinateur VARCHAR(255)
    ,nom_machine       VARCHAR(255)
    ,ram               INT
    ,date_achat        date
    ,prix               DECIMAL
    ,image              VARCHAR(255)
    ,salle_id           INT
    , PRIMARY KEY(id_ordinateur)
    ,constraint FK_SALLE_INFO FOREIGN KEY (salle_id) REFERENCES salle_info(id_salle)
);
INSERT INTO salle_info (id_salle, nom_salle, etage) VALUES
(NULL, 'Alpha',1),
(NULL, 'Mac',2),
(NULL, 'DEC',1);

INSERT INTO ordinateur (id_ordinateur, marque_ordinateur, nom_machine, ram, date_achat, salle_id, prix, image) VALUES
(NULL, 'HP', 'HP-1', 32, '2018-02-15', 1, 1000,'hp.jpg'),
(NULL, 'HP', 'HP-2', 32, '2018-02-15', 1, 1000,'hp.jpg'),
(NULL, 'HP', 'HP-3', 32, '2018-02-15', 1, 1000,'hp.jpg'),
(NULL, 'HP', 'HP-4', 32, '2018-02-15', 1, 1000,'hp.jpg'),
(NULL, 'HP', 'HP-5', 32, '2019-02-15', 1, 1000,'hp.jpg'),
(NULL, 'HP', 'HP-6', 32, '2019-02-15', 1, 1000,'hp.jpg'),
(NULL, 'Apple', 'iMac3', 32, '2020-10-16', 2, 1500,'imac.jpg'),
(NULL, 'Apple', 'iMac1', 32, '2020-10-16', 2, 1500,'imac.jpg'),
(NULL, 'Apple', 'iMac2', 32, '2020-10-16', 2, 1500,'imac.jpg'),
(NULL, 'Apple', 'iMac4', 32, '2018-01-30', 2, 1500,'imac.jpg'),
(NULL, 'Apple', 'MacPro2', 64, '2019-01-30', 2, 1700,'macpro.jpg'),
(NULL, 'Apple', 'MacPro1', 64, '2019-01-30', 2, 1700,'macpro.jpg'),
(NULL, 'Apple', 'iMac7', 32, '2018-01-30', 2, 1500,'imac.jpg'),
(NULL, 'Apple', 'iMac8', 16, '2018-01-30', 2, 1500,'imac.jpg'),
(NULL, 'Dell', 'Dell-1', 32, '2018-07-10', 3, 1100,'dell.jpg'),
(NULL, 'Dell', 'Dell-2', 32, '2018-07-10', 3, 1100,'dell.jpg'),
(NULL, 'Dell', 'Dell-3', 32, '2018-07-10', 3, 1100,'dell.jpg'),
(NULL, 'Dell', 'Dell-4', 32, '2018-07-10', 3, 1100,'dell.jpg'),
(NULL, 'Asus', 'Asus-6', 16, '2018-11-02', 3, 1100,'asus.jpg'),
(NULL, 'Asus', 'Asus-7', 16, '2019-11-02', 3, 900,'asus.jpg'),
(NULL, 'Asus', 'Asus-8', 16, '2019-11-02', 3, 900,'asus.jpg'),
(NULL, 'Asus', 'Asus-9', 16, '2019-11-02', 3, 900,'asus.jpg'),
(NULL, 'MSI', 'MSI-1', 16, '2018-02-18', 3, 800,'msi.jpg'),
(NULL, 'MSI', 'MSI-2', 16, '2018-02-18', 3, 800,'msi.jpg'),
(NULL, 'MSI', 'MSI-3', 16, '2018-02-18', 3, 800,'msi.jpg'),
(NULL, 'MSI', 'MSI-4', 16, '2018-02-18', 3, 800,'msi.jpg');


ALTER TABLE ordinateur DROP FOREIGN KEY FK_SALLE_INFO;
ALTER TABLE ordinateur ADD CONSTRAINT FK_SALLE_INFO FOREIGN KEY (salle_id) REFERENCES salle_info (id_salle) ON DELETE CASCADE;
