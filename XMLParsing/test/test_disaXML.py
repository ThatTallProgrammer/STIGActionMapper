import unittest
from unittest import TestCase
from XMLParsing.disaXML import *


class TestXML(TestCase):
    def test_extract_namespace(self) -> None:
        data = (
            ("https://uri.test.com", "{https://uri.test.com}Group"),
            ("", "Group")
        )
        for case in data:
            self.assertEqual(case[0], XML.extract_namespace(case[1]))


# class TestXCCDF(TestCase):
#     # def test_get_vulnerabilities(self) -> None:
#     #     xccdf = XCCDF("/home/onetallprogrammer/PycharmProjects/XMLParsing/XCCDFFiles/U_ASD_STIG_V5R1_Manual-xccdf.xml")
#     #     stigs = xccdf.get_stigs()
#     #     for vid in stigs.keys():
#     #         print(stigs[vid])


if __name__ == "__main__":
    unittest.main()
