from app import app
from flask import Flask, request, flash
from flask import redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from sqlalchemy import sql
from sqlalchemy.sql.elements import Null
import os
from os import getenv
from authCheck import autGuard, adminGuard, sadminGuard
from db import db
import users
import inventory
import diary
import datetime

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#app.secret_key = getenv("SECRET_KEY")
#db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    """Tarkistetaan tunnukset"""
    user = users.login(username)
    if user == None:
        """väärä käyttäjänimi"""
        flash("Väärä käyttäjänimi!")
    else:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            """Oikeat tunnukset"""
            session["username"] = username
            session["role"] = user[2]
            session["id"] = user[0]
            session["csrf_token"] = os.urandom(16).hex()

        else:
            """väärä salasana"""
            flash("Väärä salasana!")

    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    del session["role"]
    del session["id"]
    del session["csrf_token"]
    flash("Kirjauduit onnistuneesti ulos.")
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    names = users.askUsernames()
    for name in names:
        print(name[0])
        if username == name[0]:
            flash("Tämä käyttäjänimi on jo käytössä. Valitse joku toinen.")
            return render_template("register.html", username=username, password=password)
    users.addUser(username, password, hash_value)
    flash("Käyttäjä rekisteröity onnistuneesti.")
    return redirect("/")


@app.route("/registerinput", methods=["GET"])
def registerinput():
    return render_template("register.html")


@app.route("/hallinnoikayttajia", methods=["GET"])
@autGuard
def hallinnoikayttajia():
    tiedot = users.getUsersByRole()
    id = session["id"]
    return render_template("hallinnoikayttajia.html", tiedot=tiedot, id=id)


@app.route("/muutaroolia", methods=["POST"])
@autGuard
@sadminGuard
def muutaroolia():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    role = request.form["roolit"]
    id = request.form["id"]
    users.changeRole(role, id)
    return redirect("/hallinnoikayttajia")


@app.route("/poistakayttaja", methods=["POST"])
@autGuard
@sadminGuard
def poistakayttaja():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    id = request.form["id"]
    users.deleteUser(id)
    return redirect("/hallinnoikayttajia")


@app.route("/inventaario", methods=["GET", "POST"])
@autGuard
def inventaario():
    if request.method == "POST":
        if "id" in request.form:
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            id = request.form["id"]
            inventory.delItem(id)
        else:
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            tuote = request.form["tuote"]
            kuvaus = request.form["kuvaus"]
            maara = request.form["maara"]
            inventory.addItem(tuote, kuvaus, maara)
    tuotteet = inventory.getItems()
    return render_template("inventaario.html", tuotteet=tuotteet)


@app.route("/varasto/<int:id>", methods=["GET", "POST"])
@autGuard
@adminGuard
def poll(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    rivi = inventory.showItemInfo(id)
    return render_template("muokkaaesinetta.html", id=id, rivi=rivi)


@app.route("/paivitatuote", methods=["POST"])
@autGuard
@adminGuard
def paivitatuote():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    tuote = request.form["tuote"]
    kuvaus = request.form["kuvaus"]
    maara = request.form["maara"]
    id = request.form["id"]
    inventory.updateItem(tuote, kuvaus, maara, id)
    flash("Tuote päivitetty onnistuneesti.")
    return redirect("/inventaario")


@app.route("/paivakirja", methods=["GET", "POST"])
@autGuard
def paivakirja():
    merkinnat = diary.getDiary()
    return render_template("paivakirja.html", merkinnat=merkinnat)


@app.route("/uusikalenterimerkinta", methods=["GET"])
@autGuard
def uusikalenterimerkinta():
    return render_template("uusikalenterimerkinta.html")


@app.route("/lahetakmerkinta", methods=["POST"])
@autGuard
def lahetakmerkinta():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    merkinta = request.form["merkinta"]
    kirjoittaja = request.form["kirjoittaja"]
    diary.newDiaryEntry(merkinta, kirjoittaja)
    flash("Kalenterimerkintä lisätty onnistuneesti.")
    return redirect("/paivakirja")


@app.route("/poistakmerkinta", methods=["POST"])
@autGuard
@adminGuard
def poistakmerkinta():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    poistettava = request.form["poistettavaid"]
    diary.delDiaryEntry(poistettava)
    return redirect("/paivakirja")


@app.route("/kavijalaskuri", methods=["GET"])
@autGuard
def kavijalaskuri():
    now = datetime.datetime.now()
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    dmy = '{}-{}-{}'.format(year, month, day)
    ryhma = ""
    nuoria = 0
    aikuisia = 0
    ulkopaikkakuntalainen = 0
    kaynnit = diary.getVisitors()
    return render_template("kavijalaskuri.html", dmy=dmy, ryhma=ryhma, nuoria=nuoria, aikuisia=aikuisia, ulkopaikkakuntalainen=ulkopaikkakuntalainen, kaynnit=kaynnit)

@app.route("/paivitakavijalaskuri", methods=["POST"])
@autGuard
def paivitakavijalaskuri():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    ryhma = request.form["ryhma"]
    pvm = request.form["pvm"]
    print("päivämäärä: ", pvm)
    nuoria = request.form["nuoria"]
    aikuisia = request.form["aikuisia"]
    ulkopaikkakuntalainen = request.form["ulkopaikkakuntalainen"]
    print(int(nuoria) + int(aikuisia))
    if int(nuoria) + int(aikuisia) < 1:
        print("ulkopaikkakuntalainen: ", ulkopaikkakuntalainen, " nuoria: ", nuoria, " aikuisia: ", aikuisia)
        flash("Lisää useampi kuin nolla osallistujaa.")
        kaynnit = diary.getVisitors()
        return render_template("kavijalaskuri.html", dmy=pvm, ryhma=ryhma, nuoria=nuoria, aikuisia=aikuisia, ulkopaikkakuntalainen=ulkopaikkakuntalainen, kaynnit=kaynnit)
    if int(ulkopaikkakuntalainen) > (int(nuoria) + int(aikuisia)):
        print("ulkopaikkakuntalainen: ", ulkopaikkakuntalainen, " nuoria: ", nuoria, " aikuisia: ", aikuisia)
        flash("Ulkopaikkakuntalaisia ei voi olla enempää kuin kävijöitä yhteensä.")
        kaynnit = diary.getVisitors()
        return render_template("kavijalaskuri.html", dmy=pvm, ryhma=ryhma, nuoria=nuoria, aikuisia=aikuisia, ulkopaikkakuntalainen=ulkopaikkakuntalainen, kaynnit=kaynnit)
    diary.updateVisitors(ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen)
    flash("Kolokäynti lisätty onnistuneesti.")
    return redirect("/kavijalaskuri")


@app.route("/haekavijalaskuri", methods=["GET"])
@autGuard
def haekavijalaskuri():
    nyt = datetime.datetime.now()
    vuosi = '{:02d}'.format(nyt.year)
    kaynnit = diary.getVisitorsByYear(vuosi)
    maara = diary.getVisitorsAmountByYear(vuosi)
    return render_template("haekavijalaskuri.html", kaynnit=kaynnit, vuosi=vuosi, maara=maara)

@app.route("/haevuodenkavijat", methods=["POST"])
@autGuard
def haevuodenkavijat():
    vuosi = request.form["vuosi"]
    kaynnit = diary.getVisitorsByYear(vuosi)
    maara = diary.getVisitorsAmountByYear(vuosi)
    return render_template("haekavijalaskuri.html", kaynnit=kaynnit, vuosi=vuosi, maara=maara)