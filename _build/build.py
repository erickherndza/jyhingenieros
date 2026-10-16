import json, html, re, os, urllib.parse
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raíz del sitio
P = json.load(open(OUT + '/_data/projects.json', encoding='utf8'))
e = html.escape

SITE = 'J&H Ingenieros'
TEL = '(809) 473-4992'
TEL_HREF = 'tel:+18094734992'
WA_NUMBER = '18094734992'   # CONFIGURAR: número de WhatsApp con código de país, sin + ni espacios
MAIL = 'info@jyhingenieros.com'
FB = 'https://www.facebook.com/jyhingenieros.srl'
IG = 'https://www.instagram.com/jyhingeniero.srl/'
MAP = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d946.0222565466133!2d-69.93485093410553!3d18.479626211854093!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xcf896c22d54af0a1!2sJ%26H+Ingenieros%2C+SRL.!5e0!3m2!1sen!2sdo!4v1501467328005'

# ---------------- traducciones (clave = texto en español) ----------------
EN = {
 # navegación / chrome
 'Inicio': 'Home', 'Nosotros': 'About us', 'Servicios': 'Services', 'Proyectos': 'Projects', 'Clientes': 'Clients', 'Contacto': 'Contact',
 'Contáctenos': 'Contact us', 'Saltar al contenido': 'Skip to content', 'Abrir menú': 'Open menu', 'Principal': 'Main',
 'Serrallés, Piantini · Santo Domingo, R.D.': 'Serrallés, Piantini · Santo Domingo, D.R.',
 'Ingeniería de servicios completos: construcción, planificación y control en República Dominicana y el Caribe.': 'Full-service engineering: construction, planning and control in the Dominican Republic and the Caribbean.',
 'Navegación': 'Navigation',
 'Edificaciones': 'Buildings', 'Aeropuertos y obras viales': 'Airports and road works', 'Obras marinas': 'Marine works',
 'Planificación y control': 'Planning and control',
 'Obras viales y aeroportuarias': 'Road and airport works',
 '© {SITE}, SRL. Todos los derechos reservados.': '© {SITE}, SRL. All rights reserved.',
 'L-V 8:00–17:00 · Sáb 8:00–12:00': 'Mon–Fri 8:00 am–5:00 pm · Sat 8:00 am–12:00 pm',
 'José Amado Soler 33, Condominio Roshanna, Suite 4D, Serrallés, Sector Piantini, Santo Domingo, República Dominicana, 10125':
   'José Amado Soler 33, Condominio Roshanna, Suite 4D, Serrallés, Sector Piantini, Santo Domingo, Dominican Republic, 10125',
 '¿Tiene un proyecto en mente?': 'Have a project in mind?', 'Solicitar información': 'Request information',
 # home
 'J&H Ingenieros | Construcción e ingeniería de servicios completos en Santo Domingo': 'J&H Ingenieros | Construction and full-service engineering in Santo Domingo',
 'J&H Ingenieros: empresa de ingeniería de servicios completos en Santo Domingo. Construcción de obras civiles y marinas, planificación, presupuestos, control de costos y supervisión.':
   'J&H Ingenieros: full-service engineering company in Santo Domingo. Construction of civil and marine works, planning, budgeting, cost control and supervision.',
 'Empresa de ingeniería de servicios completos': 'Full-service engineering company',
 'Construcción de obras civiles, hoteleras y marinas, con planificación, presupuestos, control de costos y supervisión, en República Dominicana y el Caribe.':
   'Construction of civil, hotel and marine works, backed by planning, budgeting, cost control and supervision, in the Dominican Republic and the Caribbean.',
 '01. Especialidades': '01. Specialties', '02. Quiénes somos': '02. Who we are', '03. Nuestros servicios': '03. Our services',
 '04. Proyectos': '04. Projects', '05. Misión, visión y valores': '05. Mission, vision and values', '06. Descargas': '06. Downloads',
 'Ver todos': 'View all', 'Construimos y supervisamos hoteles, villas, aeropuertos y obras marinas, con control de costos y de calidad en cada fase del proyecto.': 'We build and supervise hotels, villas, airports and marine works, with cost and quality control at every stage of the project.', 'Presupuestos, planificación, auditoría y tasaciones para decidir con certeza antes y durante la ejecución de la obra.': 'Budgeting, planning, audit and appraisals to make decisions with certainty before and during construction.', 'Nuestros servicios': 'Our services', 'Anterior': 'Previous', 'Siguiente': 'Next', 'Conózcanos': 'Learn more about us',
 'Una empresa de ingeniería de servicios completos: planificamos, controlamos y construimos': 'A full-service engineering company: we plan, control and build',
 'Somos una empresa de ingeniería de servicios completos: planificación, control y construcción. Con más de 25 años de ejercicio continuo en la República Dominicana, construimos y damos servicio a importantes empresas de los sectores inmobiliario, hotelero turístico y de transporte aéreo (aeropuertos, helipuertos, hangares); así como para grandes proyectos marinos y viales.':
   'We are a full-service engineering company: planning, control and construction. With more than 25 years of continuous practice in the Dominican Republic, we build for and serve major companies in the real estate, tourism and hotel, and air transport sectors (airports, heliports, hangars), as well as large marine and road projects.',
 'Construcción de obras civiles, hoteleras y marinas': 'Construction of civil, hotel and marine works',
 'Presupuestos y control de costos': 'Budgeting and cost control',
 'Supervisión y administración de obras': 'Construction supervision and administration',
 'Auditoría de proyectos y tasaciones': 'Project audits and appraisals',
 'Experiencia que construye confianza': 'Experience that builds trust',
 'Nuestra experiencia profesional ha sido en la construcción de proyectos hoteleros, civiles, viales, hidráulicas y marinos. Así como en la Supervisión y Administración de la Construcción de Proyectos; Asesoría en Costos de proyectos de construcción en República Dominicana y Presupuestos, Planificación, Control de Costos, Auditoria de Proyectos en cualquier fase de ejecución y Tasaciones.':
   'Our professional experience has been in the construction of hotel, civil, road, hydraulic and marine projects, as well as in the supervision and administration of project construction; cost advisory for construction projects in the Dominican Republic; and budgeting, planning, cost control, project audits at any stage of execution, and appraisals.',
 'Misión': 'Mission', 'Visión': 'Vision', 'Valores': 'Values',
 'Desarrollar importantes proyectos en el país que nos hacen acreedores de la confianza de nuestros clientes.':
   'To develop important projects in the country that earn us the trust of our clients.',
 'Convertirnos en un marco de referencia en la Industria Constructora, siendo distinguidos por nuestras innovaciones y altos niveles de calidad, entrega a tiempo y precio competitivo.':
   'To become a benchmark in the construction industry, distinguished by our innovation and high standards of quality, on-time delivery and competitive pricing.',
 'Economía • Tiempo • Credibilidad • Compromiso • Calidad • Trabajo en equipo • Cumplimiento en excelencia.':
   'Economy • Time • Credibility • Commitment • Quality • Teamwork • Excellence in delivery.',
 'Perfil de la Empresa': 'Company Profile', 'Diseño Estructural': 'Structural Design', 'Diseño Eléctrico': 'Electrical Design', 'Diseño Sanitario': 'Sanitary Design',
 # stats
 'Años de experiencia': 'Years of experience',
 'En proyectos hoteleros, civiles, viales e hidráulicos en República Dominicana y el Caribe.': 'In hotel, civil, road and hydraulic projects in the Dominican Republic and the Caribbean.',
 'Proyectos en portafolio': 'Projects in portfolio',
 'Presupuestos, supervisión, auditoría y construcción de obras.': 'Budgeting, supervision, audit and construction of works.',
 'Áreas de especialidad': 'Areas of specialty',
 'Edificaciones, obras viales, obras marinas y planificación y control.': 'Buildings, road works, marine works, and planning and control.',
 # nosotros
 'Nosotros | J&H Ingenieros': 'About us | J&H Ingenieros',
 'Conozca a J&H Ingenieros: más de 35 años de experiencia en presupuestos y construcción de proyectos en República Dominicana y el Caribe.':
   'Meet J&H Ingenieros: more than 35 years of experience in project budgeting and construction in the Dominican Republic and the Caribbean.',
 '01. Quiénes somos': '01. Who we are', '02. Especialidades': '02. Specialties', '03. Misión, visión y valores': '03. Mission, vision and values',
 'Nosotros somos J&H Ingenieros': 'We are J&H Ingenieros',
 'JYH Ingenieros es una empresa especialista en la elaboración de presupuestos de proyectos de construcción en Santo Domingo, puntera en el desarrollo de proyectos en la República Dominicana y el Caribe, con más de 35 años de experiencia acumulada en el sector de la construcción de proyectos: hoteleros, turísticos, residenciales, civiles, viales e hidráulicos, diseño y ejecución de playas artificiales, marinas y rompeolas; con trabajos realizados en varios países del Caribe.':
   'JYH Ingenieros is a company specialized in preparing construction project budgets in Santo Domingo, a leader in project development in the Dominican Republic and the Caribbean, with more than 35 years of accumulated experience in the project construction sector: hotel, tourism, residential, civil, road and hydraulic projects, and the design and execution of artificial beaches, marinas and breakwaters, with work carried out in several Caribbean countries.',
 'Descargar perfil': 'Download profile',
 'Resorts hoteleros': 'Hotel resorts', 'Viviendas y villas': 'Houses and villas', 'Estructuras metálicas y ligeras': 'Metal and light structures',
 'Aeropuertos': 'Airports', 'Carreteras': 'Roads', 'Puentes': 'Bridges',
 'Construcción y mantenimiento de playas': 'Beach construction and maintenance', 'Construcción de rompeolas, marinas y muelles': 'Construction of breakwaters, marinas and piers',
 'Dragados hidráulicos y mecánicos': 'Hydraulic and mechanical dredging',
 'Especialidades en planeación y control': 'Specialties in planning and control',
 'Planificación de proyectos': 'Project planning', 'Confección de presupuestos': 'Budget preparation', 'Auditorías a proyectos': 'Project audits',
 'Tasaciones': 'Appraisals', 'Supervisión': 'Supervision',
 # servicios
 'Servicios | J&H Ingenieros': 'Services | J&H Ingenieros',
 'Edificaciones, obras viales y aeroportuarias, obras marinas, planificación y control de proyectos en República Dominicana.':
   'Buildings, road and airport works, marine works, project planning and control in the Dominican Republic.',
 '01. Servicios': '01. Services', 'Construcción, supervisión, costos y control': 'Construction, supervision, costs and control',
 'Construcción, supervisión, asesoría en costos, presupuestos, planificación, control de costos, auditoría y tasaciones, en cualquier fase de ejecución del proyecto.':
   'Construction, supervision, cost advisory, budgeting, planning, cost control, audit and appraisals, at any stage of project execution.',
 'Ver más': 'Learn more', 'Ver proyectos': 'View projects', 'Escríbenos por WhatsApp': 'Chat with us on WhatsApp',
 'Hola, me gustaría recibir información sobre sus servicios.': 'Hello, I would like to receive information about your services.', 'Descripción': 'Description', 'Galería': 'Gallery', 'Más proyectos de': 'More projects in',
 'Volver a': 'Back to', 'Imagen': 'Image', 'Proyecto': 'Project',
 'Próximamente publicaremos proyectos de esta categoría.': 'Projects in this category will be published soon.',
 '02. Otros servicios de': '02. Other services in',
 '04. Proyectos destacados': '04. Featured projects', 'Construcciones': 'Constructions',
 'Construcción de bermas': 'Berm construction', 'Construcción de marinas y muelles': 'Marina and pier construction',
 'Construcción de rompeolas': 'Breakwater construction', 'Construcción de playas': 'Beach construction', 'Mantenimiento de playas': 'Beach maintenance',
 'Viviendas': 'Houses', 'Villas': 'Villas', 'Auditoría': 'Audit', 'Supervisión de proyectos': 'Project supervision',
 '02. Proyectos relacionados': '02. Related projects',
 '{t}: servicios y proyectos de J&H Ingenieros en República Dominicana y el Caribe.': '{t}: services and projects by J&H Ingenieros in the Dominican Republic and the Caribbean.',
 # proyectos
 'Proyectos | J&H Ingenieros': 'Projects | J&H Ingenieros',
 'Portafolio de proyectos de J&H Ingenieros: hoteles, villas, aeropuertos, obras marinas y más.':
   'J&H Ingenieros project portfolio: hotels, villas, airports, marine works and more.',
 '01. Portafolio': '01. Portfolio', 'Todos': 'All', 'Filtrar proyectos': 'Filter projects',
 # clientes
 'Clientes | J&H Ingenieros': 'Clients | J&H Ingenieros', 'Empresas que han confiado en J&H Ingenieros.': 'Companies that have trusted J&H Ingenieros.',
 '01. Nuestros clientes': '01. Our clients', 'Logo de cliente': 'Client logo',
 # contacto
 'Contacto | J&H Ingenieros': 'Contact | J&H Ingenieros',
 'Contacte a J&H Ingenieros en Santo Domingo: (809) 473-4992, info@jyhingenieros.com.': 'Contact J&H Ingenieros in Santo Domingo: (809) 473-4992, info@jyhingenieros.com.',
 '01. Contacto': '01. Contact', 'Hablemos de su proyecto': "Let's talk about your project",
 'Dirección': 'Address', 'Teléfono': 'Phone', 'Correo': 'Email', 'Horario': 'Hours',
 'L-V: 8:00 am a 5:00 pm<br>Sáb: 8:00 am a 12:00 pm': 'Mon–Fri: 8:00 am – 5:00 pm<br>Sat: 8:00 am – 12:00 pm',
 'Nombre': 'Name', 'Correo electrónico': 'Email', 'Asunto': 'Subject', 'Mensaje': 'Message', 'Enviar mensaje': 'Send message',
 'Ubicación de J&H Ingenieros': 'J&H Ingenieros location',
}
# ---------------- datos de proyectos ----------------
GROUPS = {   # clave = servicio; el título se usa como etiqueta en las tarjetas
    'edificaciones': ('Edificaciones',), 'viales': ('Obras viales y aeroportuarias',),
    'marinas': ('Obras marinas',), 'planificacion': ('Planificación y control',),
}
def norm(t): return re.sub(r'\s+', ' ', t).strip().lower()
PROJ = []
for p in sorted(P, key=lambda x: x['titulo'].lower()):
    PROJ.append({'title': p['titulo'], 'title_en': p.get('titulo_en') or p['titulo'], 'slug': p['slug'],
                 'file': p['imagenes'][0] if p.get('imagenes') else None, 'gallery': p.get('imagenes', []),
                 'paras': p.get('descripcion', []), 'paras_en': p.get('descripcion_en', []),
                 'subs': set(p.get('subservicios', [])), 'featured': bool(p.get('destacado')), 'groups': set()})
