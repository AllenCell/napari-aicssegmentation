# Hook specifications: https://napari.org/docs/dev/plugins/hook_specifications.html

from aicssegmentation.core.pre_processing_utils import image_smoothing_gaussian_3d
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QMessageBox
from aicssegmentation.structure_wrapper_config.structure_config_utils import load_workflow_config, apply_on_single_image_with_config
from aicssegmentation.structure_wrapper import WorkflowStep, WorkflowEngine

"""
The class name here gets converted to title case and gets displayed as both the title of the
plugin window and the title displayed in the app menu dropdown.
"""
class AllenCellStructureSegmenter(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Sec61b")
        btn.clicked.connect(self.apply_workflow)

        desc = QLabel("Click button to apple the whole sec61b workflow. Result is displayed as a new channel.")
        desc.setWordWrap(True)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(desc)
        self.layout().addWidget(btn)

    def smooth_image(self):
        """Guassian Blur on an image, and add it as a new layer"""
        if self.has_image():
            # Name to add based off previous image's name
            name = self.viewer.layers[len(self.viewer.layers) - 1].name + ": Guassian Blur"

            # Adding the image to the viewer
            self.viewer.add_image(image_smoothing_gaussian_3d(self.viewer.layers[0].data, sigma=3.0), name=name)


        else:
            self.show_message_box("Error: No Image", "Load an image before running guassian blur")

    def has_image(self):
        """Determines if there is already an image loaded onto napari"""
        if len(self.viewer.layers) == 0:
            return False
        else:
            return True

    def show_message_box(self, title, message):
        """Show a message box with the specified title and message"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        return msg.exec()


    def apply_workflow(self):
        engine = WorkflowEngine.WorkflowEngine("sec61b", self.viewer.layers[0].data)
        engine.execute_all()
        self.viewer.add_image(engine.get_most_recent_result(), name="sec61b")



@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return AllenCellStructureSegmenter

