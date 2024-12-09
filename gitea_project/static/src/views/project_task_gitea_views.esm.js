/** @odoo-module **/

/**
    # Copyright 2024 len-foss/Lambdao
    # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

import {ListController} from "@web/views/list/list_controller";
import {listView} from "@web/views/list/list_view";
import {patch} from "@web/core/utils/patch";
import {projectTaskKanbanView} from "@project/views/project_task_kanban/project_task_kanban_view";
import {registry} from "@web/core/registry";
import {useGiteaButton} from "@gitea_project/views/project_task_gitea_hook.esm";

export class ProjectTaskListController extends ListController {
    setup() {
        super.setup();
        useGiteaButton();
    }
}

registry.category("views").add("project_task_gitea_tree", {
    ...listView,
    Controller: ProjectTaskListController,
    buttonTemplate: "GiteaListView.buttons",
});

patch(projectTaskKanbanView.Controller.prototype, "project_task_gitea_kanban", {
    setup() {
        this._super(...arguments);
        useGiteaButton();
    },
});
projectTaskKanbanView.buttonTemplate = "GiteaKanbanView.buttons";
