# Tango Holding — sitio web

Réplica estática del sitio de Tango Holding que estaba en Wix, hecha en HTML, CSS y
JavaScript puros. Sin frameworks, sin build obligatorio, sin dependencias.

---

## PASO 0 — Poner las imágenes (hacelo primero)

La carpeta `assets/img/` viene **vacía** porque las 38 imágenes (46 MB) se descargaron
aparte, directamente desde el CDN de Wix, en un archivo llamado **`tango-assets.zip`**
que quedó en tu carpeta de **Descargas**.

1. Descomprimí `tango-assets.zip`.
2. Copiá los 38 archivos **adentro de `assets/img/`**.

Tiene que quedar así:

```
assets/img/logo.png
assets/img/hero-1.jpg   hero-2.jpg   hero-3.jpg
assets/img/about-bg.jpg  services-bg.jpg  contact-bg.jpg
assets/img/team-martin.png
assets/img/icon-1-analysis.png … icon-5-assetmgmt.png
assets/img/proj-01.jpg … proj-25.jpg
```

Para ver el sitio en tu compu antes de publicarlo, abrí `index.html` con doble clic.
(El formulario solo funciona una vez publicado en Netlify.)

---

## Cómo publicarlo en Netlify (5 minutos)

### 1. Subir el código a GitHub

1. Entrá a <https://github.com/new> y creá un repositorio (por ejemplo `tangoholding-web`).
   Puede ser privado.
2. Subí todo el contenido de esta carpeta. La forma más simple es arrastrar los archivos
   a la pantalla *"uploading an existing file"* de GitHub.

> Si preferís la consola:
> ```bash
> git init
> git add .
> git commit -m "Sitio Tango Holding"
> git branch -M main
> git remote add origin https://github.com/TU-USUARIO/tangoholding-web.git
> git push -u origin main
> ```

### 2. Conectar Netlify

1. Entrá a <https://app.netlify.com> → **Add new site** → **Import an existing project**.
2. Elegí GitHub y seleccioná el repositorio.
3. Dejá la configuración como viene (`netlify.toml` ya trae todo):
   - **Build command**: vacío
   - **Publish directory**: `.`
4. **Deploy**. En menos de un minuto tenés el sitio online en una URL `*.netlify.app`.

### 3. Activar las notificaciones del formulario

El formulario usa **Netlify Forms** (gratis hasta 100 envíos por mes).

1. En Netlify: **Site configuration** → **Forms** → **Form notifications**.
2. **Add notification** → **Email notification**.
3. Poné `santiago@tangoholding.com` y guardá.

Los mensajes también quedan guardados en el panel de Netlify (**Forms** → `contacto`).

### 4. Conectar el dominio tangoholding.com

> **Importante**: hoy `tangoholding.com` está registrado en Wix y **no está conectado a
> ningún sitio**. Tenés dos caminos:
>
> **A. Dejar el dominio en Wix** y apuntarlo a Netlify cambiando los DNS.
> Sale más barato que el plan Premium de Wix, pero seguís pagando la renovación del
> dominio a Wix.
>
> **B. Transferir el dominio** a otro registrador (Namecheap, Cloudflare, Porkbun).
> Es lo más limpio y lo más barato a largo plazo. Requiere desbloquear el dominio en
> Wix y pedir el código de autorización (EPP).

En cualquiera de los dos casos, en Netlify:

1. **Domain management** → **Add a domain** → `tangoholding.com`.
2. Netlify te da los registros DNS a cargar (o sus nameservers).
3. Cargalos en el panel de dominios de Wix (o del registrador nuevo).
4. El certificado HTTPS lo emite Netlify solo, gratis.

---

## Estructura

```
.
├── index.html            Home en español
├── en/index.html         Home en inglés
├── assets/
│   ├── css/style.css     Todos los estilos
│   ├── js/main.js        Slideshow, menú, galería, formulario
│   └── img/              Todas las imágenes (38 archivos)
├── reportes2q-2023.html … reportes2q-2026.html   Reportes trimestrales (13)
├── juankeser-*.html      Área de reportes juankeser (8)
├── favicon.svg
├── netlify.toml          Configuración de Netlify (redirects, cache, headers)
├── robots.txt
├── sitemap.xml
└── _build/               Herramientas internas (no se publica nada crítico)
    ├── content.py         TODO el texto de la home, en un solo lugar
    ├── build.py           Regenera index.html y en/index.html
    ├── reportes.json      Los 225 links a reportes, por trimestre y por fondo
    ├── build_reportes.py  Regenera las 21 páginas de reportes
    └── preview.py         Genera una copia autocontenida para previsualizar
```

---

## El área de reportes para inversores

Las páginas `/reportes3q-2023` … `/reportes2q-2026` y `/juankeser-*` replican **exactamente
los mismos paths** que tenían en Wix. Eso es lo que hace que los links dentro de los PDFs
que ya circulan entre los inversores vuelvan a funcionar.

**No cambies esos nombres de archivo.** Si renombrás `reportes2q-2026.html`, rompés todos
los PDFs que ya mandaste.

### Los links dentro de los PDFs de los inversores

Los reportes que se le mandan a cada inversor llevan links con esta forma:

