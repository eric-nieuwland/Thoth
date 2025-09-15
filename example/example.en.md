# 000 - Thoth norm definitions

Starting with the fourth incarnation of the Secure Software Development (SSD) standards framework of the Dutch Center for Information security and Privacy protection (CIP) norm texts are managed and maintained as YAML definitions. This allows for tools to process the definitions, e.g. to render the texts in various formats. The base tool to create, manage, and maintain the YAML definitions is called 'thoth'. This norm text is not a part of SSD itself but serves as demonstration and documentation of the file format of the YAML definitions supported by 'thoth'. Please note definitions are designed to support multi-lingual texts. Each text fragment that can be defined in multiple languages is prefixed by a two-character language code (ISO 639), e.g. 'en' (English) or 'nl' (Dutch).

## scope

The scope defines to which aspect(s) of an application the norm applies.

## triggers

- A trigger defines when the norm is applicable. Triggers may be repeated as often as needed.

## criteria

- A criterium defines an aspect of compliance with the norm. Criteria may be repeated as often as needed.

## objectives

- An objective defines a goal to achieve by adherence to the norm. Objectives may be repeated as often as needed.

## risks

- A risk defines a negative effect that may result from non-adherence to the norm. Risks may be repeated as often as needed.

## drivers

| Well-known source | Bekende bron |
| --- | --- |
| Examples of names are 'NIST', 'ISO27002:2022', and 'BIO'<br/>A driver defines a(n informational) source for the norm<br/>A driver's detail refer to specific parts within the source<br/>Details may be repeated as often as needed.<br/>Drivers may be repeated as often as needed.<br/>As drivers only contain codes, they do not support multiple languages | Voorbeelden van namen zijn 'NIST', 'ISO27002:2022' en 'BIO'<br/>Een driver definieert een (informatie) bron voor de norm<br/>Een detail van een driver verwijst naar specifieke onderdelen van de bron<br/>Details mogen zo vaak als nodig herhaald worden.<br/>Drivers mogen zo vaak als nodig herhaald worden.<br/>Omdat drivers alleen codes bevatten, zijn ze niet meertalig |

## indicators

### 01 An indicator has a title and a description

An indicator defines how to comply with a norm. Indicators may be repeated as often as needed and should have consecutively numbered identifiers. Identifiers should have a fixed number of digits; this requires quotes around the identifier.

#### conformity indicators

01/01
: A conformity defines a detail of the indicator. Conformities may be repeated as often as needed and should have consecutively numbered identifiers. Identifiers should have a fixed number of digits; this requires quotes around the identifier.
: _Each conformity may provide guidance for e.g. developers or auditors._

#### explanation

An indicator must provide an explanation as to how it contributes to the objective(s).



## references

Title or other reference - [https://optional.url](https://optional.url)

- A note may provide some additional information. Notes may be repeated as often as needed.
- References may be repeated as often as needed.

ISO 639 (Language codes) - [https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)

- Source of the two-character language codes used by 'thoth'.




rendered by Thoth on 2025/09/15 at 13:11 in 'en' from example.yaml