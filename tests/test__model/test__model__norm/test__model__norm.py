import unittest


from model.norm.norm import Norm

class TestTemplate(unittest.TestCase):
    """
    tests using the template() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_template_python(self):
        """
        conversion to plain Python objects
        """
        # given
        norm = Norm.template("en")
        # when
        actual = norm.model_dump()
        # then
        expect = {
            "identifier": "|[ norm identifier ]|",
            "title": {
                "en": "|[ please fill with text ]|",
            },
            "intro": {
                "en": "|[ please fill with text ]|",
            },
            "scope": {
                "en": "|[ please fill with text ]|",
            },
            "triggers": [
                {
                    "en": "|[ please fill with text ]|",
                },
            ],
            "criteria": [
                {
                    "en": "|[ please fill with text ]|",
                },
            ],
            "objectives": [
                {
                    "en": "|[ please fill with text ]|",
                },
            ],
            "risks": [
                {
                    "en": "|[ please fill with text ]|",
                },
            ],
            "drivers": [
                {
                    "name": "|[ please name driver ]|",
                    "details": [
                        "|[ driver detail #1 ]|",
                        "|[ driver detail #2 ]|",
                    ],
                },
            ],
            "indicators": [
                {
                    "identifier": "01",
                    "title": {
                        "en": "|[ please fill with text ]|",
                    },
                    "description": {
                        "en": "|[ please fill with text ]|",
                    },
                    "conformities": [
                        {
                            "identifier": "01",
                            "description": {
                                "en": "|[ please fill with text ]|",
                            },
                            "guidance": {
                                "en": "|[ please fill with text ]|",
                            },
                        },
                        {
                            "identifier": "02",
                            "description": {
                                "en": "|[ please fill with text ]|",
                            },
                            "guidance": {
                                "en": "|[ please fill with text ]|",
                            },
                        },
                    ],
                    "explanation": {
                        "en": "|[ please fill with text ]|",
                    },
                },
                {
                    "identifier": "02",
                    "title": {
                        "en": "|[ please fill with text ]|",
                    },
                    "description": {
                        "en": "|[ please fill with text ]|",
                    },
                    "conformities": [
                        {
                            "identifier": "01",
                            "description": {
                                "en": "|[ please fill with text ]|",
                            },
                            "guidance": {
                                "en": "|[ please fill with text ]|",
                            },
                        },
                        {
                            "identifier": "02",
                            "description": {
                                "en": "|[ please fill with text ]|",
                            },
                            "guidance": {
                                "en": "|[ please fill with text ]|",
                            },
                        },
                    ],
                    "explanation": {
                        "en": "|[ please fill with text ]|",
                    },
                },
            ],
            "references": [
                {
                    "name": "|[ please name reference ]|",
                    "url": "https://optional.url",
                    "notes": [
                        {
                            "en": "|[ please fill with text ]|",
                        },
                    ],
                },
            ],
        }
        self.assertDictEqual(expect, actual)

    def test_template_yaml(self):
        """
        conversion to YAML definition
        """
        # given
        norm = Norm.template("en")
        # when
        actual = norm.as_yaml().strip()
        # then
        expect = """
identifier: '|[ norm identifier ]|'

title:
  en: '|[ please fill with text ]|'

intro:
  en: '|[ please fill with text ]|'

scope:
  en: '|[ please fill with text ]|'

triggers:
- en: '|[ please fill with text ]|'

criteria:
- en: '|[ please fill with text ]|'

objectives:
- en: '|[ please fill with text ]|'

risks:
- en: '|[ please fill with text ]|'

drivers:

- name: '|[ please name driver ]|'
  details:
  - '|[ driver detail #1 ]|'
  - '|[ driver detail #2 ]|'

indicators:
# ============================================================================
- identifier: '01'
  title:
    en: '|[ please fill with text ]|'
  description:
    en: '|[ please fill with text ]|'

  conformities:
  # ------------------------------------------
  - identifier: '01'
    description:
      en: '|[ please fill with text ]|'
    guidance:
      en: '|[ please fill with text ]|'
  # ------------------------------------------
  - identifier: '02'
    description:
      en: '|[ please fill with text ]|'
    guidance:
      en: '|[ please fill with text ]|'
  # ------------------------------------------

  explanation:
    en: '|[ please fill with text ]|'
# ============================================================================
- identifier: '02'
  title:
    en: '|[ please fill with text ]|'
  description:
    en: '|[ please fill with text ]|'

  conformities:
  # ------------------------------------------
  - identifier: '01'
    description:
      en: '|[ please fill with text ]|'
    guidance:
      en: '|[ please fill with text ]|'
  # ------------------------------------------
  - identifier: '02'
    description:
      en: '|[ please fill with text ]|'
    guidance:
      en: '|[ please fill with text ]|'
  # ------------------------------------------

  explanation:
    en: '|[ please fill with text ]|'
# ============================================================================

references:

- name: '|[ please name reference ]|'
  url: https://optional.url
  notes:
  - en: '|[ please fill with text ]|'
""".strip()
        self.assertEqual(expect, actual)

    def test_template_full_circle(self):
        """
        load YAML definition
        """
        # given
        norm = Norm.template("en")
        # when
        actual = Norm.from_yaml(norm.as_yaml())
        # then
        self.assertIsNot(norm, actual)  # not the same object
        expect = norm
        self.assertEqual(expect, actual)  # but same data


if __name__ == "__main__":
    unittest.main()