```
https://www.tangoholding.com/_files/ugd/405a64_<archivo>.pdf
```

Esa era la URL pública que Wix le daba a cada archivo cuando el dominio estaba conectado.
`netlify.toml` tiene una regla que redirige `/_files/ugd/*` al lugar donde los PDFs viven
hoy. **Esa regla no se toca ni se borra**: sin ella, todos los links de los reportes ya
enviados dan 404.

La ventaja de que apunten a `tangoholding.com` y no directo a Wix es que el destino lo
controlás vos: si algún día mudás los PDFs a otro servidor, cambiás la dirección de `to`
en esa regla y listo. Los PDFs que ya están en la calle siguen funcionando.

### Dónde están los archivos PDF

Los 172 reportes (525 MB) **siguen alojados en Wix**, en
`6737a04c-….filesusr.com/ugd/…`. Las páginas nuevas linkean ahí.

Por eso: **no borres el sitio de Wix.** Dejalo en plan Free (no cuesta nada). El día que
lo borres, los 172 links mueren.

Para mudar los PDFs a un servidor propio más adelante, cambiá `PDF_BASE` en
`_build/build_reportes.py` y regenerá las páginas.

### Agregar un trimestre nuevo

1. Editá `_build/reportes.json` copiando el bloque del trimestre anterior.
2. Cambiá el título, el trimestre y los links a los PDFs nuevos.
3. `python3 _build/build_reportes.py`

Estas páginas llevan `noindex` y `Disallow` en robots.txt: se llega por link directo,
pero Google no las indexa.

---

## Cómo editar el contenido

### Cambios chicos

Editá `index.html` (español) o `en/index.html` (inglés) directamente. Son archivos HTML
comunes y corrientes.

### Cambios que afectan a los dos idiomas

Editá `_build/content.py` — ahí están los textos, los servicios y la lista completa de
proyectos — y después regenerá las dos páginas:

```bash
python3 _build/build.py
```

### Agregar o cambiar un proyecto

1. Poné la imagen nueva en `assets/img/` (por ejemplo `proj-26.jpg`).
2. Agregá la entrada en la lista `PROJECTS` de `_build/content.py`:
   ```python
   ("proj-26.jpg", "NOMBRE DEL PROYECTO", "CIUDAD, ESTADO",
    ["Multifamily Project", "Ground Up Development", "300 Unidades &amp; Amenities"],
    ["Multifamily Project", "Ground Up Development", "300 Units &amp; Amenities"]),
   ```
   La primera lista es el texto en español, la segunda en inglés.
3. Corré `python3 _build/build.py`.
4. Subí los cambios a GitHub. Netlify vuelve a publicar solo.

---

## Diferencias respecto al sitio de Wix

Cosas que cambiaron, y por qué:

| Tema | Wix | Acá |
|---|---|---|
| Tipografías | Lulo Clean y Avenir (con licencia de Wix) | **Montserrat** y **Mulish** (Google Fonts, libres). Son las alternativas libres más parecidas; la licencia de Wix no se puede llevar a otro hosting. |
| Formulario | Wix Forms | Netlify Forms, mismo comportamiento (mensaje de gracias sin recargar la página) |
| Proyectos en inglés | La galería aparecía **vacía** en la versión en inglés (un bug del sitio actual) | Se ven los 25 proyectos en los dos idiomas |
| Idiomas | `?lang=en` | `/en/` — mejor para SEO. `netlify.toml` redirige las URLs viejas |
| Peso | ~5 MB de JavaScript de Wix | ~25 KB de CSS + JS propios |

**Ya replicado:** las 21 páginas del área de inversores (12 trimestres de reportes +
8 páginas del área juankeser), con 225 links a reportes y los mismos paths que Wix.

**Ventanas emergentes de proyecto:** al hacer clic en un proyecto de la galería se abre
una ventana con el título, la ubicación, la descripción y las fotos — igual que en Wix.
El diseño, el comportamiento y el marcado ya están hechos; los datos van en
`_build/lightboxes.json` y las fotos en `assets/img/lb/`.

**Pendiente:** las 25 páginas de las propiedades de Houston (Westgate, Panera,
Applebee's, 3 Parcels, Inline y sus subpáginas de inquilinos, números, ubicación y
contacto).

---

## Antes de dar de baja Wix

- [ ] El sitio nuevo está publicado y `tangoholding.com` apunta ahí
- [ ] Llega un mail de prueba del formulario
- [ ] Descargaste las páginas de inversores que quieras conservar (siguen solo en Wix)
- [ ] Resolviste qué hacer con el dominio (transferirlo o dejarlo en Wix)

---

## Falta una imagen suelta

`assets/img/rep-hero.jpg` es la foto de portada de las páginas de reportes. No pudo
descargarse automáticamente (Chrome bloquea las descargas seguidas). Bajala de acá y
guardala con ese nombre exacto dentro de `assets/img/`:

https://static.wixstatic.com/media/405a64_a1224dc8d97e4858b2d05e6d1db96cec~mv2.jpg

Si no la ponés, las páginas de reportes funcionan igual: el hero queda con fondo azul
oscuro en vez de la foto.
