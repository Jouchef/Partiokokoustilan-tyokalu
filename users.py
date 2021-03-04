from db import db

def login(username):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user