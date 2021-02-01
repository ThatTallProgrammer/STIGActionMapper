import xml.etree.ElementTree as ElementTree
from XMLParsing.stig import *


class XML:
    def __init__(self, xml_path: str) -> None:
        self.xml_path = xml_path
        self.tree = None
        self.root = None
        self.namespace = None
        self.readin()

    def readin(self):
        try:
            self.tree = ElementTree()
            self.tree.parse(self.xml_path)
            self.root = self.tree.getroot()
            self.namespace = XML.extract_namespace(self.root.tag)
        except FileNotFoundError:
            pass # TODO log exception

    @staticmethod
    def extract_namespace(tag: str) -> str:
        if tag[0] == "{":
            ns, bracket, relative_tag = tag[1:].partition("}")
            return ns
        return ""


class XCCDF(XML):
    def get_fq_tag(self, tag) -> str:
        return "{}{}{}{}".format("{", self.namespace, "}", tag)

    def get_vulnerabilities(self):
        tag = self.get_fq_tag("Group")
        return self.root.iter(tag)

    def get_stigs(self) -> dict:
        stigs_by_id = {}
        for stig_xml in self.get_vulnerabilities():
            stigs_by_id[stig_xml.attrib['id']] = self.get_stig_from_element_tree(stig_xml)
        return stigs_by_id

    def get_stig_from_element_tree(self, elem: ElementTree) -> Stig:
        stig_data = dict()
        stig_data["vid"] = elem.attrib['id']
        return Stig(stig_data)
