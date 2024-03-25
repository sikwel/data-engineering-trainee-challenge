# siːkwəl: Data Engineering Trainee Challenge 🚀

Moin moin! Willkommen zum Data Engineering Trainee-Projekt – hier geht's um Docker, Python, Open-Meteo API und ein paar Daten! Lies dir die Anleitung sorgsam durch und starte direkt mit dem Projekt.

## Was du brauchst

### Git

Kein Git? Kein Problem! Schnapp es dir hier: [Git Downloads](https://git-scm.com/downloads)

### Docker Desktop

Für die Challenge benötigst du Docker Desktop: [Docker Desktop](https://www.docker.com/products/docker-desktop)

#### Für Windows-Nutzer: WSL2 ist ein Muss

Falls du Windows nutzt, vergewissere dich, dass WSL2 installiert ist. Hier findest du eine Anleitung: [WSL2 Installation Guide](https://docs.docker.com/desktop/wsl/)

### VSCode

Als Entwicklungsumgebung nutzen wir einen vordefinierten Docker-Container. Hier haben wir dir schonmal ein paar hilfreiche Pakete vorinstalliert. Damit das läuft, benötigst du VSCode. Falls du bereits eine andere IDE hast, die sich mit einem Docker-Container verbindet, auch gut!

## Projekt-Setup

1. Klone das Repo:

    ```bash
    git clone https://github.com/sikwel/data-engineering-trainee-challenge.git
    cd data-engineering-trainee-challenge
    ```

2. Öffne das Projekt in Visual Studio Code – der Devcontainer regelt!

3. Falls etwas fehlt installiere es dir einfach per `pip`.

4. Du findest im Container auch einige hilfreiche Extensions für VSCode wie beispielsweise einen SQL Client. Diesen kannst du nutzen um später eine Verbindung zur Datenbank herzustellen. Auch hier gilt, hast du bereits etwas auf deinem Laptop installiert, kannst du auch diesen nutzen.

## Was wir machen

Unser Test-Projekt hat ein paar Aufgaben für dich vorgesehen:

1. **Mit der Open-Meteo API das Wetter checken:**
    - Schnapp dir die [Wetterdaten](https://open-meteo.com/) mit der Open-Meteo API.
    - Nutze Pythons `request` library
    - Wir wollen uns historische Wetterdaten (auf Stundenbasis) für **Oldenburg** anschauen. Uns interessieren vor allem folgende Parameter:
        - Temperature
        - Relative Humidity
        - Rain
        - Weather Code
        - Wind Speed
        - Surface Pressure
    - Überlege dir ein geeigntes Logging im Fehler- oder Erfolgsfall. Das hilft nicht nur beim Debugging sondern freut den Benutzer 👍
    - Python macht's möglich
    - Zeige deine Skills im Umgang mit APIs und Datenextraktion.

2. **Daten in PostgreSQL pumpen:**
    - Wir haben dir einen PostgreSQL Server mit allem drum und dran in den DevContainer gelegt.
    - Wir wollen die Daten später pro Stunde auswerten können. Überlege dir also, wie du diese auf Basis des Response in dein Postgres schreiben musst.
    - Die Verbindungsdaten findest du am Ende der Anleitung.

3. **Steuerung des Python-Skripts:**
    - Folgende Parameter des API-Aufrufs sollten per Kommandozeile überschrieben werden können:
        - Latitude
        - Longitude
        - Start Date
        - End Date
        - Timezone
    - Wenn kein End Date übergeben wurde, soll das der aktuelle Tag genommen werden

4. **Orchestrierung:**
    - Überlege dir, wie eine geeignete Orchestrierung des Skripts aussehen kann.
    - Implementiere das die Orchestrierung / Scheduling im DevContainer.

5. **...and beyond:**
    - Halt den Code clean und kommentiere klug.
    - Definiere Funktionen und Klassen wo sinnvoll.
    - Nutze `git` um dein Projekt zu versionieren und am Ende wieder in das Repository zu pushen, damit wir uns dein Ergebnis anschauen können.

## Let's Code!

Viel Erfolg und vor allem viel Spaß beim Coden! Bei Fragen stehen wir dir zur Verfügung. Happy coding! 🚀✨

## Anhang

### Credentials

Wir haben die Credentials bewusst weggelassen, schau mal ob du die selbst rausfinden kannst. 😉🤞🍀

### Nützliche Links

- [Open-Meteo Dokumentation](https://open-meteo.com/en/docs)
- [DevContainers](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container)
