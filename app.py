from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from models import db, Livre, Emprunt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    livres = Livre.query.all()
    return render_template('index.html', livres=livres)

@app.route('/ajouter', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']
        categorie = request.form['categorie']
        image_url = request.form['image_url']
        nouveau_livre = Livre(
            titre=titre,
            auteur=auteur,
            annee=annee,
            categorie=categorie,
            image_url=image_url
        )
        db.session.add(nouveau_livre)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    livre = Livre.query.get_or_404(id)
    if request.method == 'POST':
        livre.titre = request.form['titre']
        livre.auteur = request.form['auteur']
        livre.annee = request.form['annee']
        livre.categorie = request.form['categorie']
        livre.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_book.html', livre=livre)

@app.route('/supprimer/<int:id>')
def supprimer(id):
    livre = Livre.query.get_or_404(id)
    db.session.delete(livre)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/emprunter/<int:id>')
def emprunter(id):
    livre = Livre.query.get_or_404(id)
    if livre.disponible:
        emprunt = Emprunt(nom_emprunteur="Lecteur", livre_id=livre.id, date_emprunt=date.today())
        livre.disponible = False
        db.session.add(emprunt)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/retour/<int:id>', methods=['POST'])
def retour(id):
    emprunt = Emprunt.query.get_or_404(id)
    emprunt.date_retour = date.today()
    emprunt.livre.disponible = True
    db.session.commit()
    return redirect(url_for('borrowed_books'))


@app.route('/emprunts')
def borrowed_books():
    emprunts = Emprunt.query.all()
    return render_template('borrowed_books.html', emprunts=emprunts)

if __name__ == '__main__':
    app.run(debug=True)
