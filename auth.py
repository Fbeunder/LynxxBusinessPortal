#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Authentication Module

Dit bestand bevat de authenticatiefunctionaliteit voor de Lynxx Business Portal.
Het implementeert Google OAuth voor authenticatie met @lynxx.com accounts.
"""

import os
import sys
import functools
import json
import logging
from typing import Dict, Any, Optional, Union, Callable
from flask import redirect, request, url_for, session, flash, abort
import requests
from oauthlib.oauth2 import WebApplicationClient
from config import Config

# Logging setup
logger = logging.getLogger('auth')

# OAuth Client initialiseren met foutafhandeling
def get_oauth_client():
    """
    Initialiseert de OAuth client op een veilige manier met foutafhandeling.
    
    Returns:
        WebApplicationClient of None: De geïnitialiseerde client of None bij een fout.
    """
    if not Config.GOOGLE_CLIENT_ID:
        logger.error("Google Client ID ontbreekt in configuratie")
        return None
    try:
        return WebApplicationClient(Config.GOOGLE_CLIENT_ID)
    except Exception as e:
        logger.error(f"Fout bij het initialiseren van OAuth client: {e}")
        return None

# OAuth Client initialiseren
client = get_oauth_client()


def get_google_provider_cfg():
    """
    Haalt de Google OAuth 2.0 provider configuratie op.
    
    Returns:
        dict: De Google provider configuratie of None bij een fout.
    """
    try:
        response = requests.get(Config.GOOGLE_DISCOVERY_URL, timeout=10)
        response.raise_for_status()  # Controleer op HTTP fouten
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Netwerkfout bij ophalen Google provider config: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse fout bij ophalen Google provider config: {e}")
        return None
    except Exception as e:
        logger.error(f"Onverwachte fout bij ophalen Google provider config: {e}")
        return None


def oauth_login():
    """
    Start het Google OAuth inlogproces.
    
    Returns:
        Redirect: Redirect naar Google's OAuth login pagina of foutpagina.
    """
    # Controleer of OAuth geconfigureerd is
    if not client:
        flash("Authenticatie is niet correct geconfigureerd. Neem contact op met de beheerder.", "error")
        logger.error("OAuth login poging zonder geldige client")
        return redirect(url_for("login"))
    
    # Haal Google provider configuratie op
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        flash("Kan geen verbinding maken met Google authenticatiediensten. Probeer het later opnieuw.", "error")
        logger.error("Kon geen Google provider configuratie ophalen")
        return redirect(url_for("login"))
    
    # Construct the request URL for Google login
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    try:
        # Use the client to construct the request URL
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        
        # Redirect to the authorization URL
        return redirect(request_uri)
    except Exception as e:
        logger.error(f"Fout bij voorbereiden OAuth verzoek: {e}")
        flash("Er is een fout opgetreden bij het opstarten van het inlogproces.", "error")
        return redirect(url_for("login"))


def oauth_callback():
    """
    Verwerkt de callback van Google OAuth na succesvolle authenticatie.
    Controleert of het e-mailadres eindigt op @lynxx.com.
    
    Returns:
        Redirect: Redirect naar de homepage na succesvolle authenticatie,
                 of naar de inlogpagina met een foutmelding.
    """
    # Controleer of OAuth geconfigureerd is
    if not client:
        flash("Authenticatie is niet correct geconfigureerd. Neem contact op met de beheerder.", "error")
        logger.error("OAuth callback poging zonder geldige client")
        return redirect(url_for("login"))
    
    # Get the authorization code from the request parameters
    code = request.args.get("code")
    if not code:
        flash("Geen autorisatiecode ontvangen van Google.", "error")
        logger.warning("OAuth callback zonder autorisatiecode")
        return redirect(url_for("login"))
    
    # Haal Google provider configuratie op
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        flash("Kan geen verbinding maken met Google authenticatiediensten. Probeer het later opnieuw.", "error")
        logger.error("Kon geen Google provider configuratie ophalen tijdens callback")
        return redirect(url_for("login"))
    
    # Get the token endpoint
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    try:
        # Prepare the token request
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        
        # Controleer of OAuth secrets beschikbaar zijn
        if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
            flash("OAuth authenticatie is niet volledig geconfigureerd.", "error")
            logger.error("OAuth secrets ontbreken tijdens token request")
            return redirect(url_for("login"))
        
        # Exchange the authorization code for tokens
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
            timeout=10
        )
        token_response.raise_for_status()  # Controleer op HTTP fouten
        
        # Parse the token response
        client.parse_request_body_response(json.dumps(token_response.json()))
        
        # Get the user info endpoint
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        
        # Use the token to get the user's profile information
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=10)
        userinfo_response.raise_for_status()  # Controleer op HTTP fouten
        
        # Parse the user info response
        userinfo = userinfo_response.json()
        
        # Validate that the user has an email
        if not userinfo.get("email"):
            flash("Geen e-mailadres ontvangen van Google.", "error")
            logger.warning("Geen e-mailadres in Google userinfo response")
            return redirect(url_for("login"))
        
        if not userinfo.get("email_verified", False):
            flash("Je Google e-mailadres is niet geverifieerd.", "error")
            logger.warning(f"Niet-geverifieerd e-mailadres: {userinfo.get('email')}")
            return redirect(url_for("login"))
        
        # Check if the email belongs to the allowed domain
        if not domain_validate(userinfo.get("email", "")):
            flash(f"Je moet een @{Config.ALLOWED_DOMAIN} e-mailadres gebruiken om in te loggen.", "error")
            logger.warning(f"Inlogpoging met ongeldig domein: {userinfo.get('email')}")
            return redirect(url_for("login"))
        
        # Store the user information in the session
        session["user"] = {
            "id": userinfo["sub"],
            "email": userinfo["email"],
            "name": userinfo.get("name", ""),
            "given_name": userinfo.get("given_name", ""),
            "picture": userinfo.get("picture", "")
        }
        
        logger.info(f"Gebruiker succesvol ingelogd: {userinfo['email']}")
        
        # Redirect to the homepage
        return redirect(url_for("index"))
    except requests.RequestException as e:
        logger.error(f"Netwerkfout tijdens OAuth flow: {e}")
        flash("Er is een netwerkfout opgetreden tijdens het inloggen. Probeer het later opnieuw.", "error")
        return redirect(url_for("login"))
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse fout tijdens OAuth flow: {e}")
        flash("Er is een fout opgetreden bij het verwerken van de inloggegevens.", "error")
        return redirect(url_for("login"))
    except Exception as e:
        logger.error(f"Onverwachte fout tijdens OAuth flow: {e}")
        flash("Er is een onverwachte fout opgetreden tijdens het inloggen.", "error")
        return redirect(url_for("login"))


def domain_validate(email: str) -> bool:
    """
    Controleert of het e-mailadres eindigt op het toegestane domein.
    
    Args:
        email (str): Het e-mailadres om te valideren.
        
    Returns:
        bool: True als het e-mailadres eindigt op het toegestane domein, anders False.
    """
    if not email:
        return False
    
    return email.lower().endswith(f"@{Config.ALLOWED_DOMAIN}")


def get_user_info() -> Optional[Dict[str, Any]]:
    """
    Haalt de gebruikersinformatie op uit de sessie.
    
    Returns:
        dict: Gebruikersinformatie of None als de gebruiker niet is ingelogd.
    """
    return session.get("user")


def require_login(f: Callable) -> Callable:
    """
    Decorator voor routes die authenticatie vereisen.
    Als de gebruiker niet is ingelogd, wordt hij doorgestuurd naar de inlogpagina.
    
    Args:
        f: De functie die gedecoreerd wordt.
        
    Returns:
        function: De gedecoreerde functie.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_user_info():
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f: Callable) -> Callable:
    """
    Decorator voor routes die admin rechten vereisen.
    Als de gebruiker geen admin is, wordt een 403 fout getoond.
    
    Args:
        f: De functie die gedecoreerd wordt.
        
    Returns:
        function: De gedecoreerde functie.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        user_info = get_user_info()
        if not user_info:
            return redirect(url_for("login"))
        
        if not Config.is_admin_user(user_info.get('email')):
            logger.warning(f"Toegang tot admin functie geweigerd voor gebruiker: {user_info.get('email')}")
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def logout():
    """
    Logt de gebruiker uit door de sessie te wissen.
    
    Returns:
        Redirect: Redirect naar de inlogpagina.
    """
    # Log de uitlogactie voor audit doeleinden
    user_info = get_user_info()
    if user_info:
        logger.info(f"Gebruiker uitgelogd: {user_info.get('email')}")
    
    session.clear()
    flash("Je bent succesvol uitgelogd.", "info")
    return redirect(url_for("login"))
