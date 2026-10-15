# CLAUDE.md — Web nueva J&H Ingenieros

Sitio **HTML estático bilingüe (ES/EN)** que reemplaza el WordPress de https://www.jyhingenieros.com.
Cliente: J&H Ingenieros, SRL (Santo Domingo, R.D.). Desarrollo: Erick Hernández Arias.

- Repositorio: https://github.com/erickherndza/jyhingenieros (rama `main`)
- Demo para el cliente (GitHub Pages): https://erickherndza.github.io/jyhingenieros/ (EN: `/en/`)
- Se republica sola con cada `git push` a `main` (1–3 min).

## Estado

Fase actual: **el cliente valida el diseño**. No tocar el formulario ni el número de WhatsApp hasta que apruebe.

## Cómo está hecho

Las páginas HTML **se generan**; no se editan a mano (se sobrescriben al regenerar).

| Ruta | Qué es |
|---|---|
| `_data/projects.json` | Fuente de verdad de los 47 proyectos (título/descripción ES y EN, subservicios, imágenes, destacado) |
| `_build/build.py` | Genera las 150 páginas (ES en raíz, EN en `en/`). Contiene plantilla, menú, pie y diccionario `EN` de la interfaz |
| `_build/agregar_proyecto.py` | Asistente para sumar un proyecto nuevo y regenerar |
| `_build/LEEME.md` | Instrucciones de mantenimiento |
| `assets/css/style.css`, `assets/js/main.js` | Estilos y JS (no generados; se editan directo) |
| `assets/img/{gallery,clients,services,sub}` | Imágenes |

Las carpetas con `_` no las publica GitHub Pages (el código no queda expuesto).

### Flujo habitual

```
python3 _build/agregar_proyecto.py          # nuevo proyecto (pregunta título, texto, subservicios, fotos)
python3 _build/build.py                     # regenerar tras editar datos/plantilla
git add -A && git commit -m "..." && git push
```

Cambios de **diseño**: editar `assets/css/style.css` (no requiere regenerar).
Cambios de **textos, menú, pie, teléfono, traducciones**: editar `_build/build.py` y regenerar.
`build.py` agrega `?v=<hash>` al CSS/JS para forzar recarga en navegadores con caché.

## Estructura del sitio (replica la del WordPress original)

Servicios → servicio → subservicio (lista de proyectos) → página de proyecto (galería + descripción).
**No existe una página general "Proyectos"** (decisión del cliente/estructura original).

- Servicios: Edificaciones · Aeropuertos y obras viales · Obras marinas · Planificación y control.
- Cada proyecto se asigna a uno o más subservicios con `subservicios` (slugs) en el JSON.
- Subservicios sin proyectos (Puentes, Marinas y muelles, Dragados) muestran "Próximamente…".
- Páginas: `index`, `nosotros`, `servicios`, `servicio-*`, `servicio-*-<sub>`, `proyecto-<slug>`, `clientes`, `contacto`.

## Decisiones de diseño y reglas

- **Apariencia:** inspirada en el template Builto (ThemeForest) **sin copiar su código** (es de pago; solo se tomó la estructura visual).
- **Colores (medidos del logo):** azul `#3c5478`, dorado `#b49048`. Variables en `:root` de `style.css`.
- **Tipografía (pedido explícito del cliente, "muy quisquillosos"):** Montserrat.
  **Black 900** = títulos (`h1`, `h2`), **Bold 700** = subtítulos/menú/botones (`h3`, `h4`), **Regular 400** = texto. No introducir otras fuentes ni pesos.
