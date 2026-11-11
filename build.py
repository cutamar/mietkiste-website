#!/usr/bin/env python3
"""Builds the static Mietkiste website into docs/ (served by GitHub Pages).

Run: python3 build.py
"""
import json
from datetime import date
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
SITE = "https://mietkiste.ch"
# Add the CNAME file only once mietkiste.ch points to GitHub Pages:
#   python3 build.py --domain
WITH_DOMAIN = "--domain" in sys.argv

PHONE_DISPLAY = "076 509 95 17"
PHONE_TEL = "+41765099517"
WA = "https://wa.me/41765099517"
EMAIL = "info@mietkiste.ch"
SHARELY = "https://www.sharely.ch/de/profil/3b8d8166-ce87-4f62-a841-324b7e6430e0"
TUTTI_PUZZI = "https://www.tutti.ch/de/vi/aargau/haushalt/geraete-utensilien/polster-teppichreiniger-mieten-kaercher-puzzi-brugg/81777608"
TUTTI_DRYER = "https://www.tutti.ch/de/vi/aargau/garten-handwerk/werkzeuge-maschinen/bautrockner-luftentfeuchter-mieten-wasserschaden-brugg/81777306"


def wa(text):
    from urllib.parse import quote
    return f"{WA}?text={quote(text)}"


ICON = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4a.5.5 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3Z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>',
    "sofa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 11V8a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v3"/><path d="M2 13a2 2 0 0 1 4 0v2h12v-2a2 2 0 0 1 4 0v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2Z"/><path d="M6 19v2M18 19v2"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.7s6 6.4 6 11.3a6 6 0 0 1-12 0c0-4.9 6-11.3 6-11.3Z"/><path d="M9 15a3 3 0 0 0 3 3"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 4h14v12H1zM15 9h4l4 4v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    "receipt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 2h14v20l-3-2-2 2-2-2-2 2-2-2-3 2Z"/><path d="M9 7h6M9 11h6M9 15h4"/></svg>',
    "handshake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m11 17 2 2a1 1 0 0 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 0 0 3-3l-3.9-3.9a2 2 0 0 0-2.8 0l-.9.9a1 1 0 0 1-3-3l2.8-2.8a5 5 0 0 1 6 .8L21 7"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 0 0 3-3M3 4h8"/></svg>',
    "menu": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
}

NAV = [
    ("/teppichreiniger-mieten/", "Teppichreiniger"),
    ("/bautrockner-mieten/", "Bautrockner"),
    ("/partner/", "Für Partner"),
    ("/#kontakt", "Kontakt"),
]


def layout(path, title, description, body, schema=None):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == path else ""}>{label}</a>'
        for href, label in NAV
    )
    schema_tag = (
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
        if schema else ""
    )
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{'<meta name="robots" content="noindex">' if path == "/404.html" else f'<link rel="canonical" href="{SITE}{path}">'}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mietkiste">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="de_CH">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c5f5c">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" href="/assets/favicon-512.png">
<link rel="apple-touch-icon" href="/assets/favicon-180.png">
<link rel="stylesheet" href="/assets/style.css">
{schema_tag}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/icon-76.png" alt="" width="38" height="38">mietkiste</a>
    <button class="nav-toggle" aria-label="Menü öffnen" aria-expanded="false" onclick="var n=document.querySelector('.nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">{ICON['menu']}</button>
    <nav class="nav">{nav}<a class="btn btn-wa btn-sm" href="{wa('Hallo Mietkiste, ich habe eine Anfrage:')}">{ICON['wa']}WhatsApp</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/" style="color:#fff"><img src="/assets/icon-76.png" alt="" width="38" height="38">mietkiste</a>
        <p style="margin-top:12px">Vermietung von Reinigungs- und Trocknungsgeräten in der Region Brugg, Baden, Aarau und Zürich.</p>
      </div>
      <div>
        <p class="footer-title">Angebot</p>
        <ul>
          <li><a href="/teppichreiniger-mieten/">Teppich- &amp; Polsterreiniger</a></li>
          <li><a href="/bautrockner-mieten/">Bautrockner &amp; Luftentfeuchter</a></li>
          <li><a href="/partner/">Für Verwaltungen &amp; Firmen</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-title">Kontakt</p>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="{WA}">WhatsApp</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Mietkiste</span>
      <span><a href="/impressum/">Impressum</a> · <a href="/datenschutz/">Datenschutz</a></span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa('Hallo Mietkiste, ich habe eine Anfrage:')}" aria-label="Per WhatsApp anfragen">{ICON['wa']}</a>
