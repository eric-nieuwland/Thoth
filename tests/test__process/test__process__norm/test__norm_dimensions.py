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


class TestNormDimensionsInit(unittest.TestCase):
    """
    test NormDimensions creation
    """

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
            drivers={},
            indicators={
                "<ignore>": [
                    "<ignore>",
                ],
            },
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
            drivers={
                "<ignore>": [],
            },
            indicators={
                "<ignore>": [
                    "<ignore>",
                ],
            },
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
            drivers={
                "<ignore>" : [
                    "<ignore>",
                    "<ignore>",
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>": [
                    "<ignore>",
                    "<ignore>",
                    "<ignore>",
                ],
            },
            references=3,
        )
        self.assertEqual(expect, actual)


class TestNormDimensionsJoin(unittest.TestCase):
    """
    test NormDimensions.__or__() function
    """

    def setUp(self):
        self.maxDiff = None

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
            drivers={
                "<ignore>" : [],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
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
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
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
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
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
            drivers={},
            indicators={},
            references=0,
        )
        dim2 = NormDimensions(
            languages=["<ignore>"],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        # when
        actual = dim1 | dim2
        # then
        expect = NormDimensions(
            languages=["<ignore>", "bar"],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
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
            drivers={},
            indicators={},
            references=0,
        )
        dim2 = NormDimensions(
            languages=[],
            triggers=3,
            criteria=0,
            objectives=1,
            risks=0,
            drivers={},
            indicators={},
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
            drivers={},
            indicators={},
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
            drivers={
                "<ignore 1>" : [
                    "<ignore 1.1>",
                ],
                "<ignore 2>": [
                    "<ignore 2.1>",
                ],
            },
            indicators={},
            references=0,
        )
        dim2 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={
                "<ignore 3>": [
                    "<ignore 3.1>",
                ],
                "<ignore 2>": [
                    "<ignore 2.1>",
                ],
            },
            indicators={},
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
            drivers={
                "<ignore 1>" : [
                    "<ignore 1.1>",
                ],
                "<ignore 2>": [
                    "<ignore 2.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.1>",
                ],
            },
            indicators={},
            references=0,
        )
        self.assertEqual(expect, actual)


class TestNormDimensionsSub(unittest.TestCase):
    """
    test NormDimensions.__sub__() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_zero_zero(self):
        # given
        dim1 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        dim2 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        # when
        actual = dim1 - dim2
        # then
        expect = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        self.assertEqual(expect, actual)

    def test_one_zero(self):
        # given
        dim1 = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            references=1,
        )
        dim2 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        # when
        actual = dim1 - dim2
        # then
        expect = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            references=1,
        )
        self.assertEqual(expect, actual)

    def test_zero_one(self):
        # given
        dim1 = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        dim2 = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            references=1,
        )
        # when
        actual = dim1 - dim2
        # then
        expect = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        self.assertEqual(expect, actual)

    def test_one_one(self):
        # given
        dim1 = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            references=1,
        )
        dim2 = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            indicators={
                "<ignore>" : [
                    "<ignore>",
                ],
            },
            references=1,
        )
        # when
        actual = dim1 - dim2
        # then
        expect = NormDimensions(
            languages=[],
            triggers=0,
            criteria=0,
            objectives=0,
            risks=0,
            drivers={},
            indicators={},
            references=0,
        )
        self.assertEqual(expect, actual)

    def test_complex(self):
        # given
        dim1 = NormDimensions(
            languages=["en", "nl"],
            triggers=3,
            criteria=3,
            objectives=3,
            risks=3,
            drivers={
                "<ignore 1>" : [
                    "<ignore 1.1>",
                ],
                "<ignore 2>": [
                    "<ignore 2.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.1>",
                ],
            },
            indicators={
                "<ignore 1>" : [
                    "<ignore 1.1>",
                ],
                "<ignore 2>": [
                    "<ignore 2.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.1>",
                ],
            },
            references=3,
        )
        dim2 = NormDimensions(
            languages=["en"],
            triggers=1,
            criteria=1,
            objectives=1,
            risks=1,
            drivers={
                "<ignore 2>" : [
                    "<ignore 2.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.2>",
                ],
                "<ignore 4>": [
                    "<ignore 4.2>",
                ],
            },
            indicators={
                "<ignore 2>" : [
                    "<ignore 2.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.2>",
                ],
                "<ignore 4>": [
                    "<ignore 4.2>",
                ],
            },
            references=1,
        )
        # when
        actual = dim1 - dim2
        # then
        expect = NormDimensions(
            languages=["nl"],
            triggers=2,
            criteria=2,
            objectives=2,
            risks=2,
            drivers={
                "<ignore 1>" : [
                    "<ignore 1.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.1>",
                ],
            },
            indicators={
                "<ignore 1>" : [
                    "<ignore 1.1>",
                ],
                "<ignore 3>": [
                    "<ignore 3.1>",
                ],
            },
            references=2,
        )
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
