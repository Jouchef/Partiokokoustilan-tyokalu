from flask import Flask,request
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy import sql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #Tarkistetaan tunnukset
    session["usernmae"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/inventaario", methods=["GET", "POST"])
def inventaario():
    if request.method == "POST":
        if "id" in request.form:
            id = request.form["id"]
            sql2 = "DELETE FROM tavaralistaus WHERE id = :id"
            db.session.execute(sql2, {"id":id})
            db.session.commit()
        else:
            tuote = request.form["tuote"]
            kuvaus = request.form["kuvaus"]
            maara = request.form["maara"]
            sql1 = "INSERT INTO tavaralistaus (tuote, kuvaus, maara) VALUES(:tuote, :kuvaus, :maara)"
            db.session.execute(sql1, {"tuote":tuote, "kuvaus":kuvaus, "maara":maara})
            db.session.commit()
    sql = "SELECT tuote, kuvaus, maara, id FROM tavaralistaus"
    result = db.session.execute(sql)
    tuotteet = result.fetchall()
    return render_template("inventaario.html", tuotteet=tuotteet)

@app.route("/varasto/<int:id>", methods=["GET", "POST"])
def poll(id):
    sql = "SELECT * FROM tavaralistaus WHERE id=:id"
    tulos = db.session.execute(sql, {"id":id})
    rivi = tulos.fetchall()
    return render_template("muokkaaesinetta.html", id=id, rivi=rivi)

@app.route("/paivitatuote", methods=["POST"])
def paivitatuote():
    tuote = request.form["tuote"]
    kuvaus = request.form["kuvaus"]
    maara = request.form["maara"]
    id = request.form["id"]
    sql = "UPDATE tavaralistaus SET tuote=:tuote, kuvaus=:kuvaus, maara=:maara WHERE id=:id"
    db.session.execute(sql, {"tuote":tuote, "kuvaus":kuvaus, "maara":maara, "id":id})
    db.session.commit()
    return redirect("/inventaario")


@app.route("/paivakirja", methods=["GET", "POST"])
def paivakirja():
    haku = db.session.execute("SELECT * FROM paivakirja")
    merkinnat = haku.fetchall()
    return render_template("paivakirja.html", merkinnat=merkinnat)


@app.route("/uusikalenterimerkinta", methods=["POST", "GET"])
def uusikalenterimerkinta():
    return render_template("uusikalenterimerkinta.html", )

@app.route("/lahetakmerkinta", methods=["POST"])
def lahetakmerkinta():
    merkinta = request.form["merkinta"]
    kirjoittaja = request.form["kirjoittaja"]
    sql = "INSERT INTO paivakirja (merkinta, kukakirjoitti) VALUES(:merkinta, :kirjoittaja)"
    db.session.execute(sql, {"merkinta":merkinta, "kirjoittaja":kirjoittaja})
    db.session.commit()
    return redirect("/paivakirja")

@app.route("/poistakmerkinta", methods=["POST"])
def poistakmerkinta():
    poistettava = request.form["poistettavaid"]
    sql = "DELETE FROM paivakirja WHERE id = :poistettava"
    db.session.execute(sql, {"poistettava":poistettava})
    db.session.commit()
    return redirect("/paivakirja")