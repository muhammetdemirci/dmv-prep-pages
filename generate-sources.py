"""Render the public source inventory exported from the DMV Prep application."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'sources.json').read_text())
sources = data['sources']
overrides = json.loads((ROOT / 'source-overrides.json').read_text())
assert len({s['url'] for s in sources}) == len(sources)
assert len(data['states']) == 50

copy = {
    'en': {
        'title': 'Official information sources', 'support': 'Support', 'privacy': 'Privacy',
        'disclaimer': 'DMV Prep is an independent study app. It does not represent a government entity and is not affiliated with, endorsed by, or authorized by any DMV or government agency.',
        'intro': 'Original practice questions combine shared driving fundamentals with selected state rules. They are not official exam questions. This directory lists the handbook, statute, knowledge-test and road-safety references used by version 0.4.0 (Android 6).',
        'scope': 'The state sections list local references. Shared driving fundamentals also use the New York and California handbooks and the federal safety publications in the shared section. A shared reference is not a statement that every state has the same law. Always check your own state’s current handbook and requirements. Some study checks use app-defined formats; practice does not guarantee passing.',
        'date': 'Inventory assembled November 6, 2026. This is an inventory date, not a new factual review of every source. Government publishers may change their publications.',
        'jump': 'Find your state', 'shared': 'Shared driving and federal safety references',
        'sharedNote': 'These sources support general driving fundamentals across state banks. New York chapters and California guidance remain identified as such.',
        'external': 'Links open the original publisher’s page or document. Arkansas DPS and Louisiana OMV publish some documents through media.ark.org and PowerDMS; both the government entry page and document are listed.',
        'access': 'If a publisher’s website is unavailable from your location, use the USAGov state profile above its citations to find the state motor vehicle agency and government contacts.',
        'state_profile': 'Find state agencies on USAGov',
        'agency_directory': 'State motor vehicle agencies on USAGov',
        'nhtsa_directory': 'NHTSA contact and website on USAGov',
        'fmcsa_directory': 'FMCSA contact and website on USAGov',
        'json': 'Download the complete source inventory (JSON)', 'back': 'Back to top',
        'moved': 'Where a cited address has moved or can be difficult to access, we provide a related government reference. The downloadable inventory records the exact citations used by this app version.',
        'alternative': 'Related government reference',
    },
    'es': {
        'title': 'Fuentes oficiales de información', 'support': 'Soporte', 'privacy': 'Privacidad',
        'disclaimer': 'DMV Prep es una aplicación de estudio independiente. No representa a ningún organismo gubernamental ni está afiliada, respaldada o autorizada por ningún DMV u organismo gubernamental.',
        'intro': 'Las preguntas originales de práctica combinan fundamentos compartidos de conducción con algunas normas estatales. No son preguntas oficiales del examen. Este directorio enumera las referencias de manuales, leyes, requisitos del examen teórico y seguridad vial utilizadas por la versión 0.4.0 (Android 6).',
        'scope': 'Las secciones estatales incluyen las referencias locales. Los fundamentos compartidos también utilizan los manuales de Nueva York y California y las publicaciones federales de la sección compartida. Una referencia compartida no significa que todos los estados tengan la misma ley. Consulta el manual y los requisitos vigentes de tu estado. Algunas prácticas usan formatos definidos por la aplicación; practicar no garantiza aprobar.',
        'date': 'Inventario preparado el 6 de noviembre de 2026. Es la fecha del inventario, no una nueva revisión factual de todas las fuentes. Los organismos pueden actualizar sus publicaciones.',
        'jump': 'Encuentra tu estado', 'shared': 'Referencias compartidas de conducción y seguridad federal',
        'sharedNote': 'Estas fuentes respaldan los fundamentos generales de los bancos estatales. Los capítulos de Nueva York y la orientación de California conservan su identificación.',
        'external': 'Los enlaces abren la página o el documento original. Arkansas DPS y Louisiana OMV publican algunos documentos mediante media.ark.org y PowerDMS; se incluyen la página gubernamental y el documento.',
        'access': 'Si el sitio del organismo no está disponible desde tu ubicación, usa el perfil de USAGov que aparece antes de las citas para encontrar la agencia estatal de vehículos motorizados y los contactos gubernamentales.',
        'state_profile': 'Encuentra organismos estatales en USAGov (en inglés)',
        'agency_directory': 'Organismos estatales de vehículos motorizados en USAGov (en inglés)',
        'nhtsa_directory': 'Contacto y sitio web de NHTSA en USAGov (en inglés)',
        'fmcsa_directory': 'Contacto y sitio web de FMCSA en USAGov (en inglés)',
        'json': 'Descargar el inventario completo de fuentes (JSON)', 'back': 'Volver arriba',
        'moved': 'Cuando una dirección citada ha cambiado o puede ser difícil de abrir, incluimos una referencia gubernamental relacionada. El inventario descargable conserva las citas exactas de esta versión de la aplicación.',
        'alternative': 'Referencia gubernamental relacionada',
    },
}

def render(locale):
    c = copy[locale]
    suffix = '' if locale == 'en' else '-es'
    other = 'sources-es.html' if locale == 'en' else 'sources.html'
    other_label = 'Español' if locale == 'en' else 'English'

    def source_link(source):
        override = overrides.get(source['url'])
        title = source['titles'][0]
        url = source['url']
        note = ''
        if override:
            title = override.get('title', title)
            url = override['url']
            note = escape(c['alternative']) + '<br>'
        address = escape(url, quote=True)
        return f'<li><strong>{escape(title[locale])}</strong><br>{note}<a href="{address}">{address}</a></li>'

    def links(entries):
        return '<ul class="source-list">' + ''.join(map(source_link, entries)) + '</ul>'
    agency_links = (
        '<p><a href="https://www.usa.gov/agencies/national-highway-traffic-safety-administration">'
        + c['nhtsa_directory'] + '</a><br>'
        + '<a href="https://www.usa.gov/agencies/federal-motor-carrier-safety-administration">'
        + c['fmcsa_directory'] + '</a></p>'
    )
    sections = '<section id="shared"><h2>' + c['shared'] + '</h2><p>' + c['sharedNote'] + '</p>' + agency_links + links([s for s in sources if s['shared']]) + '</section>'
    for state in data['states']:
        state_slug = state['name']['en'].lower().replace(' ', '-')
        state_profile = f'<p><a href="https://www.usa.gov/states/{state_slug}">{c["state_profile"]}</a></p>'
        sections += '<section id="' + state['code'] + '"><h2>' + escape(state['name'][locale]) + ' (' + state['code'] + ')</h2>' + state_profile + links([s for s in sources if state['code'] in s['states']]) + '<p><a href="#main">' + c['back'] + '</a></p></section>'
    jump = '<nav class="state-index" aria-label="' + c['jump'] + '"><a href="#shared">' + ('Shared' if locale == 'en' else 'Compartidas') + '</a>' + ''.join('<a href="#' + s['code'] + '">' + escape(s['name'][locale]) + '</a>' for s in data['states']) + '</nav>'
    html = f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{c['title']} · DMV Prep"><title>{c['title']} · DMV Prep</title><link rel="icon" href="icon.png"><link rel="stylesheet" href="styles.css"></head>
<body><a class="skip" href="#main">{c['jump']}</a><div class="wrap"><header><a class="brand" href="index.html"><img src="icon.png" width="50" height="50" alt="">DMV Prep</a><nav aria-label="Navigation"><a href="support{suffix}.html">{c['support']}</a><a href="privacy{suffix}.html">{c['privacy']}</a><a href="{other}" lang="{'es' if locale == 'en' else 'en'}">{other_label}</a></nav></header>
<main id="main"><h1>{c['title']}</h1><div class="card"><p>{c['disclaimer']}</p></div><p class="lead">{c['intro']}</p><p>{c['scope']}</p><p>{c['external']}</p><p>{c['moved']}</p><p>{c['access']}</p><p><a href="https://www.usa.gov/state-motor-vehicle-services">{c['agency_directory']}</a></p><p class="meta">{c['date']}</p><p><a href="sources.json">{c['json']}</a></p><h2>{c['jump']}</h2>{jump}{sections}</main>
<footer><p>{c['disclaimer']}</p><p>© 2026 MD Teknoloji Bilişim ve Ticaret Anonim Şirketi</p></footer></div></body></html>
'''
    for source in sources:
        assert escape(overrides.get(source['url'], source)['url'], quote=True) in html, source['url']
    (ROOT / ('sources' + suffix + '.html')).write_text(html)

for locale in copy:
    render(locale)
print(f'Rendered both languages with all {len(sources)} distinct official-source URLs and 50 state sections.')