</body>
</html>
"""


def faq(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items
    ) + "</div>"


def faq_schema(items):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


BUSINESS = {
    "@type": "LocalBusiness",
    "@id": f"{SITE}/#business",
    "name": "Mietkiste",
    "description": "Vermietung von Teppich- und Polsterreinigern sowie Bautrocknern und Luftentfeuchtern in der Region Brugg, Baden, Aarau und Zürich.",
    "url": SITE + "/",
    "logo": f"{SITE}/assets/logo.png",
    "image": f"{SITE}/assets/og.png",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "priceRange": "CHF 15–149",
    "areaServed": [{"@type": "City", "name": c} for c in
                   ["Brugg", "Baden", "Wettingen", "Aarau", "Lenzburg", "Zürich"]],
    "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "email": EMAIL,
                     "contactType": "customer service", "availableLanguage": ["de", "en"]},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "17:00", "closes": "21:00"},
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Saturday", "Sunday"], "opens": "09:00", "closes": "18:00"},
    ],
    "sameAs": [SHARELY],
}

DELIVERY = "Lieferung in der Region Brugg, Baden, Aarau und Zürich (bis ca. 40 Min. ab Brugg): CHF 25 pro Weg."
TOWNS = "Brugg, Baden, Wettingen, Aarau, Lenzburg, Zürich und Umgebung"


def breadcrumb_schema(path, name):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mietkiste", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path},
        ],
    }


def service_schema(path, name, service_type, description, offers):
    """Rental service with its prices, linked to the business."""
    return {
        "@type": "Service",
        "@id": f"{SITE}{path}#service",
        "name": name,
        "serviceType": service_type,
        "description": description,
        "url": SITE + path,
        "provider": {"@id": f"{SITE}/#business"},
        "areaServed": BUSINESS["areaServed"],
        "offers": [
            {"@type": "Offer", "name": label, "price": str(price), "priceCurrency": "CHF"}
            for label, price in offers
        ],
    }

REVIEWS = [
    ("Hat alles bestens geklappt, gerne wieder ☺️", "Nadine, Teppich- &amp; Polsterreiniger"),
    ("Super Vermieter, jederzeit wieder!", "Heiko, Bautrockner"),
    ("Sehr freundlicher und unkomplizierter Kontakt!", "Sefer, Teppich- &amp; Polsterreiniger"),
]


def reviews_block():
    cards = "".join(
        f'<div class="review"><div class="stars" aria-label="5 von 5 Sternen">★★★★★</div><p>«{t}»</p><div class="who">{w}</div></div>'
        for t, w in REVIEWS
    )
    return f"""
<section class="section alt">
  <div class="wrap">
    <div class="center">
      <div class="eyebrow">Bewertungen</div>
      <h2>5.0 von 5 Sternen</h2>
      <p class="lead">Echte Bewertungen unserer Kundinnen und Kunden auf <a href="{SHARELY}" rel="noopener">Sharely</a>.</p>
    </div>
    <div class="grid-3" style="margin-top:28px">{cards}</div>
  </div>
</section>"""


def cta_block(title, text, wa_text):
    return f"""
<section class="section">
  <div class="wrap">
    <div class="cta">
      <div><h2>{title}</h2><p>{text}</p></div>
      <div class="btn-row">
        <a class="btn btn-wa" href="{wa(wa_text)}">{ICON['wa']}Per WhatsApp anfragen</a>
        <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{ICON['phone']}{PHONE_DISPLAY}</a>
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- Home
HOME_FAQ = [
    ("Wie kann ich ein Gerät reservieren?",
     f"Am schnellsten per WhatsApp oder Telefon ({PHONE_DISPLAY}). Bitte frage mindestens 24 Stunden im Voraus an. Wenn du über eine Plattform mit Versicherung buchen möchtest, findest du uns auch auf Sharely."),
    ("Liefert ihr die Geräte?",
     DELIVERY + " Abholung in Brugg ist kostenlos."),
    ("Gibt es eine Kaution?",
     "Bei Direktmiete verlangen wir eine Kaution von CHF 150 pro Gerät, bar oder per TWINT. Du erhältst sie bei der Rückgabe sofort zurück."),
    ("Wie bezahle ich?",
     "Bar oder per TWINT bei der Übergabe. Für Verwaltungen und Firmen ist auf Anfrage auch Rechnung möglich."),
    ("Bekomme ich eine Quittung für die Versicherung?",
     "Ja, auf Wunsch erhältst du eine Quittung, zum Beispiel für die Gebäude- oder Hausratversicherung nach einem Wasserschaden."),
]

