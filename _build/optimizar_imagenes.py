#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reduce el peso de las imágenes del sitio sin cambiar cómo se ve.

Parte SIEMPRE de las originales en _build/originales/ (no de las ya optimizadas),
así se puede correr las veces que haga falta sin degradar la calidad.

Qué hace:
  * Achica cada imagen al tamaño en el que realmente se muestra (x2 para pantallas
    retina). No tiene sentido bajar 1800 px para mostrarlos a 380.
  * Genera una versión WebP al lado de cada JPEG. El HTML usa <picture>: el navegador
    elige WebP si lo soporta y JPEG si no.
  * Recorta la foto del equipo al círculo que se ve, en vez de bajar la foto entera.

Uso:  python3 _build/optimizar_imagenes.py
"""
import os
import shutil
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, "_build", "originales")
DEST = os.path.join(ROOT, "assets", "img")

# ancho máximo por tipo de imagen (ya contemplando pantallas retina)
REGLAS = [
    ("hero-",     1440, 70, True),   # foto a pantalla completa
    ("about-bg",  1280, 64, False),  # fondo: va detrás de un panel oscuro
    ("services-bg", 1280, 64, False),
    ("contact-bg", 1280, 64, False),
    ("proj-",      700, 76, True),   # miniatura de la galería (~350 px)
    ("lb/",        850, 76, False),  # foto del carrusel de la ventana emergente
]

# La foto del equipo se ve dentro de un círculo de 141 px. En vez de bajar la foto
# entera de 500x920, se recorta exactamente el pedazo visible.
AVATAR = {
    "archivo": "team-martin.png",
    "recorte": (104, 55, 489, 443),   # calculado del encuadre que hacía Wix
    "salida": 300,
}


def regla(rel):
    for pref, ancho, q, webp in REGLAS:
        if rel.startswith(pref) or os.path.basename(rel).startswith(pref):
            return ancho, q, webp
    return None


def guardar_jpeg(im, destino, q):
    im.convert("RGB").save(destino, "JPEG", quality=q, optimize=True,
                           progressive=True, subsampling=2)


def procesar():
    total_antes = total_despues = 0
    n_webp = 0

    for base, _, archivos in os.walk(ORIG):
        for nombre in sorted(archivos):
            src = os.path.join(base, nombre)
            rel = os.path.relpath(src, ORIG).replace("\\", "/")
            dst = os.path.join(DEST, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            total_antes += os.path.getsize(src)

            if nombre == AVATAR["archivo"]:
                im = ImageOps.exif_transpose(Image.open(src))
                im = im.crop(AVATAR["recorte"])
                lado = AVATAR["salida"]
                im = im.resize((lado, lado), Image.LANCZOS)
                jpg = os.path.splitext(dst)[0] + ".jpg"
                guardar_jpeg(im, jpg, 84)
                im.convert("RGB").save(os.path.splitext(dst)[0] + ".webp",
                                       "WEBP", quality=82, method=6)
                total_despues += os.path.getsize(jpg)
                n_webp += 1
                print("  recortado  %-22s %5d KB" % (rel, os.path.getsize(jpg) / 1024))
                continue

            r = regla(rel)
            if r is None:                       # íconos, logo: se copian tal cual
                shutil.copy2(src, dst)
                total_despues += os.path.getsize(dst)
                continue

            ancho, q, hacer_webp = r
            im = ImageOps.exif_transpose(Image.open(src))
            if im.width > ancho:
                alto = round(im.height * ancho / im.width)
                im = im.resize((ancho, alto), Image.LANCZOS)

            guardar_jpeg(im, dst, q)
            total_despues += os.path.getsize(dst)

            if hacer_webp:
                w = os.path.splitext(dst)[0] + ".webp"
                im.convert("RGB").save(w, "WEBP", quality=q, method=6)
                n_webp += 1

    print("\nantes:   %6.2f MB" % (total_antes / 1048576))
    print("después: %6.2f MB  (+ %d archivos WebP)" % (total_despues / 1048576, n_webp))


if __name__ == "__main__":
    if not os.path.isdir(ORIG):
        raise SystemExit("Falta %s (las imágenes originales sin tocar)." % ORIG)
    procesar()
