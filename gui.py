import sys
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QFrame, QLineEdit, QPushButton,
    QGraphicsDropShadowEffect
)
from PySide6.QtGui import QFont, QTextCursor, QColor

from assistant import Assistant
from command import Command
from translations import text_reshape_farsi


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #b0b0b0;
                border: 1px solid #3a3a3a;
                border-radius: 16px;
                padding: 6px 16px;
                font-size: 12px;
                font-family: 'Segoe UI', 'Arial';
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border-color: #5a5a5a;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)
        # سایه ملایم
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                border-color: #5a5a5a;
                color: #ffffff;
                border-radius: 16px;
                padding: 6px 16px;
                font-size: 12px;
                font-family: 'Segoe UI', 'Arial';
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #b0b0b0;
                border: 1px solid #3a3a3a;
                border-radius: 16px;
                padding: 6px 16px;
                font-size: 12px;
                font-family: 'Segoe UI', 'Arial';
            }
        """)
        super().leaveEvent(event)


class ModernToggleButton(ModernButton):
    def __init__(self, text_on, text_off, parent=None):
        super().__init__(text_off, parent)
        self.text_on = text_on
        self.text_off = text_off
        self.is_checked = False

    def toggle(self):
        self.is_checked = not self.is_checked
        if self.is_checked:
            self.setText(self.text_on)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2a5a3a;
                    color: #ffffff;
                    border: 1px solid #4a8a5a;
                    border-radius: 16px;
                    padding: 6px 16px;
                    font-size: 12px;
                    font-family: 'Segoe UI', 'Arial';
                }
                QPushButton:hover {
                    background-color: #3a6a4a;
                }
            """)
        else:
            self.setText(self.text_off)
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #b0b0b0;
                    border: 1px solid #3a3a3a;
                    border-radius: 16px;
                    padding: 6px 16px;
                    font-size: 12px;
                    font-family: 'Segoe UI', 'Arial';
                }
                QPushButton:hover {
                    background-color: #2a2a2a;
                    border-color: #5a5a5a;
                    color: #ffffff;
                }
            """)
        self.update()

    def setChecked(self, checked):
        if checked != self.is_checked:
            self.toggle()


class ChatBubble(QFrame):
    def __init__(self, text, is_user=False, time=None, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.time = time or datetime.now().strftime("%H:%M")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        if is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2a4a6a;
                    border-radius: 16px 16px 4px 16px;
                    padding: 10px 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2a2a2a;
                    border-radius: 16px 16px 16px 4px;
                    padding: 10px 14px;
                    border: 1px solid #3a3a3a;
                }
            """)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setStyleSheet("color: #e0e0e0;")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.label)

        time_label = QLabel(self.time)
        time_label.setFont(QFont("Segoe UI", 8))
        time_label.setStyleSheet("color: #666666;")
        time_label.setAlignment(Qt.AlignRight)
        layout.addWidget(time_label)

        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(250)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.opacity_anim.start()


class NovaGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # پنجره بدون حاشیه با شفافیت (اختیاری، می‌توانید غیرفعال کنید)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(100, 100, 760, 600)
        self.setMinimumSize(600, 450)

        self.assistant = Assistant("Nova")
        self.command = Command(self.assistant)
        self.command.set_gui_mode(True)
        self.assistant.load()

        self.setup_ui()
        self.add_message("Hello! I'm Nova. \nHow can I help you?", is_user=False)

    def setup_ui(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-radius: 16px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 8)
        central_widget.setGraphicsEffect(shadow)

        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ====== هدر ======
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                border-bottom: 1px solid #2a2a2a;
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)

        # آواتار
        avatar = QLabel("🤖")
        avatar.setFont(QFont("Segoe UI", 24))
        avatar.setStyleSheet("color: #4fc3f7;")
        header_layout.addWidget(avatar)

        # عنوان و وضعیت
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        title = QLabel("Nova Assistant")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0;")
        text_layout.addWidget(title)

        self.status_label = QLabel(" Online • Normal Mode")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #888888;")
        text_layout.addWidget(self.status_label)

        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        # دکمه حالت هوشمند
        self.smart_btn = ModernToggleButton(" Smart ON", " Smart Mode")
        self.smart_btn.clicked.connect(self.toggle_smart_mode)
        header_layout.addWidget(self.smart_btn)

        # دکمه‌های کنترل پنجره
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(16, 16)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5f57;
                border: none;
                border-radius: 8px;
                color: #4a0000;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7a7a;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)

        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(16, 16)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd2e;
                border: none;
                border-radius: 8px;
                color: #4a3a00;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffd64a;
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        header_layout.addWidget(minimize_btn)

        main_layout.addWidget(header)

        # ====== ناحیه چت ======
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #1a1a1a;
                border: none;
            }
            QScrollBar:vertical {
                background: #222222;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #3a3a3a;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4a4a4a;
            }
        """)

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: #1a1a1a;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(10)
        self.chat_layout.setContentsMargins(20, 15, 20, 15)
        self.chat_layout.addStretch()

        self.chat_scroll.setWidget(self.chat_container)
        main_layout.addWidget(self.chat_scroll)

        # ====== پایین ======
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-top: 1px solid #2a2a2a;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
                padding: 10px 15px;
            }
        """)

        footer_layout = QVBoxLayout(footer)
        footer_layout.setSpacing(8)
        footer_layout.setContentsMargins(15, 8, 15, 10)

        # دکمه‌های سریع
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(6)

        quick_commands = [
            (" Weather", "weather"),
            (" Joke", "joke"),
            (" Fact", "fact"),
            (" Search", "search"),
            (" Help", "help"),
        ]

        for label, cmd in quick_commands:
            btn = ModernButton(label)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            quick_layout.addWidget(btn)

        quick_layout.addStretch()
        footer_layout.addLayout(quick_layout)

        # نوار ورودی
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Segoe UI", 12))
        self.input_field.setPlaceholderText("Type a message or command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #222222;
                color: #d0d0d0;
                border: 1px solid #2a2a2a;
                border-radius: 20px;
                padding: 10px 16px;
                font-size: 13px;
                font-family: 'Segoe UI', 'Arial';
            }
            QLineEdit:focus {
                border-color: #4a6a8a;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        # دکمه ارسال
        send_btn = QPushButton("➤")
        send_btn.setFixedSize(42, 42)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a5a7a;
                color: #ffffff;
                border: none;
                border-radius: 21px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3a6a8a;
            }
            QPushButton:pressed {
                background-color: #1a4a6a;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)

        # دکمه Clear
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(42, 42)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a1a1a;
                color: #884444;
                border: none;
                border-radius: 21px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a2a2a;
                color: #aa5555;
            }
        """)
        clear_btn.clicked.connect(self.clear_output)
        input_layout.addWidget(clear_btn)

        footer_layout.addLayout(input_layout)
        main_layout.addWidget(footer)

    def add_message(self, text, is_user=False):
        reshaped = text_reshape_farsi(text)
        bubble = ChatBubble(reshaped, is_user)

        if is_user:
            bubble.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        else:
            bubble.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        self.add_message(user_input, is_user=True)
        self.input_field.clear()

        self.command.process_command(user_input)
        response = self.command.last_output

        if response:
            self.add_message(response, is_user=False)
        else:
            self.add_message("No response received. Try again.", is_user=False)

    def quick_command(self, command):
        self.input_field.setText(command)
        self.send_message()

    def toggle_smart_mode(self):
        self.smart_btn.toggle()
        if self.smart_btn.is_checked:
            self.assistant.smart_mode = True
            self.assistant.load_smart_history()
            self.status_label.setText(" Online • Smart Mode (Active)")
            self.add_message(" Smart mode activated. You can ask anything!", is_user=False)
        else:
            self.assistant.smart_mode = False
            self.assistant.save_smart_history()
            self.status_label.setText(" Online • Normal Mode")
            self.add_message(" Normal mode activated.", is_user=False)

    def clear_output(self):
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.add_message(" Chat cleared.", is_user=False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos'):
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.pos() + delta)
            self.drag_pos = event.globalPosition().toPoint()


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet("QWidget { background-color: #1a1a1a; color: #d0d0d0; }")

    window = NovaGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()