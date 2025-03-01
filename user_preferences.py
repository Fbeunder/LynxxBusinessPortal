#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - User Preferences Module

Dit bestand bevat functionaliteit voor het beheren van gebruikersvoorkeuren
zoals favoriete apps en app-ordening.
"""

import os
import json
import logging
from pathlib import Path
from flask import session
from config import Config

class UserPreferences:
    """Klasse voor het beheren van gebruikersvoorkeuren"""

    # Pad voor het opslaan van gebruikersvoorkeuren
    PREFERENCES_DIR = Config.BASE_DIR / 'user_preferences'

    @classmethod
    def get_user_preferences_file(cls, user_id):
        """
        Krijg het pad naar het voorkeuren-bestand van de gebruiker.
        
        Args:
            user_id (str): De ID van de gebruiker.
            
        Returns:
            Path: Pad naar het voorkeuren-bestand.
        """
        # Zorg ervoor dat de directory bestaat
        if not cls.PREFERENCES_DIR.exists():
            cls.PREFERENCES_DIR.mkdir(parents=True)
        
        return cls.PREFERENCES_DIR / f"{user_id}.json"
    
    @classmethod
    def get_preferences(cls, user_id):
        """
        Haal de voorkeuren van een gebruiker op.
        
        Args:
            user_id (str): De ID van de gebruiker.
            
        Returns:
            dict: De voorkeuren van de gebruiker, of een standaard configuratie.
        """
        if not user_id:
            return cls.get_default_preferences()
        
        preferences_file = cls.get_user_preferences_file(user_id)
        
        try:
            if preferences_file.exists():
                with open(preferences_file, 'r') as f:
                    return json.load(f)
            return cls.get_default_preferences()
        except Exception as e:
            logging.error(f"Error loading user preferences: {e}")
            return cls.get_default_preferences()
    
    @classmethod
    def save_preferences(cls, user_id, preferences):
        """
        Sla de voorkeuren van een gebruiker op.
        
        Args:
            user_id (str): De ID van de gebruiker.
            preferences (dict): De voorkeuren van de gebruiker.
            
        Returns:
            bool: True als het opslaan is gelukt, anders False.
        """
        if not user_id:
            return False
        
        try:
            # Valideer de data structuur
            if not isinstance(preferences, dict):
                preferences = cls.get_default_preferences()
            
            preferences_file = cls.get_user_preferences_file(user_id)
            
            with open(preferences_file, 'w') as f:
                json.dump(preferences, f, indent=4)
            
            return True
        except Exception as e:
            logging.error(f"Error saving user preferences: {e}")
            return False
    
    @classmethod
    def get_default_preferences(cls):
        """
        Krijg de standaard voorkeuren.
        
        Returns:
            dict: Standaard voorkeuren.
        """
        return {
            "favorites": [],
            "order": [],
            "theme": "default"
        }
    
    @classmethod
    def toggle_favorite(cls, user_id, app_index):
        """
        Toggle een app als favoriet.
        
        Args:
            user_id (str): De ID van de gebruiker.
            app_index (int): De index van de app in de lijst.
            
        Returns:
            bool: True als de wijziging is gelukt, anders False.
        """
        if not user_id:
            return False
        
        preferences = cls.get_preferences(user_id)
        
        if app_index in preferences["favorites"]:
            preferences["favorites"].remove(app_index)
        else:
            preferences["favorites"].append(app_index)
        
        return cls.save_preferences(user_id, preferences)
    
    @classmethod
    def update_order(cls, user_id, order):
        """
        Update de volgorde van apps.
        
        Args:
            user_id (str): De ID van de gebruiker.
            order (list): Lijst met indices in de gewenste volgorde.
            
        Returns:
            bool: True als de wijziging is gelukt, anders False.
        """
        if not user_id or not isinstance(order, list):
            return False
        
        preferences = cls.get_preferences(user_id)
        preferences["order"] = order
        
        return cls.save_preferences(user_id, preferences)
    
    @classmethod
    def apply_preferences(cls, user_id, apps):
        """
        Pas gebruikersvoorkeuren toe op de lijst met apps.
        
        Args:
            user_id (str): De ID van de gebruiker.
            apps (list): Lijst met apps.
            
        Returns:
            list: Lijst met apps, aangepast naar gebruikersvoorkeuren.
        """
        if not user_id or not apps:
            return apps
        
        preferences = cls.get_preferences(user_id)
        favorites = preferences.get("favorites", [])
        order = preferences.get("order", [])
        
        # Markeert favorieten
        for i, app in enumerate(apps):
            app["is_favorite"] = i in favorites
        
        # Past ordening toe als die is ingesteld
        if order and all(0 <= idx < len(apps) for idx in order):
            ordered_apps = [apps[idx] for idx in order]
            missing_apps = [app for i, app in enumerate(apps) if i not in order]
            return ordered_apps + missing_apps
        
        return apps
