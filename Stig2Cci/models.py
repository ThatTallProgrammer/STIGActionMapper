from django.db import models


class Rule(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    weight = models.CharField(max_length=5)
    severity = models.CharField(max_length=50)
    stig_id = models.CharField(max_length=50)
    title = models.TextField()
    vuln_discussion = models.TextField()
    check_id = models.CharField(max_length=50)
    check_text = models.TextField()
    fix_id = models.CharField(max_length=50)
    fix_text = models.TextField()
    legacy_id = models.CharField(max_length=50)
    cci_id = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        string = "ID: {}\n".format(self.id)
        string += "Weight: {}\n".format(self.weight)
        string += "Severity: {}\n".format(self.severity)
        string += "Stig ID: {}\n".format(self.stig_id)
        string += "Title: {}\n".format(self.title)
        string += "Vulnerability Discussion: {}\n".format(self.vuln_discussion)
        string += "Check ID: {}\n".format(self.check_id)
        string += "Check Text: {}\n".format(self.check_text)
        string += "Fix ID: {}\n".format(self.fix_id)
        string += "Fix Text: {}\n".format(self.fix_text)
        string += "Legacy ID: {}\n".format(self.legacy_id)
        string += "CCI ID: {}\n".format(self.cci_id)

        return string


class Group(models.Model):
    group_id = models.CharField(primary_key=True, max_length=12)
    legacy_group_id = models.CharField(max_length=50)
    group_title = models.CharField(max_length=50)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)

    class Meta:
        ordering = ['group_id']

    def __str__(self):
        string = "Group ID: {}\n".format(self.group_id)
        string += "Legacy Group ID: {}\n".format(self.legacy_group_id)
        string += "Group Title: {}".format(self.group_title)
        # string += ":::Rule::: \n{}".format(self.rule)

        return string


