from flask import Flask, request, flash
from flask import redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql
from sqlalchemy.sql.elements import Null
import os
from os import getenv
from functools import wraps

def autGuard(f):
    @wraps(f)
    def checklogin(*args, **kwargs):
        username = session.get("username", "null")
        if username == "null":
            flash("Kirjaudu sisään käyttääksesi sivustoa")
            return redirect("/")
        return f(*args, **kwargs)

    return checklogin

def adminGuard(f):
    @wraps(f)
    def checklogin(*args, **kwargs):
        role = session.get("role", "null")
        if role not in ["sadmin", "admin"]:
            flash("Sinulla ei ole tälle sivulle käyttöoikeutta.")
            return redirect("/")
        return f(*args, **kwargs)

    return checklogin

def sadminGuard(f):
    @wraps(f)
    def checklogin(*args, **kwargs):
        role = session.get("role")
        if role != "sadmin":
            flash("Sinulla ei ole tälle sivulle käyttöoikeutta..")
            return redirect("/")
        return f(*args, **kwargs)

    return checklogin