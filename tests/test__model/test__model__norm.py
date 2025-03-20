import unittest


from model.norm import Norm

class TestNormLoremIpsum(unittest.TestCase):
    """
    tests using the lorem_ipsum() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_lorem_ipsum_python(self):
        """
        conversion to plain Python objects
        """
        # given
        norm = Norm.lorem_ipsum()
        # when
        actual = norm.model_dump()
        # then
        expect = {
            "identifier": "identifioram normii",
            "title": {
                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
            },
            "intro": {
                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
            },
            "scope": {
                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
            },
            "triggers": [
                {
                    "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                    "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                },
            ],
            "criteria": [
                {
                    "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                    "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                },
            ],
            "objectives": [
                {
                    "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                    "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                },
            ],
            "risks": [
                {
                    "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                    "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                },
            ],
            "drivers": [
                {
                    "name": "driverius namum",
                    "details": [
                        "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    ],
                },
            ],
            "indicators": [
                {
                    "identifier": "identificatio indicatros",
                    "title": {
                        "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    },
                    "description": {
                        "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    },
                    "conformities": [
                        {
                            "identifier": "identia conformus",
                            "description": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                            "guidance": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                        },
                        {
                            "identifier": "identia conformus",
                            "description": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                            "guidance": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                        },
                    ],
                    "explanation": {
                        "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    },
                },
                {
                    "identifier": "identificatio indicatros",
                    "title": {
                        "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    },
                    "description": {
                        "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    },
                    "conformities": [
                        {
                            "identifier": "identia conformus",
                            "description": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                            "guidance": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                        },
                        {
                            "identifier": "identia conformus",
                            "description": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                            "guidance": {
                                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                            },
                        },
                    ],
                    "explanation": {
                        "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                        "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                    },
                },
            ],
            "references": [
                {
                    "name": "referentia namum",
                    "url": "http://loremipsum.io",
                    "notes": [
                        {
                            "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                            "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
                        },
                    ],
                },
            ],
        }
        self.assertDictEqual(expect, actual)

    def test_lorem_ipsum_yaml(self):
        """
        conversion to YAML definition
        """
        # given
        norm = Norm.lorem_ipsum()
        # when
        actual = norm.as_yaml().strip()
        # then
        expect = """
identifier: identifioram normii
title:
  en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
intro:
  en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
scope:
  en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
triggers:
- en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
criteria:
- en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
objectives:
- en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
risks:
- en: Lorem ipsum odor amet, consectetuer adipiscing elit.
  nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
drivers:
- name: driverius namum
  details:
  - Lorem ipsum odor amet, consectetuer adipiscing elit.
  - Ut odio quis primis tortor phasellus nisl aptent auctor a.
indicators:
- identifier: identificatio indicatros
  title:
    en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  description:
    en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  conformities:
  - identifier: identia conformus
    description:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
    guidance:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  - identifier: identia conformus
    description:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
    guidance:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  explanation:
    en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
- identifier: identificatio indicatros
  title:
    en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  description:
    en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  conformities:
  - identifier: identia conformus
    description:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
    guidance:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  - identifier: identia conformus
    description:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
    guidance:
      en: Lorem ipsum odor amet, consectetuer adipiscing elit.
      nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
  explanation:
    en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
references:
- name: referentia namum
  url: http://loremipsum.io
  notes:
  - en: Lorem ipsum odor amet, consectetuer adipiscing elit.
    nl: Ut odio quis primis tortor phasellus nisl aptent auctor a.
        """.strip()
        self.assertEqual(expect, actual)

    def test_lorem_ipsum_full_circle(self):
        """
        load YAML definition
        """
        # given
        norm = Norm.lorem_ipsum()
        # when
        actual = Norm.from_yaml(norm.as_yaml())
        # then
        self.assertIsNot(norm, actual)  # not the same object
        expect = norm
        self.assertEqual(expect, actual)  # but same data



if __name__ == '__main__':
    unittest.main()
