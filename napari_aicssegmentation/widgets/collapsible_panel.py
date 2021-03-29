from pathlib import Path

from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget
)

DIR = Path.cwd() / "napari_aicssegmentation"


"""
A collapsible panel with a title box that can be clicked to toggle open/closed.

Params:
    step:       Number representing the workflow step. This will be displayed as part of the
                    title and be used as a part of the object name for identification.
    title:      String
    children:   List of QWidget objects to be added as panel contents
    isOpen:     Boolean, whether the panel is open or collapsed
    isEnabled:  Boolean, overwrites the built-in property QWidget.enabled property
"""


class CollapsiblePanel(QWidget):
    def __init__(self, step, title, children, isOpen=True, isEnabled=True):
        super().__init__()
        self.step = step
        self.title = title
        self.children = children
        self.isOpen = isOpen
        self.setEnabled(isEnabled)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 11, 0, 11)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setObjectName(f"collapsiblePanel{step}")

        self.title_box = self.create_title_box()
        self.content_box = self.create_content_box()

        self.layout.addWidget(self.title_box)
        self.layout.addWidget(self.content_box)

    def create_title_box(self):
        title_box = QFrame()
        title_box_layout = QHBoxLayout()
        title_box_layout.setContentsMargins(9, 9, 9, 9)
        title_box.setLayout(title_box_layout)
        title_box.setFixedHeight(40)

        if self.isEnabled is False:
            self.isOpen = False
            title_box.setDisabled(True)
        elif self.isOpen is False:
            title_box.setObjectName("titleBoxClosed")

        # Need HTML due to this bug: https://bugreports.qt.io/browse/QTBUG-90853
        title = QLabel(f'<span>{self.step}.&nbsp;{self.title}</span>')
        icon = QLabel()
        icon.setPixmap(QPixmap(str(DIR / "assets/icons/gear.svg")))
        title_box_layout.addWidget(title)
        title_box_layout.addStretch()
        title_box_layout.addWidget(icon)

        return title_box

    def create_content_box(self):
        content_box = QFrame()
        content_box_layout = QVBoxLayout()
        content_box_layout.setContentsMargins(9, 9, 9, 9)
        content_box.setLayout(content_box_layout)
        content_box.setObjectName("contentBox")

        for child_widget in self.children:
            content_box_layout.addWidget(child_widget)
        
        if self.isOpen is False:
            content_box.hide()
        return content_box
    
    def mousePressEvent(self, event):
        if self.title_box.underMouse():
            if self.isOpen:
                self.isOpen = False
                self.content_box.hide()
                self.title_box.setObjectName("titleBoxClosed")
            else:
                self.isOpen = True
                self.content_box.show()
                self.title_box.setObjectName("")
            self.title_box.setStyle(self.title_box.style())