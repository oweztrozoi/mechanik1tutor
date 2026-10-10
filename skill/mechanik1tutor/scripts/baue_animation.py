#!/usr/bin/env python3
"""Mechanik1Tutor – Animation zusammensetzen.

KI-generiert (Claude, Anthropic) – kein offizielles Lehrmaterial.

  python3 scripts/baue_animation.py inhalt.js widget.html --chat   # Fragment für die Chat-Ansicht (show_widget)
  python3 scripts/baue_animation.py inhalt.js seite.html           # eigenständige Seite (Artifact/Datei)
  python3 scripts/baue_animation.py inhalt.js widget.html --chat --voll   # Chat ohne CDN (Engine eingebettet)
  python3 scripts/baue_animation.py --kopf                         # Köpfe + CDN-Bündel (assets/dist/m1t-chat.js) neu erzeugen

Chat-Modus nutzt standardmäßig die per CDN geladene Engine (URL in assets/cdn.txt): das Fragment
enthält dann nur noch den Inhalt (~4–6 kB statt ~25 kB). Ist assets/cdn.txt leer, wird eingebettet.

Ergebnis = Kopf (CSS, Gerüst, Engine) + inhalt.js + Abschluss. Bausteine, Trägermodul und 3D werden nur\neingebunden, wenn der Inhalt sie benutzt. assets/kopf-*.html enthalten alles (für Arbeit ohne Codeausführung).
inhalt.js enthält CONFIG, LEGEND, build(), STEPS, PRAXIS (Muster: assets/beispiele/inhalt-*.js).
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.path.join(ROOT, "assets", "engine")
KCSS = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">'
KJS = '<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>'
CHAT_CSS = (":root:root:root{--bg:var(--surface-1);--card:var(--surface-2);--ink:var(--text-primary);--muted:var(--text-secondary);"
            "--line:var(--border-strong);--struct:var(--text-primary);--hatch:var(--text-secondary);--accent:var(--text-accent)}"
            ".wrap{padding:0}h1,h2,h3{font-weight:500}.card{border-width:.5px}"
            ".sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}")
ENDE_CHAT = "\n</script>\n"
ENDE_SEITE = "\n</script>\n</body>\n</html>\n"


def kompakt(code):
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    return "\n".join(l.strip() for l in code.splitlines() if l.strip())


def lies(n):
    return open(os.path.join(ENG, n), encoding="utf8").read()


MODUL_START = "/* ---------- Grundformen"
MODUL_ENDE = "/* ---------- Ablaufsteuerung"


def bloecke(teil):
    """Zerlegt den Modulteil in Top-Level-Definitionen {name: code}."""
    out, name, buf = {}, None, []
    for zeile in teil.splitlines(True):
        m = re.match(r"(?:function\s+(\w+)|const\s+(\w+)\s*=)", zeile)
        if m:
            if name: out[name] = "".join(buf)
            name, buf = m.group(1) or m.group(2), [zeile]
        elif name:
            buf.append(zeile)
    if name: out[name] = "".join(buf)
    return out


def engine(inhalt=None):
    """Basis immer; Bausteine, Trägermodul und 3D nur, wenn (transitiv) benutzt."""
    js = lies("engine.js")
    a, b = js.index(MODUL_START), js.index(MODUL_ENDE)
    if inhalt is None:
        return kompakt(js)
    bl = {k: kompakt(v) for k, v in bloecke(js[a:b]).items()}
    noetig, offen = [], [inhalt]
    while offen:
        code = offen.pop()
        for k, v in bl.items():
            if k not in noetig and re.search(r"(?<![\w.])" + k + r"\b", code):
                noetig.append(k); offen.append(v)
    teile = [v for k, v in bl.items() if k in noetig]   # Originalreihenfolge
    return kompakt(js[:a]) + "\n" + "\n".join(teile) + "\n" + kompakt(js[b:])


def koepfe(inhalt=None):
    css, skel, js = kompakt(lies("style.css")), lies("skelett.html"), engine(inhalt)
    skel_chat = re.sub(r"\s*<header>.*?</header>", "", skel, flags=re.S)
    skel_chat = "\n".join(l.strip() for l in skel_chat.splitlines() if l.strip())
    css_chat = css.replace("data-theme", "data-mode")
    css_chat = re.sub(r"(?m)^body\{[^}]*\}\n?", "", css_chat)
    css_chat = re.sub(r"(?m)^button(:hover)?\{[^}]*\}\n?", "", css_chat)
    chat = (KCSS + "\n<style>\n" + css_chat + "\n" + CHAT_CSS + "\n</style>\n"
            '<h2 class="sr-only">Schritt-für-Schritt-Animation zu Mechanik 1</h2>\n' + skel_chat + "\n" + KJS + "\n<script>\n" + js + "\n")
    seite = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Mechanik Schritt für Schritt</title>\n'
             + KCSS + "\n" + KJS + "\n<style>\n" + css + "\n</style>\n</head>\n<body>\n" + skel + "<script>\n" + js + "\n")
    if inhalt is None:
        for n, t in (("kopf-chat.html", chat), ("kopf-seite.html", seite)):
            open(os.path.join(ROOT, "assets", n), "w", encoding="utf8").write(t)
        sr = '<h2 class="sr-only">Schritt-für-Schritt-Animation zu Mechanik 1</h2>'
        bundle = ("/* Mechanik1Tutor – Chat-Engine (CDN). KI-generiert (Claude, Anthropic), kein offizielles Lehrmaterial. Baut Stil und Gerüst in <div id=\"m1t\"> und startet, sobald der Inhalt geladen ist. */\n"
                  "(function(){var r=document.getElementById(\"m1t\")||document.body.appendChild(document.createElement(\"div\"));"
                  "var h=document.head||document.body,st=document.createElement(\"style\");st.textContent=" + json.dumps(css_chat + "\n" + CHAT_CSS) + ";h.appendChild(st);"
                  "var l=document.createElement(\"link\");l.rel=\"stylesheet\";l.href=" + json.dumps(re.search(r'href="([^"]+)"', KCSS).group(1)) + ";h.appendChild(l);"
                  "r.innerHTML=" + json.dumps(sr + skel_chat) + ";})();\n" + js + "\n")
        os.makedirs(os.path.join(ROOT, "assets", "dist"), exist_ok=True)
        open(os.path.join(ROOT, "assets", "dist", "m1t-chat.js"), "w", encoding="utf8").write(bundle)
    return chat, seite


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    chat, seite = koepfe()
    if "--kopf" in sys.argv:
        print(f"Köpfe neu: chat {len(chat)} Zeichen, seite {len(seite)} Zeichen"); return
    if len(a) != 2:
        sys.exit(__doc__)
    inhalt = open(a[0], encoding="utf8").read()
    if "</script" in inhalt.lower():
        sys.exit("Der Inhalt darf kein </script> enthalten.")
    for p in ("const CONFIG", "const LEGEND", "function build", "const STEPS", "const PRAXIS"):
        if p not in inhalt:
            sys.exit("Fehlt im Inhalt: " + p)
    # Häufigster Fehler: einfacher Backslash in JS-Strings ("\\;" statt "\\\\;") verschluckt TeX-Befehle
    for nr, z in enumerate(inhalt.splitlines(), 1):
        for m in re.finditer(r"(?<!\\)\\(?![\\nt`'\"$u])(.)", z):
            sys.exit(f"Zeile {nr}: einfacher Backslash vor '{m.group(1)}' – in JS-Strings \\\\ schreiben.")
    chat, seite = koepfe(inhalt)
    cdn_datei = os.path.join(ROOT, "assets", "cdn.txt")
    cdn = open(cdn_datei, encoding="utf8").read().strip() if os.path.exists(cdn_datei) else ""
    if "--chat" in sys.argv and cdn and "--voll" not in sys.argv:
        out = ('<div id="m1t"></div>\n' + KJS + '\n<script src="' + cdn + '"></script>\n'
               '<script type="text/plain" id="m1t-inhalt">\n' + inhalt + '\n</script>\n'
               '<script>(function w(n){if(window.traeger){var s=document.createElement("script");'
               's.textContent=document.getElementById("m1t-inhalt").textContent;document.body.appendChild(s);}'
               'else if(n<240)setTimeout(function(){w(n+1)},25);'
               'else document.getElementById("m1t").textContent="Die Animations-Engine konnte nicht geladen werden. '
               'Schreib „ohne CDN“, dann kommt die Animation vollständig eingebettet.";})(0)</script>\n')
    elif "--chat" in sys.argv:
        out = chat + inhalt + ENDE_CHAT
    else:
        out = seite + inhalt + ENDE_SEITE
    open(a[1], "w", encoding="utf8").write(out)
    print(f"geschrieben: {a[1]} ({len(out)} Zeichen, davon Inhalt {len(inhalt)})")


if __name__ == "__main__":
    main()
