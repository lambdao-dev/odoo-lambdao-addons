# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    "name": "Gitea Project",
    "summary": "Gitea Project",
    "version": "16.0.1.0.1",
    "category": "Project",
    "website": "https://lambdao.dev",
    "author": "fah-mili,Lambdao",
    "license": "AGPL-3",
    "installable": True,
    "data": ["views/project_task.xml", "views/project_project.xml"],
    "depends": ["gitea", "project"],
    "assets": {
        "web.assets_backend": [
            "gitea_project/static/src/views/*.js",
            "gitea_project/static/src/views/*.xml",
        ],
    },
}
