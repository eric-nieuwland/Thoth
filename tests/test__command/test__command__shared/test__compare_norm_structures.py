import io
import unittest
from unittest.mock import MagicMock, call, patch

from command.shared.compare_norm_structures import (
    _x_conformities,
    _x_conformity,
    _x_difference,
    _x_drivers,
    _x_identifier,
    _x_indicator,
    _x_indicators,
    compare_norm_structures,
)


class TestXDifference(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.values = (None, 42, "foo", {42: "foo"}, ["foo", "bar"], {"baz", "foo"})

    def test_same(self):
        # given
        what = "MOCK what"
        for v1 in self.values:
            v2 = v1
            # when
            actual = _x_difference(what, v1, v2)
            # then
            expect = []
            self.assertListEqual(expect, actual, msg=f"failed for {v1=}")

    def test_different(self):
        # given
        what = "MOCK what"
        for i1 in range(len(self.values)):
            v1 = self.values[i1]
            for i2 in range(len(self.values)):
                if i1 == i2:
                    continue
                v2 = self.values[i2]
                # when
                actual = _x_difference(what, v1, v2)
                # then
                expect = [
                    f"MOCK what: {v1} <-> {v2}",
                ]
                self.assertListEqual(expect, actual, msg=f"failed for {v1=}, {v2=}")


class TestXIdentifier(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_same(self):
        # given
        id1 = id2 = "MOCK id"
        # when
        actual = _x_identifier(id1, id2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_difference(self):
        # given
        id1 = "MOCK id #1"
        id2 = "MOCK id #2"
        # when
        actual = _x_identifier(id1, id2)
        # then
        expect = [
            "identifier: MOCK id #1 <-> MOCK id #2",
        ]
        self.assertListEqual(expect, actual)


class TestXDrivers(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none_none(self):
        # given
        drivers1 = None
        drivers2 = None
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_empty_none(self):
        # given
        drivers1 = []
        drivers2 = None
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_none_empty(self):
        # given
        drivers1 = None
        drivers2 = []
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_empty_empty(self):
        # given
        drivers1 = []
        drivers2 = []
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_empty(self):
        # given
        drivers1 = [
            "MOCK drivers1 #1",
        ]
        drivers2 = []
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: MOCK drivers1 #1 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_empty(self):
        # given
        drivers1 = [
            "MOCK drivers1 #1",
            "MOCK drivers1 #2",
            "MOCK drivers1 #3",
        ]
        drivers2 = []
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: MOCK drivers1 #1 <-> --"],
            ["driver: MOCK drivers1 #2 <-> --"],
            ["driver: MOCK drivers1 #3 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_empty_one(self):
        # given
        drivers1 = []
        drivers2 = [
            "MOCK drivers2 #1",
        ]
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: -- <-> MOCK drivers2 #1"],
        ]
        self.assertListEqual(expect, actual)

    def test_empty_some(self):
        # given
        drivers1 = []
        drivers2 = [
            "MOCK drivers2 #1",
            "MOCK drivers2 #2",
            "MOCK drivers2 #3",
        ]
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: -- <-> MOCK drivers2 #1"],
            ["driver: -- <-> MOCK drivers2 #2"],
            ["driver: -- <-> MOCK drivers2 #3"],
        ]
        self.assertListEqual(expect, actual)

    def test_one_one(self):
        # given
        drivers1 = [
            "MOCK drivers1 #1",
        ]
        drivers2 = [
            "MOCK drivers2 #1",
        ]
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: MOCK drivers1 #1 <-> MOCK drivers2 #1"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_one(self):
        # given
        drivers1 = [
            "MOCK drivers1 #1",
            "MOCK drivers1 #2",
            "MOCK drivers1 #3",
        ]
        drivers2 = [
            "MOCK drivers2 #1",
        ]
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: MOCK drivers1 #1 <-> MOCK drivers2 #1"],
            ["driver: MOCK drivers1 #2 <-> --"],
            ["driver: MOCK drivers1 #3 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_some(self):
        # given
        drivers1 = [
            "MOCK drivers1 #1",
            "MOCK drivers1 #2",
            "MOCK drivers1 #3",
        ]
        drivers2 = [
            "MOCK drivers2 #1",
            "MOCK drivers2 #2",
            "MOCK drivers2 #3",
        ]
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: MOCK drivers1 #1 <-> MOCK drivers2 #1"],
            ["driver: MOCK drivers1 #2 <-> MOCK drivers2 #2"],
            ["driver: MOCK drivers1 #3 <-> MOCK drivers2 #3"],
        ]
        self.assertListEqual(expect, actual)

    def test_same(self):
        # given
        drivers1 = [
            "MOCK drivers1 #1",
            "MOCK drivers1 #2",
            "MOCK drivers1 #3",
        ]
        drivers2 = [
            "MOCK drivers2 #1",
            "MOCK drivers2 #2",
            "MOCK drivers2 #3",
        ]
        # when
        actual = _x_drivers(drivers1, drivers2)
        # then
        expect = [
            ["driver: MOCK drivers1 #1 <-> MOCK drivers2 #1"],
            ["driver: MOCK drivers1 #2 <-> MOCK drivers2 #2"],
            ["driver: MOCK drivers1 #3 <-> MOCK drivers2 #3"],
        ]
        self.assertListEqual(expect, actual)


class TestXConformity(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none_none(self):
        # given
        conformity1 = None
        conformity2 = None
        # when
        actual = _x_conformity(conformity1, conformity2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_x_none(self):
        # given
        conformity1 = MagicMock()
        conformity1.identifier = "MOCK conformity1"
        conformity2 = None
        # when
        actual = _x_conformity(conformity1, conformity2)
        # then
        expect = [
            "  conformity/identifier: MOCK conformity1 <-> --",
        ]
        self.assertListEqual(expect, actual)

    def test_none_x(self):
        # given
        conformity1 = None
        conformity2 = MagicMock()
        conformity2.identifier = "MOCK conformity2"
        # when
        actual = _x_conformity(conformity1, conformity2)
        # then
        expect = [
            "  conformity/identifier: -- <-> MOCK conformity2",
        ]
        self.assertListEqual(expect, actual)

    def test_x_y(self):
        # given
        conformity1 = MagicMock()
        conformity1.identifier = "MOCK conformity1"
        conformity2 = MagicMock()
        conformity2.identifier = "MOCK conformity2"
        # when
        actual = _x_conformity(conformity1, conformity2)
        # then
        expect = [
            "  conformity/identifier: MOCK conformity1 <-> MOCK conformity2",
        ]
        self.assertListEqual(expect, actual)


class TestXConformities(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty_empty(self):
        # given
        conformities1 = []
        conformities2 = []
        # when
        actual = _x_conformities(conformities1, conformities2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_empty(self):
        # given
        conformities1_1 = MagicMock()
        conformities1_1.identifier = "MOCK conformities1 #1"
        conformities1 = [
            conformities1_1,
        ]
        conformities2 = []
        # when
        actual = _x_conformities(conformities1, conformities2)
        # then
        expect = [
            ["  conformity/identifier: MOCK conformities1 #1 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_empty(self):
        # given
        conformities1_1 = MagicMock()
        conformities1_1.identifier = "MOCK conformities1 #1"
        conformities1_2 = MagicMock()
        conformities1_2.identifier = "MOCK conformities1 #2"
        conformities1_3 = MagicMock()
        conformities1_3.identifier = "MOCK conformities1 #3"
        conformities1 = [
            conformities1_1,
            conformities1_2,
            conformities1_3,
        ]
        conformities2 = []
        # when
        actual = _x_conformities(conformities1, conformities2)
        # then
        expect = [
            ["  conformity/identifier: MOCK conformities1 #1 <-> --"],
            ["  conformity/identifier: MOCK conformities1 #2 <-> --"],
            ["  conformity/identifier: MOCK conformities1 #3 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_empty_one(self):
        # given
        conformities2_1 = MagicMock()
        conformities2_1.identifier = "MOCK conformities2 #1"
        conformities1 = []
        conformities2 = [
            conformities2_1,
        ]
        # when
        actual = _x_conformities(conformities1, conformities2)
        # then
        expect = [
            ["  conformity/identifier: -- <-> MOCK conformities2 #1"],
        ]
        self.assertListEqual(expect, actual)

    def test_empty_some(self):
        # given
        conformities2_1 = MagicMock()
        conformities2_1.identifier = "MOCK conformities2 #1"
        conformities2_2 = MagicMock()
        conformities2_2.identifier = "MOCK conformities2 #2"
        conformities2_3 = MagicMock()
        conformities2_3.identifier = "MOCK conformities2 #3"
        conformities1 = []
        conformities2 = [
            conformities2_1,
            conformities2_2,
            conformities2_3,
        ]
        # when
        actual = _x_conformities(conformities1, conformities2)
        # then
        expect = [
            ["  conformity/identifier: -- <-> MOCK conformities2 #1"],
            ["  conformity/identifier: -- <-> MOCK conformities2 #2"],
            ["  conformity/identifier: -- <-> MOCK conformities2 #3"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_same(self):
        # given
        conformities1_1 = MagicMock()
        conformities1_1.identifier = "MOCK conformities1 #1"
        conformities1_2 = MagicMock()
        conformities1_2.identifier = "MOCK conformities same"
        conformities1_3 = MagicMock()
        conformities1_3.identifier = "MOCK conformities1 #3"
        conformities2_1 = MagicMock()
        conformities2_1.identifier = "MOCK conformities2 #1"
        conformities2_2 = MagicMock()
        conformities2_2.identifier = "MOCK conformities same"
        conformities2_3 = MagicMock()
        conformities2_3.identifier = "MOCK conformities2 #3"
        conformities1 = [
            conformities1_1,
            conformities1_2,
            conformities1_3,
        ]
        conformities2 = [
            conformities2_1,
            conformities2_2,
            conformities2_3,
        ]
        # when
        actual = _x_conformities(conformities1, conformities2)
        # then
        expect = [
            ["  conformity/identifier: MOCK conformities1 #1 <-> MOCK conformities2 #1"],
            [],
            ["  conformity/identifier: MOCK conformities1 #3 <-> MOCK conformities2 #3"],
        ]
        self.assertListEqual(expect, actual)


class TestXIndicator(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none_none(self):
        # given
        indicator1 = None
        indicator2 = None
        # when
        actual = _x_indicator(indicator1, indicator2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_x_none(self):
        # given
        indicator1 = MagicMock()
        indicator1.identifier = "MOCK indicator1"
        indicator2 = None
        # when
        actual = _x_indicator(indicator1, indicator2)
        # then
        expect = [
            "indicator/identifier: MOCK indicator1 <-> --",
        ]
        self.assertListEqual(expect, actual)

    def test_none_x(self):
        # given
        indicator1 = None
        indicator2 = MagicMock()
        indicator2.identifier = "MOCK indicator2"
        # when
        actual = _x_indicator(indicator1, indicator2)
        # then
        expect = [
            "indicator/identifier: -- <-> MOCK indicator2",
        ]
        self.assertListEqual(expect, actual)

    def test_x_y(self):
        # given
        indicator1 = MagicMock()
        indicator1.identifier = "MOCK indicator1"
        indicator1.conformities = []
        indicator2 = MagicMock()
        indicator2.identifier = "MOCK indicator2"
        indicator2.conformities = []
        # when
        actual = _x_indicator(indicator1, indicator2)
        # then
        expect = [
            ["indicator/identifier: MOCK indicator1 <-> MOCK indicator2"],
            [],
        ]
        self.assertListEqual(expect, actual)

    def test_x_x(self):
        # given
        indicator1 = MagicMock()
        indicator1.identifier = "MOCK indicator"
        indicator1.conformities = []
        indicator2 = MagicMock()
        indicator2.identifier = "MOCK indicator"
        indicator2.conformities = []
        # when
        actual = _x_indicator(indicator1, indicator2)
        # then
        expect = [
            [],
            [],
        ]
        self.assertListEqual(expect, actual)


class TestXIndicators(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty_empty(self):
        # given
        indicators1 = []
        indicators2 = []
        # when
        actual = _x_indicators(indicators1, indicators2)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one_empty(self):
        # given
        indicators1_1 = MagicMock()
        indicators1_1.identifier = "MOCK indicators1 #1"
        indicators1 = [
            indicators1_1,
        ]
        indicators2 = []
        # when
        actual = _x_indicators(indicators1, indicators2)
        # then
        expect = [
            ["indicator/identifier: MOCK indicators1 #1 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_empty(self):
        # given
        indicators1_1 = MagicMock()
        indicators1_1.identifier = "MOCK indicators1 #1"
        indicators1_2 = MagicMock()
        indicators1_2.identifier = "MOCK indicators1 #2"
        indicators1_3 = MagicMock()
        indicators1_3.identifier = "MOCK indicators1 #3"
        indicators1 = [
            indicators1_1,
            indicators1_2,
            indicators1_3,
        ]
        indicators2 = []
        # when
        actual = _x_indicators(indicators1, indicators2)
        # then
        expect = [
            ["indicator/identifier: MOCK indicators1 #1 <-> --"],
            ["indicator/identifier: MOCK indicators1 #2 <-> --"],
            ["indicator/identifier: MOCK indicators1 #3 <-> --"],
        ]
        self.assertListEqual(expect, actual)

    def test_empty_one(self):
        # given
        indicators2_1 = MagicMock()
        indicators2_1.identifier = "MOCK indicators2 #1"
        indicators1 = []
        indicators2 = [
            indicators2_1,
        ]
        # when
        actual = _x_indicators(indicators1, indicators2)
        # then
        expect = [
            ["indicator/identifier: -- <-> MOCK indicators2 #1"],
        ]
        self.assertListEqual(expect, actual)

    def test_empty_some(self):
        # given
        indicators2_1 = MagicMock()
        indicators2_1.identifier = "MOCK indicators2 #1"
        indicators2_2 = MagicMock()
        indicators2_2.identifier = "MOCK indicators2 #2"
        indicators2_3 = MagicMock()
        indicators2_3.identifier = "MOCK indicators2 #3"
        indicators1 = []
        indicators2 = [
            indicators2_1,
            indicators2_2,
            indicators2_3,
        ]
        # when
        actual = _x_indicators(indicators1, indicators2)
        # then
        expect = [
            ["indicator/identifier: -- <-> MOCK indicators2 #1"],
            ["indicator/identifier: -- <-> MOCK indicators2 #2"],
            ["indicator/identifier: -- <-> MOCK indicators2 #3"],
        ]
        self.assertListEqual(expect, actual)

    def test_some_same(self):
        # given
        indicators1_1 = MagicMock()
        indicators1_1.identifier = "MOCK indicators1 #1"
        indicators1_1.conformities = []
        indicators1_2 = MagicMock()
        indicators1_2.identifier = "MOCK indicators same"
        indicators1_2.conformities = []
        indicators1_3 = MagicMock()
        indicators1_3.identifier = "MOCK indicators1 #3"
        indicators1_3.conformities = []
        indicators2_1 = MagicMock()
        indicators2_1.identifier = "MOCK indicators2 #1"
        indicators2_1.conformities = []
        indicators2_2 = MagicMock()
        indicators2_2.identifier = "MOCK indicators same"
        indicators2_2.conformities = []
        indicators2_3 = MagicMock()
        indicators2_3.identifier = "MOCK indicators2 #3"
        indicators2_3.conformities = []
        indicators1 = [
            indicators1_1,
            indicators1_2,
            indicators1_3,
        ]
        indicators2 = [
            indicators2_1,
            indicators2_2,
            indicators2_3,
        ]
        # when
        actual = _x_indicators(indicators1, indicators2)
        # then
        expect = [
            [["indicator/identifier: MOCK indicators1 #1 <-> MOCK indicators2 #1"], []],
            [[], []],
            [["indicator/identifier: MOCK indicators1 #3 <-> MOCK indicators2 #3"], []],
        ]
        self.assertListEqual(expect, actual)


class TestCompareNormStructures(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch("command.shared.compare_norm_structures._x_indicators")
    @patch("command.shared.compare_norm_structures._x_drivers")
    @patch("command.shared.compare_norm_structures._x_identifier")
    @patch("command.shared.compare_norm_structures.Norm")
    def test_it(
        self,
        mock_norm,
        mock_x_identifier,
        mock_x_drivers,
        mock_x_indicators,
    ):
        norm_mock = MagicMock()
        norm_mock.identifier = "MOCK norm identifier"
        norm_mock.drivers = "MOCK norm drivers"
        norm_mock.indicators = "MOCK norm indicators"
        mock_x_identifier.return_value = "MOCK X Identifier"
        mock_x_drivers.return_value = "MOCK X Drivers"
        mock_x_indicators.return_value = "MOCK X Indicators"
        # given
        norm1 = norm_mock
        norm2 = norm_mock
        # when
        actual = compare_norm_structures(norm1, norm2)
        # then
        expect = []
        self.assertListEqual(expect, mock_norm.mock_calls)
        expect = [
            call("MOCK norm identifier", "MOCK norm identifier"),
        ]
        self.assertListEqual(expect, mock_x_identifier.mock_calls)
        expect = [
            call("MOCK norm drivers", "MOCK norm drivers"),
        ]
        self.assertListEqual(expect, mock_x_drivers.mock_calls)
        expect = [
            call("MOCK norm indicators", "MOCK norm indicators"),
        ]
        self.assertListEqual(expect, mock_x_indicators.mock_calls)
        expect = [
          "MOCK X Identifier",
          "MOCK X Drivers",
          "MOCK X Indicators",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
