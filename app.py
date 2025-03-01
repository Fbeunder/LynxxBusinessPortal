#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Main Application

Dit is de hoofdmodule van de Lynxx Business Portal applicatie.
Het bevat de Flask applicatie en routes voor de webinterface.
"""

import os
import datetime
from flask import Flask, render_template, redirect, url_for, session, jsonify
from flask_session import Session
from config import Config
import auth

# Initialiseer Flask applicatie
app = Flask(__name__)
app.config.from_object(Config)

# Initialiseer sessie
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# Jinja filters toevoegen
@app.template_filter('now')
def _jinja2_filter_now(format_=None):
    """Jinja filter voor de huidige datum/tijd."""
    return datetime.datetime.now()

@app.route('/')
@auth.require_login
def index():
    """
    Route voor de hoofdpagina.
    Als de gebruiker is ingelogd, toont deze de portal.
    Anders wordt de gebruiker doorgestuurd naar de inlogpagina.
    """
    # Haal gebruikersinformatie op om weer te geven in de template
    user_info = auth.get_user_info()
    
    # Laad apps uit de configuratie
    apps = Config.load_apps().get("apps", [])
    
    return render_template('index.html', user=user_info, apps=apps)

@app.route('/login')
def login():
    """
    Route voor de inlogpagina.
    """
    # Als de gebruiker al is ingelogd, stuur door naar de hoofdpagina
    if auth.get_user_info():
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    """
    Start de Google OAuth flow.
    """
    return auth.oauth_login()

@app.route('/login/google/callback')
def google_callback():
    """
    Verwerkt de Google OAuth callback.
    """
    return auth.oauth_callback()

@app.route('/logout')
def logout():
    """
    Logt de gebruiker uit.
    """
    return auth.logout()

@app.errorhandler(404)
def page_not_found(e):
    """Afhandeling van 404 fouten"""
    return render_template('error.html', error=404), 404

@app.errorhandler(500)
def server_error(e):
    """Afhandeling van 500 fouten"""
    return render_template('error.html', error=500), 500

if __name__ == '__main__':
    # Start de ontwikkelingsserver
    # In productie zal een WSGI server worden gebruikt
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
