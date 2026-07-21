import os
import sys
import random

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QMenu


def resource_path(filename):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.drag_offset = QPoint()
        self.dragging = False
        self.auto_move = True
        self.target = None

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.label = QLabel(self)

        image_path = resource_path("character_transparent.png")
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            raise FileNotFoundError(image_path)

        pixmap = pixmap.scaled(
            260,
            360,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.size())
        self.resize(pixmap.size())

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.right() - self.width() - 30,
            screen.bottom() - self.height() - 30
        )

        self.walk_timer = QTimer(self)
        self.walk_timer.timeout.connect(self.choose_position)
        self.walk_timer.start(5000)

        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.smooth_move)
        self.move_timer.start(30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.target = None
            self.drag_offset = (
                event.globalPosition().toPoint() - self.pos()
            )

        elif event.button() == Qt.RightButton:
            self.show_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(
                event.globalPosition().toPoint() - self.drag_offset
            )

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.auto_move = not self.auto_move

    def show_menu(self, position):
        menu = QMenu(self)

        toggle = QAction(
            "关闭自动移动" if self.auto_move else "开启自动移动",
            self
        )
        toggle.triggered.connect(self.toggle_move)
        menu.addAction(toggle)

        center = QAction("移动到屏幕中央", self)
        center.triggered.connect(self.move_center)
        menu.addAction(center)

        menu.addSeparator()

        quit_action = QAction("退出桌宠", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        menu.exec(position)

    def toggle_move(self):
        self.auto_move = not self.auto_move

    def move_center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.target = QPoint(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

    def choose_position(self):
        if not self.auto_move or self.dragging:
            return

        screen = QApplication.primaryScreen().availableGeometry()
        margin = 20

        self.target = QPoint(
            random.randint(
                screen.left() + margin,
                screen.right() - self.width() - margin
            ),
            random.randint(
                screen.top() + margin,
                screen.bottom() - self.height() - margin
            )
        )

    def smooth_move(self):
        if self.target is None or self.dragging:
            return

        current = self.pos()
        dx = self.target.x() - current.x()
        dy = self.target.y() - current.y()

        if abs(dx) < 3 and abs(dy) < 3:
            self.move(self.target)
            self.target = None
            return

        self.move(
            current.x() + int(dx * 0.04),
            current.y() + int(dy * 0.04)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