home_body = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Gerätevermietung Region Brugg</div>
      <h1>Reinigungs- und Trocknungsgeräte mieten, ohne sie kaufen zu müssen.</h1>
      <p class="lead">Profi-Geräte für Sofa, Teppich und Autositze oder für die Trocknung nach einem Wasserschaden. Sauber, geprüft und mit kurzer Einführung. Abholung in Brugg oder Lieferung bis Baden, Aarau und Zürich.</p>
      <div class="btn-row">
        <a class="btn btn-wa" href="{wa('Hallo Mietkiste, ich möchte ein Gerät mieten:')}">{ICON['wa']}Per WhatsApp anfragen</a>
        <a class="btn btn-ghost" href="#angebot">Angebot ansehen</a>
      </div>
      <div class="trust">
        <span><span class="stars">★★★★★</span> 5.0 auf Sharely</span>
        <span>{ICON['truck']} Lieferung in der Region</span>
        <span>{ICON['receipt']} Quittung für die Versicherung</span>
      </div>
    </div>
    <div class="hero-art"><img src="/assets/logo.png" alt="Mietkiste Logo" width="480" height="331"></div>
  </div>
</section>

<section class="section" id="angebot">
  <div class="wrap">
    <div class="center">
      <div class="eyebrow">Angebot</div>
      <h2>Was möchtest du erledigen?</h2>
      <p class="lead">Wir vermieten professionelle Geräte für zwei Aufgaben, die im Alltag immer wieder vorkommen.</p>
    </div>
    <div class="grid-2" style="margin-top:32px">
      <div class="card">
        <div class="icon">{ICON['sofa']}</div>
        <h3>Reinigen: Teppich- &amp; Polsterreiniger</h3>
        <ul>
          <li>Sofa, Sessel, Stühle und Matratzen</li>
          <li>Teppiche und Teppichböden</li>
          <li>Autositze und Innenraum</li>
          <li>Ideal vor der Wohnungsabgabe</li>
        </ul>
        <div class="price">ab <strong>CHF 22</strong> pro Tag</div>
        <a class="btn btn-primary" href="/teppichreiniger-mieten/">Details &amp; Preise</a>
      </div>
      <div class="card">
        <div class="icon y">{ICON['drop']}</div>
        <h3>Trocknen: Bautrockner &amp; Luftentfeuchter</h3>
        <ul>
          <li>Wasserschaden und nasse Keller</li>
          <li>Renovation und Neubau</li>
          <li>Feuchte Räume, Wäsche trocknen</li>
          <li>Quittung für die Versicherung</li>
        </ul>
        <div class="price">ab <strong>CHF 49</strong> pro Woche</div>
        <a class="btn btn-primary" href="/bautrockner-mieten/">Details &amp; Preise</a>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="center">
      <div class="eyebrow">So funktioniert's</div>
      <h2>In drei Schritten zum Gerät</h2>
    </div>
    <div class="grid-3" style="margin-top:32px">
      <div class="card"><div class="step-num">1</div><h3>Anfragen</h3><p>Schreib uns per WhatsApp oder ruf an. Wir bestätigen dir Verfügbarkeit und Preis, meistens innert weniger Stunden.</p></div>
      <div class="card"><div class="step-num">2</div><h3>Abholen oder liefern lassen</h3><p>Hol das Gerät in Brugg ab oder lass es dir bringen. Bei der Übergabe zeigen wir dir kurz, wie alles funktioniert.</p></div>
      <div class="card"><div class="step-num">3</div><h3>Nutzen und zurückgeben</h3><p>Nach der Miete bringst du das Gerät zurück oder wir holen es ab. Die Kaution erhältst du sofort zurück.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <div class="eyebrow">Für Verwaltungen &amp; Firmen</div>
      <h2>Ein verlässlicher Partner für Wasserschäden und Wohnungsabgaben</h2>
      <p class="lead">Hausverwaltungen, Hauswarte, Umzugs- und Reinigungsfirmen erhalten bei uns schnelle Antworten, Lieferung vor Ort und auf Wunsch Rechnung.</p>
      <a class="btn btn-primary" href="/partner/">Mehr für Partner</a>
    </div>
    <div class="card">
      <ul class="checklist">
        <li>Kurzfristige Lieferung in der Region nach Absprache</li>
        <li>Ein fester Ansprechpartner per Telefon und WhatsApp</li>
        <li>Quittung oder Rechnung für Versicherung und Buchhaltung</li>
        <li>Saubere, geprüfte Geräte mit Einführung</li>
      </ul>
    </div>
  </div>
