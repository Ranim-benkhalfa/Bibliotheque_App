from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    auteur = db.Column(db.String(100))
    annee = db.Column(db.Integer)
    categorie = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(200))

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_emprunteur = db.Column(db.String(100))
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'))
    date_emprunt = db.Column(db.Date)
    date_retour = db.Column(db.Date, nullable=True)
    livre = db.relationship('Livre', backref='emprunts')
