# Animationen – Referenz

Fertige Engine: Schrittsteuerung, Farben, KaTeX, Bausteine, Trägermodul (rechnet selbst), 3D-Ansicht. **Du schreibst nur `inhalt.js`** mit `CONFIG`, `LEGEND`, `build()`, `STEPS`, `PRAXIS`. Vorher das Muster `assets/beispiele/inhalt-konzept-moment.js` lesen (Konzept mit Grundformen); `traeger()` und `ansicht3d()` sind unten vollständig beschrieben.

## Ablauf
1. Werte rechnen und prüfen. Bei Balken liefert `traeger()` sie; sonst selbst rechnen (Code). Zahlen in Texte per `tx(wert,stellen)` (Formel, Dezimalkomma) bzw. `fmt()` (Fließtext) einsetzen, nicht abtippen.
2. Drehbuch: 4–10 Schritte, je eine Idee. Rechenbeispiel: Aufgabe → Freischneiden → Gleichungen (mind. eine als `ask`) → Kontrolle → Verläufe/Ergebnis → Plausibilität. Konzept: Situation → Intuition → Definition → Deutung → Rechnen → Folgerung.
3. Bauen:
   - Chat (bevorzugt, wenn ein Inline-Widget-Werkzeug wie `show_widget` da ist): `python3 scripts/baue_animation.py inhalt.js w.html --chat`, Inhalt von `w.html` unverändert als Widget-Code übergeben. Titel im Antworttext nennen (im Chat nicht im Widget). Steht in `assets/cdn.txt` eine URL, lädt das Fragment die Engine per CDN und enthält nur den Inhalt (~5 kB). Schreibt die Person „ohne CDN“ oder meldet eine leere/fehlerhafte Animation: mit `--chat --voll` neu bauen (Engine eingebettet).
   - Sonst / zum Behalten: `python3 scripts/baue_animation.py inhalt.js seite.html` → Artifact oder Datei.
   - Das Skript bindet nur benutzte Bausteine ein und meldet einfache Backslashes (häufigster Fehler).
   - Ohne Codeausführung: mit CDN-URL das Muster eines mit `--chat` gebauten Fragments übernehmen (Inhalt steht in `<script type="text/plain" id="m1t-inhalt">` und wird gestartet, sobald die Engine geladen ist); sonst `assets/kopf-chat.html` (bzw. `kopf-seite.html`) + Inhalt + `</script>` (Seite zusätzlich `</body></html>`).
   - Nach Änderungen an `assets/engine/`: `--kopf` ausführen (erneuert Köpfe und `assets/dist/m1t-chat.js`); für die CDN die neue Datei ins Repository pushen und den neuen Commit-Hash in `assets/cdn.txt` eintragen.
4. Wenn möglich rendern und Screenshot prüfen (Überlappungen, Formelbreite).

## Farben – Skizze und Formel identisch
`"A"` blau `\cA{}` · `"B"` orange `\cB{}` · `"C"` grün `\cC{}` · `"D"` rot `\cD{}` · `"E"` violett `\cE{}` · `"F"` türkis `\cF{}`
Eine Größe = eine Farbe in allen Schritten, auch eingesetzte Zahlen (`\cD{4}`) und Ergebnisse. Bewährt: Lasten D, Lagerkräfte A/B, Querkraft/Abstände C, Momente E, Komponenten/Hilfsgrößen F. Neutral: `"var(--muted)"`. In `LEGEND` jede Farbe nennen. In JS-Strings Backslash doppelt (`"\\cA{F}"`); in Template-Strings ebenso.

## STEPS
`{title, text, tex, ask, hl:[ids], dim:true}`. `text` HTML mit `$…$`; `tex` eine Display-Formel (lang → `\\begin{aligned}…\\end{aligned}`); `ask` versteckt `tex` bis „Lösung zeigen“ (Abspielen stoppt dort); `hl` lässt Elemente mit diesen `id` pulsieren, `dim` blendet den Rest ab. `PRAXIS={title,text}` erscheint im letzten Schritt (`always:true` immer).

## API (Pixel, SVG-y nach unten; Standard-viewBox 600×380, ändern mit `viewbox(w,h)`)
`at(von,bis=∞)` – folgende Elemente ab Schritt `von` (0-basiert) sichtbar. Fast alle Funktionen nehmen `{id}` für `hl`.

**Grundformen:** `line(x1,y1,x2,y2,{c,w,dash})` · `arrow(x1,y1,x2,y2,c,label,{loff,lpos,double,w})` · `force(x,y,grad,len,c,label,{mode:"tip"|"tail",loff})` (Winkel mathematisch: 0 rechts, 90 oben; „tip“ = Spitze am Punkt) · `moment(cx,cy,r,ccw,c,label,{start,span,loff})` · `beam(x1,y1,x2,y2)` · `poly(pkte,{close,fill,c,dash})` · `rect` · `circle` · `point(x,y,label,{c,dx,dy})` · `label(x,y,"F_{Az}",c,{size,anchor})` · `text(x,y,"Klartext",{c,size,anchor})` · `dim(x1,y1,x2,y2,"4 m",{off})` · `axes(x,y,{dirs:{x:"right",z:"down"},len})` · `diagram(pkte,y0,c,label)`

