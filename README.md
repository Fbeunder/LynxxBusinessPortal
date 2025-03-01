# Lynxx Business Portal

Een centrale webomgeving voor toegang tot alle Lynxx bedrijfsapplicaties.

![Lynxx Logo](https://lynxx.eu/images/logo.png)

## 🌟 Overzicht

De Lynxx Business Portal is een centrale toegangsplaats waar Lynxx medewerkers alle bedrijfsapplicaties kunnen vinden en gebruiken. De portal bevat een interactief 3D-roterend Lynxx logo in de header en presenteert alle beschikbare apps in een overzichtelijke tegel-interface.

### Belangrijkste functies:

- **Centrale toegang**: Eén plek voor alle interne applicaties
- **Google OAuth2 authenticatie**: Veilig inloggen met je Lynxx Google account
- **Interactief 3D logo**: Visueel aantrekkelijke interface met Three.js animatie
- **Dynamische app-tegels**: Applicaties worden automatisch geladen uit configuratie
- **Domeinvalidatie**: Alleen @lynxx.com e-mailadressen hebben toegang

## 🚀 Installatie

### Voorvereisten

- Python 3.8+
- Flask
- Google OAuth client credentials

### Stappen

1. Clone de repository:
   ```bash
   git clone https://github.com/Fbeunder/LynxxBusinessPortal.git
   cd LynxxBusinessPortal
   ```

2. Installeer de benodigde packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Maak een `.env` bestand aan gebaseerd op `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Vul de benodigde omgevingsvariabelen in, inclusief Google OAuth client gegevens:
   ```
   FLASK_SECRET_KEY=jouw_geheime_sleutel
   GOOGLE_CLIENT_ID=jouw_google_client_id
   GOOGLE_CLIENT_SECRET=jouw_google_client_secret
   ADMIN_EMAILS=admin1@lynxx.com,admin2@lynxx.com
   ```

5. Start de applicatie:
   ```bash
   python app.py
   ```

De portal is nu bereikbaar op http://localhost:5000

## ⚙️ Configuratie

### App-tegels configureren

Applicaties worden geconfigureerd in het `apps.json` bestand. Je kunt apps toevoegen, wijzigen of verwijderen door dit bestand aan te passen:

```json
{
  "apps": [
    {
      "name": "App Naam",
      "url": "https://app-url.com",
      "description": "Korte beschrijving van de app",
      "icon": "fa-icon-naam"
    }
  ]
}
```

### Omgevingsvariabelen

| Variabele | Beschrijving | Voorbeeld |
|-----------|-------------|-----------|
| FLASK_SECRET_KEY | Geheime sleutel voor Flask sessies | `random_string_here` |
| GOOGLE_CLIENT_ID | Google OAuth client ID | `123456789.apps.googleusercontent.com` |
| GOOGLE_CLIENT_SECRET | Google OAuth client secret | `ABCdef123456` |
| ADMIN_EMAILS | Komma-gescheiden lijst van admin emails | `admin@lynxx.com,manager@lynxx.com` |
| LOG_LEVEL | Logging niveau | `INFO` |

## 🏗️ Projectstructuur

```
LynxxBusinessPortal/
├── app.py                  # Hoofdapplicatie
├── auth.py                 # Authenticatie module
├── config.py               # Configuratie beheer
├── apps.json               # App-definities
├── requirements.txt        # Python dependencies
├── .env.example            # Voorbeeld omgevingsvariabelen 
├── static/                 # Statische bestanden
│   ├── css/
│   │   └── style.css       # CSS-styling
│   ├── js/
│   │   ├── main.js         # JavaScript core functionaliteit
│   │   ├── logo3d.js       # 3D logo implementatie
│   │   └── lynxx-logo-model.js  # Logo model definitie
│   └── img/                # Afbeeldingen en icons
└── templates/              # HTML templates
    ├── base.html           # Basis template
    ├── index.html          # Homepage met app-tegels
    ├── login.html          # Login pagina
    └── error.html          # Error pagina
```

## 🔒 Beveiliging

- Authenticatie via Google OAuth2
- Domeinvalidatie voor @lynxx.com emails
- CSRF-bescherming
- Admin-controle voor bepaalde functionaliteit
- Veilige sessiemanagement

## 👨‍💻 Ontwikkeling

### Nieuwe functies toevoegen

1. Fork de repository
2. Maak een nieuwe branch: `git checkout -b feature/jouw-feature`
3. Commit je wijzigingen: `git commit -m 'Add some feature'`
4. Push naar de branch: `git push origin feature/jouw-feature`
5. Open een Pull Request

### Code testen

Handmatige tests:
- Test authenticatie flow
- Controleer of app-tegels correct worden weergegeven
- Controleer of het 3D logo correct draait en interactief is
- Verify error handling

## 📋 Toekomstige uitbreidingen

- Admin interface voor app-beheer
- Personalisatie-opties voor gebruikers
- Zoekfunctionaliteit voor apps
- Gebruiksstatistieken dashboard
- Mobile-responsive design verbeteringen

## 📄 Licentie

Intern project - Alle rechten voorbehouden © 2025 Lynxx