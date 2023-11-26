# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "gitea.repository.mixin"]

    @api.model
    def _get_gitea_issue_model(self):
        return "project.task"

    def _get_vals_from_gitea_issue(
        self, issue, key_title="name", key_body="description"
    ):
        result = super()._get_vals_from_gitea_issue(
            issue, key_title=key_title, key_body=key_body
        )
        result["project_id"] = self.id
        return result