SERVICES = {
    'edificaciones': dict(file='servicio-edificaciones.html', stem='servicio-edificaciones', title='Edificaciones', img='assets/img/services/edificaciones.jpg',
        items=[('Resorts hoteleros', 'assets/img/sub/resorts-hoteleros.jpg', 'resorts-hoteleros', {'resorts-hoteleros'}),
               ('Viviendas', 'assets/img/sub/viviendas.jpg', 'viviendas', {'viviendas'}),
               ('Villas', 'assets/img/sub/villas.jpg', 'villas', {'villas'}),
               ('Estructuras metálicas y ligeras', 'assets/img/sub/estructuras-metalicas.jpg', 'estructuras-metalicas', {'estructuras-metalicas'}),
               ('Construcciones', None, 'construcciones', {'construcciones', 'construcciones-institucionales'})]),
    'viales': dict(file='servicio-obras-viales.html', stem='servicio-obras-viales', title='Aeropuertos y obras viales', img='assets/img/services/obras-viales.jpg',
        items=[('Aeropuertos', None, 'aeropuertos', {'aeropuertos'}), ('Carreteras', None, 'carreteras', {'carreteras', 'obras-viales'}),
               ('Puentes', None, 'puentes', set())]),
    'marinas': dict(file='servicio-obras-marinas.html', stem='servicio-obras-marinas', title='Obras marinas', img='assets/img/services/obras-marinas.jpg',
        items=[('Construcción de bermas', 'assets/img/sub/bermas.jpg', 'bermas', {'construccion-de-bermas'}),
               ('Construcción de marinas y muelles', 'assets/img/sub/marinas.jpg', 'marinas-y-muelles', set()),
               ('Construcción de rompeolas', 'assets/img/sub/rompeolas.jpg', 'rompeolas', {'construccion-de-rompeolas'}),
               ('Dragados hidráulicos y mecánicos', 'assets/img/sub/dragados.jpg', 'dragados', set()),
               ('Construcción de playas', 'assets/img/sub/playas.jpg', 'playas', {'construccion-de-playas'}),
               ('Mantenimiento de playas', 'assets/img/sub/playas.jpg', 'mantenimiento-de-playas', {'mantenimiento-de-playas'})]),
    'planificacion': dict(file='servicio-planificacion.html', stem='servicio-planificacion', title='Planificación y control', img='assets/img/services/planificacion.jpg',
        items=[('Planificación de proyectos', 'assets/img/sub/planificacion.jpg', 'planificacion-de-proyectos', {'planificacion-de-proyectos'}),
               ('Confección de presupuestos', None, 'confeccion-de-presupuestos', {'confeccion-de-presupuestos', 'presupuestos', 'asesorias', 'licitaciones'}),
               ('Auditoría', 'assets/img/sub/auditoria.jpg', 'auditoria', {'auditoria'}),
               ('Tasaciones', None, 'tasaciones', {'tasaciones'}),
               ('Supervisión de proyectos', 'assets/img/sub/supervision.jpg', 'supervision-de-proyectos', {'supervision-de-proyectos', 'superviciones'})]),
}
SV = list(SERVICES.values())
for _m in PROJ:
    for _k, _sv in SERVICES.items():
        if any(i[2] in _m['subs'] for i in _sv['items']):
            _m['groups'].add(_k)
