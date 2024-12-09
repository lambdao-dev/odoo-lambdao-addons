/** @odoo-module **/

/**
    # Copyright 2024 len-foss/Lambdao
    # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

import {useService} from "@web/core/utils/hooks";

const {useComponent} = owl;

export function useGiteaButton() {
    const component = useComponent();

    component.onClickGitea = () => {
        const project_id = component.props.context.default_project_id;
        component.model.orm.call(
            "project.project",
            "gitea_import_issues",
            [[project_id]],
            {}
        );
    };
}
