"""Advanced SEO pass for the TrustRoute site. Safe to re-run after any page change.

  python tools/seo.py

For every page in site/ it:
  - adds robots snippet directives and og:locale to indexable pages
  - preloads the hero image (faster Largest Contentful Paint)
  - writes one JSON-LD block (id="seo-graph"): BreadcrumbList, Service / SoftwareApplication for
    products, FAQPage from the page's own questions, WebSite on the home page
  - refreshes the home page Organization data with every product
and regenerates site/sitemap.xml and site/llms.txt.
"""
import datetime, html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
BASE = 'https://trustroutetechnologies.com'
ORG_ID = BASE + '/#organization'
TODAY = datetime.date.today().isoformat()
SKIP = {'switch-simulators.html', 'trustforge.html', '404.html'}  # redirects + error page
ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'

PRODUCTS = {   # file -> (name, kind)
    'sms-banking.html': ('SMS Banking', 'Service'), 'whatsapp-banking.html': ('WhatsApp Banking', 'Service'),
    'wallet-banking.html': ('Wallet Banking', 'Service'), 'switchproof.html': ('SwitchProof', 'Service'),
    'feip.html': ('FEIP', 'Service'), 'meridian.html': ('Meridian', 'Service'), 'ai-banking.html': ('AI Banking', 'Service'),
    'agency-banking.html': ('Agency Banking', 'Service'), 'settledesk.html': ('SettleDesk', 'Service'),
    'trustcts.html': ('TrustCTS', 'Service'),
}
SECTIONS = {'about.html': 'The Firm', 'advisory.html': 'Advisory', 'solutions.html': 'Solutions',
            'contact.html': 'Contact', 'privacy.html': 'Privacy', 'terms.html': 'Terms'}

def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def meta(s, name):
    m = re.search(r'<meta (?:name|property)="' + re.escape(name) + r'" content="([^"]*)"', s)
    return html.unescape(m.group(1)) if m else ''

def url_for(rel):
    if rel == 'index.html':
        return BASE + '/'
    if rel == 'insights/index.html':
        return BASE + '/insights/'
    return BASE + '/' + rel[:-5]

def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}

pages = sorted(p for p in SITE.rglob('*.html') if p.name not in SKIP and 'assets' not in p.parts)
summary = []
for p in pages:
    rel = p.relative_to(SITE).as_posix()
    s = p.read_text(encoding='utf-8')
    url = url_for(rel)
    noindex = 'name="robots" content="noindex"' in s
    title = text(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    desc = meta(s, 'description')
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    h1 = text(h1m.group(1)) if h1m else title

    # robots directives + og:locale
    if not noindex and 'max-image-preview' not in s:
        s = s.replace('<meta name="description"', ROBOTS + '\n<meta name="description"', 1)
    if 'og:locale' not in s and 'property="og:site_name"' in s:
        s = s.replace('<meta property="og:site_name"', '<meta property="og:locale" content="en_CA">\n<meta property="og:site_name"', 1)

    # preload the hero background image
    s = re.sub(r'\n<link rel="preload" as="image"[^>]*>', '', s)
    hm = re.search(r'class="(?:hero|page-hero[^"]*)">\s*<div class="ph" style="background-image:url\(\'([^\']+)\'\)', s)
    if hm:
        s = s.replace('<link rel="icon"', f'<link rel="preload" as="image" href="{hm.group(1)}" fetchpriority="high">\n<link rel="icon"', 1)

    # structured data graph
    graph = []
    if rel == 'index.html':
        graph.append({'@type': 'WebSite', '@id': BASE + '/#website', 'url': BASE + '/', 'name': 'TrustRoute Technologies',
                      'publisher': {'@id': ORG_ID}, 'inLanguage': 'en'})
    elif rel.startswith('insights/'):
        trail = [('Home', BASE + '/'), ('Insights', BASE + '/insights/')]
        if rel != 'insights/index.html':
            trail.append((h1, url))
        graph.append(crumbs(trail))
    elif rel in PRODUCTS:
        graph.append(crumbs([('Home', BASE + '/'), ('Solutions', BASE + '/solutions'), (PRODUCTS[rel][0], url)]))
    else:
        graph.append(crumbs([('Home', BASE + '/'), (SECTIONS.get(rel, h1), url)]))

    if rel in PRODUCTS:
        name, kind = PRODUCTS[rel]
        if kind == 'SoftwareApplication':
            graph.append({'@type': 'SoftwareApplication', '@id': url + '#software', 'name': name, 'url': url,
                          'description': desc, 'applicationCategory': 'DeveloperApplication', 'operatingSystem': 'Web',
                          'sameAs': 'https://forge.trustroutetechnologies.com/', 'publisher': {'@id': ORG_ID},
                          'offers': [
                              {'@type': 'Offer', 'name': 'Free', 'price': '0', 'priceCurrency': 'USD'},
                              {'@type': 'Offer', 'name': 'Partner', 'price': '100', 'priceCurrency': 'USD',
                               'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': '100', 'priceCurrency': 'USD',
                                                      'unitText': 'per seat per month'}}]})
        else:
            graph.append({'@type': 'Service', '@id': url + '#service', 'name': name, 'url': url, 'description': desc,
                          'serviceType': 'Banking technology', 'provider': {'@id': ORG_ID}, 'areaServed': 'Worldwide'})

    faqs = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', s, re.S)
    if faqs:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': text(q), 'acceptedAnswer': {'@type': 'Answer', 'text': text(a)}} for q, a in faqs]})

    s = re.sub(r'\n<script type="application/ld\+json" id="seo-graph">.*?</script>', '', s, flags=re.S)
    if graph:
        block = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
        s = s.replace('</head>', '<script type="application/ld+json" id="seo-graph">\n' + block + '\n</script>\n</head>', 1)

    p.write_text(s, encoding='utf-8')
    if not noindex:
        summary.append((rel, url, title, desc))