</section>

{reviews_block()}

<section class="section" id="kontakt">
  <div class="wrap split">
    <div>
      <div class="eyebrow">Kontakt &amp; Liefergebiet</div>
      <h2>Wir sind in der Region Brugg für dich da</h2>
      <p>Abholung in Brugg. {DELIVERY}</p>
      <div class="area"><span>Brugg</span><span>Baden</span><span>Aarau</span><span>Zürich</span><span>und Umgebung</span></div>
      <div class="btn-row">
        <a class="btn btn-wa" href="{wa('Hallo Mietkiste, ich habe eine Anfrage:')}">{ICON['wa']}WhatsApp</a>
        <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{ICON['phone']}{PHONE_DISPLAY}</a>
      </div>
      <p class="note">Oder per E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div class="card">
      <h3>Erreichbarkeit</h3>
      <ul class="hours">
        <li><span>Montag bis Freitag</span><span>17:00 – 21:00</span></li>
        <li><span>Samstag und Sonntag</span><span>09:00 – 18:00</span></li>
      </ul>
      <p class="note">Übergaben ausserhalb dieser Zeiten nach Absprache.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap prose" style="margin-inline:auto">
    <div class="center"><div class="eyebrow">Fragen</div><h2>Häufige Fragen</h2></div>
    {faq(HOME_FAQ)}
  </div>
</section>

