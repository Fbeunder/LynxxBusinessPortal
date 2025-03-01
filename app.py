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
from user_preferences import UserPreferences

# Initialiseer Flask applicatie
app = Flask(__name__)
app.config.from_object(Config)

# Initialiseer sessie
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Jinja filters toevoegen
@app.template_filter('now')
def _jinja2_filter_now(format_=None):
    """Jinja filter voor de huidige datum/tijd."""
    return datetime.datetime.now()

# Maak 'now' functie beschikbaar in templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now}

# Maak 'is_admin' functie beschikbaar in templates
@app.context_processor
def inject_admin_check():
    return {'is_admin': auth.is_admin}

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
    
    # Pas gebruikersvoorkeuren toe op de apps
    if user_info:
        apps = UserPreferences.apply_preferences(user_info.get("id"), apps)
    
    return render_template('index.html', user=user_info, apps=apps, personalize=True)

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
    Admin dashboard route.
    Alleen toegankelijk voor gebruikers met admin-rechten.
    """
    user_info = auth.get_user_info()
    apps = Config.load_apps().get("apps", [])
    
    return render_template('admin.html', user=user_info, apps=apps)

# API routes voor app-beheer
@app.route('/api/apps', methods=['GET'])
@auth.require_admin
def get_apps():
    """
    API endpoint om alle apps op te halen.
    """
    apps = Config.load_apps().get("apps", [])
    return jsonify({"status": "success", "apps": apps})

@app.route('/api/apps', methods=['POST'])
@auth.require_admin
def add_app():
    """
    API endpoint om een nieuwe app toe te voegen.
    """
    try:
        # Valideer invoer
        data = request.get_json()
        if not data or not all(key in data for key in ["name", "url", "description"]):
            return jsonify({"status": "error", "message": "Missende verplichte velden"}), 400
        
        # Haal huidige apps op
        apps_data = Config.load_apps()
        
        # Voeg nieuwe app toe
        app_data = {
            "name": data["name"],
            "url": data["url"],
            "description": data["description"],
            "icon": data.get("icon", "link")
        }
        apps_data["apps"].append(app_data)
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            return jsonify({"status": "success", "app": app_data}), 201
        else:
            return jsonify({"status": "error", "message": "Kon app niet opslaan"}), 500
    except Exception as e:
        logging.error(f"Error adding app: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/apps/<int:app_id>', methods=['PUT'])
@auth.require_admin
def update_app(app_id):
    """
    API endpoint om een bestaande app bij te werken.
    """
    try:
        # Valideer invoer
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Geen data ontvangen"}), 400
        
        # Haal huidige apps op
        apps_data = Config.load_apps()
        
        # Controleer of app bestaat
        if app_id < 0 or app_id >= len(apps_data["apps"]):
            return jsonify({"status": "error", "message": "App niet gevonden"}), 404
        
        # Update app
        app = apps_data["apps"][app_id]
        app["name"] = data.get("name", app["name"])
        app["url"] = data.get("url", app["url"])
        app["description"] = data.get("description", app["description"])
        app["icon"] = data.get("icon", app.get("icon", "link"))
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            return jsonify({"status": "success", "app": app})
        else:
            return jsonify({"status": "error", "message": "Kon app niet opslaan"}), 500
    except Exception as e:
        logging.error(f"Error updating app: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/apps/<int:app_id>', methods=['DELETE'])
@auth.require_admin
def delete_app(app_id):
    """
    API endpoint om een app te verwijderen.
    """
    try:
        # Haal huidige apps op
        apps_data = Config.load_apps()
        
        # Controleer of app bestaat
        if app_id < 0 or app_id >= len(apps_data["apps"]):
            return jsonify({"status": "error", "message": "App niet gevonden"}), 404
        
        # Verwijder app
        deleted_app = apps_data["apps"].pop(app_id)
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            return jsonify({"status": "success", "deleted": deleted_app})
        else:
            return jsonify({"status": "error", "message": "Kon app niet verwijderen"}), 500
    except Exception as e:
        logging.error(f"Error deleting app: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/apps/reorder', methods=['POST'])
@auth.require_admin
def reorder_apps():
    """
    API endpoint om de volgorde van apps aan te passen.
    """
    try:
        # Valideer invoer
        data = request.get_json()
        if not data or "order" not in data:
            return jsonify({"status": "error", "message": "Geen volgorde ontvangen"}), 400
        
        # Haal huidige apps op
        apps_data = Config.load_apps()
        current_apps = apps_data["apps"]
        
        # Controleer of de volgorde geldig is
        order = data["order"]
        if not all(isinstance(i, int) and 0 <= i < len(current_apps) for i in order):
            return jsonify({"status": "error", "message": "Ongeldige volgorde"}), 400
        
        # Orden de apps
        new_apps = [current_apps[i] for i in order]
        apps_data["apps"] = new_apps
        
        # Sla de bijgewerkte apps op
        if Config.save_apps(apps_data):
            return jsonify({"status": "success", "apps": new_apps})
        else:
            return jsonify({"status": "error", "message": "Kon volgorde niet opslaan"}), 500
    except Exception as e:
        logging.error(f"Error reordering apps: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# User preference routes
@app.route('/api/user/favorites/<int:app_id>', methods=['POST'])
@auth.require_login
def toggle_favorite(app_id):
    """
    API endpoint om een app als favoriet te markeren of de markering op te heffen.
    """
    try:
        user_info = auth.get_user_info()
        if not user_info:
            return jsonify({"status": "error", "message": "Niet ingelogd"}), 401
        
        # Haal huidige apps op om te valideren dat de app_id bestaat
        apps = Config.load_apps().get("apps", [])
        if app_id < 0 or app_id >= len(apps):
            return jsonify({"status": "error", "message": "App niet gevonden"}), 404
        
        # Toggle favoriet status
        if UserPreferences.toggle_favorite(user_info["id"], app_id):
            # Haal bijgewerkte voorkeuren op
            preferences = UserPreferences.get_preferences(user_info["id"])
            return jsonify({
                "status": "success", 
                "favorites": preferences["favorites"],
                "is_favorite": app_id in preferences["favorites"]
            })
        else:
            return jsonify({"status": "error", "message": "Kon favoriet niet opslaan"}), 500
    except Exception as e:
        logging.error(f"Error toggling favorite: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/user/order', methods=['POST'])
@auth.require_login
def update_user_order():
    """
    API endpoint om de persoonlijke volgorde van apps aan te passen.
    """
    try:
        user_info = auth.get_user_info()
        if not user_info:
            return jsonify({"status": "error", "message": "Niet ingelogd"}), 401
        
        # Valideer invoer
        data = request.get_json()
        if not data or "order" not in data:
            return jsonify({"status": "error", "message": "Geen volgorde ontvangen"}), 400
        
        # Haal huidige apps op
        apps = Config.load_apps().get("apps", [])
        
        # Controleer of de volgorde geldig is
        order = data["order"]
        if not all(isinstance(i, int) and 0 <= i < len(apps) for i in order):
            return jsonify({"status": "error", "message": "Ongeldige volgorde"}), 400
        
        # Update de persoonlijke volgorde
        if UserPreferences.update_order(user_info["id"], order):
            return jsonify({"status": "success", "order": order})
        else:
            return jsonify({"status": "error", "message": "Kon volgorde niet opslaan"}), 500
    except Exception as e:
        logging.error(f"Error updating user order: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/user/preferences', methods=['GET'])
@auth.require_login
def get_user_preferences():
    """
    API endpoint om de voorkeuren van de gebruiker op te halen.
    """
    try:
        user_info = auth.get_user_info()
        if not user_info:
            return jsonify({"status": "error", "message": "Niet ingelogd"}), 401
        
        preferences = UserPreferences.get_preferences(user_info["id"])
        return jsonify({"status": "success", "preferences": preferences})
    except Exception as e:
        logging.error(f"Error getting user preferences: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
