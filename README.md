# Lynxx Business Portal

Een centrale webportal voor het toegang krijgen tot de zakelijke applicaties van Lynxx.

## Beschrijving

De Lynxx Business Portal is een webomgeving waar Lynxx medewerkers de belangrijkste bedrijfsapps van Lynxx kunnen vinden. De portal biedt een centrale toegangsplaats tot bedrijfsapplicaties, authenticeert gebruikers via Google accounts binnen het lynxx.com domein, en presenteert de beschikbare apps als tegels in een overzichtelijke interface.

De portal heeft onder andere de volgende features:
- Google OAuth authenticatie met domeinvalidatie
- Dynamisch geladen app-tegels vanuit configuratie
- 3D-roterende Lynxx logo in de header
- Admin beheermogelijkheden voor geautoriseerde gebruikers
- Uitgebreide logging en foutafhandeling

## Installatie

### Vereisten

- Python 3.8 of hoger
- Pip (Python package manager)
- Google OAuth credentials

### Stappen

1. Clone de repository:
   ```
   git clone https://github.com/Fbeunder/LynxxBusinessPortal.git
   cd LynxxBusinessPortal
   ```

2. Installeer de benodigde packages:
   ```
   pip install -r requirements.txt
   ```

3. Maak een kopie van het `.env.example` bestand naar `.env`:
   ```
   cp .env.example .env
   ```

4. Pas de `.env` file aan met jouw configuratie:
   - Genereer een `SECRET_KEY` voor de beveiligde sessies
   - Voeg je Google OAuth credentials toe (`GOOGLE_CLIENT_ID` en `GOOGLE_CLIENT_SECRET`)
   - Stel admin gebruikers in via `ADMIN_USERS`
   - Pas eventueel andere instellingen aan naar behoefte

5. Start de applicatie:
   ```
   python app.py
   ```

## Configuratie

### Omgevingsvariabelen

Je kunt de applicatie configureren met de volgende omgevingsvariabelen (in je .env bestand):

| Variabele | Beschrijving | Standaardwaarde |
|-----------|--------------|-----------------|
| SECRET_KEY | Geheime sleutel voor Flask sessies | dev-secret-key-change-in-production |
| FLASK_ENV | Omgeving (development/production) | development |
| PORT | Poort waarop de server draait | 5000 |
| HOST | Host waarop de server draait | 0.0.0.0 |
| LOG_LEVEL | Logging niveau (DEBUG/INFO/WARNING/ERROR/CRITICAL) | INFO |
| GOOGLE_CLIENT_ID | Google OAuth client ID | None |
| GOOGLE_CLIENT_SECRET | Google OAuth client secret | None |
| ALLOWED_DOMAIN | Toegestane e-mail domein voor inloggen | lynxx.com |
| ADMIN_USERS | Komma-gescheiden lijst van admin e-mailadressen | [] |
| APP_NAME | Naam van de applicatie | Lynxx Business Portal |
| APP_DESCRIPTION | Beschrijving van de applicatie | Centraal portaal voor Lynxx business applicaties |

### App configuratie

De apps die worden weergegeven in de portal worden geconfigureerd in het `apps.json` bestand. Elke app heeft de volgende eigenschappen:

```json
{
  "apps": [
    {
      "name": "App Naam",
      "url": "https://app-url.com",
      "description": "Korte beschrijving",
      "icon": "icon-naam"
    }
  ]
}
```

## Gebruik

1. Open de portal in je browser via `http://localhost:5000` (of het geconfigureerde adres)
2. Log in met je Google account (@lynxx.com)
3. Gebruik de app-tegels om naar de gewenste applicaties te navigeren

## Admin functionaliteit

Gebruikers die als admin zijn geconfigureerd hebben extra mogelijkheden:
- Valideren van de configuratie
- Toegang tot extra API endpoints
- Mogelijkheid om instellingen aan te passen (in toekomstige versies)

## Ontwikkeling

### Mappenstructuur

```
LynxxBusinessPortal/
├── app.py              # Hoofdapplicatie bestand
├── auth.py             # Authenticatie module
├── config.py           # Configuratie module
├── apps.json           # App definities
├── .env                # Omgevingsvariabelen (niet in repository)
├── .env.example        # Voorbeeld omgevingsvariabelen
├── requirements.txt    # Python dependencies
├── static/             # Statische bestanden
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript bestanden
│   └── img/            # Afbeeldingen
└── templates/          # HTML templates
    ├── base.html       # Basis template
    ├── index.html      # Hoofdpagina
    ├── login.html      # Inlogpagina
    └── error.html      # Foutpagina's
```

## Licentie

Intern gebruik door Lynxx - Alle rechten voorbehouden
