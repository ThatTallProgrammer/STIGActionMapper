import unittest
import os
from unittest import TestCase
from XMLParsing.disaXML import *


class TestXML(TestCase):
    def setUp(self):
        self.test_xccdf_path = os.path.abspath("XMLParsing/testXML/xccdf.xml")

    def test_extract_namespace(self) -> None:
        data = (
            ("https://uri.test.com", "{https://uri.test.com}Group"),
            ("", "Group")
        )
        for case in data:
            expected = case[0]
            actual = XML.extract_namespace(case[1])

            self.assertEqual(expected, actual)

    def test_readinfromfile_when_exists(self) -> None:
        xml = XML()
        xml.readin_from_file(self.test_xccdf_path)

        self.assertNotEqual(xml.root, None)
        self.assertNotEqual(xml.tree, None)

    def test_readinfromfile_when_notexists(self) -> None:
        xml = XML()

        with self.assertRaises(FileNotFoundError):
            xml.readin_from_file("nonexistant.xml")

    def test_getfqtag(self) -> None:
        xml = XML()
        xml.readin_from_file(self.test_xccdf_path)

        expected = "{http://checklists.nist.gov/xccdf/1.1}Benchmark"
        actual = xml.get_fq_tag("Benchmark")

        self.assertEqual(expected, actual)


class TestXCCDF(TestCase):
    def setUp(self):
        self.test_xccdf_path = os.path.abspath("XMLParsing/testXML/xccdf.xml")

    def test_getstigs(self) -> None:
        xccdf = XCCDF(self.test_xccdf_path)
        stig1 = Group()
        stig1.group_id = "V-222387"
        stig2 = Group()
        stig2.group_id = "V-222388"

        expected = {
            "V-222387": stig1,
            "V-222388": stig2
        }
        actual = xccdf.get_stigs()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
