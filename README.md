# Nordwerk Industrie-Service – Website (Kundenprojekt 01)

Statische Website für **Nordwerk Industrie-Service** (fiktives Unternehmen,
Lehrprojekt HAW Hamburg). Erzeugt mit der PepeGroup-Factory als erster
Kundenauftrag (Termin 3).

## Öffnen

```bash
python3 -m http.server 8000
```

Dann http://localhost:8000 öffnen.

## Produkttest (separater Aufruf)

```bash
python -m unittest test_website -v
```

## Inhalt

- Firmenname und Hauptaussage
- Leistungen (Wartungsplanung, Ersatzteilkoordination, Betriebsdokumentation)
- Zielgruppen und Arbeitsweise
- Kontakt: `mailto:kontakt@nordwerk.example`
- Übungshinweis: fiktives Unternehmen, keine realen Angebote