**Bausteine:** `festlager(x,y,{rot})` · `loslager(x,y,{rot})` (Gelenk bei x,y; `rot` in Grad dreht das Lager) · `einspannung(x,y,"left"|"right"|"top"|"bottom",h)` = `wand` · `boden(x,y,w)` · `decke(x,y,w)` · `gelenk(x,y)` · `pendelstab(x1,y1,x2,y2,{label})` · `seil(…,{label})` · `feder(x1,y1,x2,y2,{label,n})` · `rolle(x,y,r)` · `ebene(x,y,len,grad)` → `e.auf(s)` liefert Punkt auf der Ebene · `quader(x,y,b,h,{deg,label})` (x,y = Mitte Unterseite) · `winkel(cx,cy,r,a1,a2,c,"α")` · `streckenlast(x1,x2,y,h1,h2,c,label)` · `schnitt(x,y1,y2,"Schnitt")` · `fkb(x,y,w,h,"Freikörperbild")` · `fachwerk({K:[x,y],…},[["K1","K2","U_1",c],…],{nr:true})`

**Trägermodul** (gerader Balken, Theorie 1. Ordnung, z nach unten):
```js
const T=traeger({l:10, lager:"fest-los"|"einsp-links"|"einsp-rechts", xA:0, xB:10, x0:60, y:110, px:48,
  lasten:[{F:4,x:1.5,name:"F_1",id:"F1"}, {q:2,von:0,bis:4,q2:0,name:"q"}, {M:8,x:2,ccw:true,name:"M_0"}]});
// Werte: T.A, T.B (Lagerkräfte nach oben positiv), T.ME (Einspannmoment, ccw positiv), T.Q(x), T.M(x) (Durchhang positiv), T.Mmax, T.xMmax, T.X(m)→px
// Zeichnen in build(): T.zeichnen({lagerBis}) · T.reaktionen({horizontal,namen}) · T.masse() · T.qVerlauf(y0,{h}) · T.mVerlauf(y0,{h})
```
Lasten positiv = nach unten. `xA/xB` erlauben Kragarme. Verläufe werden mit Werten an allen Sprüngen und am Extremum beschriftet. Geprüft: Gleichlast, Kragträger, Einzelmoment, Kragarm.

**3D** (`ansicht3d`, orthografisch, Rechtssystem, z nach oben). Drehen per Ziehen, dazu **ViewCube** oben rechts wie in AutoCAD: Fläche → Normalansicht, Ecke → Isometrie, Pfeile → Nachbarseite, „Home“ → Startansicht, alles animiert.
```js
const V=ansicht3d({x:270,y:215,s:120,yaw:55,pitch:25,zentrum:[mx,my,mz]});  // s = px/Einheit; zentrum = Drehpunkt (Modellmitte)
V.achsen(len,{o:[x,y,z]}) · V.linie(a,b,{w,dash}) · V.pfeil(a,b,c,label) · V.kraft(p,vektor,c,label,{mode}) · V.moment(p,vektor,c,label) (Doppelpfeil)
V.punkt(p,label) · V.text(p,"…") · V.flaeche([p1,p2,…],{c,fillOpacity}) · V.quader(ecke,[dx,dy,dz],{c}) · V.bogen(mitte,r,n1,n2,a1,a2,c,"α")
V.gehe("vorne"|"hinten"|"links"|"rechts"|"oben"|"unten"|"home"|[yaw,pitch])
```
Ein Schritt kann die Ansicht wechseln: `{title:…, view:"vorne"}` (z. B. Vorderansicht, wenn ein Winkel unverzerrt sichtbar sein soll; danach `view:"home"`). Vorne = Blick von −y, Rechts = von +x, Oben = von +z.
**Wann 3D:** räumliche Kraftsysteme und Gleichgewicht, Kreuzprodukt/Moment als Vektor, Dyname, räumliche Lager (Kugelgelenk), Trägheitstensor/Hauptachsen, Spannungszustand am Würfel, schiefe Biegung, Torsion. Für ebene Probleme bleibt 2D klarer.

## Layout-Tipps
Maßstab als Funktion (`const X=m=>60+48*m`). Lasten oben, Reaktionen unten, Verläufe darunter (Q bei ~y0=250, M bei ~y0=320, viewBox-Höhe ~430). Beschriftungen mit `loff` von Pfeilen wegschieben. Bemaßungen mit `at(0,k)` nach einigen Schritten ausblenden.