NAV = [('index.html', 'Inicio'), ('nosotros.html', 'Nosotros'), ('servicios.html', 'Servicios'),
       ('clientes.html', 'Clientes'), ('contacto.html', 'Contacto')]
ADDR = 'José Amado Soler 33, Condominio Roshanna, Suite 4D, Serrallés, Sector Piantini, Santo Domingo, República Dominicana, 10125'

ICON = lambda d, extra='': f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{d}</svg>'
ARROW = '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
I_PIN = ICON('<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>')
I_MAIL = ICON('<rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/>')
I_TEL = ICON('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>')
I_FB = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6.5c0-.7.3-1 1.1-1H17V2h-2.6C11.5 2 10 3.7 10 6.2V8H7.5v3.5H10V22h4V11.5h2.7L17 8z"/></svg>'
I_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
I_DOC = ICON('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M12 11v6m-3-3 3 3 3-3"/>')

import hashlib
def _ver(rel):
    try:
        return hashlib.md5(open(os.path.join(OUT, rel), 'rb').read()).hexdigest()[:8]
    except OSError:
        return '0'
V_CSS, V_JS = _ver('assets/css/style.css'), _ver('assets/js/main.js')

missing = set()
def build(lang):
    en = lang == 'en'
    A = '../' if en else ''           # prefijo de assets
    DIR = OUT + ('/en' if en else '')
    os.makedirs(DIR, exist_ok=True)
    def t(s):
        if not en: return s
        if s in EN: return EN[s]
        if s in EN.values(): return s
        missing.add(s); return s
    def ptitle(m):
        return m['title_en'] if en else m['title']
    def asset(p): return A + p if p else p

    def proj_card(m):
        gl = ', '.join(t(GROUPS[g][0]) for g in sorted(m['groups']))
        ttl = ptitle(m)
        img = f'<img src="{e(asset(m["file"]))}" alt="{e(ttl)}" loading="lazy">' if m['file'] else '<div class="ph"></div>'
        return (f'<a class="proj" href="proyecto-{m["slug"]}.html" data-cats="{" ".join(sorted(m["groups"]))}">{img}'
                f'<div class="cap"><b>{e(ttl)}</b><span>{e(gl)}</span></div></a>')

    def layout(fname, title, desc, body, banner=None, crumbs=None):
        nav = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == fname or (fname.startswith("servicio-") and h == "servicios.html") else ""}>{t(l)}</a></li>' for h, l in NAV)
        ban = ''
        if banner:
            cr = ''
            if crumbs:
                cr = '<div class="crumbs">' + '<i>/</i>'.join(f'<a href="{h}">{t(l)}</a>' if h else e(l) for h, l in crumbs) + '</div>'
            ban = f'<header class="banner" style="background-image:url({asset(banner[1])})"><div class="wrap"><h1>{banner[0]}</h1>{cr}</div></header>'
        credit = f'<a href="https://www.erickhernandezarias.net/" target="_blank" rel="noopener">Erick Hernández Arias</a>'
        if en:
            copyright_html = ('© 2026 JYH Ingenieros is a company specialized in preparing construction project budgets '
                              'for the Dominican Republic and the Caribbean. All rights reserved. '
                              f'Design and development — {credit}.')
        else:
            copyright_html = ('© 2026 JYH Ingenieros es una empresa especialista en la elaboración de presupuestos de proyectos de construcción '
                              'para República Dominicana y el Caribe. Todos los derechos reservados. '
                              f'Diseño y desarrollo — {credit}.')
        other = ('../' + fname) if en else ('en/' + fname)
        sw_es = f'<a href="{other if en else fname}" hreflang="es" lang="es"{" aria-current=\"true\"" if not en else ""}>ES</a>'
        sw_en = f'<a href="{fname if en else other}" hreflang="en" lang="en"{" aria-current=\"true\"" if en else ""}>EN</a>'
        alt_es = ('../' if en else '') + fname
        alt_en = fname if en else 'en/' + fname
        return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="alternate" hreflang="es" href="{alt_es}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="icon" href="{A}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{A}assets/css/style.css?v={V_CSS}">
