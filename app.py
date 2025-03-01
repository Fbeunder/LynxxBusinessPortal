#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Main Application

Dit is de hoofdmodule van de Lynxx Business Portal applicatie.
Het bevat de Flask applicatie en routes voor de webinterface.
"""

import os
import datetime
import logging
from flask import Flask, render_template, redirect, url_for, session, jsonify, request, flash
from flask_session import Session
from config import Config
import auth

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    app_data = Config.load_apps()
    apps = app_data.get("apps", [])
    
    # Log het aantal geladen apps voor debugging
    logger.info(f"Geladen apps: {len(apps)}")
    
    return render_template('index.html', user=user_info, apps=apps)

@app.route('/api/apps')
@auth.require_login
def get_apps():
    """
    API route voor het ophalen van apps als JSON.
    Handig voor frontend JavaScript of mobiele clients.
    """
    app_data = Config.load_apps()
    return jsonify(app_data)

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
    logger.warning(f"404 fout: {request.path}")
    return render_template('error.html', error=404), 404

@app.errorhandler(500)
def server_error(e):
    """Afhandeling van 500 fouten"""
    logger.error(f"500 fout: {str(e)}")
    return render_template('error.html', error=500), 500

if __name__ == '__main__':
    # Start de ontwikkelingsserver
    # In productie zal een WSGI server worden gebruikt
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Lynxx Business Portal on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
