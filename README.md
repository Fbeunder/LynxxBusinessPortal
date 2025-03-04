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

### Virtuele omgeving opzetten (aanbevolen)

Het is sterk aanbevolen om een virtuele Python-omgeving te gebruiken voor de installatie en het uitvoeren van de Lynxx Business Portal. Dit voorkomt conflicten met andere Python-projecten en zorgt voor een schone, geïsoleerde omgeving.

#### Voor Windows:

1. Open een Command Prompt of PowerShell venster
2. Navigeer naar de projectmap:
   ```
   cd pad\naar\LynxxBusinessPortal
   ```
3. Maak een virtuele omgeving aan:
   ```
   python -m venv venv
   ```
4. Activeer de virtuele omgeving:
   ```
   venv\Scripts\activate
   ```

#### Voor macOS/Linux:

1. Open een terminal venster
2. Navigeer naar de projectmap:
   ```bash
   cd pad/naar/LynxxBusinessPortal
   ```
3. Maak een virtuele omgeving aan:
   ```bash
   python3 -m venv venv
   ```
4. Activeer de virtuele omgeving:
   ```bash
   source venv/bin/activate
   ```

Je terminal prompt zou nu moeten veranderen, wat aangeeft dat je virtuele omgeving actief is (meestal zie je `(venv)` aan het begin van de prompt).

### Installatiestappen

1. Clone de repository:
   ```bash
   git clone https://github.com/Fbeunder/LynxxBusinessPortal.git
   cd LynxxBusinessPortal
   ```

2. Maak en activeer een virtuele omgeving (zie bovenstaande instructies)

3. Installeer de benodigde packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Maak een `.env` bestand aan gebaseerd op `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Vul de benodigde omgevingsvariabelen in, inclusief Google OAuth client gegevens:
   ```
   FLASK_SECRET_KEY=jouw_geheime_sleutel
   GOOGLE_CLIENT_ID=jouw_google_client_id
   GOOGLE_CLIENT_SECRET=jouw_google_client_secret
   ADMIN_EMAILS=admin1@lynxx.com,admin2@lynxx.com
   FLASK_ENV=development  # Gebruik 'development' voor lokale ontwikkeling, 'production' voor productie
   ```

6. Start de applicatie:
   ```bash
   python app.py
   ```

De portal is nu bereikbaar op http://localhost:5000

### Virtuele omgeving beheren

- Om de virtuele omgeving te deactiveren:
  ```
  deactivate
  ```

- Om de virtuele omgeving later opnieuw te activeren, voer je opnieuw het activatiecommando uit:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`

- Om de afhankelijkheden in je virtuele omgeving bij te werken:
  ```
  pip install -r requirements.txt
  ```

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

### Google OAuth configuratie

1. Ga naar [Google Cloud Console](https://console.cloud.google.com/)
2. Maak een nieuw project of selecteer een bestaand project
3. Ga naar "APIs & Services" > "Credentials"
4. Klik op "Create Credentials" > "OAuth client ID"
5. Selecteer "Web application" als applicatietype
6. Voeg de geautoriseerde redirect URIs toe:
   - Voor lokale ontwikkeling: `http://localhost:5000/login/google/callback`
   - Voor productie: `https://jouw-domein.com/login/google/callback`
7. Kopieer de Client ID en Client Secret naar je `.env` bestand

### HTTPS vereisten en ontwikkelomgeving

OAuth 2.0 vereist standaard HTTPS voor veilige communicatie. In de code wordt dit automatisch afgehandeld:

- **Ontwikkelomgeving**: Als `FLASK_ENV=development` is ingesteld, wordt HTTPS verificatie automatisch uitgeschakeld via de `OAUTHLIB_INSECURE_TRANSPORT=1` omgevingsvariabele zodat je lokaal kunt ontwikkelen zonder HTTPS.
- **Productieomgeving**: In productie moet je HTTPS gebruiken. Zorg ervoor dat je server correct is geconfigureerd met SSL/TLS certificaten.

> **Let op**: In productie moet `FLASK_ENV` worden ingesteld op `production` of worden weggelaten om de HTTPS-vereisten te behouden!

#### Troubleshooting OAuth problemen

Als je de foutmelding `InsecureTransportError` tegenkomt, kan dit betekenen dat:

1. `FLASK_ENV` niet correct is ingesteld op `development` in je `.env` bestand
2. De instelling niet correct wordt geladen

Je kunt dit op meerdere manieren oplossen:

- Controleer of je `.env` bestand correct is en `FLASK_ENV=development` bevat
- Herstart de Flask applicatie nadat je wijzigingen hebt aangebracht in het `.env` bestand
- Stel de omgevingsvariabele handmatig in voordat je de app start:
  - Windows: `set OAUTHLIB_INSECURE_TRANSPORT=1`
  - macOS/Linux: `export OAUTHLIB_INSECURE_TRANSPORT=1`

De applicatie zal automatisch detecteren of het in een ontwikkelomgeving draait op basis van zowel de `FLASK_ENV` als de `Config.DEBUG` instelling. Als een van beide aangeeft dat het een ontwikkelomgeving is, wordt `OAUTHLIB_INSECURE_TRANSPORT=1` ingesteld.

### Omgevingsvariabelen

| Variabele | Beschrijving | Voorbeeld |
|-----------|-------------|-----------|
| FLASK_SECRET_KEY | Geheime sleutel voor Flask sessies | `random_string_here` |
| GOOGLE_CLIENT_ID | Google OAuth client ID | `123456789.apps.googleusercontent.com` |
| GOOGLE_CLIENT_SECRET | Google OAuth client secret | `ABCdef123456` |
| ADMIN_EMAILS | Komma-gescheiden lijst van admin emails | `admin@lynxx.com,manager@lynxx.com` |
| FLASK_ENV | Omgeving (development/production) | `development` |
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
    ├── admin.html          # Admin dashboard
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

- Personalisatie-opties voor gebruikers
- Zoekfunctionaliteit voor apps
- Gebruiksstatistieken dashboard
- Mobile-responsive design verbeteringen

## 📄 Licentie

Intern project - Alle rechten voorbehouden © 2025 Lynxx