</head>
<body>
<a class="skip" href="#main">{t('Saltar al contenido')}</a>
<div class="topbar"><div class="wrap">
  <div class="row contact">
    <span class="it">{I_PIN}{t('Serrallés, Piantini · Santo Domingo, R.D.')}</span>
    <a href="mailto:{MAIL}">{I_MAIL}{MAIL}</a>
    <a href="{TEL_HREF}">{I_TEL}{TEL}</a>
  </div>
  <div class="row right">
    <div class="lang" aria-label="Idioma / Language">{sw_es}<span>/</span>{sw_en}</div>
    <div class="social"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{I_FB}</a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I_IG}</a></div>
  </div>
</div></div>
<header class="site-header"><div class="bar">
  <a class="logo" href="index.html"><img src="{A}assets/img/logo.png" alt="{SITE} — Plan · Control · Build"></a>
  <nav class="nav" id="nav" aria-label="{t('Principal')}"><ul>{nav}</ul></nav>
  <div class="head-cta"><a class="touch" href="contacto.html">{t('Contáctenos')} {ARROW}</a></div>
  <button class="burger" aria-expanded="false" aria-controls="nav" aria-label="{t('Abrir menú')}"><span></span></button>
</div></header>
<main id="main">
{ban}
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="foot">
    <div><a class="foot-logo" href="index.html"><img src="{A}assets/img/logo.png" alt="{SITE} — Plan · Control · Build"></a>
      <p>{t('Ingeniería de servicios completos: construcción, planificación y control en República Dominicana y el Caribe.')}</p></div>
    <div><h4>{t('Navegación')}</h4><ul>{''.join(f'<li><a href="{h}">{t(l)}</a></li>' for h, l in NAV)}</ul></div>
    <div><h4>{t('Servicios')}</h4><ul>
      {''.join(f'<li><a href="{x["file"]}">{t(x["title"])}</a></li>' for x in SV)}</ul></div>
    <div><h4>{t('Contacto')}</h4><ul>
      <li>{e(t(ADDR))}</li>
      <li><a href="{TEL_HREF}">{TEL}</a></li>
      <li><a href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
  </div>
  <div class="copy"><p>{copyright_html}</p></div>
