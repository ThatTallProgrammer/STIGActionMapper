from xml.etree.ElementTree import ElementTree
from html import unescape
from Stig2Cci.models import *
import re


class XML:
    def __init__(self) -> None:
        self.tree = None
        self.root = None
        self.namespace = None

    def readin_from_file(self, xml_path) -> None:
        try:
            self.tree = ElementTree()
            self.tree.parse(xml_path)
            self.root = self.tree.getroot()
            self.namespace = XML.extract_namespace(self.root.tag)
        except FileNotFoundError:
            print("Standin error for a better loggin solution later")
            raise

    def get_fq_tag(self, tag) -> str:
        return "{}{}{}{}".format("{", self.namespace, "}", tag)

    @staticmethod
    def extract_namespace(tag: str) -> str:
        if tag[0] == "{":
            ns, bracket, relative_tag = tag[1:].partition("}")
            return ns
        return ""


class XCCDF(XML):
    def __init__(self, xccdf_path):
        self.readin_from_file(xccdf_path)

    def get_stigs(self) -> dict:
        tag = self.get_fq_tag("Group")
        stigs_by_id = {}
        for stig_xml in self.root.iter(tag):
            stigs_by_id[stig_xml.attrib["id"]] = self.get_group_from_element_tree(stig_xml)

        return stigs_by_id

    def get_profile_from_element_tree(self, elem: ElementTree) -> Group:


    def get_group_from_element_tree(self, elem: ElementTree) -> Group:
        group_id = elem.attrib["id"]
        group_title = elem.find(self.get_fq_tag("title")).text
        rule = elem.find(self.get_fq_tag("Rule"))
        rule_id = rule.attrib["id"]
        rule_weight = rule.attrib["weight"]
        rule_severity = rule.attrib["severity"]
        stig_id = rule.find(self.get_fq_tag("version")).text
        rule_title = rule.find(self.get_fq_tag("title")).text
        rule_idents = rule.findall(self.get_fq_tag("ident"))
        fix_id = rule.find(self.get_fq_tag("fix")).attrib["id"]
        fix_text = rule.find(self.get_fq_tag("fixtext")).text
        check = rule.find(self.get_fq_tag("check"))
        check_id = check.attrib["system"]
        check_text = check.find(self.get_fq_tag("check-content")).text

        legacy_group_id = ""
        legacy_rule_id = ""
        cci_id = ""

        rule_description = rule.find(self.get_fq_tag("description")).text
        vuln_discussion_pattern = "<VulnDiscussion>((.|\\s)*)</VulnDiscussion>"
        vuln_discussion = re.search(vuln_discussion_pattern, rule_description).group(1)

        rule_id_pattern = "SV-\\d+"
        group_id_pattern = "V-\\d+"
        cci_id_pattern = "CCI-\\d+"

        for ident in rule_idents:
            text = ident.text
            if re.match(rule_id_pattern, text):
                legacy_rule_id = text
            elif re.match(group_id_pattern, text):
                legacy_group_id = text
            elif re.match(cci_id_pattern, text):
                cci_id = text

        rule_model = Rule(
            id=rule_id,
            weight=rule_weight,
            severity=rule_severity,
            stig_id=stig_id,
            title=rule_title,
            vuln_discussion=vuln_discussion,
            check_id=check_id,
            check_text=check_text,
            fix_id=fix_id,
            fix_text=fix_text,
            legacy_id=legacy_rule_id,
            cci_id=cci_id
        )

        # print(":::RULE:::\n\n{}".format(rule_model))

        group_model = Group(
            group_id=group_id,
            group_title=group_title,
            legacy_group_id=legacy_group_id,
            rule_id=rule_model
        )

        # print(":::GROUP:::\n\n{}".format(group_model))

        return group_model
