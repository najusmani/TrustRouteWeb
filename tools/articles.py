"""Builds the Insights article pages (site/insights/<slug>.html) from the ARTICLES list below.

Run:  python tools/articles.py
To edit an article, change its text here and re-run; to add one, append a dict to ARTICLES.
Header and footer are copied from site/switchproof.html so articles always match the site.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
BASE = 'https://trustroutetechnologies.com'
IMG = 'https://images.unsplash.com/photo-{id}?w={w}&q=80&auto=format&fit=crop'
PUBLISHED = '2026-11-09'
PUBLISHED_HUMAN = '9 November 2026'
AUTHOR = 'TrustRoute Technologies'

ARTICLES = [
{
 'slug': 'introducing-ai-and-agency-banking',
 'category': 'News',
 'title': 'Introducing AI Banking and Agency Banking',
 'seo_title': 'Introducing AI Banking and Agency Banking | TrustRoute',
 'description': 'Two new TrustRoute solutions: AI Banking for customers, staff and risk teams, and Agency Banking to bring banking closer to every customer.',
 'image': '1531746790731-6c087fecd65a', 'image_alt': 'A white robotic hand, representing artificial intelligence',
 'takeaways': [
   'AI Banking brings AI to customers, staff and risk teams, with people in control.',
   'Agency Banking turns local shops and outlets into points of service.',
   'Both integrate with your core banking system and our other solutions.',
   'Demonstrations are available now.',
 ],
 'body': """
<p class="lead">Today we are introducing two new solutions. Both answer the same question that banks ask us most often: how do we serve more customers, better, without adding cost and risk?</p>

<h2>AI Banking: intelligence, <em>under your control</em></h2>
<p>AI is changing what customers expect and what banking teams can do. But in a regulated industry, AI is only valuable when it is useful, explainable and governed. <a href="/ai-banking">AI Banking</a> brings it to four places where it helps most:</p>
<ul>
<li><strong>A customer AI assistant</strong> that answers questions, checks balances and guides customers through everyday tasks on the web, in your app or on WhatsApp, and hands over to a person when needed.</li>
<li><strong>A staff AI copilot</strong> that helps employees find policies, summarise documents and draft responses.</li>
<li><strong>Fraud and anomaly detection</strong> that flags unusual transactions and behaviour for review.</li>
<li><strong>Credit scoring and risk</strong> insights that support, rather than replace, your credit decisions.</li>
</ul>
<p>Every capability is designed with human oversight, audit trails and data protection from the start. AI suggests and flags; your people decide.</p>

<h2>Agency Banking: closer to <em>every customer</em></h2>
<p>Branches cannot be everywhere, but trusted local agents can. <a href="/agency-banking">Agency Banking</a> turns shops and outlets into points of service, so customers can deposit and withdraw cash, open accounts, complete KYC and make payments close to home. Banks get the tools to run the network: agent onboarding and management, float visibility, and commissions that are calculated and paid automatically.</p>

<h2>Built to work together</h2>
<p>Both solutions integrate with your core banking system and complement our existing range. The AI assistant can run alongside <a href="/whatsapp-banking">WhatsApp Banking</a>; agents give <a href="/wallet-banking">Wallet Banking</a> customers convenient places to cash in and out; and <a href="/meridian">Meridian</a> brings it all together in a single view of each customer.</p>

<h2>See them in action</h2>
<p>Demonstrations of AI Banking and Agency Banking are available now. If you are exploring how AI or agent networks could work at your institution, we would be glad to show you, and to talk through how each would fit your systems, your customers and your regulator.</p>
""",
},
{
 'slug': 'iso-20022-migration',
 'category': 'Payments',
 'title': 'ISO 20022 migration: what banks should be planning for now',
 'seo_title': 'ISO 20022 Migration: What Banks Should Plan Now | TrustRoute',
 'description': 'The cross-border deadline has passed, but ISO 20022 work is not finished. Where banks should focus next: data, translation, testing and operations.',
 'image': '1513635269975-59663e0ac1ad', 'image_alt': 'City skyline at dusk',
 'takeaways': [
   'Treat ISO 20022 as a data programme, not a message-format change.',
   'Map every payment flow, not just cross-border messages.',
   'Translation was meant as a bridge; plan to retire it.',
   'Test end to end: switch, core, screening and reconciliation together.',
 ],
 'body': """
