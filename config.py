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
    
    # Google OAuth configuratie (zal later worden ingevuld)
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # Domein restrictie voor inloggen
    ALLOWED_DOMAIN = "lynxx.com"
    
    # Default apps wanneer apps.json ontbreekt of ongeldig is
    DEFAULT_APPS = {
        "apps": [
            {
                "name": "Gmail",
                "url": "https://gmail.com",
                "description": "Google Mail",
                "icon": "📧"
            },
            {
                "name": "Harvest",
                "url": "https://lynxx.harvestapp.com",
                "description": "Time tracking",
                "icon": "⏰"
            },
            {
                "name": "Confluence",
                "url": "https://lynxx.atlassian.net/wiki/home",
                "description": "Knowledge base",
                "icon": "📚"
            }
        ]
    }
    
    @classmethod
    def validate_apps_data(cls, data):
        """
        Valideert de structuur van de app configuratie.
        
        Args:
            data (dict): De te valideren app configuratie
            
        Returns:
            bool: True als de data geldig is, anders False
        """
        if not isinstance(data, dict) or "apps" not in data:
            logging.error("Apps data mist 'apps' key of is geen dictionary")
            return False
            
        if not isinstance(data["apps"], list):
            logging.error("Apps data bevat geen lijst van apps")
            return False
            
        required_keys = ["name", "url", "description"]
        
        for app in data["apps"]:
            if not isinstance(app, dict):
                logging.error(f"App is geen dictionary: {app}")
                return False
                
            # Controleer of alle verplichte sleutels aanwezig zijn
            for key in required_keys:
                if key not in app:
                    logging.error(f"App mist verplichte sleutel '{key}': {app}")
                    return False
                    
            # Controleer of URL geldig is
            if not app["url"].startswith(("http://", "https://")):
                logging.error(f"App URL is ongeldig (moet beginnen met http:// of https://): {app['url']}")
                return False
                
        return True
    
    @classmethod
    def load_apps(cls):
        """
        Laad de app configuratie uit het apps.json bestand.
        
        Returns:
            dict: Een dictionary met app configuraties.
        """
        try:
            if cls.APPS_CONFIG_FILE.exists():
                with open(cls.APPS_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if cls.validate_apps_data(data):
                        return data
                    else:
                        logging.warning("Ongeldig apps.json bestand gevonden, terugvallen op standaardconfiguratie")
                        return cls.DEFAULT_APPS
            else:
                logging.warning(f"Apps configuratiebestand niet gevonden: {cls.APPS_CONFIG_FILE}")
                return cls.DEFAULT_APPS
        except json.JSONDecodeError as e:
            logging.error(f"Fout bij het parsen van apps.json: {e}")
            return cls.DEFAULT_APPS
        except Exception as e:
            logging.error(f"Fout bij het laden van apps.json: {e}")
            return cls.DEFAULT_APPS
