#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las páginas del área de reportes para inversores a partir de
_build/reportes.json (extraído del sitio original en Wix).

Uso:  python3 _build/build_reportes.py
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_build", "reportes.json")
SITE = "https://www.tangoholding.com"

# Los PDFs siguen alojados en el file hosting de Wix. Mientras el sitio de Wix
# exista (alcanza con el plan Free) estos links funcionan. Para mudarlos a
# Netlify o a un bucket propio, cambiá solo esta constante.
PDF_BASE = "https://6737a04c-ebe9-4353-a225-ee5c8d4c83da.filesusr.com/ugd/"

DOC_ICON = (
    '<svg class="doc" viewBox="0 0 80 100" aria-hidden="true">'
    '<path d="M6 4h44l24 24v68H6z"/><path d="M50 4v24h24"/></svg>'
)

FLAG_ES = ('<svg class="flag" viewBox="0 0 30 20" aria-hidden="true">'
           '<rect width="30" height="20" fill="#c60b1e"/>'
           '<rect y="5" width="30" height="10" fill="#ffc400"/></svg>')

HEADER = """<header class="site-header">
  <div class="col">
    <a class="logo" href="/" aria-label="Tango Holding">
      <img src="/assets/img/logo.png" alt="Tango Holding" width="205" height="35">
    </a>
    <div class="header-right">
      <button class="menu-btn" type="button" aria-expanded="false"
              aria-controls="nav-panel">MENU</button>
      <div class="lang">
        <button class="lang-btn" type="button" aria-expanded="false" aria-label="Español">
          %s
          <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="lang-menu">
          <a href="/" hreflang="es">%s Español</a>
          <a href="/en/" hreflang="en">English</a>
        </div>
      </div>
    </div>
    <nav class="nav-panel" id="nav-panel" aria-label="MENU">
      <a href="/#quienes-somos">QUIÉNES SOMOS</a>
      <a href="/#servicios">SERVICIOS</a>
      <a href="/#proyectos">PROYECTOS</a>
      <a href="/#contacto">CONTACTO</a>
    </nav>
  </div>
</header>""" % (FLAG_ES, FLAG_ES)


def esc(s):
    return html.escape(s, quote=False)


def fix_paren(s):
    """Al extraer el texto de Wix a veces se pierde el paréntesis de apertura."""
    s = s.strip()
    if s.endswith(")") and "(" not in s:
        s = "(" + s
    return s


def render(slug, page):
    hero = esc(page.get("hero") or "Reportes")
    intro = page.get("intro") or ""
    title = page.get("title") or (hero + " | Tango Holding")

    # agrupar los items por fondo, respetando el orden de aparición
    groups, order = {}, []
    for it in page["items"]:
        key = it.get("f", 0)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(it)

    fondo_text = {f["y"]: f["t"] for f in page.get("fondos", [])}

    blocks = []
    for key in order:
        lines = fondo_text.get(key) or []
        head = "<br>".join(esc(l) for l in lines)
        items = []
        for it in groups[key]:
            lines = [fix_paren(l) for l in it["n"]]
            if not lines:
                # El reporte consolidado no trae etiqueta propia en el sitio de
                # Wix: su nombre es el título de la página.
                lines = [intro.strip() or "Reporte consolidado"]
            name = "<br>".join(esc(l) for l in lines)
            href = it["h"]
            if not href.startswith("http"):
                href = PDF_BASE + href
            items.append(
                '          <a class="rep-item" href="%s" target="_blank" rel="noopener">\n'
                '            <span class="rep-name">%s</span>\n'
                "            %s\n"
                "          </a>" % (href, name, DOC_ICON)
            )
        blocks.append(
            '  <section class="fondo">\n'
            '    <div class="col">\n'
            "      %s\n"
            '      <div class="rep-grid">\n%s\n      </div>\n'
            "    </div>\n"
            "  </section>"
            % (("<h2>%s</h2>" % head) if head else "", "\n".join(items))
        )

    intro_html = ""
    if intro:
        intro_html = (
            '  <section class="rep-intro">\n    <div class="col">'
            "<h2>%s</h2></div>\n  </section>\n" % esc(intro)
        )

    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="robots" content="noindex, nofollow">
<meta name="referrer" content="no-referrer">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
<link rel="stylesheet" href="/assets/css/reportes.css">
</head>
<body class="rep">

%s

<main id="main">

  <section class="rep-hero">
    <div class="section-bg" style="background-image:url('/assets/img/rep-hero.jpg')"></div>
    <div class="col">
      <div class="rep-hero-panel">
        <h1>%s</h1>
        <span class="rule"></span>
      </div>
    </div>
  </section>

%s%s

  <section class="rep-note">
    <div class="col">
      <p>Área de reportes para inversores de Tango Holding ·
         <a href="/">Volver al sitio</a></p>
    </div>
  </section>

</main>

<script src="/assets/js/main.js" defer></script>
</body>
</html>
""" % (esc(title), HEADER, hero, intro_html,
       "\n\n".join(blocks))


def main():
    if not os.path.exists(DATA):
        raise SystemExit(
            "Falta %s. Es el archivo que se extrae del sitio de Wix." % DATA)

    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)

    n = 0
    for slug, page in data.items():
        if page.get("err"):
            print("  ! %s: %s" % (slug, page["err"]))
            continue
        out = os.path.join(ROOT, slug + ".html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(render(slug, page))
        print("escrito: %s.html  (%d fondos, %d reportes)"
              % (slug, len(page.get("fondos", [])), len(page["items"])))
        n += 1
    print("\n%d páginas generadas." % n)


if __name__ == "__main__":
    main()