<p class="lead">For many banks, ISO 20022 felt like a deadline to survive. The coexistence period for cross-border payment instructions on the SWIFT network ended in November 2025, yet the real work of the migration is far from over.</p>

<p>Meeting the cross-border cut-over was necessary, but it was never the whole story. Domestic high-value and instant payment schemes are on their own timelines, internal systems still speak older formats, and many institutions crossed the line by translating messages rather than truly adopting the richer data ISO 20022 carries. The question now is not whether you are compliant, but whether you are getting the value the standard was designed to deliver.</p>

<h2>Know where you actually are</h2>
<p>Start with an honest inventory. List every payment flow that touches your bank (cross-border, domestic real-time gross settlement, instant payments, card settlement and internal transfers) and record, for each one, which format it uses at every hop. It is common to find that a message arrives in ISO 20022, is converted to a legacy format for the core banking system, and is converted back again on the way out. Each conversion is a place where data can be lost.</p>

<h2>Data is the real migration</h2>
<p>ISO 20022 is valuable because it is structured. Names, addresses, purposes and remittance information each have their own place, instead of being squeezed into free-text fields. That structure is what enables better sanctions screening, straight-through processing and richer information for customers. But it only helps if your systems capture and preserve it.</p>
<ul>
<li><strong>Structured addresses:</strong> check that customer and counterparty addresses are held in structured form in your core and onboarding systems, not just in a single text line.</li>
<li><strong>Truncation:</strong> identify every point where a field is shortened to fit an older system. Truncated data is lost data.</li>
<li><strong>Reference data:</strong> review how you hold identifiers such as Legal Entity Identifiers and purpose codes, and who maintains them.</li>
</ul>

<h2>Do not let translation become permanent</h2>
<p>Translating between legacy formats and ISO 20022 was a sensible way to meet the deadline. As a long-term architecture, it is a liability: every translation layer adds cost, latency and risk, and strips away the richer data that made the migration worthwhile. Make a plan, with dates, to move each internal system to native ISO 20022 handling, starting with the flows that carry the most volume or the most compliance risk.</p>

<h2>Test end to end, not message by message</h2>
<p>A message that validates against the schema can still fail in production. Real problems appear between systems: the switch accepts a message the core banking system cannot post, screening raises alerts on data it has never seen before, or reconciliation breaks because references no longer match. Testing should follow a payment from initiation to settlement and reconciliation, including rejections, returns and investigations, not just the happy path.</p>

<h2>Prepare operations and screening teams</h2>
<p>Richer data changes daily work. Sanctions screening sees more information, which can improve accuracy but may also change alert volumes. Investigations and exceptions teams need to read new message types confidently. Brief these teams early and give them examples drawn from your own traffic.</p>

<h2>A practical next 90 days</h2>
<ol>
<li><strong>Weeks 1 to 4:</strong> complete the payment-flow inventory and identify every translation and truncation point.</li>
<li><strong>Weeks 5 to 8:</strong> prioritise flows by volume and risk, and agree a target date to remove each translation layer.</li>
<li><strong>Weeks 9 to 12:</strong> build an end-to-end test set from real scenarios, and run it against your current setup to establish a baseline.</li>
</ol>

<p>ISO 20022 rewards the banks that treat it as an opportunity to clean up their payment data and architecture. The deadline has passed; the advantage is still there to be taken.</p>
""",
},
{
 'slug': 'sms-banking-reach',
 'category': 'Channels',
 'title': 'Why SMS banking still reaches customers that apps cannot',
 'seo_title': 'Why SMS Banking Still Reaches Customers Apps Cannot | TrustRoute',
 'description': 'Mobile apps get the attention, but SMS and USSD still reach every phone. Where SMS banking fits, how to keep it secure, and how to design it well.',
 'image': '1556742049-0cfed4f6a45d', 'image_alt': 'Customer using a mobile phone',
 'takeaways': [
   'Not every customer can, or wants to, use a banking app.',
   'SMS and USSD work on any phone, without data or downloads.',
   'Use SMS for what it does well, and be clear about its security limits.',
   'Plan channels together: SMS, WhatsApp and apps can share one integration.',
 ],
 'body': """
