# Cómo mantener el sitio

Las páginas HTML **se generan** desde una plantilla y un archivo de datos. No las edites a mano:
se sobrescriben al regenerar.

## Estructura

| Ruta | Qué es |
|---|---|
| `_data/projects.json` | Todos los proyectos (título, descripción ES/EN, subservicios, imágenes, destacado) |
| `_build/build.py` | Genera las 150 páginas (ES en la raíz, EN en `en/`) |
| `_build/agregar_proyecto.py` | Asistente para agregar un proyecto nuevo |
| `assets/img/gallery/` | Fotos de los proyectos |
| `assets/img/clients/` | Logos de clientes (cualquier imagen nueva aparece sola en Clientes) |

Requisito: Python 3 (no necesita instalar nada más).

## Agregar un proyecto (cada mes)

```
python3 _build/agregar_proyecto.py
```

Responde las preguntas (título, descripción, subservicios, imágenes). El script copia las
fotos, actualiza `_data/projects.json` y regenera todas las páginas. Luego:

```
git add -A && git commit -m "Nuevo proyecto: NOMBRE" && git push
```

## Editar o quitar un proyecto

Abre `_data/projects.json`, cambia o borra su bloque y ejecuta `python3 _build/build.py`.

- `subservicios`: lista de identificadores (p. ej. `"villas"`, `"auditoria"`). Un proyecto puede tener varios.
- `destacado: true` lo muestra en la home.
- `imagenes`: la primera es la portada.

## Cambiar textos generales (teléfono, pie, menú, traducciones)

Están en `_build/build.py` (arriba: teléfono, correo, WhatsApp `WA_NUMBER`; después, el
diccionario `EN` con las traducciones de la interfaz). Edita y ejecuta `python3 _build/build.py`.

## Pendiente de configurar

- `FORM_ENDPOINT` en el formulario de contacto (Formspree, Web3Forms…).
- `WA_NUMBER` con el número real de WhatsApp.
