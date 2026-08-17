#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera index.html (español) y en/index.html (inglés) a partir de content.py.

Uso:  python3 _build/build.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import HERO_SLIDES, SERVICES, PROJECTS, ES, EN  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LB_DATA = os.path.join(ROOT, "_build", "lightboxes.json")
SITE = "https://www.tangoholding.com"

FLAG_ES = ('<svg class="flag" viewBox="0 0 30 20" aria-hidden="true">'
           '<rect width="30" height="20" fill="#c60b1e"/>'
           '<rect y="5" width="30" height="10" fill="#ffc400"/></svg>')

FLAG_EN = ('<svg class="flag" viewBox="0 0 30 20" aria-hidden="true">'
           '<rect width="30" height="20" fill="#fff"/>'
           '<g fill="#b22234">'
           '<rect width="30" height="1.54"/><rect y="3.08" width="30" height="1.54"/>'
           '<rect y="6.15" width="30" height="1.54"/><rect y="9.23" width="30" height="1.54"/>'
           '<rect y="12.31" width="30" height="1.54"/><rect y="15.38" width="30" height="1.54"/>'
           '<rect y="18.46" width="30" height="1.54"/></g>'
           '<rect width="13" height="10.77" fill="#3c3b6e"/></svg>')

FLAGS = {"es": FLAG_ES, "en": FLAG_EN}
LANG_NAME = {"es": "Español", "en": "English"}


def lightbox_json():
    """Datos de las ventanas emergentes de proyecto, extraídas del sitio de Wix."""
    import json
    if not os.path.exists(LB_DATA):
        return "[]"
    with open(LB_DATA, encoding="utf-8") as fh:
        return json.dumps(json.load(fh), ensure_ascii=False, separators=(",", ":"))


def rel(t, path):
    """Prefijo correcto según el idioma (las páginas EN viven en /en/)."""
    return path if t["lang"] == "es" else "../" + path


def hero(t):
    slides, copies, dots = [], [], []
    for i, s in enumerate(HERO_SLIDES):
        cls = " active" if i == 0 else ""
        lazy = "" if i == 0 else 'loading="lazy" '
        act = ' class="active"' if i == 0 else ""
        src = rel(t, "assets/img/" + s["img"])
        nl = "\n"
        slides.append(
            f'        <div class="hero-slide{cls}">'
            f'<img src="{src}" alt="" {lazy}decoding="async"></div>'
        )
        copies.append(
            f'        <div class="slide-copy{cls}">{nl}'
            f'          <p class="hero-title">{s["title"]}</p>{nl}'
            f'          <p class="hero-sub">{s["sub"]}</p>{nl}'
            f'        </div>'
        )
        dots.append(
            f'        <li role="presentation"><button type="button" role="tab"'
            f'{act} aria-label="{i + 1}"></button></li>'
        )
    return "\n".join(slides), "\n".join(copies), "\n".join(dots)


def services(t):
    out = []
    for cfg, label in zip(SERVICES, t["services"]):
        out.append(
            f'          <div class="service">\n'
            f'            <img src="{rel(t, "assets/img/" + cfg["icon"])}" alt="" '
            f'width="{cfg["w"]}" height="{cfg["w"]}" loading="lazy" decoding="async">\n'
            f'            <h3>{label}</h3>\n'
            f'          </div>'
        )
    return "\n".join(out)


def projects(t):
    idx = 3 if t["lang"] == "es" else 4
    out = []
    for p in PROJECTS:
        img, title, place = p[0], p[1], p[2]
        lines = "\n".join(
            f'                <p class="p-line">{l}</p>' for l in p[idx]
        )
        out.append(
            f'          <figure class="gallery-item" tabindex="0">\n'
            f'            <img src="{rel(t, "assets/img/" + img)}" alt="{title}" '
            f'loading="lazy" decoding="async">\n'
            f'            <figcaption class="overlay">\n'
            f'              <p class="p-title">{title}</p>\n'
            f'              <p class="p-place">{place}</p>\n'
            f'              <p class="p-rule" aria-hidden="true">_</p>\n'
            f'{lines}\n'
            f'            </figcaption>\n'
            f'          </figure>'
        )
    return "\n".join(out)