<p class="lead">Banks invest heavily in mobile apps, and rightly so. Yet a meaningful share of customers will never download one. For them, a simple text message is still the most reliable way to bank.</p>

<h2>The app gap</h2>
<p>Apps assume a smartphone, enough storage, a data connection and the confidence to install and trust software. Many customers lack at least one of these: people in rural areas with patchy coverage, older customers who prefer simple tools, small businesses using a basic handset, and anyone who simply does not want another app. These customers still need to know their balance, receive alerts and move money.</p>

<h2>What SMS and USSD do well</h2>
<p>SMS and USSD work on every mobile phone, over the basic mobile network, without data or downloads. They are familiar, fast and resilient: when data networks are congested or an app is unavailable, a text message usually still gets through. That makes them well suited to:</p>
<ul>
<li><strong>Balance and mini-statement enquiries</strong> answered in seconds.</li>
<li><strong>Transaction alerts</strong> that help customers spot problems early.</li>
<li><strong>Simple transfers and payments</strong> to known beneficiaries, within sensible limits.</li>
<li><strong>Service continuity</strong> when other channels are down.</li>
</ul>

<h2>Be clear about security</h2>
<p>SMS was not designed as a secure channel, and a good SMS banking service is honest about that. Protect customers with a PIN on every transaction, sensible transaction limits, and controls against SIM-swap fraud, such as checking for recent SIM changes before allowing sensitive actions. Never send full account numbers or other sensitive data in a message. For one-time passcodes, SMS remains widely used, but banks should offer stronger options where customers can use them.</p>

<h2>Design for the channel</h2>
<p>SMS banking succeeds when it is simple. Keep commands short and memorable, confirm every transaction clearly, and support the languages your customers actually use. USSD menus should be shallow, with the most common tasks one or two steps away. Test with real customers on basic handsets, not just with staff on smartphones.</p>

<h2>Not either-or</h2>
<p>SMS banking is not a rival to your app; it is part of the same channel strategy. A well-designed integration with your core banking system can serve SMS, USSD, WhatsApp and the app from one set of services, so new features reach every channel without being built several times.</p>

<h2>Measure what matters</h2>
<p>Track active users, the most-used commands, failed requests and the share of customers for whom SMS is their only digital channel. Those numbers show the real reach of the service, and often make a stronger case for it than any assumption about how customers ought to bank.</p>
""",
},
{
 'slug': 'simulating-the-switch',
 'category': 'Assurance',
 'title': 'Simulating the switch: certify before you go live',
 'seo_title': 'Simulating the Switch: Certify Before Go-Live | TrustRoute',
 'description': 'Testing against live ATMs, POS terminals and networks is slow and costly. How simulation-led testing reduces risk, rework and certification surprises.',
 'image': '1601597111158-2fceff292cdc', 'image_alt': 'A customer entering a PIN at an ATM',
 'takeaways': [
   'Simulators let you test any scenario, on demand, without live devices.',
   'The failures that hurt are reversals, time-outs and edge cases, not the happy path.',
   'Run a regression suite after every change, not just before go-live.',
   'Keep evidence: it shortens certification and helps with audits.',
 ],
 'body': """
<p class="lead">Every change to a payment switch carries risk: a new card product, a scheme mandate, a core banking upgrade. The safest place to find a problem is in the test lab, long before a customer is standing at an ATM.</p>

<h2>Why live testing falls short</h2>
<p>Testing against real ATMs, POS terminals, hosts and networks is slow, expensive and hard to repeat. Test cards and devices are limited, scheme test environments must be booked, and some scenarios, such as a host timing out halfway through a transaction, are almost impossible to reproduce on demand. The result is that teams test what is easy rather than what is risky.</p>

<h2>What simulation means</h2>
<p>A simulator stands in for one of the parties in a transaction. It can play the ATM or POS terminal that starts a transaction, the host or core banking system that approves it, or the scheme or network in between. Because each party is software, every response can be scripted: approve, decline, delay, return a malformed message, or not answer at all.</p>