</div></footer>
<a class="wa-float" href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(t('Hola, me gustaría recibir información sobre sus servicios.'))}" target="_blank" rel="noopener" aria-label="{t('Escríbenos por WhatsApp')}">
  <svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.55 4.18 1.6 6L4 29l8.1-1.55a12 12 0 0 0 3.94.66C22.68 28.1 28 22.7 28 16.04 28 9.4 22.68 3 16.04 3zm0 21.9c-1.2 0-2.38-.32-3.4-.93l-.24-.15-4.8.92.94-4.67-.16-.25a9.9 9.9 0 0 1-1.52-5.26c0-5.5 4.47-9.97 9.98-9.97 5.5 0 9.98 4.47 9.98 9.97 0 5.5-4.48 10.34-9.78 10.34zm5.47-7.46c-.3-.15-1.77-.87-2.04-.97-.28-.1-.48-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.22 3.08.15.2 2.1 3.2 5.08 4.49.7.3 1.26.48 1.69.62.7.22 1.35.2 1.86.12.57-.08 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/></svg>
</a>
<script src="{A}assets/js/main.js?v={V_JS}"></script>
</body>
</html>
"""

    def cta():
        return f"""<section class="cta"><div class="wrap"><h2>{t('¿Tiene un proyecto en mente?')}</h2>
<a class="btn" href="contacto.html">{t('Solicitar información')} {ARROW}</a></div></section>"""

    def write(name, content): open(f'{DIR}/{name}', 'w', encoding='utf8').write(content)

    def stats():
        return f"""<section class="stats"><div class="wrap">
  <div class="stat"><b>35+</b><h3>{t('Años de experiencia')}</h3><p>{t('En proyectos hoteleros, civiles, viales e hidráulicos en República Dominicana y el Caribe.')}</p></div>
  <div class="stat"><b>{len(PROJ)}</b><h3>{t('Proyectos en portafolio')}</h3><p>{t('Presupuestos, supervisión, auditoría y construcción de obras.')}</p></div>
  <div class="stat"><b>4</b><h3>{t('Áreas de especialidad')}</h3><p>{t('Edificaciones, obras viales, obras marinas y planificación y control.')}</p></div>
</div></section>"""

    def mvv():
        return f"""<div class="mvv">
  <div class="item"><h3>{t('Misión')}</h3><p>{t('Desarrollar importantes proyectos en el país que nos hacen acreedores de la confianza de nuestros clientes.')}</p></div>
  <div class="item"><h3>{t('Visión')}</h3><p>{t('Convertirnos en un marco de referencia en la Industria Constructora, siendo distinguidos por nuestras innovaciones y altos niveles de calidad, entrega a tiempo y precio competitivo.')}</p></div>
  <div class="item"><h3>{t('Valores')}</h3><p>{t('Economía • Tiempo • Credibilidad • Compromiso • Calidad • Trabajo en equipo • Cumplimiento en excelencia.')}</p></div>
</div>"""

    # ---- index ----
    feat = [m for m in PROJ if m['featured'] and m['file']]
    docs = [('assets/docs/perfil-corporativo-jyh-ingenieros.pdf', 'Perfil de la Empresa'), ('assets/docs/diseno-estructural.pdf', 'Diseño Estructural'),
            ('assets/docs/diseno-electrico.pdf', 'Diseño Eléctrico'), ('assets/docs/diseno-sanitario.pdf', 'Diseño Sanitario')]
    SLIDES = [('Empresa de ingeniería de servicios completos', 'Construcción de obras civiles, hoteleras y marinas, con planificación, presupuestos, control de costos y supervisión, en República Dominicana y el Caribe.'),
              ('Construcción, supervisión, costos y control', 'Construimos y supervisamos hoteles, villas, aeropuertos y obras marinas, con control de costos y de calidad en cada fase del proyecto.'),
              ('Planificación y control', 'Presupuestos, planificación, auditoría y tasaciones para decidir con certeza antes y durante la ejecución de la obra.')]
    home = f"""
<section class="hero hero-slider" aria-roledescription="carousel" aria-label="{t('Nuestros servicios')}">
  <div class="slides">
    {''.join(f'<div class="slide{" is-active" if n == 0 else ""}" role="group" aria-roledescription="slide" aria-label="{n+1} / {len(SLIDES)}"><img src="{A}assets/img/slides/slide-{n+1}.jpg" alt="" {"fetchpriority=high" if n == 0 else "loading=lazy"} width="1920" height="900"><div class="wrap">{"<h1>" if n == 0 else "<h2>"}{e(t(ttl))}{"</h1>" if n == 0 else "</h2>"}<p class="sub">{t(sub)}</p><div class="btns"><a class="btn" href="contacto.html">{t("Contáctenos")} {ARROW}</a><a class="btn navy" href="servicios.html">{t("Servicios")} {ARROW}</a></div></div></div>' for n, (ttl, sub) in enumerate(SLIDES))}
  </div>
  <div class="slider-ui">
    <div class="dots">{''.join(f'<button type="button" aria-label="{n+1}"{" aria-current=true" if n == 0 else ""}></button>' for n in range(len(SLIDES)))}</div>
    <div class="arrows"><button type="button" class="prev" aria-label="{t('Anterior')}">‹</button><button type="button" class="next" aria-label="{t('Siguiente')}">›</button></div>
  </div>
