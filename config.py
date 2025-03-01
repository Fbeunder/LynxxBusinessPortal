#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Configuration

Dit bestand bevat de configuratie voor de Lynxx Business Portal applicatie.
Het laadt instellingen uit omgevingsvariabelen en uit configuratiebestanden.
"""

import os
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dotenv import load_dotenv

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('config')

# Laad .env bestand als het bestaat
load_dotenv()

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
    ALLOWED_DOMAIN = os.environ.get('ALLOWED_DOMAIN') or "lynxx.com"
    
    # Admin configuratie
    ADMIN_USERS = os.environ.get('ADMIN_USERS', '').split(',') if os.environ.get('ADMIN_USERS') else []
    
    # Applicatie instellingen
    APP_NAME = os.environ.get('APP_NAME') or "Lynxx Business Portal"
    APP_DESCRIPTION = os.environ.get('APP_DESCRIPTION') or "Centraal portaal voor Lynxx business applicaties"
    
    # Server instellingen
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # Log niveau instellen
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    @classmethod
    def get_log_level(cls) -> int:
        """
        Verkrijg het juiste logging niveau op basis van LOG_LEVEL configuratie.
        
        Returns:
            int: Het logging niveau (bijvoorbeeld logging.INFO).
        """
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(cls.LOG_LEVEL, logging.INFO)
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Valideer de essentiële configuratie-instellingen.
        
        Returns:
            bool: True als de configuratie geldig is, anders False.
        """
        # Controleer essentiële configuratie
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            logger.warning("Secret key niet geconfigureerd of gebruikt development waarde")
            if not cls.DEBUG:
                logger.error("Secret key moet worden aangepast in productie!")
                return False
        
        # Controleer OAuth configuratie
        if not cls.GOOGLE_CLIENT_ID or not cls.GOOGLE_CLIENT_SECRET:
            logger.warning("Google OAuth niet volledig geconfigureerd, inloggen zal niet werken")
            if not cls.DEBUG:
                logger.error("Google OAuth moet worden geconfigureerd in productie!")
                return False
        
        return True
    
    @classmethod
    def load_apps(cls) -> Dict[str, Any]:
        """
        Laad de app configuratie uit het apps.json bestand.
        Geeft standaardwaarden terug als het bestand niet bestaat of ongeldig is.
        
        Returns:
            dict: Een dictionary met app configuraties.
        """
        try:
            if cls.APPS_CONFIG_FILE.exists():
                with open(cls.APPS_CONFIG_FILE, 'r') as f:
                    apps_config = json.load(f)
                
                # Valideer het apps formaat
                if not isinstance(apps_config, dict) or not isinstance(apps_config.get('apps', []), list):
                    logger.error("Ongeldig apps.json formaat, terugvallen op standaardwaarden")
                    return cls._get_default_apps()
                
                # Valideer individuele app entries
                valid_apps = []
                for app in apps_config.get('apps', []):
                    if cls._validate_app_entry(app):
                        valid_apps.append(app)
                    else:
                        logger.warning(f"Ongeldige app configuratie: {app}")
                
                if not valid_apps and apps_config.get('apps'):
                    logger.error("Geen geldige apps gevonden in apps.json, terugvallen op standaardwaarden")
                    return cls._get_default_apps()
                
                apps_config['apps'] = valid_apps
                return apps_config
            else:
                logger.warning(f"apps.json niet gevonden op pad: {cls.APPS_CONFIG_FILE}")
                return cls._get_default_apps()
        except json.JSONDecodeError as e:
            logger.error(f"Error bij het parsen van apps.json: {e}")
            return cls._get_default_apps()
        except Exception as e:
            logger.error(f"Onverwachte error bij het laden van apps configuratie: {e}")
            return cls._get_default_apps()
    
    @classmethod
    def _validate_app_entry(cls, app: Dict[str, Any]) -> bool:
        """
        Valideer een individuele app entry uit de apps.json.
        
        Args:
            app (dict): De app configuratie om te valideren.
            
        Returns:
            bool: True als de app configuratie geldig is, anders False.
        """
        required_fields = ['name', 'url']
        for field in required_fields:
            if field not in app or not app[field]:
                return False
        
        # Controleer of URL geldig formaat heeft
        if not app['url'].startswith(('http://', 'https://')):
            return False
        
        return True
    
    @classmethod
    def _get_default_apps(cls) -> Dict[str, Any]:
        """
        Geef standaard app configuraties terug voor wanneer het laden van apps.json mislukt.
        
        Returns:
            dict: Een dictionary met standaard app configuraties.
        """
        logger.info("Gebruik standaard apps configuratie")
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
    
    @classmethod
    def save_apps(cls, apps_config: Dict[str, Any]) -> bool:
        """
        Sla de app configuratie op in het apps.json bestand.
        
        Args:
            apps_config (dict): De app configuratie om op te slaan.
            
        Returns:
            bool: True als het opslaan is gelukt, anders False.
        """
        try:
            # Valideer de apps configuratie voor het opslaan
            if not isinstance(apps_config, dict) or not isinstance(apps_config.get('apps', []), list):
                logger.error("Ongeldige apps configuratie format, niet opslaan")
                return False
            
            # Valideer individuele app entries
            valid_apps = []
            for app in apps_config.get('apps', []):
                if cls._validate_app_entry(app):
                    valid_apps.append(app)
                else:
                    logger.warning(f"Ongeldige app configuratie wordt overgeslagen: {app}")
            
            if not valid_apps and apps_config.get('apps'):
                logger.error("Geen geldige apps in de configuratie, niet opslaan")
                return False
            
            # Update met alleen geldige apps
            apps_config['apps'] = valid_apps
            
            # Sla de configuratie op
            with open(cls.APPS_CONFIG_FILE, 'w') as f:
                json.dump(apps_config, f, indent=2)
            
            logger.info(f"Apps configuratie succesvol opgeslagen in {cls.APPS_CONFIG_FILE}")
            return True
        except Exception as e:
            logger.error(f"Error bij het opslaan van apps configuratie: {e}")
            return False
    
    @classmethod
    def is_admin_user(cls, email: Optional[str]) -> bool:
        """
        Controleer of een gebruiker admin rechten heeft.
        
        Args:
            email (str, optional): Het e-mailadres van de gebruiker.
            
        Returns:
            bool: True als de gebruiker admin rechten heeft, anders False.
        """
        if not email:
            return False
        
        email = email.lower()
        return email in [admin.lower() for admin in cls.ADMIN_USERS]
