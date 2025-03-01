#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Main Application

Dit is de hoofdmodule van de Lynxx Business Portal applicatie.
Het bevat de Flask applicatie en routes voor de webinterface.
"""

import os
from flask import Flask, render_template, redirect, url_for, session, jsonify
from flask_session import Session
from config import Config

# Initialiseer Flask applicatie
app = Flask(__name__)
app.config.from_object(Config)

# Initialiseer sessie
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

@app.route('/')
def index():
    """
    Route voor de hoofdpagina.
    Als de gebruiker is ingelogd, toont deze de portal.
    Anders wordt de gebruiker doorgestuurd naar de inlogpagina.
    """
    # Voorlopig alleen een basispagina renderen
    # Authenticatie wordt later geïmplementeerd
    return render_template('index.html')

@app.route('/login')
def login():
    """
    Route voor de inlogpagina.
    Hier zal later Google OAuth worden geïmplementeerd.
    """
    return render_template('login.html')

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
