import unittest

from pathlib import Path

from thoth.command.shared.output_format import OutputFormat


class TestOutputFormat(unittest.TestCase):
    """
    test various OutputFormat functions
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_create(self):
        # given
        for name, expect in (
            ("html", OutputFormat.HTML),
            ("docx", OutputFormat.DOCX),
            ("md", OutputFormat.MD),
            ("txt", OutputFormat.TEXT),
        ):
            # when
            actual = OutputFormat(name)
            # then
            self.assertEqual(expect, actual, msg=f"failed for {format}")

    def test_no_create(self):
        # given
        for name in (
            "xlsx",
            "mpg",
            "jpg",
            "odt",
        ):
            # when
            # then
            with self.assertRaises(ValueError):
                _ = OutputFormat(name)

    def test_all(self):
        # given
        # when
        actual = OutputFormat.all()
        # then
        expect = (
            OutputFormat.HTML,
            OutputFormat.DOCX,
            OutputFormat.MD,
            OutputFormat.TEXT,
        )
        self.assertTupleEqual(expect, actual)

    def test_from_path_none(self):
        # given
        path = None
        # when
        actual = OutputFormat.from_path(path)
        # then
        expect = None
        self.assertEqual(expect, actual)

    def test_from_path_known(self):
        # given
        for path, expect in (
            (Path("yada.html"), OutputFormat.HTML),
            (Path("yada.docx"), OutputFormat.DOCX),
            (Path("yada.md"), OutputFormat.MD),
            (Path("yada.txt"), OutputFormat.TEXT),
        ):
            # when
            actual = OutputFormat.from_path(path)
            # then
            self.assertEqual(expect, actual, msg=f"failed for {path}")

    def test_from_path_unknown(self):
        # given
        for path in (
            Path("yada.xlsx"),
            Path("yada.mpg"),
            Path("yada.jpg"),
            Path("yada.odt"),
        ):
            # when
            actual = OutputFormat.from_path(path)
            # then
            expect = None
            self.assertEqual(expect, actual, msg=f"failed for {path}")

    def test_resolve(self):
        # given
        for format, expect in (
            (OutputFormat.HTML, OutputFormat.TEXT),
            (OutputFormat.DOCX, OutputFormat.DOCX),
            (OutputFormat.MD, OutputFormat.TEXT),
            (OutputFormat.TEXT, OutputFormat.TEXT),
        ):
            # when
            actual = format.resolve()
            # then
            self.assertEqual(expect, actual, msg=f"failed for {format}")


if __name__ == "__main__":
    unittest.main()
