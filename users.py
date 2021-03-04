from db import db

def login(username):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user

def askUsernames():
    sqlnimet = "SELECT username FROM users"
    names = (db.session.execute(sqlnimet)).fetchall()
    return names

def addUser(username, password, hash_value):
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()    

def getUsersByRole():
    sql = "SELECT id, username, role FROM users ORDER BY role DESC"
    tiedot = (db.session.execute(sql)).fetchall()
    return tiedot

def changeRole(role, id):
    sql = "UPDATE users SET role=:role WHERE id=:id"
    db.session.execute(sql, {"role": role, "id": id})
    db.session.commit()

def deleteUser(id):
    sql = "DELETE FROM users WHERE id = :id"
    db.session.execute(sql, {"id": id})
    db.session.commit()