<h2>Test the scenarios that hurt</h2>
<p>Most incidents in production do not come from the normal purchase or withdrawal. They come from the edges. A good test set covers:</p>
<ul>
<li><strong>Reversals and time-outs:</strong> what happens when a response never arrives, and is the customer's money correctly restored?</li>
<li><strong>Duplicates:</strong> a repeated request must not result in a repeated debit.</li>
<li><strong>Partial approvals and declines</strong>, with the right response codes reaching the customer.</li>
<li><strong>Stand-in processing</strong> when the host is unavailable, including posting once it returns.</li>
<li><strong>Field-level edge cases</strong> in the message specification, such as unusual amounts, currencies and optional fields.</li>
</ul>

<h2>Make regression routine</h2>
<p>Once scenarios are scripted, they can be run again and again. Build a regression suite and run it after every change, whether that is a switch upgrade, a new parameter or a core banking patch. Problems found the day after a change are cheap; problems found by customers are not.</p>

<h2>Keep the evidence</h2>
<p>Scheme and network certification asks you to show that your system behaves correctly. Simulation produces that evidence as a by-product: message logs, expected and actual results, and a clear record of what was tested and when. Keeping it organised shortens certification, supports internal audit, and makes the next round of changes faster.</p>

<h2>Close the loop with reconciliation</h2>
<p>A transaction is only truly correct when the accounting is correct. Extend testing beyond the switch to check that every approved, reversed and stand-in transaction is posted, settled and reconciled as expected. This is where many go-lives stumble, and where simulation-led testing pays for itself.</p>

<p>Our <a href="/switchproof">SwitchProof</a> product brings this approach to banks running Oracle FLEXCUBE, combining regression, load and UAT testing with stand-in processing and reconciliation reporting.</p>
""",
},
{
 'slug': 'choosing-a-payment-switch',
 'category': 'Strategy',
 'title': 'Choosing a payment switch: questions to ask before the RFP',
 'seo_title': 'Choosing a Payment Switch: Questions Before the RFP | TrustRoute',
 'description': 'A payment switch is a decade-long decision. The questions selection committees should answer on coverage, resilience, integration, security and cost.',
 'image': '1497366811353-6870744d04b2', 'image_alt': 'Quiet modern office interior',
 'takeaways': [
   'Define your own requirements before you read a single vendor brochure.',
   'Probe resilience and stand-in, not just headline throughput.',
   'Integration with your core banking system decides the real cost.',
   'Ask how change requests are priced: that is where budgets slip.',
 ],
 'body': """
<p class="lead">A payment switch sits at the heart of a bank for a decade or more. Choosing one is as much about how you will live with it as about what it can do on the day you buy it.</p>

<h2>Start with your own requirements</h2>
<p>Before issuing a request for proposal, agree internally what the switch must do: the channels it must serve, the schemes and networks it must connect to, the transaction volumes you expect in five years, and the services you want to launch. A clear statement of need keeps the evaluation focused on your bank rather than on each vendor's favourite features.</p>

<h2>Coverage and standards</h2>
<ul>
<li>Which card schemes, domestic networks and payment systems are supported today, and which are certified in your market?</li>
<li>Which ISO 8583 variants and which ISO 20022 messages are supported, and how are new mandates delivered?</li>
<li>How are channels such as ATM, POS, e-commerce, mobile and SMS connected?</li>
</ul>

<h2>Resilience, not just speed</h2>
<p>Throughput figures are easy to quote and hard to compare. Ask instead how the switch behaves under stress. How does it scale for peak days? Can it run active-active across sites? What happens to transactions in flight during a failover? How does stand-in processing work when the core banking system is unavailable, and how are those transactions posted afterwards?</p>

<h2>Integration with your core</h2>
<p>The cost of a switch is often decided by its integration with your core banking system, not by its licence. Ask for real examples of integration with your core platform, how account and limit checks are performed, and how reconciliation between the switch and the core is handled. Pre-built connectors are valuable only if they match how your bank actually operates.</p>

<h2>Security and compliance</h2>
<p>Confirm how the vendor supports PCI DSS requirements, how keys are managed and which hardware security modules are supported, how sensitive card data is protected, and what audit trails are available. Ask how security patches are delivered and how quickly.</p>

<h2>Operations</h2>
<p>Your operations team will use the switch every day. Look at monitoring and alerting, dispute and chargeback handling, reconciliation and settlement reporting, and how parameters and configuration changes are controlled and approved.</p>

