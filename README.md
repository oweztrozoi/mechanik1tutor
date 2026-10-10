# Mechanik1Tutor

Ein Claude-Skill für Technische Mechanik 1 (Statik und Festigkeitslehre), der Konzepte und Rechenbeispiele mit **steuerbaren Schritt-für-Schritt-Animationen** direkt im Chat erklärt.

> **KI-generiert:** Dieses Repository wurde vollständig von einer KI (Claude, Anthropic) erstellt. Es ist kein offizielles Lehrmaterial, enthält keine offiziellen Unterlagen der TU Wien und kann Fehler enthalten.

## Funktionen

- **Farbige Größen:** Jede Größe hat in Skizze, Text und Formel dieselbe Farbe.
- **Fertige Bausteine:** Lager, Einspannung, Pendelstab, Seil, Feder, schiefe Ebene, Fachwerk, Streckenlast, Bemaßung.
- **Trägermodul:** berechnet und zeichnet Lagerkräfte, Querkraft- und Momentenverlauf automatisch.
- **3D-Ansicht:** drehbar, mit ViewCube wie in AutoCAD.
- **Tutor-Verhalten:** Praxisbeispiele zu jedem Thema; Aufgaben werden Schritt für Schritt bis zum Ende gerechnet.

## Installation

Den Ordner `skill/mechanik1tutor` als Zip packen und in Claude unter *Einstellungen → Skills* hochladen. Eigene Kursunterlagen können optional als Markdown in `references/unterlagen/` ergänzt werden.

## Aufbau

```
skill/mechanik1tutor/
├── SKILL.md                    Anleitung für Claude
├── references/                 Animations-API, Praxisbeispiele, optionale Unterlagen
├── scripts/baue_animation.py   baut Animationen und prüft auf Fehler
└── assets/
    ├── engine/                 Quellcode der Engine
    ├── dist/m1t-chat.js        gebündelte Engine, per jsDelivr geladen
    └── beispiele/              Muster-Animation
```

Im Chat wird die Engine über jsDelivr aus diesem Repository geladen (Adresse in `assets/cdn.txt`). So muss Claude pro Animation nur den Inhalt schreiben, etwa 5 kB statt 25 kB.

**Engine ändern:** in `assets/engine/` bearbeiten, `python3 skill/mechanik1tutor/scripts/baue_animation.py --kopf` ausführen, pushen und den neuen Commit-Hash in `assets/cdn.txt` eintragen.
