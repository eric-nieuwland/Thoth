# 000 - Thoth normdefinities

Met de komst van versie 4 van het normenkader voor Secure Software Development (SSD) van het Centrum voor Informatiebeveiliging en Privacybescherming (CIP) worden normteksten beheerd en onderhouden als YAML-definities. Hierdoor kunnen tools gebruikt worden om bijvoorbeeld teksten op te maken in verschillende documentformaten. De basistool voor het maken, beheren en onderhouden van de YAML-definities hete 'thoth'. Deze normtekst is geen onderdeel van SSD zelf, maar dient als demonstratie en documentatie van het bestandsformaat van de YAML-definitie die 'thoth' ondersteunt. Merk op dat de definities bedoeld zijn om meertaligheid te ondersteunen. Elk tekstfragment dat in meerdere talen kan worden gedefinieerd, wordt vooraf gegaan door de twee-lettercode van de taal (ISO 639), bijvoorbeeld 'en' (Engels) of 'nl' (Nederlands).

## scope

De scope definieert op welk(e) aspect(en) van een applicatie de norm van toepassing is.

## triggers

- Een trigger definieert wanneer de norm van toepassing is. Triggers mogen zo vaak als nodig herhaald worden.

## criteria

- Een criterium definieert een aspect van voldoen aan de norm. Criteria mogen zo vaak als nodig herhaald worden.

## objectives

- Een objective definieert een te bereiken doel, door aan de norm te voldoen. Objective mogen zo vaak als nodig herhaald worden.

## risks

- Een risico (risk) definieert een negatief effect dat kan optreden wanneer niet aan de norm voldaan wordt. Risico's (risks) mogen zo vaak als nodig herhaald worden.

## drivers

| Well-known source | Bekende bron |
| --- | --- |
| Examples of names are 'NIST', 'ISO27002:2022', and 'BIO'<br/>A driver defines a(n informational) source for the norm<br/>A driver's detail refer to specific parts within the source<br/>Details may be repeated as often as needed.<br/>Drivers may be repeated as often as needed.<br/>As drivers only contain codes, they do not support multiple languages | Voorbeelden van namen zijn 'NIST', 'ISO27002:2022' en 'BIO'<br/>Een driver definieert een (informatie) bron voor de norm<br/>Een detail van een driver verwijst naar specifieke onderdelen van de bron<br/>Details mogen zo vaak als nodig herhaald worden.<br/>Drivers mogen zo vaak als nodig herhaald worden.<br/>Omdat drivers alleen codes bevatten, zijn ze niet meertalig |

## indicators

### 01 Een indicator heeft een titel en een beschrijving

Een indicator definieert hoe aan een norm voldaan moet worden. Indicators mogen zo vaak als nodig herhaald worden en moeten opvolgend genummerde identifier hebben. Identifiers moeten een vast aantal cijfers bevatten; dit vereist quotes rond de identifier.

#### conformity indicators

01/01
: Een conformiteit (conformity) definieert een detail van een indicator. Conformiteiten (conformities) mogen zo vaak als nodig herhaald worden en moeten opvolgend genummerde identifier hebben. Identifiers moeten een vast aantal cijfers bevatten; dit vereist quotes rond de identifier.
: _Elke conformiteit mag voorzien in een richtsnoer (guidance) voor bijvoorbeeld ontwikkelaars of auditors._

#### explanation

Een indicator moet uitleg (explanation) geven van de bijdrage die het levert aan een of meer objectives.



## references

Title or other reference - [https://optional.url](https://optional.url)

- Een opmerking (note) kan aanvullende informatie geven. Opmerkingen (notes) mogen zo vaak als nodig herhaald worden.
- References mogen zo vaak als nodig herhaald worden.

ISO 639 (Language codes) - [https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)

- Bron van de twee-lettercodes die 'thoth' gebruikt.




rendered by Thoth on 2025/09/15 at 13:11 in 'nl' from example.yaml