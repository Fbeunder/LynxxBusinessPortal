#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Main Application

Dit is de hoofdmodule van de Lynxx Business Portal applicatie.
Het bevat de Flask applicatie en routes voor de webinterface.
"""

import os
import sys
import logging
import datetime
from typing import Dict, Any, Optional, Union, Tuple
from flask import Flask, render_template, redirect, url_for, session, jsonify, request, flash, abort
from flask_session import Session
from config import Config
import auth

# Initialiseer logging
logging.basicConfig(
    level=Config.get_log_level(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('app')

# Valideer de configuratie
if not Config.validate_config():
    logger.warning("Configuratie validatie mislukt, applicatie kan mogelijk niet correct werken")
    if not Config.DEBUG:
        logger.error("Configuratieproblemen in productie, applicatie wordt gestopt")
        sys.exit(1)

# Initialiseer Flask applicatie
app = Flask(__name__)
app.config.from_object(Config)

# Configuratie van sessie
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=1)  # Sessie verloopt na 1 dag
Session(app)

# Jinja filters toevoegen
@app.template_filter('now')
def _jinja2_filter_now(format_=None):
    """Jinja filter voor de huidige datum/tijd."""
    return datetime.datetime.now()

@app.template_filter('is_admin')
def _jinja2_filter_is_admin(user):
    """Jinja filter om te controleren of een gebruiker admin rechten heeft."""
    if not user:
        return False
    return Config.is_admin_user(user.get('email'))

@app.route('/')
@auth.require_login
def index():
    """
    Route voor de hoofdpagina.
    Als de gebruiker is ingelogd, toont deze de portal.
    Anders wordt de gebruiker doorgestuurd naar de inlogpagina.
    """
    try:
        # Haal gebruikersinformatie op om weer te geven in de template
        user_info = auth.get_user_info()
        
        # Laad apps uit de configuratie
        apps = Config.load_apps().get("apps", [])
        
        # Voeg informatie toe over of de gebruiker admin rechten heeft
        is_admin = Config.is_admin_user(user_info.get('email')) if user_info else False
        
        return render_template('index.html', 
                              user=user_info, 
                              apps=apps, 
                              is_admin=is_admin,
                              app_name=Config.APP_NAME,
                              app_description=Config.APP_DESCRIPTION)
    except Exception as e:
        logger.error(f"Error bij laden van index pagina: {e}")
        return render_template('error.html', error="Er is een fout opgetreden bij het laden van de portal"), 500

@app.route('/login')
def login():
    """
    Route voor de inlogpagina.
    """
    # Als de gebruiker al is ingelogd, stuur door naar de hoofdpagina
    if auth.get_user_info():
        return redirect(url_for('index'))
    
    return render_template('login.html', app_name=Config.APP_NAME)

@app.route('/login/google')
def google_login():
    """
    Start de Google OAuth flow.
    """
    # Controleer of Google OAuth correct is geconfigureerd
    if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
        logger.error("Google OAuth niet geconfigureerd")
        flash("Google inloggen is niet beschikbaar. Neem contact op met de systeembeheerder.", "error")
        return redirect(url_for('login'))
    
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

@app.route('/api/config/validate', methods=['GET'])
@auth.require_login
def validate_config():
    """
    API endpoint om de configuratie te valideren.
    Alleen toegankelijk voor admin gebruikers.
    """
    user_info = auth.get_user_info()
    if not Config.is_admin_user(user_info.get('email')):
        logger.warning(f"Niet-geautoriseerde toegangspoging tot configuratie validatie door {user_info.get('email')}")
        abort(403)  # Forbidden
    
    result = {
        "valid": Config.validate_config(),
        "apps_config_exists": Config.APPS_CONFIG_FILE.exists(),
        "admin_users_configured": len(Config.ADMIN_USERS) > 0,
        "oauth_configured": bool(Config.GOOGLE_CLIENT_ID and Config.GOOGLE_CLIENT_SECRET)
    }
    
    return jsonify(result)

@app.errorhandler(403)
def forbidden(e):
    """Afhandeling van 403 fouten"""
    logger.warning(f"403 fout: {request.path}")
    return render_template('error.html', error=403, message="Je hebt geen toegang tot deze pagina"), 403

@app.errorhandler(404)
def page_not_found(e):
    """Afhandeling van 404 fouten"""
    logger.warning(f"404 fout: {request.path}")
    return render_template('error.html', error=404, message="Deze pagina bestaat niet"), 404

@app.errorhandler(500)
def server_error(e):
    """Afhandeling van 500 fouten"""
    logger.error(f"500 fout: {str(e)}")
    return render_template('error.html', error=500, message="Er is een interne serverfout opgetreden"), 500

if __name__ == '__main__':
    # Start de ontwikkelingsserver
    # In productie zal een WSGI server worden gebruikt
    logger.info(f"Applicatie {Config.APP_NAME} wordt gestart op {Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