</section>

<section class="block"><div class="wrap">
  <div class="label">{t('01. Especialidades')}</div>
  <div class="tiles">
    {''.join(f'<a class="tile" href="{x["file"]}"><div><small>0{i+1}</small><h3>{e(t(x["title"]))}</h3></div>{ARROW}</a>' for i, x in enumerate(SV))}
  </div>
</div></section>

<section class="block" style="padding-top:0"><div class="wrap">
  <div class="label">{t('02. Quiénes somos')}</div>
  <div class="split">
    <img src="{A}assets/img/hero-2.jpg" alt="J&amp;H Ingenieros" loading="lazy">
    <div class="vr"></div>
    <div>
      <h2>{t('Una empresa de ingeniería de servicios completos: planificamos, controlamos y construimos')}</h2>
      <p>{t('Somos una empresa de ingeniería de servicios completos: planificación, control y construcción. Con más de 25 años de ejercicio continuo en la República Dominicana, construimos y damos servicio a importantes empresas de los sectores inmobiliario, hotelero turístico y de transporte aéreo (aeropuertos, helipuertos, hangares); así como para grandes proyectos marinos y viales.')}</p>
      <ul class="checks"><li>{t('Construcción de obras civiles, hoteleras y marinas')}</li><li>{t('Presupuestos y control de costos')}</li><li>{t('Supervisión y administración de obras')}</li><li>{t('Auditoría de proyectos y tasaciones')}</li></ul>
      <a class="btn" href="nosotros.html">{t('Conózcanos')} {ARROW}</a>
    </div>
  </div>
</div></section>

<section class="block dark"><div class="wrap">
  <div class="label">{t('03. Nuestros servicios')} <a href="servicios.html">{t('Ver todos')} {ARROW}</a></div>
  <div class="svc-row">
    <div class="svc-big">{t('Experiencia que construye confianza')}</div>
    {''.join(f'<a class="svc-item" href="{x["file"]}"><small>0{i+1}</small><h3>{e(t(x["title"]))}</h3><p>{" · ".join(e(t(y[0])) for y in x["items"][:3])}</p></a>' for i, x in enumerate(SV))}
  </div>
  <p style="margin-top:56px;max-width:70ch;color:#d5dce5">{t('Nuestra experiencia profesional ha sido en la construcción de proyectos hoteleros, civiles, viales, hidráulicas y marinos. Así como en la Supervisión y Administración de la Construcción de Proyectos; Asesoría en Costos de proyectos de construcción en República Dominicana y Presupuestos, Planificación, Control de Costos, Auditoria de Proyectos en cualquier fase de ejecución y Tasaciones.')}</p>
</div></section>

{stats()}

<section class="block"><div class="wrap">
  <div class="label">{t('04. Proyectos destacados')} <a href="servicios.html">{t('Ver todos')} {ARROW}</a></div>
  <div class="grid g3">{''.join(proj_card(m) for m in feat)}</div>
</div></section>

<section class="block soft"><div class="wrap">
  <div class="label">{t('05. Misión, visión y valores')}</div>
  <div class="dark" style="background:var(--blue);padding:56px 48px">{mvv()}</div>
</div></section>

<section class="block"><div class="wrap">
  <div class="label">{t('06. Descargas')}</div>
  <div class="docs">
    {''.join(f'<a class="doc" href="{A}{h}" target="_blank" rel="noopener">{I_DOC}<span>{t(l)}</span></a>' for h, l in docs)}
  </div>
</div></section>
{cta()}
"""
    write('index.html', layout('index.html', t('J&H Ingenieros | Construcción e ingeniería de servicios completos en Santo Domingo'),
          t('J&H Ingenieros: empresa de ingeniería de servicios completos en Santo Domingo. Construcción de obras civiles y marinas, planificación, presupuestos, control de costos y supervisión.'), home))

    # ---- nosotros ----
    nos = f"""
<section class="block"><div class="wrap">
  <div class="label">{t('01. Quiénes somos')}</div>
  <div class="split">
    <img src="{A}assets/img/hero-3.jpg" alt="J&amp;H Ingenieros" loading="lazy">
    <div class="vr"></div>
    <div>
      <h2>{t('Nosotros somos J&H Ingenieros').replace('&', '&amp;')}</h2>
      <p>{t('JYH Ingenieros es una empresa especialista en la elaboración de presupuestos de proyectos de construcción en Santo Domingo, puntera en el desarrollo de proyectos en la República Dominicana y el Caribe, con más de 35 años de experiencia acumulada en el sector de la construcción de proyectos: hoteleros, turísticos, residenciales, civiles, viales e hidráulicos, diseño y ejecución de playas artificiales, marinas y rompeolas; con trabajos realizados en varios países del Caribe.')}</p>
      <a class="btn" href="{A}assets/docs/perfil-corporativo-jyh-ingenieros.pdf" target="_blank" rel="noopener">{t('Descargar perfil')} {ARROW}</a>
    </div>
  </div>
</div></section>

