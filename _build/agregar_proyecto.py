#!/usr/bin/env python3
"""Agrega un proyecto nuevo al sitio y regenera todas las páginas (ES + EN).

Uso:   python3 _build/agregar_proyecto.py
Pide: título, descripción, subservicio(s), imágenes. Escribe en _data/projects.json,
copia las imágenes a assets/img/gallery/ y ejecuta _build/build.py.
"""
import ast, json, os, re, shutil, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, '_data', 'projects.json')
GALLERY = os.path.join(ROOT, 'assets', 'img', 'gallery')


def servicios():
    """Lee SERVICES desde build.py para ofrecer la lista de subservicios."""
    src = open(os.path.join(ROOT, '_build', 'build.py'), encoding='utf8').read()
    ns = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'SERVICES':
            exec(ast.get_source_segment(src, n), ns)
    return ns['SERVICES']


def slugify(t):
    t = unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:70].strip('-')


def ask(msg, required=True, default=None):
    while True:
        v = input(msg + (f' [{default}]' if default else '') + ': ').strip()
        if not v and default is not None:
            return default
        if v or not required:
            return v
        print('  Este dato es obligatorio.')


def main():
    projects = json.load(open(DATA, encoding='utf8'))
    taken = {p['slug'] for p in projects}

    print('\n== Nuevo proyecto ==')
    titulo = ask('Título en español')
    titulo_en = ask('Título en inglés (Enter = igual al español)', required=False) or titulo
    slug = slugify(titulo)
    if slug in taken:
        sys.exit(f'Ya existe un proyecto con el nombre "{slug}". Usa un título distinto.')

    print('\nDescripción en español (una línea por párrafo; línea vacía para terminar):')
    desc = []
    while True:
        l = input('  > ').strip()
        if not l:
            break
        desc.append(l)
    print('Descripción en inglés, mismo orden (línea vacía para terminar; Enter directo = repetir el español):')
    desc_en = []
    while True:
        l = input('  > ').strip()
        if not l:
            break
        desc_en.append(l)
    if not desc_en:
        desc_en = list(desc)
        if desc:
            print('  (aviso: se usará el texto en español en la página en inglés)')

    print('\nSubservicios disponibles:')
    opciones = []
    for sk, sv in servicios().items():
        print(f'  {sv["title"]}')
        for n, img, s, cats in sv['items']:
            opciones.append(s)
            print(f'    {len(opciones):2d}. {n}')
    sel = ask('Números separados por coma (puede ser más de uno)')
    subs = []
    for x in re.split(r'[,\s]+', sel):
        if x.isdigit() and 1 <= int(x) <= len(opciones):
            subs.append(opciones[int(x) - 1])
    if not subs:
        sys.exit('No elegiste ningún subservicio válido.')

    print('\nImágenes: arrastra los archivos a la terminal o pega sus rutas (la primera es la portada).')
    raw = ask('Rutas', required=False)
    paths = [p.replace('\\ ', ' ').strip("'\"") for p in re.findall(r"(?:'[^']+'|\"[^\"]+\"|(?:\\ |\S)+)", raw)]
    imgs = []
    for i, p in enumerate(paths, 1):
        p = os.path.expanduser(p)
        if not os.path.isfile(p):
            print(f'  ! no existe: {p}')
            continue
        ext = os.path.splitext(p)[1].lower()
        dst = f'{slug}-{i}{ext}'
        shutil.copy2(p, os.path.join(GALLERY, dst))
        imgs.append('assets/img/gallery/' + dst)

    dest = ask('¿Mostrar en "Proyectos destacados" de la home? (s/n)', default='n').lower().startswith('s')

    projects.append({'slug': slug, 'titulo': titulo, 'titulo_en': titulo_en, 'descripcion': desc,
                     'descripcion_en': desc_en, 'subservicios': subs, 'imagenes': imgs, 'destacado': dest})
    json.dump(projects, open(DATA, 'w', encoding='utf8'), ensure_ascii=False, indent=2)
    print(f'\nProyecto "{titulo}" agregado ({len(imgs)} imágenes). Regenerando el sitio…')
    subprocess.run([sys.executable, os.path.join(ROOT, '_build', 'build.py')], check=True)
    print('\nListo. Revisa los cambios y súbelos:\n  git add -A && git commit -m "Nuevo proyecto: %s" && git push' % titulo)


if __name__ == '__main__':
    main()
