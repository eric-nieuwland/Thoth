import shutil
import unittest

from filecmp import dircmp
from pathlib import Path
from tempfile import mkdtemp

from thoth.templates.copy_templates import _shared_files_helper, shared_files


class TestSharedFilesHelper(unittest.TestCase):
    """
    test _shared_files_helper() function
    """

    def setUp(self) -> None:
        self.tempdir = Path(mkdtemp())
        self.maxDiff = None

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)

    def test_same_empty(self):
        # given
        dcmp = dircmp(self.tempdir, self.tempdir)
        prefix = Path(self.tempdir)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_same_with_only_empty_subs(self):
        # given
        (self.tempdir / "foo" / "bar").mkdir(parents=True, exist_ok=True)
        dcmp = dircmp(self.tempdir, self.tempdir)
        prefix = Path(self.tempdir)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_same_one_file(self):
        # given
        (self.tempdir / "foo.txt").touch(exist_ok=True)
        dcmp = dircmp(self.tempdir, self.tempdir)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = [
            self.tempdir / "foo.txt",
        ]
        self.assertListEqual(expect, actual)

    def test_same_some_files(self):
        # given
        (self.tempdir / "foo.txt").touch(exist_ok=True)
        (self.tempdir / "bar.png").touch(exist_ok=True)
        (self.tempdir / "baz").touch(exist_ok=True)
        dcmp = dircmp(self.tempdir, self.tempdir)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = [
            self.tempdir / "bar.png",
            self.tempdir / "baz",
            self.tempdir / "foo.txt",
        ]
        self.assertListEqual(expect, actual)

    def test_different_same_files(self):
        # given
        (a := self.tempdir / "a").mkdir(parents=True, exist_ok=True)
        (b := self.tempdir / "b").mkdir(parents=True, exist_ok=True)
        for d in (a, b):
            (d / "foo.txt").touch(exist_ok=True)
            (d / "bar.png").touch(exist_ok=True)
            (d / "baz").touch(exist_ok=True)
        dcmp = dircmp(a, b)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = [
            b / "bar.png",
            b / "baz",
            b / "foo.txt",
        ]
        self.assertListEqual(expect, actual)

    def test_different_partial_overlap(self):
        # given
        (a := self.tempdir / "a").mkdir(parents=True, exist_ok=True)
        (b := self.tempdir / "b").mkdir(parents=True, exist_ok=True)
        for d in (a, b):
            (d / f"only-in.{d.name}").touch(exist_ok=True)  # different in each directory!
            (d / "foo.txt").touch(exist_ok=True)
            (d / "bar.png").touch(exist_ok=True)
            (d / "baz").touch(exist_ok=True)
        dcmp = dircmp(a, b)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = [
            b / "bar.png",
            b / "baz",
            b / "foo.txt",
        ]
        self.assertListEqual(expect, actual)

    def test_complex(self):
        # given
        (a := self.tempdir / "a").mkdir(parents=True, exist_ok=True)
        (b := self.tempdir / "b").mkdir(parents=True, exist_ok=True)
        for d in (a, b):
            (d / f"only-in.{d.name}").touch(exist_ok=True)
            (d / "foo.txt").touch(exist_ok=True)
            (dd := d / "sub-dir").mkdir(parents=True, exist_ok=True)
            (dd / f"only-in.{d.name}").touch(exist_ok=True)
            (dd / "bar.png").touch(exist_ok=True)
            (ddd := dd / "sub-sub-dir").mkdir(parents=True, exist_ok=True)
            (ddd / f"only-in.{d.name}").touch(exist_ok=True)
            (ddd / "baz").touch(exist_ok=True)
        dcmp = dircmp(a, b)
        # when
        actual = list(sorted(_shared_files_helper(dcmp)))
        # then
        expect = [
            b / "foo.txt",
            b / "sub-dir" / "bar.png",
            b / "sub-dir" / "sub-sub-dir" / "baz",
        ]
        self.assertListEqual(expect, actual)


class TestSharedFiles(unittest.TestCase):
    """
    test shared_files() function
    """

    def setUp(self) -> None:
        self.tempdir = Path(mkdtemp())
        self.maxDiff = None

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)

    def test_same_empty(self):
        # given
        left = self.tempdir
        right = self.tempdir
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_same_with_only_empty_subs(self):
        # given
        (self.tempdir / "foo" / "bar").mkdir(parents=True, exist_ok=True)
        left = self.tempdir
        right = self.tempdir
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_same_one_file(self):
        # given
        (self.tempdir / "foo.txt").touch(exist_ok=True)
        left = self.tempdir
        right = self.tempdir
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = [
            Path("foo.txt"),
        ]
        self.assertListEqual(expect, actual)

    def test_same_some_files(self):
        # given
        (self.tempdir / "foo.txt").touch(exist_ok=True)
        (self.tempdir / "bar.png").touch(exist_ok=True)
        (self.tempdir / "baz").touch(exist_ok=True)
        left = self.tempdir
        right = self.tempdir
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = [
            Path("bar.png"),
            Path("baz"),
            Path("foo.txt"),
        ]
        self.assertListEqual(expect, actual)

    def test_different_same_files(self):
        # given
        (a := self.tempdir / "a").mkdir(parents=True, exist_ok=True)
        (b := self.tempdir / "b").mkdir(parents=True, exist_ok=True)
        for d in (a, b):
            (d / "foo.txt").touch(exist_ok=True)
            (d / "bar.png").touch(exist_ok=True)
            (d / "baz").touch(exist_ok=True)
        left = a
        right = b
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = [
            Path("bar.png"),
            Path("baz"),
            Path("foo.txt"),
        ]
        self.assertListEqual(expect, actual)

    def test_different_partial_overlap(self):
        # given
        (a := self.tempdir / "a").mkdir(parents=True, exist_ok=True)
        (b := self.tempdir / "b").mkdir(parents=True, exist_ok=True)
        for d in (a, b):
            (d / f"only-in.{d.name}").touch(exist_ok=True)  # different in each directory!
            (d / "foo.txt").touch(exist_ok=True)
            (d / "bar.png").touch(exist_ok=True)
            (d / "baz").touch(exist_ok=True)
        left = a
        right = b
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = [
            Path("bar.png"),
            Path("baz"),
            Path("foo.txt"),
        ]
        self.assertListEqual(expect, actual)

    def test_complex(self):
        # given
        (a := self.tempdir / "a").mkdir(parents=True, exist_ok=True)
        (b := self.tempdir / "b").mkdir(parents=True, exist_ok=True)
        for d in (a, b):
            (d / f"only-in.{d.name}").touch(exist_ok=True)
            (d / "foo.txt").touch(exist_ok=True)
            (dd := d / "sub-dir").mkdir(parents=True, exist_ok=True)
            (dd / f"only-in.{d.name}").touch(exist_ok=True)
            (dd / "bar.png").touch(exist_ok=True)
            (ddd := dd / "sub-sub-dir").mkdir(parents=True, exist_ok=True)
            (ddd / f"only-in.{d.name}").touch(exist_ok=True)
            (ddd / "baz").touch(exist_ok=True)
        left = a
        right = b
        # when
        actual = list(sorted(shared_files(left, right)))
        # then
        expect = [
            Path("foo.txt"),
            Path("sub-dir", "bar.png"),
            Path("sub-dir", "sub-sub-dir", "baz"),
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
