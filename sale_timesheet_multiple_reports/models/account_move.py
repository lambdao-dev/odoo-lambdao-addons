# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_mail_template(self):
        if all(m.move_type == "out_invoice" for m in self) and self.timesheet_ids:
            res = "sale_timesheet_multiple_reports.email_template_invoice_timesheets"
        else:
            res = super()._get_mail_template()
        return res
