# Hook specifications: https://napari.org/docs/dev/plugins/hook_specifications.html
import traceback
import napari
import logging
from napari_aicssegmentation.ui_manager import UIManager
from aicssegmentation.core.pre_processing_utils import image_smoothing_gaussian_3d
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QVBoxLayout
from .mvc.mpp_view import MppView
from .core.view_manager import ViewManager
from .util.debug_utils import debug_class
"""
The class name here gets converted to title case and gets displayed as both the title of the
plugin window and the title displayed in the app menu dropdown.
"""
log = logging.getLogger(__name__)

@debug_class
class AllenCellStructureSegmenter(QWidget):
    def __init__(self, napari_viewer: napari.Viewer):
        super().__init__()
           
        self.viewer = napari_viewer
        self.setLayout(QVBoxLayout())
        base_layout = self.layout()

        ui_manager=UIManager(napari_viewer, base_layout)
        self._view_manager = ViewManager(base_layout)
        view=MppView(ui_manager)
        self._view_manager.load_view(view)
            
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return AllenCellStructureSegmenter
