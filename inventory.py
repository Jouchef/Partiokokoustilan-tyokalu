from db import db

def delItem(id):
    sql2 = "DELETE FROM tavaralistaus WHERE id = :id"
    db.session.execute(sql2, {"id": id})
    db.session.commit()  

def addItem(tuote, kuvaus, maara):
    sql1 = "INSERT INTO tavaralistaus (tuote, kuvaus, maara) VALUES(:tuote, :kuvaus, :maara)"
    db.session.execute(
        sql1, {"tuote": tuote, "kuvaus": kuvaus, "maara": maara})
    db.session.commit() 

def getItems():
    sql = "SELECT tuote, kuvaus, maara, id FROM tavaralistaus"
    result = db.session.execute(sql)
    tuotteet = result.fetchall()
    return tuotteet

def showItemInfo(id):
    sql = "SELECT * FROM tavaralistaus WHERE id=:id"
    tulos = db.session.execute(sql, {"id": id})
    rivi = tulos.fetchall()
    return rivi   

def updateItem(tuote, kuvaus, maara, id):
    sql = "UPDATE tavaralistaus SET tuote=:tuote, kuvaus=:kuvaus, maara=:maara WHERE id=:id"
    db.session.execute(
        sql, {"tuote": tuote, "kuvaus": kuvaus, "maara": maara, "id": id})
    db.session.commit()       