- **Logo:** `assets/img/logo.png` (480×283, idéntico al del sitio original). Cabecera con fondo blanco, 124 px en escritorio, 98/92 px en móvil. Pie: mismo logo sobre recuadro blanco.
- **Header/footer incluidos en cada página (HTML completo), NO por JS.** Cargarlos con JS perjudica SEO/GEO (rastreadores de IA y muchos bots no ejecutan JS). Si algún día el hosting soporta PHP/SSI se podría pasar a includes de servidor.
- **Móvil:** correo y teléfono en una sola línea; idioma y redes debajo. Títulos se escalan con `calc((100vw - 56px)/11.8)` para que "CONSTRUCCIÓN" no desborde.
- **Idioma:** selector ES/EN en la barra superior, con `hreflang` alternos. Las traducciones al inglés **las escribió Claude** (no se tomaron del sitio viejo, que era traducción automática mezclada); deben validarse con el cliente.
- **Copyright del pie** (texto fijado por Erick): "© 2026 JYH Ingenieros es una empresa especialista en la elaboración de presupuestos de proyectos de construcción para República Dominicana y el Caribe. Todos los derechos reservados. Diseño y desarrollo — Erick Hernández Arias" (nombre enlaza a https://www.erickhernandezarias.net/).
- Botón flotante de WhatsApp en todas las páginas (mensaje precargado ES/EN).

## Datos del cliente

- Dirección: José Amado Soler 33, Condominio Roshanna, Suite 4D, Serrallés, Sector Piantini, Santo Domingo, R.D., 10125
- Tel: (809) 473-4992 · Email: info@jyhingenieros.com
- Horario: L-V 8:00–17:00, Sáb 8:00–12:00
- Redes: facebook.com/jyhingenieros.srl · instagram.com/jyhingeniero.srl
- Se eliminaron de la lista de "Ejemplos" (por pedido del cliente): Resumen General de Presupuesto, Presupuesto Detallado, Análisis de Precios Unitarios y Estado de Mediciones, Tabla de Cuantías de Acero y Cálculo de Encofrados.

## Pendientes

1. **Formulario de contacto**: `action="FORM_ENDPOINT"` en `build.py`; falta conectarlo (Formspree / Web3Forms). Esperar validación del cliente.
2. **WhatsApp**: `WA_NUMBER` usa el fijo (809) 473-4992; conseguir el número real.
3. **Años de experiencia**: el sitio viejo decía 25, 30 y 35; la banda de cifras muestra "35+". El cliente debe fijar uno.
4. **Imágenes**: ~42 MB; optimizar (redimensionar/comprimir) antes de publicar. Varias fotos de servicio traen un recuadro oscuro incrustado (viene en el JPG original). Pedir fotos limpias.
5. **Logo** de solo 480 px: pedir SVG/PNG grande para que se vea nítido.
6. **Fuente del logo**: Montserrat es la coincidencia más cercana; confirmar la original con el diseñador.
7. **Demo pública**: agregar `noindex` mientras sea demo; al aprobar, apuntar el dominio y crear **redirecciones 301** desde las URLs viejas de WordPress (`/es_es/...`, `/archivos/project/...`).
8. **Proyectos con poco contenido**: varias descripciones son de una línea (es todo lo que existía). Un proyecto no tiene foto ("Licitación … Almacén de Muebles del Este").
9. Revisar con el cliente: grafía "Las Cañas" vs "Las Canas" y los títulos de proyectos traducidos.

## Datos extraídos del sitio original — trampas conocidas

- El sitio viejo bloquea `curl` sin User-Agent (ModSecurity, 406). Con un UA de navegador responde 200.
- Las URLs viejas usan `/es_es/` y `/en_us/` (TranslatePress). Los proyectos eran `/archivos/project/<slug>` con categorías `fw-portfolio-category-*`.
- Los proyectos venían duplicados (uno por categoría); se fusionaron (58 → 47) y se corrigieron erratas ("Aeropuero", "Mercedez", "Auditaría", "Residenses").
- El WordPress es editable en `/wp-admin` (constructor Unyson). La lista "Ejemplos" estaba en la página Home (ID 1701).

## Convenciones de trabajo

- Comunicación con Erick en **español**.
- Commits con la línea `Co-Authored-By: Claude …` indicada por el entorno.
- Probar cambios visuales en local (`python3 -m http.server`) y recargar con CSS nuevo; el navegador cachea el CSS (la demo usa `?v=hash`).
- GitHub Pages tarda 1–3 min en reflejar un push; verificar con `gh api repos/erickherndza/jyhingenieros/pages/builds/latest`.
- Al empujar, si falla con HTTP 400: `git config http.postBuffer 524288000`.