<section class="block soft"><div class="wrap">
  <div class="label">{t('02. Especialidades')}</div>
  <div class="grid g3">
    <div class="spec"><h3>{t('Edificaciones')}</h3><ul class="ticks"><li>{t('Resorts hoteleros')}</li><li>{t('Viviendas y villas')}</li><li>{t('Estructuras metálicas y ligeras')}</li></ul></div>
    <div class="spec"><h3>{t('Obras viales y aeroportuarias')}</h3><ul class="ticks"><li>{t('Aeropuertos')}</li><li>{t('Carreteras')}</li><li>{t('Puentes')}</li></ul></div>
    <div class="spec"><h3>{t('Obras marinas')}</h3><ul class="ticks"><li>{t('Construcción y mantenimiento de playas')}</li><li>{t('Construcción de rompeolas, marinas y muelles')}</li><li>{t('Dragados hidráulicos y mecánicos')}</li></ul></div>
  </div>
  <div class="spec" style="margin-top:28px"><h3>{t('Especialidades en planeación y control')}</h3>
    <ul class="ticks"><li>{t('Planificación de proyectos')}</li><li>{t('Confección de presupuestos')}</li><li>{t('Auditorías a proyectos')}</li><li>{t('Tasaciones')}</li><li>{t('Supervisión')}</li></ul></div>
</div></section>

<section class="block dark"><div class="wrap">
  <div class="label">{t('03. Misión, visión y valores')}</div>
  {mvv()}
</div></section>
{stats()}
{cta()}
"""
    write('nosotros.html', layout('nosotros.html', t('Nosotros | J&H Ingenieros'),
          t('Conozca a J&H Ingenieros: más de 35 años de experiencia en presupuestos y construcción de proyectos en República Dominicana y el Caribe.'),
          nos, (t('Nosotros'), 'assets/img/hero-1.jpg'), [('index.html', 'Inicio'), (None, t('Nosotros'))]))

    # ---- servicios ----
    sv_page = f"""
<section class="block"><div class="wrap">
  <div class="label">{t('01. Servicios')}</div>
  <h2 style="max-width:18ch">{t('Construcción, supervisión, costos y control')}</h2>
  <p class="lead" style="max-width:62ch;margin-bottom:46px">{t('Construcción, supervisión, asesoría en costos, presupuestos, planificación, control de costos, auditoría y tasaciones, en cualquier fase de ejecución del proyecto.')}</p>
  <div class="grid g4">
    {''.join(f'<a class="card" href="{x["file"]}"><img src="{A}{x["img"]}" alt="{e(t(x["title"]))}" loading="lazy"><div class="body"><h3>{e(t(x["title"]))}</h3><p>{" · ".join(e(t(i[0])) for i in x["items"][:3])}</p><span class="more">{t("Ver más")} {ARROW}</span></div></a>' for x in SV)}
  </div>
</div></section>
{cta()}
"""
    write('servicios.html', layout('servicios.html', t('Servicios | J&H Ingenieros'),
          t('Edificaciones, obras viales y aeroportuarias, obras marinas, planificación y control de proyectos en República Dominicana.'),
          sv_page, (t('Servicios'), 'assets/img/hero-2.jpg'), [('index.html', 'Inicio'), (None, t('Servicios'))]))

    for key, s in SERVICES.items():
        ttl = t(s['title'])
        cards = ''.join(
            f'<a class="card" href="{s["stem"]}-{slug}.html">' + (f'<img src="{A}{img}" alt="{e(t(n))}" loading="lazy">' if img else '') +
            f'<div class="body"><h3>{e(t(n))}</h3><span class="more">{t("Ver proyectos")} {ARROW}</span></div></a>'
            for n, img, slug, cats in s['items'])
        body = f"""
<section class="block"><div class="wrap">
  <div class="label">01. {e(ttl)}</div>
  <div class="grid g3">{cards}</div>
</div></section>
{cta()}"""
        desc = (t('{t}: servicios y proyectos de J&H Ingenieros en República Dominicana y el Caribe.').replace('{t}', ttl) if en else
                f'{ttl}: servicios y proyectos de J&H Ingenieros en República Dominicana y el Caribe.')
        write(s['file'], layout(s['file'], f'{ttl} | J&H Ingenieros', desc, body, (e(ttl), s['img']),
              [('index.html', 'Inicio'), ('servicios.html', 'Servicios'), (None, ttl)]))

        # subservicios: aquí viven las obras / proyectos
        for n, img, slug, cats in s['items']:
            projs = [m for m in PROJ if slug in m['subs']]
            sname = t(n)
            if projs:
                inner = f'<div class="grid g3">{"".join(proj_card(m) for m in projs)}</div>'
            else:
                inner = f'<p class="lead">{t("Próximamente publicaremos proyectos de esta categoría.")}</p>'
            fn = f'{s["stem"]}-{slug}.html'
            body = f"""
<section class="block"><div class="wrap">
  <div class="label">01. {e(sname)}</div>
  {inner}
</div></section>
<section class="block soft"><div class="wrap">
  <div class="label">{t('02. Otros servicios de')} {e(ttl)}</div>
  <div class="grid g3">{''.join(f'<a class="card" href="{s["stem"]}-{o[2]}.html"><div class="body"><h3>{e(t(o[0]))}</h3><span class="more">{t("Ver proyectos")} {ARROW}</span></div></a>' for o in s['items'] if o[2] != slug)}</div>
