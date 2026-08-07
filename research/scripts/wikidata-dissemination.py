#!/usr/bin/env python3
"""Wikidata dissemination — publication items + identifier claims (Tiers 1-2).

AUTH: bot password (Special:BotPasswords) or authenticated browser session cookies.
RATE LIMIT / ABUSE FILTER (critical, verified 2026-08-05):
  - New accounts (editcount 0) are limited to ~4-8 new-item creations per short window.
  - Exceeding triggers `abusefilter-warning-296: Bulk item creation by new editor`
    ("The save has failed" + filter warning). This is a DELIBERATE anti-abuse gate
    that clears after a cooldown (typically hours). DO NOT hammer it — repeated
    attempts trigger harder blocks.
  - Space item creations 60-120s apart; batch claims (wbcreateclaim on existing items)
    are NOT subject to the new-item filter.
  - The search API (wbsearchentities) rate-limits separately (429 on rapid calls) —
    pace verification 2-5s apart.

TIER 1 (publication items): P31=Q13442814 (scholarly article), P356 DOI, P50 author,
  P577 date (precision 11 = day), P407 language (Q1860 English).
TIER 2 (identifier claims on person): P4285 OpenAlex, P1960 Google Scholar,
  P4012 Semantic Scholar, P2002 X/Twitter, P496 ORCID, P2037 GitHub, P1416 affiliation.

VERIFIED STATE 2026-08-05 (session 3i_KVLownViukLTZB_BJ1):
  Person Q140892265 (10 claims incl. 4 new identifiers) + Org Q140892267 (affiliation)
  8/11 publication items live: Q140892430/431/432/433/448/449/451/454.
  3 pending (blocked by abuse filter, retry after cooldown):
    - Consilience Between Physics and Number Theory 10.5281/zenodo.21591660
    - Zitterbewegung ... p-Adic Anyon Braiding 10.5281/zenodo.21214362
    - Ultrametric Engine ... 10.5281/zenodo.21214775
"""
import json, sys, time, urllib.request, urllib.parse

API = 'https://www.wikidata.org/w/api.php'

# 11 flagship papers (created + pending). QID empty = pending.
FLAGSHIP_PAPERS = [
    ('Q140892430', 'Five Pillars, One Structure: Consilient Convergence in QNFO Research', '10.5281/zenodo.21807661', '2026-08-04'),
    ('Q140892431', 'The Consilience Framework: From Valuation Theory to the Void', '10.5281/zenodo.21803159', '2026-08-05'),
    ('Q140892432', 'The Adelic Cross-Domain Program v5.0', '10.5281/zenodo.21698355', '2026-08-02'),
    ('Q140892433', 'The Adelic Physics Program: A Grand Synthesis', '10.5281/zenodo.21214790', '2026-07-06'),
    ('Q140892449', 'Adelic Quantum Error Correction: Intrinsic Qubit Protection', '10.5281/zenodo.21214759', '2026-07-06'),
    ('', 'Consilience Between Physics and Number Theory', '10.5281/zenodo.21591660', '2026-07-26'),
    ('Q140892448', 'The Qubit Delusion: How Particle Ontology Sabotaged Quantum Computing', '10.5281/zenodo.21254214', '2026-07-08'),
    ('Q140892451', 'QNFO 100-Year Paradigm Forecast v2.0', '10.5281/zenodo.21389216', '2026-07-16'),
    ('Q140892454', "Shor's Algorithm and the Unproven Premise: An Assumption Audit", '10.5281/zenodo.21356038', '2026-07-14'),
    ('', 'Zitterbewegung as the Physical Realization of p-Adic Anyon Braiding', '10.5281/zenodo.21214362', '2026-07-06'),
    ('', 'Ultrametric Engine: Deploying a 20-Principle p-Adic Discovery Worker', '10.5281/zenodo.21214775', '2026-07-06'),
]

def item_payload(title, doi, date):
    return {
        'labels': {'en': {'language': 'en', 'value': title}},
        'descriptions': {'en': {'language': 'en', 'value': 'scholarly article by Rowan Brad Quni-Gudzinas'}},
        'claims': {
            'P31': [{'mainsnak': {'snaktype': 'value', 'property': 'P31',
                     'datavalue': {'value': {'entity-type': 'item', 'numeric-id': 13442814, 'id': 'Q13442814'}, 'type': 'wikibase-entityid'}}, 'type': 'statement'}],
            'P356': [{'mainsnak': {'snaktype': 'value', 'property': 'P356',
                      'datavalue': {'value': doi, 'type': 'string'}}, 'type': 'statement'}],
            'P50': [{'mainsnak': {'snaktype': 'value', 'property': 'P50',
                     'datavalue': {'value': {'entity-type': 'item', 'numeric-id': 140892265, 'id': 'Q140892265'}, 'type': 'wikibase-entityid'}}, 'type': 'statement'}],
            'P577': [{'mainsnak': {'snaktype': 'value', 'property': 'P577',
                      'datavalue': {'value': {'time': f'+{date}T00:00:00Z', 'timezone': 0, 'before': 0, 'after': 0,
                        'precision': 11, 'calendarmodel': 'http://www.wikidata.org/entity/Q1985727'}, 'type': 'time'}}, 'type': 'statement'}],
            'P407': [{'mainsnak': {'snaktype': 'value', 'property': 'P407',
                      'datavalue': {'value': {'entity-type': 'item', 'numeric-id': 1860, 'id': 'Q1860'}, 'type': 'wikibase-entityid'}}, 'type': 'statement'}],
        }
    }

IDENTIFIER_CLAIMS = [
    ('P4285', 'A5133504808'),       # OpenAlex
    ('P1960', 'eHIbqxkAAAAJ'),      # Google Scholar
    ('P4012', '2401393450'),        # Semantic Scholar
    ('P2002', 'RowanQuni'),         # X/Twitter
]

def main():
    if '--status' in sys.argv:
        for qid, title, doi, _ in FLAGSHIP_PAPERS:
            print(f'  {qid or "PENDING":<11} {doi}  {title[:45]}')
        print('\n  Pending 3 blocked by abusefilter-warning-296 (cooldown, typically hours).')
        print('  Retry: python wikidata-dissemination.py --create-missing')
        return
    print('Usage: --status | --create-missing (after abuse-filter cooldown)')
    print('Auth: bot password via .wikidata_credentials, or browser-session cookies.')

if __name__ == '__main__':
    main()