{cta_block("Bereit für saubere oder trockene Räume?", "Schreib uns, wir melden uns schnell.", "Hallo Mietkiste, ich möchte ein Gerät mieten:")}
"""

# ---------------------------------------------------------------- Teppichreiniger
PUZZI_FAQ = [
    ("Ist Reinigungsmittel dabei?",
     "Optional: Kärcher RM 760 Tabs, 2 Tabs für CHF 5 (eine Tankfüllung mit 8 Litern, reicht für ca. 8 bis 12 m²) oder 4 Tabs für CHF 9."),
    ("Hat das Gerät einen Schweizer Stecker?",
     "Ein Schweizer Stecker-Adapter ist immer dabei. Du kannst das Gerät an jeder normalen Steckdose betreiben."),
    ("Kann ich damit auch grosse Teppichböden reinigen?",
     "Ja, mit der Polster- und Handdüse. Eine grosse Bodendüse ist nicht dabei, für ganze Räume brauchst du deshalb etwas mehr Zeit."),
    ("Wie lange braucht der Stoff zum Trocknen?",
     "Je nach Material meistens einige Stunden. Gut lüften oder heizen beschleunigt die Trocknung."),
    ("Muss ich das Gerät gereinigt zurückgeben?",
     "Nein. Bitte nur groben Schmutz entfernen und den Schmutzwassertank leeren."),
]

puzzi_body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Mietkiste</a> › Teppichreiniger mieten</div>
    <h1>Teppich- &amp; Polsterreiniger mieten in Brugg</h1>
    <p class="lead">Kärcher Puzzi mieten statt kaufen: Mit dem professionellen Waschsauger (Sprühextraktionsgerät) reinigst du Sofa, Teppich, Matratze und Autositze in der Tiefe. Das Gerät sprüht Reinigungswasser in den Stoff und saugt das Schmutzwasser direkt wieder ab. Abholung in Brugg oder Lieferung nach {TOWNS}.</p>
    <div class="btn-row">
      <a class="btn btn-wa" href="{wa('Hallo Mietkiste, ich möchte den Teppich- und Polsterreiniger mieten. Datum:')}">{ICON['wa']}Verfügbarkeit anfragen</a>
      <a class="btn btn-ghost" href="#preise">Preise</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <h2>Ideal für</h2>
      <ul class="checklist">
        <li>Sofas, Sessel, Stühle und Polstermöbel</li>
        <li>Teppiche und Teppichböden</li>
        <li>Autositze und komplette Innenreinigung</li>
        <li>Matratzen</li>
        <li>Flecken, Tierhaare, Gerüche und verschüttete Getränke</li>
        <li>Wohnungsabgabe oder Autoverkauf</li>
      </ul>
    </div>
    <div class="card">
      <h3>Im Mietpreis enthalten</h3>
      <ul class="checklist">
        <li>Kärcher Puzzi 8/1 Waschsauger</li>
        <li>Polsterdüse, Schlauch und Zubehör</li>
        <li>Schweizer Stecker-Adapter</li>
        <li>Kurze Einführung bei der Übergabe</li>
      </ul>
      <p class="note">Reinigungsmittel optional: Kärcher RM 760, 2 Tabs CHF 5, 4 Tabs CHF 9.</p>
    </div>
  </div>
</section>

<section class="section alt" id="preise">
  <div class="wrap prose" style="margin-inline:auto">
    <h2>Preise</h2>
    <table class="table">
      <tr><th>Mietdauer</th><th>Preis</th></tr>
      <tr><td>1 Tag (24 Stunden)</td><td>CHF 22</td></tr>
      <tr><td>Wochenende (Freitag bis Sonntag)</td><td>CHF 35</td></tr>
      <tr><td>1 Woche</td><td>CHF 69</td></tr>
      <tr><td>Reinigungsmittel RM 760, 2 / 4 Tabs</td><td>CHF 5 / 9</td></tr>
    </table>
    <p class="note">Kaution CHF 150 (bar oder TWINT). {DELIVERY} Abholung in Brugg kostenlos.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>So reinigst du richtig</h2>
    <div class="grid-3" style="margin-top:20px">
      <div class="card"><div class="step-num">1</div><h3>Vorbereiten</h3><p>Grob absaugen und an einer unauffälligen Stelle testen, ob der Stoff farbecht ist.</p></div>
      <div class="card"><div class="step-num">2</div><h3>Sprühen und absaugen</h3><p>Langsame, überlappende Bahnen ziehen. Stark verschmutzte Stellen zweimal behandeln.</p></div>
      <div class="card"><div class="step-num">3</div><h3>Trocknen lassen</h3><p>Gut lüften. Nach einigen Stunden ist der Stoff wieder trocken und frisch.</p></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap prose" style="margin-inline:auto">
    <h2>Häufige Fragen</h2>
    {faq(PUZZI_FAQ)}
  </div>
</section>

{reviews_block()}
{cta_block("Teppichreiniger reservieren", "Sag uns das Datum, wir bestätigen dir die Verfügbarkeit.", "Hallo Mietkiste, ich möchte den Teppich- und Polsterreiniger mieten. Datum:")}
"""

# ---------------------------------------------------------------- Bautrockner
DRYER_FAQ = [
    ("Wie lange dauert die Trocknung nach einem Wasserschaden?",
     "Meistens 1 bis 4 Wochen, je nach Raum und Material. Ab einer Woche wird die Miete pro Tag deutlich günstiger."),
    ("Wie viel Strom braucht das Gerät?",
     "Das Gerät hat eine Leistungsaufnahme von 630 W. Im Dauerbetrieb kostet das ca. CHF 4 bis 5 pro Tag, dank Hygrostat meist weniger."),
    ("Muss ich den Wassertank ständig leeren?",
     "Nein. Mit dem mitgelieferten Schlauch für Dauerablauf kannst du das Wasser direkt in einen Abfluss leiten. Ohne Schlauch fasst der Tank 5 Liter."),
    ("Ist das Gerät laut?",
     "Mit 56 dB(A) ist es etwa so laut wie ein normales Gespräch, für einen Bautrockner eher leise."),
    ("Bekomme ich eine Quittung für die Versicherung?",
     "Ja, auf Wunsch erhältst du eine Quittung für die Gebäude- oder Hausratversicherung."),
]

