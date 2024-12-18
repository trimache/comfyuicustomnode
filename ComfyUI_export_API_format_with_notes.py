import json
from comfy.model_methods import register_custom_node


class ExportWorkflowWithNotesNode:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {
                "filename": ("STRING", {"default": "workflow_with_notes.json", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "export_workflow"

    CATEGORY = "Workflow/Export"

    def export_workflow(self, filename):
        try:
            # Access the current workflow
            from comfy.control_flow.control import Workflow

            workflow = Workflow.get_current_workflow()
            if workflow is None:
                return ("No workflow is currently loaded.",)

            # Prepare the workflow data for export
            workflow_data = workflow.to_dict()

            # Add notes nodes explicitly if not included
            for node in workflow.nodes:
                if node["type"] == "NOTE":
                    # Ensure note nodes are included
                    workflow_data.setdefault("nodes", []).append(node)

            # Save the workflow to a file
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(workflow_data, file, indent=4)

            return (f"Workflow saved to {filename}.",)

        except Exception as e:
            return (f"Error during export: {str(e)}",)


# Register the custom node
register_custom_node(ExportWorkflowWithNotesNode)
