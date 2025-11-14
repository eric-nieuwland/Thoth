import unittest
from unittest.mock import MagicMock, call, patch

from thoth.command.document.render_document import determine_format


class TestDetermineLanguage(unittest.TestCase):
    """
    test determine_format() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("thoth.command.document.render_document.OutputFormat.from_path")
    @patch("thoth.command.document.render_document._notify")
    def test__nothing(self, mock_notify, mock_from_path):
        mock_output = None
        mock_template = None
        mock_from_path.side_effect = lambda arg: {
            "output": mock_output,
            "template": mock_template,
        }.get(arg)
        # given
        template = "template"
        output = "output"
        format = None
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_format(template, output, format)
        expect = [
            call("need format from '--format', '--output', or '--template'"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)
        expect = [
            call(template),
            call(output),
        ]
        self.assertListEqual(expect, mock_from_path.mock_calls)

    @patch("thoth.command.document.render_document.OutputFormat.from_path")
    @patch("thoth.command.document.render_document._notify")
    def test__format(self, mock_notify, mock_from_path):
        mock_output = None
        mock_template = None
        mock_from_path.side_effect = lambda arg: {
            "output": mock_output,
            "template": mock_template,
        }.get(arg)
        # given
        template = None
        output = None
        format = MagicMock()
        format.resolve.return_value = "MOCK resolved format"
        # when
        actual = determine_format(template, output, format)
        # then
        expect = "MOCK resolved format"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)
        expect = []
        self.assertListEqual(expect, mock_from_path.mock_calls)

    @patch("thoth.command.document.render_document.OutputFormat.from_path")
    @patch("thoth.command.document.render_document._notify")
    def test__template(self, mock_notify, mock_from_path):
        mock_output = None
        mock_template = MagicMock()
        mock_template.resolve.return_value = "MOCK resolved template"
        mock_from_path.side_effect = lambda arg: {
            "output": mock_output,
            "template": mock_template,
        }.get(arg)
        # given
        template = "template"
        output = None
        format = None
        # when
        actual = determine_format(template, output, format)
        # then
        expect = "MOCK resolved template"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)
        expect = [
            call(template),
        ]
        self.assertListEqual(expect, mock_from_path.mock_calls)

    @patch("thoth.command.document.render_document.OutputFormat.from_path")
    @patch("thoth.command.document.render_document._notify")
    def test__output(self, mock_notify, mock_from_path):
        mock_output = MagicMock()
        mock_output.resolve.return_value = "MOCK resolved output"
        mock_template = None
        mock_from_path.side_effect = lambda arg: {
            "output": mock_output,
            "template": mock_template,
        }.get(arg)
        # given
        template = "template"
        output = "output"
        format = None
        # when
        actual = determine_format(template, output, format)
        # then
        expect = "MOCK resolved output"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)
        expect = [
            call(template),
            call(output),
        ]
        self.assertListEqual(expect, mock_from_path.mock_calls)

    @patch("thoth.command.document.render_document.FORMAT_REQUIRES_OUTPUT")
    @patch("thoth.command.document.render_document.OutputFormat.from_path")
    @patch("thoth.command.document.render_document._notify")
    def test__format_requires_output(self, mock_notify, mock_from_path, mock_format_requires_output):
        mock_output_format = MagicMock()
        mock_output_format.resolve.return_value = mock_output_format
        mock_output_format.value = "MOCK resolved output format value"
        mock_from_path.side_effect = lambda arg: {
            "output": None,
            "template": None,
        }.get(arg)
        mock_format_requires_output.__contains__.return_value = True
        # given
        template = None
        output = None
        format = mock_output_format
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_format(template, output, format)
        expect = [
            call("please use '--output' to save files of format - MOCK resolved output format value"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)
        expect = []
        self.assertListEqual(expect, mock_from_path.mock_calls)

    @patch("thoth.command.document.render_document.FORMAT_REQUIRES_OUTPUT")
    @patch("thoth.command.document.render_document.OutputFormat.from_path")
    @patch("thoth.command.document.render_document._notify")
    def test__template_requires_output(self, mock_notify, mock_from_path, mock_format_requires_output):
        mock_output_format = MagicMock()
        mock_output_format.resolve.return_value = mock_output_format
        mock_output_format.value = "MOCK resolved output format value"
        mock_from_path.side_effect = lambda arg: {
            "output": None,
            "template": mock_output_format,
        }.get(arg)
        mock_format_requires_output.__contains__.return_value = True
        # given
        template = "template"
        output = None
        format = None
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_format(template, output, format)
        expect = [
            call("please use '--output' to save files of format - MOCK resolved output format value"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)
        expect = [
            call(template),
        ]
        self.assertListEqual(expect, mock_from_path.mock_calls)


if __name__ == "__main__":
    unittest.main()
