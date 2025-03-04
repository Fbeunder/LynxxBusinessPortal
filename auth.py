#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lynxx Business Portal - Authentication Module

Dit bestand bevat de authenticatiefunctionaliteit voor de Lynxx Business Portal.
Het implementeert Google OAuth voor authenticatie met @lynxx.com accounts.
"""

import os
import functools
import json
from flask import redirect, request, url_for, session, flash, abort, current_app
import requests
from oauthlib.oauth2 import WebApplicationClient
from config import Config

# Schakel HTTPS-verificatie uit voor development
# Controleer zowel FLASK_ENV als de DEBUG setting voor zekerheid
if os.environ.get('FLASK_ENV') == 'development' or Config.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    print("Ontwikkelomgeving gedetecteerd: HTTPS-vereiste voor OAuth uitgeschakeld")

# OAuth Client setup
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    """
    Haalt de Google OAuth 2.0 provider configuratie op.
    
    Returns:
        dict: De Google provider configuratie.
    """
    try:
        return requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    except Exception as e:
        print(f"Error getting Google provider config: {e}")
        return None


def oauth_login():
    """
    Start het Google OAuth inlogproces.
    
    Returns:
        Redirect: Redirect naar Google's OAuth login pagina.
    """
    # Haal Google provider configuratie op
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        return "Error: Could not fetch Google OAuth configuration", 500
    
    # Construct the request URL for Google login
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    # Use the client to construct the request URL
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('google_callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    
    # Redirect to the authorization URL
    return redirect(request_uri)


def oauth_callback():
    """
    Verwerkt de callback van Google OAuth na succesvolle authenticatie.
    Controleert of het e-mailadres eindigt op @lynxx.com.
    
    Returns:
        Redirect: Redirect naar de homepage na succesvolle authenticatie,
                 of naar de inlogpagina met een foutmelding.
    """
    # Get the authorization code from the request parameters
    code = request.args.get("code")
    if not code:
        return "Error: No authorization code received", 400
    
    # Haal Google provider configuratie op
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        return "Error: Could not fetch Google OAuth configuration", 500
    
    # Get the token endpoint
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    # Prepare the token request
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for('google_callback', _external=True),
        code=code
    )
    
    # Exchange the authorization code for tokens
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )
    
    # Parse the token response
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # Get the user info endpoint
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    
    # Use the token to get the user's profile information
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    # Parse the user info response
    userinfo = userinfo_response.json()
    
    # Validate that the user has an email
    if not userinfo.get("email_verified", False):
        return "Error: User email not verified by Google", 400
    
    # Check if the email belongs to the allowed domain
    if not domain_validate(userinfo.get("email", "")):
        flash("Je moet een @lynxx.com e-mailadres gebruiken om in te loggen.", "error")
        return redirect(url_for("login"))
    
    # Store the user information in the session
    session["user"] = {
        "id": userinfo["sub"],
        "email": userinfo["email"],
        "name": userinfo.get("name", ""),
        "given_name": userinfo.get("given_name", ""),
        "picture": userinfo.get("picture", "")
    }
    
    # Redirect to the homepage
    return redirect(url_for("index"))


def domain_validate(email):
    """
    Controleert of het e-mailadres eindigt op @lynxx.com.
    
    Args:
        email (str): Het e-mailadres om te valideren.
        
    Returns:
        bool: True als het e-mailadres eindigt op @lynxx.com, anders False.
    """
    return email.lower().endswith(f"@{Config.ALLOWED_DOMAIN}")


def get_user_info():
    """
    Haalt de gebruikersinformatie op uit de sessie.
    
    Returns:
        dict: Gebruikersinformatie of None als de gebruiker niet is ingelogd.
    """
    return session.get("user")


def is_admin():
    """
    Controleert of de ingelogde gebruiker admin-rechten heeft.
    
    Returns:
        bool: True als de gebruiker admin-rechten heeft, anders False.
    """
    user = get_user_info()
    if not user:
        return False
    
    # Controleer of het e-mailadres van de gebruiker in de lijst met admin e-mailadressen staat
    admin_emails = Config.ADMIN_EMAILS
    return user.get("email", "").lower() in [email.lower() for email in admin_emails]


def require_login(f):
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


def require_admin(f):
    """
    Decorator voor routes die admin-rechten vereisen.
    Als de gebruiker geen admin-rechten heeft, wordt een 403 Forbidden-fout getoond.
    
    Args:
        f: De functie die gedecoreerd wordt.
        
    Returns:
        function: De gedecoreerde functie.
    """
    @functools.wraps(f)
    @require_login
    def decorated_function(*args, **kwargs):
        if not is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


def logout():
    """
    Logt de gebruiker uit door de sessie te wissen.
    
    Returns:
        Redirect: Redirect naar de inlogpagina.
    """
    session.clear()
    return redirect(url_for("login"))