#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Configuration

Dit bestand bevat de configuratie voor de Lynxx Business Portal applicatie.
Het laadt instellingen uit omgevingsvariabelen en uit een apps.json bestand.
"""

import os
import json
from pathlib import Path
import logging

class Config:
    """Configuratieklasse voor de applicatie"""
    
    # Basisconfiguratie
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Paden
    BASE_DIR = Path(__file__).resolve().parent
    APPS_CONFIG_FILE = BASE_DIR / 'apps.json'
    
    # Google OAuth configuratie (zal later worden ingevuld)
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # Domein restrictie voor inloggen
    ALLOWED_DOMAIN = "lynxx.com"
    
    # Admin instellingen
    ADMIN_EMAILS = []
    if os.environ.get('ADMIN_EMAILS'):
        ADMIN_EMAILS = [email.strip() for email in os.environ.get('ADMIN_EMAILS').split(',')]
    elif os.environ.get('ADMIN_EMAIL'):  # Backwards compatibility
        ADMIN_EMAILS = [os.environ.get('ADMIN_EMAIL').strip()]
    # Voeg een standaard admin toe voor ontwikkeling
    if DEBUG and not ADMIN_EMAILS:
        ADMIN_EMAILS = ['admin@lynxx.com']
    
    @classmethod
    def load_apps(cls):
        """
        Laad de app configuratie uit het apps.json bestand.
        
        Returns:
            dict: Een dictionary met app configuraties.
        """
        try:
            if cls.APPS_CONFIG_FILE.exists():
                with open(cls.APPS_CONFIG_FILE, 'r') as f:
                    return json.load(f)
            else:
                # Standaardconfiguratie als het bestand niet bestaat
                return {
                    "apps": [
                        {
                            "name": "Gmail",
                            "url": "https://gmail.com",
                            "description": "Google Mail",
                            "icon": "mail"
                        },
                        {
                            "name": "Harvest",
                            "url": "https://lynxx.harvestapp.com",
                            "description": "Time tracking",
                            "icon": "clock"
                        },
                        {
                            "name": "Confluence",
                            "url": "https://lynxx.atlassian.net/wiki/home",
                            "description": "Knowledge base",
                            "icon": "book"
                        }
                    ]
                }
        except Exception as e:
            logging.error(f"Error loading apps configuration: {e}")
            return {"apps": []}
    
    @classmethod
    def save_apps(cls, apps_data):
        """
        Slaat de app configuratie op in het apps.json bestand.
        
        Args:
            apps_data (dict): Een dictionary met app configuraties.
            
        Returns:
            bool: True als het opslaan is gelukt, anders False.
        """
        try:
            # Valideer de data structuur
            if not isinstance(apps_data, dict) or "apps" not in apps_data:
                apps_data = {"apps": apps_data} if isinstance(apps_data, list) else {"apps": []}
            
            # Zorg ervoor dat elke app een naam, url, beschrijving en icon heeft
            for app in apps_data["apps"]:
                if not all(key in app for key in ["name", "url", "description"]):
                    return False
                # Voeg een standaard icon toe indien niet aanwezig
                if "icon" not in app:
                    app["icon"] = "link"
            
            # Schrijf de configuratie naar het bestand
            with open(cls.APPS_CONFIG_FILE, 'w') as f:
                json.dump(apps_data, f, indent=4)
            
            return True
        except Exception as e:
            logging.error(f"Error saving apps configuration: {e}")
            return False
