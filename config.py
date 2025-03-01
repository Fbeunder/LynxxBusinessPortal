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
            print(f"Error loading apps configuration: {e}")
            return {"apps": []}
