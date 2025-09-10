import unittest

from thoth.model.norm_profile.profile import NormRenderProfile


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
        norm = NormRenderProfile.template()
        # when
        actual = norm.model_dump()
        # then
        expect = {
            "identifier": True,
            "title": True,
            "intro": True,
            "scope": True,
            "triggers": True,
            "criteria": True,
            "objectives": True,
            "risks": True,
            "drivers": {
                "name": True,
                "details": True,
            },
            "indicators": {
                "identifier": True,
                "title": True,
                "description": True,
                "conformities": {
                    "identifier": True,
                    "description": True,
                    "guidance": True,
                },
                "explanation": True,
            },
            "references": {
                "name": True,
                "url": True,
                "notes": True,
            },
        }
        self.assertDictEqual(expect, actual)

    def test_template_yaml(self):
        """
        conversion to YAML definition
        """
        # given
        norm = NormRenderProfile.template()
        # when
        actual = norm.as_yaml().strip()
        # then
        expect = """
identifier: true
title: true
intro: true
scope: true
triggers: true
criteria: true
objectives: true
risks: true
drivers:
  name: true
  details: true
indicators:
  identifier: true
  title: true
  description: true
  conformities:
    identifier: true
    description: true
    guidance: true
  explanation: true
references:
  name: true
  url: true
  notes: true
""".strip()
        self.assertEqual(expect, actual)

    def test_template_full_circle(self):
        """
        load YAML definition
        """
        # given
        norm = NormRenderProfile.template()
        # when
        actual = NormRenderProfile.from_yaml(norm.as_yaml())
        # then
        self.assertIsNot(norm, actual)  # not the same object
        expect = norm
        self.assertEqual(expect, actual)  # but same data



if __name__ == "__main__":
    unittest.main()