# home page organization: list every product and service
home = SITE / 'index.html'; s = home.read_text(encoding='utf-8')
m = re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', s, re.S)
if m:
    org = json.loads(m.group(1))
    org['hasOfferCatalog']['itemListElement'] = [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'url': u}} for n, u in
        [('Banking Technology Advisory', BASE + '/advisory'), ('Oracle FLEXCUBE Advisory', BASE + '/advisory#flexcube')]
        + [(v[0], url_for(k)) for k, v in PRODUCTS.items()]
        + [('TrustForge', 'https://forge.trustroutetechnologies.com/')]]
    org['knowsAbout'] = sorted(set(org.get('knowsAbout', []) + ['Cheque truncation', 'Bulk payments', 'Agency banking',
                                                                 'AI in banking', 'FLEXCUBE ODT', 'Customer intelligence']))
    org['sameAs'] = ['https://www.linkedin.com/company/trustroutetechnologies']
    org['subOrganization'] = None
    org.pop('subOrganization')
    s = s.replace(m.group(0), '<script type="application/ld+json">\n' + json.dumps(org, indent=1, ensure_ascii=False) + '\n</script>', 1)
    home.write_text(s, encoding='utf-8')

# sitemap
prio = lambda rel: '1.0' if rel == 'index.html' else '0.9' if rel in ('solutions.html', 'advisory.html') \
    else '0.6' if rel.startswith('insights/') and rel != 'insights/index.html' else '0.8'
urls = ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio(r)}</priority></url>\n' for r, u, _, _ in summary)
(SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                  + urls + '</urlset>\n', encoding='utf-8')

# llms.txt: a plain summary for AI search tools
def section(title, rels):
    rows = [f'- [{t.split(" | ")[0].split(" · ")[0]}]({u}): {d}' for r, u, t, d in summary if r in rels]
    return f'## {title}\n\n' + '\n'.join(rows) + '\n'
products = [r for r in PRODUCTS]
articles = [r for r, *_ in summary if r.startswith('insights/') and r != 'insights/index.html']
llms = ('# TrustRoute Technologies\n\n'
        '> Independent banking technology advisory and solutions for banks and financial institutions worldwide, '
        'based in Burnaby, British Columbia, Canada. Founded by Najeebullah Usmani, a former CIO and CFO with 20 years '
        'across the Middle East, Asia, the Caribbean and North America.\n\n'
        + section('Firm and advisory', ['index.html', 'about.html', 'advisory.html', 'solutions.html', 'contact.html']) + '\n'
        + section('Solutions', products) + '\n'
        + '## TrustForge app\n\n- [TrustForge](https://forge.trustroutetechnologies.com/): AI agent for Oracle FLEXCUBE customization, built on Anthropic.\n\n'
        + section('Insights', articles) + '\n'
        + '## Company profile\n\n- [LinkedIn](https://www.linkedin.com/company/trustroutetechnologies): company updates and announcements.\n')
(SITE / 'llms.txt').write_text(llms, encoding='utf-8')
print(f'pages processed: {len(pages)} | indexable: {len(summary)} | sitemap URLs: {len(summary)}')