<h2>Commercials and the long term</h2>
<ul>
<li><strong>Licensing:</strong> per transaction, per channel, per institution, or a fixed fee, and how it changes with growth.</li>
<li><strong>Change requests:</strong> how customisation is priced and how long it takes. This is where many budgets slip.</li>
<li><strong>Roadmap and support:</strong> the vendor's plans for the product, local support capacity, and the strength of their user community.</li>
</ul>

<h2>Prove it before you sign</h2>
<p>Speak to reference banks of a similar size and region, and ask what they would do differently. Where possible, run a proof of concept with your own scenarios, including failures, not just a vendor demonstration. Finally, compare the total cost of ownership over the full life of the switch, including integration, hardware, certification, support and the internal team needed to run it.</p>
""",
},
{
 'slug': 'launching-a-wallet-programme',
 'category': 'Wallets',
 'title': 'Launching a wallet programme: the decisions that matter most',
 'seo_title': 'Launching a Wallet Programme: Key Decisions | TrustRoute',
 'description': 'A successful mobile wallet is a business, not just a product. The decisions on proposition, regulation, funds, agents, merchants and operations.',
 'image': '1563986768609-322da13575f3', 'image_alt': 'Mobile phone and laptop used for payments',
 'takeaways': [
   'Start with a clear customer problem, not with features.',
   'Settle regulation and how customer funds are safeguarded early.',
   'Cash-in, cash-out and merchant acceptance make or break adoption.',
   'Budget for operations: support, fraud and reconciliation never stop.',
 ],
 'body': """
<p class="lead">Launching a mobile wallet is easy to underestimate. The technology is the visible part; the decisions that determine success sit around it, in regulation, distribution and day-to-day operations.</p>

<h2>Start with the proposition</h2>
<p>Be precise about who the wallet is for and what problem it solves. Paying salaries to workers without bank accounts, collecting payments for small merchants, sending money home and paying bills are very different propositions, with different users, fees and partners. A clear proposition shapes every later decision.</p>

<h2>Regulation and licensing</h2>
<p>Wallet programmes are regulated differently in each market. Some regulators require a dedicated licence; in others, a bank can offer a wallet under its existing licence, or a provider can operate with a licensed partner bank. Engage your regulator early and settle questions such as customer due diligence, account tiers and transaction limits before you design the product.</p>

<h2>How customer funds are held</h2>
<p>Customers must be able to trust that their money is safe. Decide how wallet balances are held and safeguarded, how the wallet ledger reconciles with those funds every day, and how settlement with partners works. This design is fundamental and difficult to change later.</p>

<h2>Cash-in, cash-out and agents</h2>
<p>For many customers, a wallet is only useful if they can easily put cash in and take it out. That often means an agent network: shops and outlets where customers can deposit and withdraw. Recruiting, training, supplying and monitoring agents is a business in its own right, and it frequently decides whether a wallet is adopted.</p>

<h2>Somewhere to spend it</h2>
<p>A wallet needs places to use it. Plan merchant acceptance from the start: QR payments, bill payment partners, and transfers to bank accounts and other wallets. Interoperability with other providers in your market can significantly increase usefulness.</p>

<h2>Onboarding and limits</h2>
<p>Tiered accounts let customers start quickly with simple checks and low limits, and move to higher limits as they provide more information. Make onboarding fast and inclusive, while matching each tier's limits to its level of verification.</p>

<h2>Operations never stop</h2>
<ul>
<li><strong>Customer support</strong> for forgotten PINs, failed transfers and disputes.</li>
<li><strong>Fraud monitoring</strong> tuned to wallet behaviour, including agent fraud.</li>
<li><strong>Daily reconciliation</strong> between the wallet ledger, partners and safeguarded funds.</li>
<li><strong>Regulatory reporting</strong> on time, every time.</li>
</ul>

<h2>Reach every customer</h2>
<p>Not every customer has a smartphone. Offering wallet services over USSD or SMS, alongside an app, can widen reach considerably, especially in the early stages of adoption.</p>

<h2>Launch, measure, improve</h2>
<p>Start with a focused launch, measure active use rather than registrations, and listen closely to agents and customers. The wallets that succeed are the ones that keep improving after launch day.</p>
""",
},
]

# ---------------------------------------------------------------- template
src = (SITE / 'switchproof.html').read_text(encoding='utf-8')
header = src[src.index('<a class="skip"'):src.index('<main id="main">')]
footer = src[src.index('<footer>'):src.index('</footer>') + len('</footer>')]
header = header.replace(' aria-current="page"', '').replace('href="/insights"', 'href="/insights/" aria-current="page"')
footer = footer.replace('href="/insights"', 'href="/insights/"')

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{seo_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="TrustRoute Technologies">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:alt" content="{image_alt}">
<meta property="article:published_time" content="{published}">
<meta property="article:section" content="{category}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>
"""

