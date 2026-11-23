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
 'slug': 'introducing-trustforge',
 'category': 'News',
 'title': 'Introducing TrustForge: an AI agent for Oracle FLEXCUBE customization',
 'seo_title': 'Introducing TrustForge: AI Agent for FLEXCUBE | TrustRoute',
 'description': 'TrustForge is an AI agent, built on Anthropic, that turns a FLEXCUBE change described in plain words into files ready to load in ODT.',
 'image': '1504639725590-34d0984388bd',
 'image_alt': 'Code on a screen, seen through a pair of glasses',
 'takeaways': [
   'TrustForge turns a FLEXCUBE change described in plain words into ODT-ready files.',
   'Every change goes in the CUSTOM layer; Oracle code stays as shipped.',
   'Nothing is built until you approve the plan.',
   'Supports FLEXCUBE Universal Banking 14.6 and 14.7; start free today.',
 ],
 'body': """
<p class="lead">Every bank running Oracle FLEXCUBE knows the pattern: a small change to a screen or a charge becomes weeks of analysis, scarce ODT specialists and a sizeable invoice. Today we are introducing <a href="/trustforge">TrustForge</a> to change that.</p>

<h2>What TrustForge is</h2>
<p>TrustForge is an AI agent for Oracle FLEXCUBE customization, built on Anthropic’s AI. It works like a senior ODT developer on your team: it understands radxml, release layers and hook packages, and the rules that make a screen load, save and deploy. It supports FLEXCUBE Universal Banking 14.6 and 14.7, and its output has been verified end to end on 14.7.0.6.0.</p>

<h2>How it works</h2>
<ol>
<li><strong>Describe:</strong> say what you need in plain words and upload your development objects: radxml, table definitions, packages or JavaScript.</li>
<li><strong>Discuss:</strong> TrustForge asks only what it needs and agrees the plan with you, item by item.</li>
<li><strong>Build:</strong> once you approve, it builds each file and checks it against ODT’s load and save rules.</li>
<li><strong>Deliver:</strong> you download the files, the deploy order and unit tests, ready to load in ODT.</li>
</ol>

<h2>Six kinds of job</h2>
<p>New FLEXCUBE screens, changes to Oracle’s own functions in the CUSTOM layer, radxml reviews, hook packages and release JavaScript, Silent ODT for bulk generation and web services, and answers to ODT questions from the guides.</p>

<h2>Built for <em>how banks work</em></h2>
<ul>
<li><strong>Oracle’s code is never edited.</strong> Changes go in the CUSTOM layer and Oracle values are checked, so upgrades stay safe.</li>
<li><strong>Nothing without approval.</strong> You see the plan and the files before anything is built.</li>
<li><strong>No secrets in files.</strong> Passwords and keys are left as placeholders for your team.</li>
<li><strong>Your data stays yours.</strong> Uploaded objects are used for your job only, and a private install keeps everything inside your network.</li>
</ul>

<h2>Real jobs, real results</h2>
<p>On a live FLEXCUBE 14.7 environment, TrustForge built a new customer risk profile screen (STDCURSK) that is now deployed and in use. On another job it added a complete sixth charge to Oracle’s ARC maintenance (IFDATMMN): 36 new fields in the CUSTOM layer, with no Oracle values changed.</p>

<h2>Start free</h2>
<p>The Free plan includes radxml reviews and ODT questions. The Partner plan is $100 USD per seat per month with all six job types, and banks can arrange a private install in their own cloud. For many changes, that means up to 90% lower development cost; savings depend on scope, and your team still reviews, deploys and tests every change.</p>
<p>Start your first job at <a href="https://forge.trustroutetechnologies.com/" target="_blank" rel="noopener">forge.trustroutetechnologies.com</a>, or read more on the <a href="/trustforge">TrustForge page</a>.</p>
""",
},
{
 'slug': 'introducing-ai-and-agency-banking',
 'category': 'News',
 'title': 'Introducing AI Banking, Agency Banking, SettleDesk and TrustCTS',
 'seo_title': 'New: AI & Agency Banking, SettleDesk, TrustCTS | TrustRoute',
 'description': 'Four new TrustRoute solutions: AI Banking, Agency Banking, SettleDesk for bulk payments and TrustCTS for cheque truncation and clearing.',
 'image': '1531746790731-6c087fecd65a', 'image_alt': 'A white robotic hand, representing artificial intelligence',
 'takeaways': [
   'AI Banking brings AI to customers, staff and risk teams, with people in control.',
   'Agency Banking turns local shops and outlets into points of service.',
   'SettleDesk checks every bulk payment against your bank before the money moves.',
   'TrustCTS clears every cheque within the window and posts it exactly once.',
   'All four integrate with your core banking system; demonstrations are available now.',
 ],
 'body': """
<p class="lead">Today we are introducing four new solutions. Each answers the same question that banks ask us most often: how do we serve more customers, better, without adding cost and risk?</p>

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

<h2>SettleDesk: every bulk payment, <em>checked first</em></h2>
<p>Payroll, vendor payments, tax and refunds usually arrive as files, and a single bad record can become a costly mistake. <a href="/settledesk">SettleDesk</a> checks every record against the bank's own systems before any money moves:</p>
<ul>
<li><strong>Checks against your bank, not just the file:</strong> migrated account numbers, live account and balance checks, duplicates across files, limits, approved payees, sanctions screening and risk scoring.</li>
<li><strong>Held, not half-paid:</strong> if any record fails, the whole file is held, corrected on the spot and reprocessed, and the person who corrects it cannot approve it.</li>
<li><strong>Approved, delivered and settled:</strong> approval chains on the web or mobile, delivery to any bank system, and tracking of every payment through to settlement and reconciliation.</li>
</ul>
<p>New file layouts are set up in the console without code, and every decision is recorded permanently, ready for audit.</p>

<h2>TrustCTS: every cheque, <em>cleared with certainty</em></h2>
<p>Cheques remain an important payment method in many markets, and continuous clearing leaves little room for delay. <a href="/trustcts">TrustCTS</a> is a cheque truncation and clearing platform that connects branch scanners, the clearing house and core banking:</p>
<ul>
<li><strong>Capture you can trust:</strong> image quality and MICR checked at the scanner and again on the server, with no browser plug-ins and store-and-forward if the network drops.</li>
<li><strong>Decided within the clearing window:</strong> inward cheques are prioritised by live expiry clocks, with straight-through decisions and signature referrals.</li>
<li><strong>Money moves exactly once:</strong> every posting goes through an idempotent journal, and unknown outcomes are resolved by inquiry, never by a blind retry.</li>
<li><strong>Reconciled three ways:</strong> clearing house, core banking and TrustCTS, with GL checks and break management.</li>
</ul>
<p>Clearing rules live in scheme packs, so new schemes plug in without changing the core; packs for India (NPCI CTS) and the Eastern Caribbean (ECACH) are in development.</p>

<h2>Built to work together</h2>
<p>All four solutions integrate with your core banking system and complement our existing range. The AI assistant can run alongside <a href="/whatsapp-banking">WhatsApp Banking</a>; agents give <a href="/wallet-banking">Wallet Banking</a> customers convenient places to cash in and out; SettleDesk delivers checked payment files straight into core systems, including Oracle FLEXCUBE; TrustCTS is pre-integrated with Oracle FLEXCUBE; and <a href="/meridian">Meridian</a> brings it all together in a single view of each customer.</p>

<h2>See them in action</h2>
<p>Demonstrations of AI Banking, Agency Banking, SettleDesk and TrustCTS are available now. If you are exploring AI, agent networks, safer bulk payments or cheque clearing at your institution, we would be glad to show you, and to talk through how each would fit your systems, your customers and your regulator.</p>
""",
},
{
 'slug': 'flexcube-custom-layer',
 'category': 'Core Banking',
 'title': 'The CUSTOM layer: customizing Oracle FLEXCUBE without breaking upgrades',
 'seo_title': 'FLEXCUBE CUSTOM Layer: Customize Without Breaking Upgrades',
 'description': 'How Oracle FLEXCUBE release layers work, what belongs in the CUSTOM layer, and a checklist for customizations that survive the next upgrade.',
 'image': '1554469384-e58fac16e23a',
 'image_alt': 'Curved glass facade of a modern building',
 'takeaways': [
   'FLEXCUBE separates Oracle code (KERNEL) from bank changes (CUSTOM).',
   'Customizations made in the CUSTOM layer survive upgrades; edits to KERNEL do not.',
   'New fields belong in extension tables, with labels and amendable settings.',
   'Check that no Oracle value changes before you load anything.',
 ],
 'body': """
<p class="lead">The most expensive FLEXCUBE customization is not the one that takes longest to build. It is the one that breaks at the next upgrade. Release layers are how you avoid that.</p>

<h2>How release layers work</h2>
<p>Oracle FLEXCUBE separates what Oracle ships from what a bank adds. Oracle’s own definitions live in the <strong>KERNEL</strong> layer. Regional or group variations can sit in a <strong>CLUSTER</strong> layer, and a bank’s own changes belong in the <strong>CUSTOM</strong> layer. At runtime, the layers combine, so a screen can show Oracle’s fields together with your own.</p>
<p>The rule that keeps upgrades safe is simple: never change KERNEL. When Oracle ships a new release, KERNEL is replaced. Anything edited there is lost or, worse, silently conflicts with the new code.</p>

<h2>What belongs <em>in the CUSTOM layer</em></h2>
<ul>
<li><strong>Screen changes</strong> in the CUSTOM section of the function’s radxml: new fields, tabs, sections and sub-screens, built in ODT.</li>
<li><strong>New data</strong> in extension tables linked to Oracle’s tables, rather than new columns on Oracle’s own tables.</li>
<li><strong>Back-end logic</strong> in the CUSTOM hook package (named for the module and function, ending in _CUSTOM) for validations, defaulting and processing.</li>
<li><strong>Front-end logic</strong> in the CUSTOM release JavaScript for the function.</li>
<li><strong>Labels and static data</strong> scripted alongside, so every environment gets the same result.</li>
</ul>

<h2>The details that cause trouble</h2>
<p>Most failed customizations fail on small things. New fields that are not marked as amendable cannot be changed on Modify, and FLEXCUBE reports an amendment error. Lists of values with poorly bound queries slow screens on large tables. Labels missing from one environment make a screen look broken in UAT. The TrustForge guides cover several of these in depth, including <a href="https://forge.trustroutetechnologies.com/learn/flexcube-st-amnd-002-amendable" target="_blank" rel="noopener">fixing ST-AMND-002 on Modify</a> and <a href="https://forge.trustroutetechnologies.com/learn/flexcube-add-field-to-screen" target="_blank" rel="noopener">adding a field in the CUSTOM layer</a>.</p>

<h2>A checklist before you load</h2>
<ol>
<li>Every new element is tagged to the CUSTOM layer and your release.</li>
<li>No Oracle (KERNEL) value has changed. Compare before and after.</li>
<li>New fields have their data source, block field, field set, labels and amendable settings.</li>
<li>Hook code only extends Oracle logic; it skips or replaces it only where that is the agreed design.</li>
<li>No passwords or keys appear in any file.</li>
<li>Deploy order and unit tests are written down, and the change is tested in your own environments.</li>
</ol>

<p><a href="/trustforge">TrustForge</a> applies this discipline automatically: it builds in the CUSTOM layer only and checks that no Oracle value changes, so your team can focus on review and testing.</p>
""",
},
{
 'slug': 'ai-flexcube-governance-checklist',
 'category': 'Strategy',
 'title': 'AI for FLEXCUBE development: a governance checklist for bank CIOs',
 'seo_title': 'AI for FLEXCUBE Development: A CIO Governance Checklist',
 'description': 'AI can cut the cost of core banking development, but banks need controls. A practical governance checklist for using AI on Oracle FLEXCUBE.',
 'image': '1600880292203-757bb62b4baf',
 'image_alt': 'Professionals reviewing work together',
 'takeaways': [
   'Share development objects only: never customer or production data.',
   'Keep a person approving every plan and every file.',
   'Enforce layer discipline and keep secrets out of generated code.',
   'Choose a deployment model your risk and compliance teams can sign off.',
 ],
 'body': """
<p class="lead">AI agents can now design FLEXCUBE screens, write hook code and review radxml in minutes. For a bank, the question is not whether the technology works, but whether it can be used under the controls a regulator expects.</p>

<h2>1. Decide what may be shared</h2>
<p>Limit AI tools to development objects: radxml, table definitions, packages and JavaScript. Customer data, production extracts and credentials should never be uploaded. Write this down as policy, and choose tools that make it easy to follow.</p>

<h2>2. Keep a person <em>in charge of every change</em></h2>
<p>The AI should propose; your developers should decide. Require a plan that is reviewed and approved before anything is built, and keep the existing review, deployment and testing steps for the files it produces.</p>

<h2>3. Enforce layer discipline</h2>
<p>Generated changes should live in the CUSTOM layer only, with a check that Oracle’s KERNEL values are unchanged. This protects upgrades and makes every change easy to identify and roll back.</p>

<h2>4. Keep secrets out of code</h2>
<p>Passwords, keys and connection strings should appear only as placeholders in generated files, to be filled in by your team through your normal secrets process.</p>

<h2>5. Choose the right deployment model</h2>
<p>Hosted tools are fastest to adopt. Where data must stay inside the bank, look for a private install that runs in your own cloud on your own model account, such as Anthropic, AWS Bedrock or Google Vertex, so nothing leaves your network.</p>

<h2>6. Keep the record</h2>
<p>Retain each job’s request, agreed plan and delivered files alongside your change records, so audit can see what was asked, what was approved and what was deployed.</p>

<h2>7. Measure the value</h2>
<p>Track cost and time per change before and after adoption, and how much rework testing finds. That evidence turns a promising pilot into an approved programme.</p>

<p>TrustForge was designed around these controls: development objects only, approval before building, CUSTOM layer only, no secrets in files, and an optional private install. Read more on the <a href="/trustforge">TrustForge page</a> or the guide to <a href="https://forge.trustroutetechnologies.com/learn/ai-assistant-core-banking-development" target="_blank" rel="noopener">using an AI assistant for core banking development, safely</a>.</p>
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
 'seo_title': 'Why SMS Banking Reaches Customers Apps Cannot | TrustRoute',
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
 'seo_title': 'Choosing a Payment Switch: Key RFP Questions | TrustRoute',
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
