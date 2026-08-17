#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera _build/preview-es.html y _build/preview-en.html: copias autocontenidas
(CSS y JS embebidos) que apuntan a las imágenes en el CDN de Wix.

Sirve solo para verificar el diseño contra el sitio original antes de tener
los archivos de imagen locales. No forma parte del sitio publicado.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CDN = "https://static.wixstatic.com/media/405a64_"

MAP = {
    "logo.png": "0b047cf0383a4c8b8d655b88d3b5a738~mv2.png",
    "hero-1.jpg": "3175e826184c4a068ddd43f2e1253fa7~mv2_d_1800_1200_s_2.jpg",
    "hero-2.jpg": "1a13bd6e6f4a4f2cbacc57dc5ee10c67~mv2.jpg",
    "hero-3.jpg": "3ad08ac5e3f14192ad10c224abab5ef6~mv2_d_1800_1200_s_2.jpg",
    "about-bg.jpg": "cfa81a82fb81419eabefa8afb8a25f60~mv2_d_1800_1200_s_2.jpg",
    "services-bg.jpg": "2f39dc87e39840c597ec48df519e68b3~mv2_d_1800_1200_s_2.jpg",
    "contact-bg.jpg": "038d51c3ce8b4f9c9d111686deb26b83~mv2_d_1800_1200_s_2.jpg",
    "team-martin.png": "92513d60ec124114b2b5b7aa1fd6d9db~mv2.png",
    "icon-1-analysis.png": "099a71688e864c1d953197e56dba4006~mv2.png",
    "icon-2-busqueda.png": "b4ebcf0651c74dbca04630846a9315c9~mv2.png",
    "icon-3-duediligence.png": "80bb9309340c4e37a46804f7c3721ac5~mv2.png",
    "icon-4-society.png": "e3e228fa75a24362b6735f3f3b69cd42~mv2.png",
    "icon-5-assetmgmt.png": "8ef7e84db2c14d3ebef98fe6959d9e9d~mv2.png",
}

PROJ = ["02abb9adae9c4ecd8b845185a933d0b7~mv2.jpg", "24f4ed977b4649cca61a681ac8f3bcc2~mv2.png",
        "68dfdfd8a2154e0b99dfdb656bd0d9c4~mv2.png", "de39516c08304fc5940b9fd67aba0c5b~mv2.png",
        "4c4bc23738d94b038abf5df6eca546d3~mv2.png", "791b4cf8918d4a1e9ca31a69976ff655~mv2.jpeg",
        "df20991c4e69472f902e87b9ee29ed68~mv2.png", "eec4b529310241dbbf3f00c03b3ff1df~mv2.jpg",
        "7dc0667667da408c8df4e4da534981ac~mv2.png", "beaaf2319a56442bb700046cde7deb8b~mv2.jpg",
        "74ffc60cda7a478bb9d08ff8f962e18c~mv2.jpg", "72389dabefd24d11a16ae1b63a751ed3~mv2.jpg",
        "1909f46227a544e5a67f51ea21ead7e3~mv2.png", "f6d5267b1b804bc99b14397cb30c00dd~mv2.png",
        "1102be894f344a88b9065e3abfa3fa3f~mv2.png", "dcc1cae4d067486c8f327495bf1ebdd2~mv2.jpg",
        "8e5474bb294144ffa0693c7624638363~mv2.jpeg", "ec9a0a8be1424a9d831f049b22f2d79f~mv2.png",
        "77dfbf50458a4518afe1ae04dec4e47d~mv2.jpg", "affe09958c1242009cb6328a6db95d74~mv2.png",
        "7332a48cf7b44034902be64e88942bc7~mv2.jpg", "eb2c411836824f53a386212949edbd06~mv2.png",
        "10f1d99129bc471bb3942b074cd0bee9~mv2.png", "f25cd70170c4480fa09e004d628fd410~mv2.jpg",
        "73dec31b30c346a0a13d626eb67db046~mv2.jpg"]

for i, mid in enumerate(PROJ):
    MAP["proj-%02d.%s" % (i + 1, mid.split(".")[-1])] = mid


def build(src, out):
    with open(src, encoding="utf-8") as fh:
        html = fh.read()
    css = open(os.path.join(ROOT, "assets/css/style.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "assets/js/main.js"), encoding="utf-8").read()

    html = re.sub(r'<link rel="stylesheet" href="[^"]*">', "<style>%s</style>" % css, html)
    html = re.sub(r'<script src="[^"]*main\.js" defer></script>', "<script>%s</script>" % js, html)

    for name, mid in MAP.items():
        html = html.replace("assets/img/" + name, CDN + mid)
        html = html.replace("../assets/img/" + name, CDN + mid)

    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("escrito:", out, len(html), "bytes")


build(os.path.join(ROOT, "index.html"), os.path.join(ROOT, "_build", "preview-es.html"))
build(os.path.join(ROOT, "en", "index.html"), os.path.join(ROOT, "_build", "preview-en.html"))
