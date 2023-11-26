# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math

import requests

from odoo import _, fields, models
from odoo.exceptions import UserError

TIMEOUT = 20


class GiteaBackend(models.Model):
    _name = "gitea.backend"
    _description = "Gitea backend"

    name = fields.Char()
    host = fields.Char(required=True)
    username = fields.Char(required=True)
    password = fields.Char(required=True)

    token = fields.Char()

    def _get_token(self):
        payload = {"name": "odoo_read_issue", "scopes": ["read:issue"]}
        url = f"{self.host}/api/v1/users/{self.username}/tokens"
        result = requests.post(
            url, json=payload, auth=(self.username, self.password), timeout=TIMEOUT
        )
        j = result.json()
        if j.get("message") == "access token name has been used already":
            # TODO: the delete request actually does not work despite getting a 204
            # we could either try a random name, or delete it through the interface
            # maybe at least throw an exception explaining this?
            url_delete = (
                f"{self.host}/api/v1/users/{self.username}/tokens/odoo_read_issue"
            )
            requests.delete(
                url_delete, auth=(self.username, self.password), timeout=TIMEOUT
            )
            requests.post(
                url, json=payload, auth=(self.username, self.password), timeout=TIMEOUT
            )
        result.raise_for_status()
        self.token = result.json()["sha1"]
        return self.token


class GiteaRepository(models.Model):
    _name = "gitea.repository"
    _description = "Gitea repository"

    name = fields.Char(required=True)
    organization = fields.Char(required=True)
    backend_id = fields.Many2one(comodel_name="gitea.backend", required=True)

    def _get_all_issues(self):
        result = self._get_issues("open")
        result += self._get_issues("closed")
        return result

    def _get_issues(self, state="open"):
        token = self.backend_id.token or ""
        if not token:
            token = self.backend_id._get_token()
        url = f"{self.backend_id.host}/api/v1/repos/{self.organization}/{self.name}/issues"
        limit = 20
        headers = {"Authorization": f"token {token}"}
        params = {"state": state, "limit": limit}
        result = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        result.raise_for_status()
        data = result.json()
        total = int(result.headers["X-Total-Count"])
        if len(data) < total:
            total_pages = math.ceil(total / limit)
            for page in range(1, total_pages):
                params["page"] = page
                result = requests.get(
                    url, params=params, headers=headers, timeout=TIMEOUT
                )
                data += result.json()
        return data


class GiteaRepositoryMixin(models.AbstractModel):
    """This mixin should load issues into another model
    implementing the issue mixin."""

    _name = "gitea.repository.mixin"
    _description = "Gitea repository mixin"

    gitea_repository_id = fields.Many2one(comodel_name="gitea.repository")

    def _get_gitea_issue_model(self):
        raise NotImplementedError

    def gitea_import_issues(self):
        self.ensure_one()
        if not self.gitea_repository_id:
            raise UserError(_("No Gitea repository defined"))
        issues = self.gitea_repository_id._get_all_issues()
        issues_by_number = {issue["number"]: issue for issue in issues}
        numbers = list(issues_by_number.keys())
        model = self.env[self._get_gitea_issue_model()]
        existing_issues = model.search([("gitea_issue_number", "in", numbers)])
        existing_numbers = existing_issues.mapped("gitea_issue_number")
        existing_by_number = {
            issue.gitea_issue_number: issue for issue in existing_issues
        }
        new_issues = model.browse()
        keys = model._get_gitea_issue_fields()
        key_title = keys["title"]
        key_body = keys["body"]
        for issue in issues:
            if issue["number"] in existing_numbers:
                existing = existing_by_number[issue["number"]]
                existing.gitea_status = issue["state"]
            else:
                vals = self._get_vals_from_gitea_issue(
                    issue, key_title=key_title, key_body=key_body
                )
                new_issues |= model.create(vals)
        return existing_issues + new_issues

    def _get_vals_from_gitea_issue(
        self, issue, key_title="name", key_body="description"
    ):
        self.ensure_one()
        return {
            key_title: f'#{issue["number"]} {issue["title"]}',
            key_body: issue["body"],
            "gitea_issue_number": issue["number"],
            "gitea_status": issue["state"],
        }


class GiteaIssueMixin(models.AbstractModel):
    """This is a mixin to hold Gitea issue information."""

    _name = "gitea.issue.mixin"
    _description = "Gitea issue mixin"

    gitea_issue_number = fields.Integer()
    gitea_status = fields.Char()

    def _get_gitea_issue_fields(self):
        """To be overriden by any model that will use other fields."""
        return {"title": "name", "body": "description"}