dryer_body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Mietkiste</a> › Bautrockner mieten</div>
    <h1>Bautrockner &amp; Luftentfeuchter mieten in Brugg</h1>
    <p class="lead">Bautrockner, Luftentfeuchter oder Raumentfeuchter mieten: Unser Industrie-Kondenstrockner entfeuchtet bis zu 60 Liter pro Tag. Für Wasserschäden, nasse Keller, Renovationen und Neubauten. Abholung in Brugg oder Lieferung nach {TOWNS}, mit Quittung für die Versicherung.</p>
    <div class="btn-row">
      <a class="btn btn-wa" href="{wa('Hallo Mietkiste, ich brauche einen Bautrockner. Ab wann und für wie lange:')}">{ICON['wa']}Verfügbarkeit anfragen</a>
      <a class="btn btn-ghost" href="#preise">Preise</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <h2>Ideal für</h2>
      <ul class="checklist">
        <li>Wasserschäden in Wohnung, Haus oder Keller</li>
        <li>Nasse oder muffige Keller</li>
        <li>Renovationen und Neubauten, schnelleres Austrocknen von Wänden und Böden</li>
        <li>Feuchte Räume und Schimmelvorbeugung</li>
        <li>Wäsche trocknen im Winter</li>
      </ul>
    </div>
    <div class="card">
      <h3>Technische Daten</h3>
      <ul class="checklist">
        <li>Bis 60 L Entfeuchtung pro Tag</li>
        <li>630 W, nur 56 dB(A)</li>
        <li>Feuchtigkeit einstellbar 10 bis 98 %, Timer, Abtauautomatik</li>
        <li>5-L-Tank oder Dauerablauf per Schlauch</li>
        <li>54 x 50 x 82 cm, 37,5 kg, auf Rollen</li>
      </ul>
    </div>
  </div>
</section>

<section class="section alt" id="preise">
  <div class="wrap prose" style="margin-inline:auto">
    <h2>Preise</h2>
    <table class="table">
      <tr><th>Mietdauer</th><th>Preis</th></tr>
      <tr><td>1 Tag (24 Stunden)</td><td>CHF 15</td></tr>
      <tr><td>1 Woche</td><td>CHF 49</td></tr>
      <tr><td>2 Wochen</td><td>CHF 85</td></tr>
      <tr><td>1 Monat</td><td>CHF 149</td></tr>
    </table>
    <p class="note">Inklusive Stromkabel, Schlauch für Dauerablauf und Kurzanleitung. Kaution CHF 150 (bar oder TWINT). {DELIVERY}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Nach einem Wasserschaden: so gehst du vor</h2>
    <div class="grid-3" style="margin-top:20px">
      <div class="card"><div class="step-num">1</div><h3>Ursache stoppen</h3><p>Wasserzufuhr stoppen, stehendes Wasser entfernen und den Schaden mit Fotos dokumentieren.</p></div>
      <div class="card"><div class="step-num">2</div><h3>Versicherung informieren</h3><p>Melde den Schaden deiner Versicherung. Die Quittung für die Gerätemiete erhältst du von uns.</p></div>
      <div class="card"><div class="step-num">3</div><h3>Trocknen</h3><p>Gerät aufstellen, Raum geschlossen halten und den Fortschritt regelmässig kontrollieren.</p></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap prose" style="margin-inline:auto">
    <h2>Häufige Fragen</h2>
    {faq(DRYER_FAQ)}
  </div>
</section>

