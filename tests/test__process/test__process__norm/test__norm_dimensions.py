import unittest

from model.norm.norm import Norm
from process.norm.norm_dimensions import NormDimensions


MINIMAL_YAML = """
identifier: '<ignore>'
title:
  en: '<ignore>'
intro:
  en: '<ignore>'
scope:
  en: '<ignore>'
triggers:
- en: '<ignore>'
criteria:
- en: '<ignore>'
objectives:
- en: '<ignore>'
risks:
- en: '<ignore>'
indicators:
- identifier: '<ignore>'
  title:
    en: '<ignore>'
  description:
    en: '<ignore>'
  conformities:
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
  explanation:
    en: '<ignore>'
""".strip()


MORE_LANGUAGES_YAML = """
identifier: '<ignore>'
title:
  en: '<ignore>'
  nl: '<negeer>'
intro:
  en: '<ignore>'
  nl: '<negeer>'
scope:
  en: '<ignore>'
  nl: '<negeer>'
triggers:
- en: '<ignore>'
  nl: '<negeer>'
criteria:
- en: '<ignore>'
  nl: '<negeer>'
objectives:
- en: '<ignore>'
  nl: '<negeer>'
risks:
- en: '<ignore>'
  nl: '<negeer>'
drivers:
- name: '<ignore>'
indicators:
- identifier: '<ignore>'
  title:
    en: '<ignore>'
    nl: '<negeer>'
  description:
    en: '<ignore>'
    nl: '<negeer>'
  conformities:
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
      nl: '<negeer>'
    guidance:
      en: '<ignore>'
      nl: '<negeer>'
  explanation:
    en: '<ignore>'
    nl: '<negeer>'
references:
- name: '<ignore>'
  url: https://optional.url
  notes:
  - en: '<ignore>'
    nl: '<negeer>'
""".strip()


MORE_PARTS_YAML = """
identifier: '<ignore>'
title:
  en: '<ignore>'
intro:
  en: '<ignore>'
scope:
  en: '<ignore>'
triggers:
- en: '<ignore>'
- en: '<ignore>'
- en: '<ignore>'
criteria:
- en: '<ignore>'
- en: '<ignore>'
- en: '<ignore>'
objectives:
- en: '<ignore>'
- en: '<ignore>'
- en: '<ignore>'
risks:
- en: '<ignore>'
- en: '<ignore>'
- en: '<ignore>'
drivers:
- name: '<ignore>'
  details:
  - '<ignore>'
  - '<ignore>'
  - '<ignore>'
- name: '<ignore>'
  details:
  - '<ignore>'
  - '<ignore>'
  - '<ignore>'
- name: '<ignore>'
  details:
  - '<ignore>'
  - '<ignore>'
  - '<ignore>'
indicators:
- identifier: '<ignore>'
  title:
    en: '<ignore>'
  description:
    en: '<ignore>'
  conformities:
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  explanation:
    en: '<ignore>'
- identifier: '<ignore>'
  title:
    en: '<ignore>'
  description:
    en: '<ignore>'
  conformities:
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  explanation:
    en: '<ignore>'
- identifier: '<ignore>'
  title:
    en: '<ignore>'
  description:
    en: '<ignore>'
  conformities:
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  - identifier: '<ignore>'
    description:
      en: '<ignore>'
    guidance:
      en: '<ignore>'
  explanation:
    en: '<ignore>'
references:
- name: '<ignore>'
  url: https://optional.url
  notes:
  - en: '<ignore>'
- name: '<ignore>'
  url: https://optional.url
  notes:
  - en: '<ignore>'
- name: '<ignore>'
  url: https://optional.url
  notes:
  - en: '<ignore>'
""".strip()


class TestNormDimensions(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_minimal(self):
        # given
        norm = Norm.from_yaml(MINIMAL_YAML)
        # when
        actual = NormDimensions.from_norm(norm)
        # then
        expect = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers=[],
            indicators=[1],
            references=0,
        )
        self.assertEqual(expect, actual)

    def test_more_languages(self):
        # given
        norm = Norm.from_yaml(MORE_LANGUAGES_YAML)
        # when
        actual = NormDimensions.from_norm(norm)
        # then
        expect = NormDimensions(
            languages=["en", "nl"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers=[0],
            indicators=[1],
            references=1,
        )
        self.assertEqual(expect, actual)

    def test_more_parts(self):
        # given
        norm = Norm.from_yaml(MORE_PARTS_YAML)
        # when
        actual = NormDimensions.from_norm(norm)
        # then
        expect = NormDimensions(
            languages=["en"],
            triggers=3,
            criteria=3,
            objectives=3,
            risks=3,
            drivers=[3, 3, 3],
            indicators=[3, 3, 3],
            references=3,
        )
        self.assertEqual(expect, actual)

    def test_minimal_vs_more_languages(self):
        # given
        dim1 = NormDimensions.from_norm(Norm.from_yaml(MINIMAL_YAML))
        dim2 = NormDimensions.from_norm(Norm.from_yaml(MORE_LANGUAGES_YAML))
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=["en", "nl"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers=[0],
            indicators=[1],
            references=1,
        )
        self.assertEqual(expect, actual)

    def test_minimal_vs_more_parts(self):
        # given
        dim1 = NormDimensions.from_norm(Norm.from_yaml(MINIMAL_YAML))
        dim2 = NormDimensions.from_norm(Norm.from_yaml(MORE_PARTS_YAML))
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=["en"],
            triggers=3,
            criteria=3,
            objectives=3,
            risks=3,
            drivers=[3, 3, 3],
            indicators=[3, 3, 3],
            references=3,
        )
        self.assertEqual(expect, actual)

    def test_more_languages_vs_more_parts(self):
        # given
        dim1 = NormDimensions.from_norm(Norm.from_yaml(MORE_LANGUAGES_YAML))
        dim2 = NormDimensions.from_norm(Norm.from_yaml(MORE_PARTS_YAML))
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=["en", "nl"],
            triggers=3,
            criteria=3,
            objectives=3,
            risks=3,
            drivers=[3, 3, 3],
            indicators=[3, 3, 3],
            references=3,
        )
        self.assertEqual(expect, actual)

    def test__merge__languages(self):
        # given
        dim1 = NormDimensions(
            languages=["bar"],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers=[],
            indicators=[],
            references=0,
        )
        dim2 = NormDimensions(
            languages=["foo"],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers=[],
            indicators=[],
            references=0,
        )
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=["bar", "foo"],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers=[],
            indicators=[],
            references=0,
        )
        self.assertEqual(expect, actual)

    def test__merge__numbers(self):
        # given
        dim1 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=3,
            objectives=0,
            risks=2,
            drivers=[],
            indicators=[],
            references=0,
        )
        dim2 = NormDimensions(
            languages=[],
            triggers=3,
            criteria=0,
            objectives=1,
            risks=0,
            drivers=[],
            indicators=[],
            references=4,
        )
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=[],
            triggers=3,
            criteria=3,
            objectives=1,
            risks=2,
            drivers=[],
            indicators=[],
            references=4,
        )
        self.assertEqual(expect, actual)

    def test__merge__lists(self):
        # given
        dim1 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers=[0, 3],
            indicators=[0, 3],
            references=0,
        )
        dim2 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers=[2, 2, 2],
            indicators=[2, 2, 2],
            references=0,
        )
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers=[2, 3, 2],
            indicators=[2, 3, 2],
            references=0,
        )
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