</div></section>
{cta()}"""
            write(fn, layout(fn, f'{sname} | J&H Ingenieros',
                  (f'{sname}: proyectos de J&H Ingenieros.' if not en else f'{sname}: projects by J&H Ingenieros.'), body,
                  (e(sname), img or s['img']), [('index.html', 'Inicio'), ('servicios.html', 'Servicios'), (s['file'], ttl), (None, sname)]))

    # ---- páginas de proyecto ----
    def paras_of(m):
        if not en: return m['paras']
        if len(m['paras_en']) < len(m['paras']):
            missing.add(f"{m['title']}: falta descripcion_en")
        return [m['paras_en'][i] if i < len(m['paras_en']) else p for i, p in enumerate(m['paras'])]
    for m in PROJ:
        ttl = ptitle(m)
        # servicio / subservicio al que pertenece (para migas de pan y "más proyectos")
        trail = None
        for key, sv in SERVICES.items():
            for n, img, slug, cats in sv['items']:
                if slug in m['subs']:
                    trail = (sv, n, slug, cats); break
            if trail: break
        crumbs = [('index.html', 'Inicio'), ('servicios.html', 'Servicios')]
        banner_img = m['file'] or 'assets/img/hero-1.jpg'
        more = ''
        if trail:
            sv, n, slug, cats = trail
            crumbs += [(sv['file'], t(sv['title'])), (f'{sv["stem"]}-{slug}.html', t(n))]
            others = [x for x in PROJ if slug in x['subs'] and x['slug'] != m['slug']]
            if others:
                more = f"""<section class="block soft"><div class="wrap">
  <div class="label">{t('Más proyectos de')} {e(t(n))} <a href="{sv["stem"]}-{slug}.html">{t('Ver todos')} {ARROW}</a></div>
  <div class="grid g3">{''.join(proj_card(x) for x in others[:6])}</div>
</div></section>"""
        crumbs.append((None, ttl))
        gal = m['gallery']
        if gal:
            thumbs = ''.join(f'<button type="button" class="thumb" data-src="{A}{g}" aria-label="{t("Imagen")} {i+1}"{" aria-current=\"true\"" if i == 0 else ""}><img src="{A}{g}" alt="" loading="lazy"></button>' for i, g in enumerate(gal)) if len(gal) > 1 else ''
            gallery = f"""<figure class="gallery"><img id="gal-main" src="{A}{gal[0]}" alt="{e(ttl)}">
  {f'<div class="thumbs">{thumbs}</div>' if thumbs else ''}</figure>"""
        else:
            gallery = ''
        desc = ''.join(f'<p>{e(p)}</p>' for p in paras_of(m))
        text = f'<div class="pdesc"><h2>{t("Descripción")}</h2>{desc}</div>' if desc else ''
        body = f"""
<section class="block"><div class="wrap pdetail">
  {gallery}
  {text}
</div></section>
{more}
{cta()}"""
        fn = f'proyecto-{m["slug"]}.html'
        write(fn, layout(fn, f'{ttl} | J&H Ingenieros',
              (paras_of(m)[0] if m['paras'] else ttl)[:160], body,
              (e(ttl), banner_img), crumbs))

    # ---- clientes ----
    cl = sorted(f for f in os.listdir(OUT + '/assets/img/clients') if f != 'fono-pagina-clientes.jpg')
    cp = f"""
<section class="block"><div class="wrap">
  <div class="label">{t('01. Nuestros clientes')}</div>
  <div class="clients">{''.join(f'<figure><img src="{A}assets/img/clients/{f}" alt="{t("Logo de cliente") if en else "Logo de cliente"}" loading="lazy"></figure>' for f in cl)}</div>
</div></section>
{cta()}"""
    write('clientes.html', layout('clientes.html', t('Clientes | J&H Ingenieros'), t('Empresas que han confiado en J&H Ingenieros.'),
          cp, (t('Clientes'), 'assets/img/hero-1.jpg'), [('index.html', 'Inicio'), (None, t('Clientes'))]))

    # ---- contacto ----
    ct = f"""
<section class="block contact-sec" style="background:url({A}assets/img/contact-bg.jpg) right center/contain no-repeat"><div class="wrap contact-grid">
  <div class="info">
    <div class="label">{t('01. Contacto')}</div><h2>{t('Hablemos de su proyecto')}</h2>
    <ul>
      <li><b>{t('Dirección')}</b>{e(t(ADDR))}</li>
      <li><b>{t('Teléfono')}</b><a href="{TEL_HREF}">{TEL}</a></li>
      <li><b>{t('Correo')}</b><a href="mailto:{MAIL}">{MAIL}</a></li>
      <li><b>{t('Horario')}</b>{t('L-V: 8:00 am a 5:00 pm<br>Sáb: 8:00 am a 12:00 pm') if en else 'L-V: 8:00 am a 5:00 pm<br>Sáb: 8:00 am a 12:00 pm'}</li>
    </ul>
  </div>
  <!-- CONFIGURAR: reemplazar FORM_ENDPOINT por la URL del servicio de formularios (p. ej. Formspree o Web3Forms) -->
  <form action="FORM_ENDPOINT" method="POST">
    <div class="row">
      <div><label for="nombre">{t('Nombre')}</label><input id="nombre" name="nombre" required autocomplete="name"></div>
      <div><label for="email">{t('Correo electrónico')}</label><input id="email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="row">
      <div><label for="telefono">{t('Teléfono')}</label><input id="telefono" name="telefono" type="tel" autocomplete="tel"></div>
      <div><label for="asunto">{t('Asunto')}</label><input id="asunto" name="asunto"></div>
    </div>
    <label for="mensaje">{t('Mensaje')}</label><textarea id="mensaje" name="mensaje" rows="6" required></textarea>
    <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn" type="submit">{t('Enviar mensaje')}</button>
  </form>
</div>
<div class="wrap"><iframe class="map" title="{t('Ubicación de J&H Ingenieros').replace('&', '&amp;') if en else 'Ubicación de J&amp;H Ingenieros'}" src="{MAP}" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</section>"""
    write('contacto.html', layout('contacto.html', t('Contacto | J&H Ingenieros'),
          t('Contacte a J&H Ingenieros en Santo Domingo: (809) 473-4992, info@jyhingenieros.com.'),
          ct, (t('Contacto'), 'assets/img/hero-3.jpg'), [('index.html', 'Inicio'), (None, t('Contacto'))]))

build('es')
build('en')
if missing:
    print('SIN TRADUCIR / REVISAR:'); [print(' -', m) for m in sorted(missing)]
print('ok', len(PROJ), 'proyectos únicos')