def words(text):
    return len(re.sub(r'<[^>]+>', ' ', text).split())

def page(a, others):
    url = f'{BASE}/insights/{a["slug"]}'
    minutes = max(3, round(words(a['body']) / 220))
    e = lambda s: html.escape(s, quote=True)
    jsonld = json.dumps({
        '@context': 'https://schema.org', '@type': 'BlogPosting',
        'headline': a['title'], 'description': a['description'],
        'image': IMG.format(id=a['image'], w=1200), 'datePublished': PUBLISHED, 'dateModified': PUBLISHED,
        'author': {'@type': 'Organization', 'name': AUTHOR, 'url': BASE + '/'},
        'publisher': {'@id': BASE + '/#organization', '@type': 'ProfessionalService', 'name': 'TrustRoute Technologies',
                      'logo': {'@type': 'ImageObject', 'url': BASE + '/assets/img/og-image.png'}},
        'mainEntityOfPage': url, 'articleSection': a['category'],
    }, indent=1, ensure_ascii=False)
    out = HEAD.format(seo_title=e(a['seo_title']), title=e(a['title']), description=e(a['description']), url=url,
                      og_image=IMG.format(id=a['image'], w=1200), image_alt=e(a['image_alt']),
                      published=PUBLISHED, category=e(a['category']), jsonld=jsonld)
    out += header
    takeaways = ''.join(f'<li>{e(t)}</li>' for t in a['takeaways'])
    related = ''.join(
        f'<a class="card rv{" s" + str(i + 2) if i else ""}" href="/insights/{o["slug"]}"><div class="im"><img src="{IMG.format(id=o["image"], w=1000)}" alt="{e(o["image_alt"])}" loading="lazy"></div>'
        f'<span class="label">{e(o["category"])}</span><h3>{e(o["title"])}</h3><span class="more">Read the article →</span></a>'
        for i, o in enumerate(others))
    out += f"""<main id="main">
<section class="page-hero short">
  <div class="ph" style="background-image:url('{IMG.format(id=a['image'], w=2200)}')" role="img" aria-label="{e(a['image_alt'])}"></div>
  <div class="veil"></div>
  <div class="wrap">
    <div class="crumbs ld d1"><a href="/">Home</a><span>/</span><a href="/insights/">Insights</a><span>/</span>{e(a['category'])}</div>
    <h1 class="ld d2" style="max-width:1000px">{e(a['title'])}</h1>
    <p class="lede ld d3">{e(a['description'])}</p>
  </div>
</section>

<article class="post"><div class="wrap">
  <div class="meta-row"><b>{e(a['category'])}</b><span>{PUBLISHED_HUMAN}</span><span>{minutes} min read</span><span>By {AUTHOR}</span></div>
  <div class="post-body">
    <div class="takeaways"><h3>Key takeaways</h3><ul>{takeaways}</ul></div>
{a['body'].strip()}
  </div>
  <div class="post-end"><p>Facing a decision like this at your institution?</p><a class="btn solid" href="/contact" data-calendly>Book an introductory call</a></div>
</div></article>

<section class="pad" style="border-top:1px solid var(--hair);margin-top:90px"><div class="wrap">
  <div class="head" style="margin-bottom:56px"><div class="label rv">More Insights</div><div><h2 class="rv s2">Continue <em>reading.</em></h2></div></div>
  <div class="cards">{related}</div>
</div></section>
</main>

{footer}

<script src="/assets/js/site.js"></script>
</body>
</html>
"""
    return out

out_dir = SITE / 'insights'
out_dir.mkdir(exist_ok=True)
for i, a in enumerate(ARTICLES):
    others = [ARTICLES[(i + k) % len(ARTICLES)] for k in (1, 2, 3)]
    (out_dir / f'{a["slug"]}.html').write_text(page(a, others), encoding='utf-8')
    print(f'{a["slug"]:34} {words(a["body"]):5} words')
