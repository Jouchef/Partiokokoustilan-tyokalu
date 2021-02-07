from flask import Flask,request, flash
from flask import redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import sql
from os import getenv
from sqlalchemy.sql.elements import Null
from functools import wraps

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

def autGuard(f):
    @wraps(f)
    def checklogin(*args, **kwargs):
        username = session.get("username", "null")
        if  username == "null":
            flash("Sinulla ei ole lupaa kyseiselle sivulle.")
            return redirect("/")
        return f(*args, **kwargs)

    return checklogin

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #Tarkistetaan tunnukset
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(user)    
    if user == None:
        #väärä käyttäjänimi
        flash("Väärä käyttäjänimi!")
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            #Oikeat tunnukset
            session["username"] = username
            session["rooli"] = user[2]
            session["id"] = user[0]

        else:
            #väärä salasana
            flash("Väärä salasana!")
    
    return redirect("/")

@app.route("/logout")
def logout():
    flash("Kirjauduit onnistuneesti ulos.")
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/registerinput", methods=["POST", "GET"])
def registerinput():
    return render_template("register.html")

@app.route("/inventaario", methods=["GET", "POST"])
@autGuard
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


@app.route("/hallinnoikayttajia", methods=["GET"])
@autGuard
def hallinnoikayttajia():
    sql = "SELECT id, username, role FROM users ORDER BY role DESC"
    tiedot = (db.session.execute(sql)).fetchall()
    id = session["id"]
    return render_template("hallinnoikayttajia.html", tiedot=tiedot, id=id)


@app.route("/muutaroolia", methods=["POST"])
@autGuard
def muutaroolia():
    role = request.form["roolit"]
    id = request.form["id"]
    sql = "UPDATE users SET role=:role WHERE id=:id"
    db.session.execute(sql, {"role":role, "id":id})
    db.session.commit()
    return redirect("/hallinnoikayttajia")


@app.route("/varasto/<int:id>", methods=["GET", "POST"])
@autGuard
def poll(id):
    sql = "SELECT * FROM tavaralistaus WHERE id=:id"
    tulos = db.session.execute(sql, {"id":id})
    rivi = tulos.fetchall()
    return render_template("muokkaaesinetta.html", id=id, rivi=rivi)

@app.route("/paivitatuote", methods=["POST"])
@autGuard
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
@autGuard
def paivakirja():
    haku = db.session.execute("SELECT * FROM paivakirja")
    merkinnat = haku.fetchall()
    return render_template("paivakirja.html", merkinnat=merkinnat)


@app.route("/uusikalenterimerkinta", methods=["POST", "GET"])
@autGuard
def uusikalenterimerkinta():
    return render_template("uusikalenterimerkinta.html", )

@app.route("/lahetakmerkinta", methods=["POST"])
@autGuard
def lahetakmerkinta():
    merkinta = request.form["merkinta"]
    kirjoittaja = request.form["kirjoittaja"]
    sql = "INSERT INTO paivakirja (merkinta, kukakirjoitti) VALUES(:merkinta, :kirjoittaja)"
    db.session.execute(sql, {"merkinta":merkinta, "kirjoittaja":kirjoittaja})
    db.session.commit()
    return redirect("/paivakirja")

@app.route("/poistakmerkinta", methods=["POST"])
@autGuard
def poistakmerkinta():
    poistettava = request.form["poistettavaid"]
    sql = "DELETE FROM paivakirja WHERE id = :poistettava"
    db.session.execute(sql, {"poistettava":poistettava})
    db.session.commit()
    return redirect("/paivakirja")

