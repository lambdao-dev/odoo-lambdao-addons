# Copyright 2023 fah-mili/Lambdao
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    "name": "Mail Multiple Reports",
    "summary": "Mail Multiple Reports",
    "version": "16.0.1.0.0",
    "category": "Mail",
    "website": "https://lambdao.dev",
    "author": "fah-mili,Lambdao",
    "license": "AGPL-3",
    "installable": True,
    "data": [
        "report/report_timesheet_templates.xml",
        "data/mail_template.xml",
    ],
    "depends": ["sale_timesheet", "mail_multiple_reports"],
}
