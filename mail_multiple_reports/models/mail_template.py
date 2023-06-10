# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import base64

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval, time


class MailTemplate(models.Model):
    _inherit = "mail.template"

    additional_reports = fields.Many2many(
        comodel_name="ir.actions.report",
        # domain=lambda self: [('model', '=', self.model)],  # TODO: dynamic domain
    )

    @api.model
    def generate_email(self, res_ids, fields):  # pylint: disable=redefined-outer-name
        results = super().generate_email(res_ids, fields)
        for template, record_ids in self._classify_per_lang(res_ids).values():
            for report in template.additional_reports:
                for res_id in record_ids:
                    if report.report_type in ["qweb-html", "qweb-pdf"]:
                        result, report_format = self.env[
                            "ir.actions.report"
                        ]._render_qweb_pdf(report, [res_id])
                    else:
                        res = self.env["ir.actions.report"]._render(report, [res_id])
                        result, report_format = res
                    result = base64.b64encode(result)
                    ext = "." + report_format
                    if report.print_report_name:
                        obj = self.env[report.model].browse(res_id)
                        vals = {"object": obj, "time": time}
                        report_name = safe_eval(report.print_report_name, vals)
                    else:
                        report_name = report.name
                    if not report_name.endswith(ext):
                        report_name += ext
                    attachments = results[res_id].get("attachments", [])
                    attachments.append((report_name, result))
                    results[res_id]["attachments"] = attachments
        return results