{reviews_block()}
{cta_block("Bautrockner reservieren", "Sag uns ab wann und für wie lange, wir melden uns schnell.", "Hallo Mietkiste, ich brauche einen Bautrockner. Ab wann und für wie lange:")}
"""

# ---------------------------------------------------------------- Partner
partner_body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Mietkiste</a> › Für Partner</div>
    <h1>Gerätemiete für Verwaltungen, Hauswarte und Firmen</h1>
    <p class="lead">Wenn ein Keller unter Wasser steht oder eine Wohnungsabgabe ansteht, zählt Tempo. Mietkiste liefert Bautrockner sowie Teppich- und Polsterreiniger in der Region Brugg, Baden, Aarau und Zürich, mit einem festen Ansprechpartner.</p>
    <div class="btn-row">
      <a class="btn btn-wa" href="{wa('Hallo Mietkiste, ich melde mich als Partner (Firma / Verwaltung):')}">{ICON['wa']}Kontakt aufnehmen</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{ICON['phone']}{PHONE_DISPLAY}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Für wen wir arbeiten</h2>
    <div class="grid-3" style="margin-top:20px">
      <div class="card"><div class="icon y">{ICON['drop']}</div><h3>Hausverwaltungen &amp; Hauswarte</h3><p>Bautrockner nach Wasserschäden, direkt zur Liegenschaft geliefert. Quittung oder Rechnung für die Versicherung.</p></div>
      <div class="card"><div class="icon">{ICON['sofa']}</div><h3>Umzugs- &amp; Reinigungsfirmen</h3><p>Teppich- und Polsterreiniger für Endreinigungen und Wohnungsabgaben, auch kurzfristig nach Absprache.</p></div>
      <div class="card"><div class="icon">{ICON['handshake']}</div><h3>Garagen &amp; Autohandel</h3><p>Polsterreiniger für Autositze und Innenraum, zum Beispiel vor dem Verkauf eines Fahrzeugs.</p></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap split">
    <div>
      <h2>Was Partner von uns erhalten</h2>
      <ul class="checklist">
        <li>Schnelle Rückmeldung per Telefon oder WhatsApp</li>
        <li>Lieferung und Abholung vor Ort nach Absprache</li>
        <li>Rechnung oder Quittung für Buchhaltung und Versicherung</li>
        <li>Saubere, geprüfte Geräte und Einführung für Ihre Mitarbeitenden</li>
        <li>Konditionen für wiederkehrende Aufträge auf Anfrage</li>
      </ul>
    </div>
    <div class="card">
      <h3>Kontakt für Partner</h3>
      <p>Rufen Sie an oder schreiben Sie uns. Wir besprechen gerne, wie wir Sie bei Wasserschäden und Wohnungsabgaben unterstützen können.</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </div>
</section>

{reviews_block()}
{cta_block("Lassen Sie uns zusammenarbeiten", "Ein kurzer Anruf genügt, um die Details zu besprechen.", "Hallo Mietkiste, ich melde mich als Partner (Firma / Verwaltung):")}
"""

# ---------------------------------------------------------------- Legal
impressum_body = f"""
<section class="page-hero"><div class="wrap"><h1>Impressum</h1></div></section>
<section class="section"><div class="wrap prose">
  <h2>Kontakt</h2>
  <p>Mietkiste<br>E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p><a class="btn btn-wa" href="{wa('Hallo Mietkiste, ich habe eine Frage:')}">{ICON['wa']}Per WhatsApp schreiben</a></p>
  <h2>Haftungsausschluss</h2>
  <p>Die Inhalte dieser Website werden mit Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität wird keine Gewähr übernommen. Preise und Verfügbarkeit gelten nach Bestätigung im Einzelfall.</p>
  <h2>Links</h2>
  <p>Für Inhalte verlinkter Websites (z.B. Sharely, tutti) sind ausschliesslich deren Betreiber verantwortlich.</p>
</div></section>
"""

datenschutz_body = f"""
<section class="page-hero"><div class="wrap"><h1>Datenschutz</h1></div></section>
<section class="section"><div class="wrap prose">
  <p>Wir nehmen den Schutz deiner Daten ernst. Diese Website verwendet keine Cookies, kein Tracking und keine Analyse-Tools.</p>
  <h2>Hosting</h2>
  <p>Die Website wird über GitHub Pages (GitHub, Inc., USA) bereitgestellt und über Cloudflare (Cloudflare, Inc., USA) ausgeliefert. Beim Aufruf verarbeiten diese Anbieter technisch notwendige Daten wie IP-Adresse, Zeitpunkt und aufgerufene Seite, um die Website auszuliefern und vor Missbrauch zu schützen.</p>
  <h2>Kontakt per WhatsApp, Telefon oder E-Mail</h2>
  <p>Wenn du uns kontaktierst, verwenden wir deine Angaben (z.B. Name, Telefonnummer, Nachricht) nur, um deine Anfrage und die Miete abzuwickeln. Bei WhatsApp gelten zusätzlich die Datenschutzbestimmungen von WhatsApp (Meta).</p>
  <h2>Deine Rechte</h2>
  <p>Du kannst jederzeit Auskunft über deine bei uns gespeicherten Daten verlangen und deren Berichtigung oder Löschung beantragen. Kontakt: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <p class="note">Stand: November 2026</p>
</div></section>
"""

notfound_body = """
<section class="page-hero"><div class="wrap center">
  <h1>Seite nicht gefunden</h1>
  <p class="lead">Diese Seite gibt es leider nicht.</p>
  <a class="btn btn-primary" href="/">Zur Startseite</a>
</div></section>
"""

