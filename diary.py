from db import db

def getDiary():
    haku = db.session.execute("SELECT * FROM paivakirja ORDER BY id DESC LIMIT 30")
    merkinnat = haku.fetchall()
    return merkinnat

def newDiaryEntry(merkinta, kirjoittaja):
    sql = "INSERT INTO paivakirja (merkinta, kukakirjoitti) VALUES(:merkinta, :kirjoittaja)"
    db.session.execute(sql, {"merkinta": merkinta, "kirjoittaja": kirjoittaja})
    db.session.commit()    

def delDiaryEntry(poistettava):
    sql = "DELETE FROM paivakirja WHERE id = :poistettava"
    db.session.execute(sql, {"poistettava": poistettava})
    db.session.commit()

def getVisitors():
    tulos = db.session.execute("SELECT ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen FROM laskuri ORDER BY id DESC LIMIT 30")
    kaynnit = tulos.fetchall()
    return kaynnit

def updateVisitors(ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen):
    sql = "INSERT INTO laskuri (ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen) VALUES (:ryhma, :pvm, :nuoria, :aikuisia, :ulkopaikkakuntalainen)"
    db.session.execute(sql, {"ryhma": ryhma, "pvm": pvm, "nuoria": nuoria, "aikuisia": aikuisia, "ulkopaikkakuntalainen": ulkopaikkakuntalainen})
    db.session.commit()