def nav_links(t):
    ids = ["quienes-somos", "servicios", "proyectos", "contacto"]
    return "\n".join(
        f'          <a href="#{i}">{label}</a>' for i, label in zip(ids, t["nav"])
    )


def render(t):
    slides, copies, dots = hero(t)
    canonical = SITE + t["self_href"]
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['description']}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{SITE}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Tango Holding">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['description']}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/hero-1.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['title']}">
<meta name="twitter:description" content="{t['description']}">
<meta name="twitter:image" content="{SITE}/assets/img/hero-1.jpg">
<meta name="theme-color" content="#053160">

<link rel="icon" href="{rel(t, 'favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel(t, 'assets/img/logo.png')}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{rel(t, 'assets/css/style.css')}">

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Organization","name":"Tango Holding",
"url":"{SITE}/","logo":"{SITE}/assets/img/logo.png","foundingDate":"2009",
"description":"{t['description']}","email":"santiago@tangoholding.com"}}
</script>
</head>
<body>

<a class="skip" href="#main">{t['skip']}</a>

<header class="site-header">
  <div class="col">
    <a class="logo" href="{t['self_href']}" aria-label="Tango Holding">
      <img src="{rel(t, 'assets/img/logo.png')}" alt="Tango Holding" width="205" height="35">
    </a>

    <div class="header-right">
      <button class="menu-btn" type="button" aria-expanded="false"
              aria-controls="nav-panel">{t['menu']}</button>

      <div class="lang">
        <button class="lang-btn" type="button" aria-expanded="false"
                aria-label="{LANG_NAME[t['lang']]}">
          {FLAGS[t['lang']]}
          <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="lang-menu">
          <a href="{t['self_href']}" hreflang="{t['lang']}">{FLAGS[t['lang']]}
            {LANG_NAME[t['lang']]}</a>
          <a href="{t['other_href']}" hreflang="{t['other_lang']}">{FLAGS[t['other_lang']]}
            {LANG_NAME[t['other_lang']]}</a>
        </div>
      </div>
    </div>

    <nav class="nav-panel" id="nav-panel" aria-label="{t['menu']}">
{nav_links(t)}
    </nav>
  </div>
</header>

<nav class="dots-nav" aria-label="{t['menu']}">
  <button type="button" aria-label="Home"></button>
  <button type="button" aria-label="{t['nav'][0]}"></button>
  <button type="button" aria-label="{t['nav'][1]}"></button>
  <button type="button" aria-label="{t['nav'][2]}"></button>
  <button type="button" aria-label="{t['nav'][3]}"></button>
</nav>

