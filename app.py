#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Main Application

Dit is de hoofdmodule van de Lynxx Business Portal applicatie.
Het bevat de Flask applicatie en routes voor de webinterface.
"""

import os
import json
import datetime
import logging
from flask import Flask, render_template, redirect, url_for, session, jsonify, request, abort, flash
from flask_session import Session
from config import Config
import auth

# Initialiseer Flask applicatie
app = Flask(__name__)
app.config.from_object(Config)

# Configureer logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('lynxx_portal')

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
    
    # Controleer of de gebruiker admin is
    is_admin = auth.is_admin()
    
    # Laad apps uit de configuratie
    apps = Config.load_apps().get("apps", [])
    
    return render_template('index.html', user=user_info, apps=apps, is_admin=is_admin)

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

# Admin routes
@app.route('/admin')
@auth.require_admin
def admin_dashboard():
    """
    Admin dashboard voor app-beheer.
    Alleen toegankelijk voor gebruikers met admin-rechten.
    """
    user_info = auth.get_user_info()
    apps = Config.load_apps().get("apps", [])
    return render_template('admin.html', user=user_info, apps=apps, is_admin=True)

@app.route('/admin/apps', methods=['POST'])
@auth.require_admin
def add_app():
    """
    API endpoint voor het toevoegen van een app.
    """
    try:
        app_data = request.json
        
        # Valideer de app data
        valid, message = Config.validate_app_data(app_data)
        if not valid:
            return jsonify({"success": False, "message": message}), 400
        
        # Laad bestaande apps
        apps_data = Config.load_apps()
        
        # Voeg nieuwe app toe
        apps_data["apps"].append(app_data)
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            logger.info(f"App toegevoegd: {app_data['name']}")
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Fout bij opslaan van apps"}), 500
    
    except Exception as e:
        logger.error(f"Fout bij toevoegen app: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/admin/apps/<int:app_id>', methods=['PUT'])
@auth.require_admin
def update_app(app_id):
    """
    API endpoint voor het bijwerken van een app.
    """
    try:
        app_data = request.json
        
        # Valideer de app data
        valid, message = Config.validate_app_data(app_data)
        if not valid:
            return jsonify({"success": False, "message": message}), 400
        
        # Laad bestaande apps
        apps_data = Config.load_apps()
        
        # Controleer of de app bestaat
        if app_id >= len(apps_data["apps"]):
            return jsonify({"success": False, "message": "App niet gevonden"}), 404
        
        # Werk de app bij
        apps_data["apps"][app_id] = app_data
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            logger.info(f"App bijgewerkt: {app_data['name']}")
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Fout bij opslaan van apps"}), 500
    
    except Exception as e:
        logger.error(f"Fout bij bijwerken app: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/admin/apps/<int:app_id>', methods=['DELETE'])
@auth.require_admin
def delete_app(app_id):
    """
    API endpoint voor het verwijderen van een app.
    """
    try:
        # Laad bestaande apps
        apps_data = Config.load_apps()
        
        # Controleer of de app bestaat
        if app_id >= len(apps_data["apps"]):
            return jsonify({"success": False, "message": "App niet gevonden"}), 404
        
        # Verwijder de app
        deleted_app = apps_data["apps"].pop(app_id)
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            logger.info(f"App verwijderd: {deleted_app['name']}")
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Fout bij opslaan van apps"}), 500
    
    except Exception as e:
        logger.error(f"Fout bij verwijderen app: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/admin/apps/reorder', methods=['POST'])
@auth.require_admin
def reorder_apps():
    """
    API endpoint voor het herordenen van apps.
    """
    try:
        data = request.json
        order = data.get('order', [])
        
        # Laad bestaande apps
        apps_data = Config.load_apps()
        
        # Controleer of de volgorde geldig is
        if len(order) != len(apps_data["apps"]):
            return jsonify({"success": False, "message": "Ongeldige volgorde"}), 400
        
        # Maak een nieuwe lijst met de juiste volgorde
        new_apps = []
        for i in order:
            if i >= len(apps_data["apps"]):
                return jsonify({"success": False, "message": "Ongeldige volgorde"}), 400
            new_apps.append(apps_data["apps"][i])
        
        # Update de apps
        apps_data["apps"] = new_apps
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            logger.info("Apps volgorde bijgewerkt")
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Fout bij opslaan van apps"}), 500
    
    except Exception as e:
        logger.error(f"Fout bij herordenen apps: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.errorhandler(403)
def forbidden(e):
    """Afhandeling van 403 fouten"""
    return render_template('error.html', error=403), 403

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=Config.DEBUG)
