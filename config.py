#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Configuration

Dit bestand bevat de configuratie voor de Lynxx Business Portal applicatie.
Het laadt instellingen uit omgevingsvariabelen en uit een apps.json bestand.
"""

import os
import json
import logging
from pathlib import Path

class Config:
    """Configuratieklasse voor de applicatie"""
    
    # Basisconfiguratie
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Paden
    BASE_DIR = Path(__file__).resolve().parent
    APPS_CONFIG_FILE = BASE_DIR / 'apps.json'
    
    # Google OAuth configuratie
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # Domein restrictie voor inloggen
    ALLOWED_DOMAIN = "lynxx.com"
    
    # Admin configuratie
    ADMIN_EMAILS = os.environ.get('ADMIN_EMAILS', '').split(',') if os.environ.get('ADMIN_EMAILS') else []
    
    # Logging configuratie
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
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
            with open(cls.APPS_CONFIG_FILE, 'w') as f:
                json.dump(apps_data, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Error saving apps configuration: {e}")
            return False
        
    @classmethod
    def validate_app_data(cls, app_data):
        """
        Valideert de gegevens van een app.
        
        Args:
            app_data (dict): De app gegevens om te valideren.
            
        Returns:
            tuple: (bool, str) Een boolean die aangeeft of de validatie is geslaagd en een foutmelding.
        """
        required_fields = ['name', 'url', 'description']
        for field in required_fields:
            if field not in app_data or not app_data[field]:
                return False, f"Veld '{field}' is verplicht."
        
        if not app_data['url'].startswith(('http://', 'https://')):
            return False, "URL moet beginnen met http:// of https://"
        
        return True, ""