<main id="main">

  <!-- ============ HERO ============ -->
  <section class="hero" id="home" data-section>
    <div class="hero-slides">
{slides}
    </div>
    <div class="hero-copy">
{copies}
    </div>
    <ul class="hero-dots" role="tablist">
{dots}
    </ul>
  </section>

  <!-- ============ QUIÉNES SOMOS ============ -->
  <section class="about" id="quienes-somos" data-section>
    <div class="section-bg" style="background-image:url('{rel(t, 'assets/img/about-bg.jpg')}')"></div>
    <div class="col">
      <div class="about-panel">
        <h2 class="panel-title">{t['about_title']}</h2>
{chr(10).join('        <p>' + p + '</p>' for p in t['about'])}
        <div class="person">
          <div class="avatar">
            <img src="{rel(t, 'assets/img/team-martin.png')}" alt="{t['person']}"
                 loading="lazy" decoding="async">
          </div>
          <p class="name">{t['person']}</p>
          <p class="role">{t['role']}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ SERVICIOS ============ -->
  <section class="services" id="servicios" data-section>
    <div class="section-bg" style="background-image:url('{rel(t, 'assets/img/services-bg.jpg')}')"></div>
    <div class="col">
      <div class="services-panel">
        <h2 class="panel-title">{t['services_title']}</h2>
        <div class="services-grid">
{services(t)}
        </div>
      </div>
    </div>
  </section>

  <!-- ============ PROYECTOS ============ -->
  <section class="projects" id="proyectos" data-section>
    <div class="col">
      <h2 class="panel-title">{t['projects_title']}</h2>
    </div>
    <div class="gallery-wrap">
      <button class="gal-arrow prev" type="button" aria-label="{t['prev']}">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
      </button>
      <div class="gallery">
{projects(t)}
      </div>
      <button class="gal-arrow next" type="button" aria-label="{t['next']}">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
      </button>
    </div>
  </section>

  <!-- ============ CONTACTO ============ -->
  <section class="contact" id="contacto" data-section>
    <div class="section-bg" style="background-image:url('{rel(t, 'assets/img/contact-bg.jpg')}')"></div>
    <div class="col">
      <div class="contact-panel">
        <h2 class="panel-title">{t['contact_title']}</h2>

        <form class="contact-form" name="contacto" method="POST"
              data-netlify="true" netlify-honeypot="bot-field"
              data-thanks="{t['f_thanks']}" data-error="{t['f_error']}">
          <input type="hidden" name="form-name" value="contacto">
          <p class="hp"><label>No completar<input name="bot-field"></label></p>

          <div class="field">
            <label for="f-name">{t['f_name']}</label>
            <input id="f-name" name="nombre" type="text" required autocomplete="name">
          </div>
          <div class="field">
            <label for="f-email">{t['f_email']}</label>
            <input id="f-email" name="email" type="email" required autocomplete="email">
          </div>
          <div class="field">
            <label for="f-msg">{t['f_msg']}</label>
            <textarea id="f-msg" name="mensaje" required></textarea>
          </div>

          <button class="btn-send" type="submit">{t['f_send']}</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>


  <!-- ============ VENTANA EMERGENTE DE PROYECTO ============ -->
  <div class="lb-overlay" role="dialog" aria-modal="true" aria-labelledby="lb-title">
    <div class="lb-panel">
      <button class="lb-close" type="button" aria-label="{t["lb_close"]}">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>
      </button>
      <h2 class="lb-title" id="lb-title"></h2>
      <p class="lb-place"></p>
      <p class="lb-rule" aria-hidden="true">&#8211;</p>
      <div class="lb-text"></div>
      <div class="lb-gallery-wrap">
        <button class="lb-arrow prev" type="button" aria-label="{t["prev"]}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
        </button>
        <div class="lb-gallery"></div>
        <button class="lb-arrow next" type="button" aria-label="{t["next"]}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
        </button>
      </div>
    </div>
  </div>

  <script type="application/json" id="lb-data">{lightbox_json()}</script>

</main>

<script src="{rel(t, 'assets/js/main.js')}" defer></script>
</body>
</html>
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("escrito:", os.path.relpath(path, ROOT))


def main():
    write(os.path.join(ROOT, "index.html"), render(ES))
    write(os.path.join(ROOT, "en", "index.html"), render(EN))

    write(os.path.join(ROOT, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
          '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          f'  <url><loc>{SITE}/</loc>\n'
          f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE}/"/>\n'
          f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/"/>\n'
          '  </url>\n'
          f'  <url><loc>{SITE}/en/</loc>\n'
          f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE}/"/>\n'
          f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/"/>\n'
          '  </url>\n'
          '</urlset>\n')

    write(os.path.join(ROOT, "robots.txt"),
          "User-agent: *\n"
          "Allow: /\n"
          "Disallow: /reportes\n"
          "Disallow: /juankeser\n\n"
          f"Sitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    main()
