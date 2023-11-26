# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "gitea.issue.mixin"]

    gitea_repository_id = fields.Many2one(related="project_id.gitea_repository_id")