PAGES = [
    ("/", "index.html", "Mietkiste | Teppichreiniger & Bautrockner mieten in Brugg",
     "Teppich- und Polsterreiniger sowie Bautrockner mieten in der Region Brugg, Baden, Aarau und Zürich. Sauber, geprüft, mit Lieferung. 5.0 Sterne.",
     home_body, {"@context": "https://schema.org", "@graph": [BUSINESS, faq_schema(HOME_FAQ)]}),
    ("/teppichreiniger-mieten/", "teppichreiniger-mieten/index.html",
     "Teppichreiniger & Polsterreiniger mieten Brugg | Mietkiste",
     "Kärcher Puzzi Teppich- und Polsterreiniger mieten in Brugg: Sofa, Teppich, Matratze, Autositze. Ab CHF 22 pro Tag, Lieferung bis Baden, Aarau, Zürich.",
     puzzi_body, {"@context": "https://schema.org", "@graph": [
         BUSINESS, faq_schema(PUZZI_FAQ),
         breadcrumb_schema("/teppichreiniger-mieten/", "Teppichreiniger mieten"),
         service_schema("/teppichreiniger-mieten/", "Teppich- & Polsterreiniger mieten (Kärcher Puzzi 8/1)",
                        "Vermietung Teppichreiniger, Polsterreiniger, Waschsauger",
                        "Kärcher Puzzi 8/1 Waschsauger für Sofa, Teppich, Matratze und Autositze, mit Schweizer Stecker-Adapter.",
                        [("1 Tag", 22), ("Wochenende", 35), ("1 Woche", 69)])]}),
    ("/bautrockner-mieten/", "bautrockner-mieten/index.html",
     "Bautrockner & Luftentfeuchter mieten in Brugg | Mietkiste",
     "Bautrockner mieten für Wasserschaden, Keller und Renovation in Brugg, Baden, Aarau und Zürich. 60 L/Tag, ab CHF 49 pro Woche, Quittung für die Versicherung.",
     dryer_body, {"@context": "https://schema.org", "@graph": [
         BUSINESS, faq_schema(DRYER_FAQ),
         breadcrumb_schema("/bautrockner-mieten/", "Bautrockner mieten"),
         service_schema("/bautrockner-mieten/", "Bautrockner & Luftentfeuchter mieten (60 L/Tag)",
                        "Vermietung Bautrockner, Luftentfeuchter",
                        "Industrie-Luftentfeuchter mit bis zu 60 Litern Entfeuchtung pro Tag für Wasserschäden, Keller, Renovation und Neubau.",
                        [("1 Tag", 15), ("1 Woche", 49), ("2 Wochen", 85), ("1 Monat", 149)])]}),
    ("/partner/", "partner/index.html", "Für Verwaltungen, Hauswarte & Firmen | Mietkiste",
     "Bautrockner und Teppichreiniger für Hausverwaltungen, Hauswarte, Umzugs- und Reinigungsfirmen in der Region Brugg. Lieferung vor Ort, Rechnung möglich.",
     partner_body, {"@context": "https://schema.org", "@graph": [
         BUSINESS, breadcrumb_schema("/partner/", "Für Partner")]}),
    ("/impressum/", "impressum/index.html", "Impressum | Mietkiste", "Impressum von Mietkiste.", impressum_body, None),
    ("/datenschutz/", "datenschutz/index.html", "Datenschutz | Mietkiste", "Datenschutzerklärung von Mietkiste.", datenschutz_body, None),
    ("/404.html", "404.html", "Seite nicht gefunden | Mietkiste", "Diese Seite wurde nicht gefunden.", notfound_body, None),
]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    shutil.copy(ROOT / "favicon.ico", OUT / "favicon.ico")
    for path, file, title, desc, body, schema in PAGES:
        target = OUT / file
        target.parent.mkdir(parents=True, exist_ok=True)
        html = layout(path, title, desc, body, schema)
        # Make internal links relative so the site works both on the custom
        # domain and on the GitHub Pages project URL (/mietkiste-website/).
        # 404.html is served from any path, so it uses absolute URLs instead.
        prefix = SITE + "/" if file == "404.html" else "../" * file.count("/") or "./"
        html = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{prefix}', html)
        target.write_text(html, encoding="utf-8")
    if WITH_DOMAIN:
        (OUT / "CNAME").write_text("mietkiste.ch\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = [p for p, *_ in PAGES if p != "/404.html"]
    today = date.today().isoformat()
    sitemap = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n')
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
