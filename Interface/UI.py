from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QWidget,
    QPushButton, QLabel, QFrame, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QTextBlockFormat, QIcon
from PyQt5.QtCore import Qt, QTimer, QPoint, QSize
from dotenv import dotenv_values
import sys
import os
import random
import logging

# Setup logging
logging.basicConfig(filename='Data/assistant.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

config_data = dotenv_values(".env")
bot_identifier = config_data.get("Assistantname", "Assistant")
user_identifier = config_data.get("Username", "User")
working_directory = os.getcwd()
previous_message_content = ""
storage_location = f"{working_directory}\\Data"

GREETING_COLLECTION = [
    f"Ready to serve, {user_identifier}.",
    f"Here for you, {user_identifier}.",
    f"Standing by, {user_identifier}.",
    f"Yes {user_identifier}, what do you need?",
    f"Present and ready, {user_identifier}.",
    f"All systems go for you, {user_identifier}.",
    f"Great to connect, {user_identifier}.",
    f"Finally, you called, {user_identifier}.",
    f"Awaiting your instructions, {user_identifier}."
]

def ProcessResponseText(response_text):
    try:
        text_lines = response_text.split('\n')
        filtered_lines = [line for line in text_lines if line.strip()]
        processed_response = '\n'.join(filtered_lines)
        return processed_response
    except Exception as e:
        logging.error(f"Error processing response text: {e}")
        return response_text

def ProcessInputQuery(input_query):
    try:
        cleaned_query = input_query.lower().strip()
        query_tokens = cleaned_query.split()
        interrogative_terms = [
            "how", "what", "who", "where", "when", "why", "which", "whose",
            "whom", "can you", "what's", "where's", "how's"
        ]

        if any(term + " " in cleaned_query for term in interrogative_terms):
            if query_tokens[-1][-1] in ['.', '?', '!']:
                cleaned_query = cleaned_query[:-1] + "?"
            else:
                cleaned_query += "?"
        else:
            if query_tokens[-1][-1] in ['.', '?', '!']:
                cleaned_query = cleaned_query[:-1] + "."
            else:
                cleaned_query += "."

        return cleaned_query.capitalize()
    except Exception as e:
        logging.error(f"Error processing input query: {e}")
        return input_query

def UpdateAudioDeviceState(device_command):
    try:
        with open(f'{storage_location}\\Mic.data', "w", encoding='utf-8') as data_file:
            data_file.write(device_command)
    except Exception as e:
        logging.error(f"Error updating audio device state: {e}")

def RetrieveAudioDeviceState():
    try:
        with open(f'{storage_location}\\Mic.data', "r", encoding='utf-8') as data_file:
            device_state = data_file.read()
        return device_state
    except Exception as e:
        logging.error(f"Error retrieving audio device state: {e}")
        return "False"

def ModifyBotOperationalState(operational_state):
    try:
        with open(f'{storage_location}\\Status.data', "w", encoding='utf-8') as data_file:
            data_file.write(operational_state)
    except Exception as e:
        logging.error(f"Error modifying bot operational state: {e}")

def RetrieveBotOperationalState():
    try:
        with open(f'{storage_location}\\Status.data', "r", encoding='utf-8') as data_file:
            operational_state = data_file.read()
        return operational_state
    except Exception as e:
        logging.error(f"Error retrieving bot operational state: {e}")
        return "Available ... "

def InitializeAudioDevice():
    UpdateAudioDeviceState("False")

def ActivateAudioDevice():
    UpdateAudioDeviceState("True")

def BuildStoragePath(file_identifier):
    complete_path = f'{storage_location}\\{file_identifier}'
    return complete_path

def DisplayContentOnScreen(display_content):
    try:
        with open(f'{storage_location}\\Responses.data', "w", encoding='utf-8') as data_file:
            data_file.write(display_content)
    except Exception as e:
        logging.error(f"Error displaying content on screen: {e}")

def SelectRandomGreeting():
    return random.choice(GREETING_COLLECTION)

class CompactConversationPanel(QWidget):
    def __init__(self):
        super().__init__()
        panel_layout = QVBoxLayout(self)
        panel_layout.setContentsMargins(5, 5, 5, 5)
        panel_layout.setSpacing(5)

        self.info_panel = QFrame()
        self.info_panel.setFrameShape(QFrame.StyledPanel)
        self.info_panel.setFixedHeight(25)
        info_arrangement = QHBoxLayout(self.info_panel)
        info_arrangement.setContentsMargins(5, 0, 5, 0)

        self.info_symbol = QLabel()
        self.info_symbol.setPixmap(QIcon.fromTheme("audio-input-microphone").pixmap(16, 16))
        self.info_text = QLabel("Available ... ")
        self.info_text.setStyleSheet("color: #ffffff; font-size: 11px;")

        info_arrangement.addWidget(self.info_symbol)
        info_arrangement.addWidget(self.info_text)
        info_arrangement.addStretch()

        panel_layout.addWidget(self.info_panel)

        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.conversation_display.setFrameStyle(QFrame.NoFrame)
        self.conversation_display.setVisible(False)

        display_font = QFont()
        display_font.setPointSize(10)
        self.conversation_display.setFont(display_font)

        self.conversation_display.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        panel_layout.addWidget(self.conversation_display)

        self.visibility_control = QPushButton("Show Chat History")
        self.visibility_control.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ffffff;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        self.visibility_control.clicked.connect(self.toggle_conversation_visibility)
        panel_layout.addWidget(self.visibility_control)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.RefreshConversation)
        self.update_timer.timeout.connect(self.RefreshBotState)
        self.update_timer.start(500)  # Increased from 200ms

        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #5a5a5a;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    def toggle_conversation_visibility(self):
        current_visibility = self.conversation_display.isVisible()
        self.conversation_display.setVisible(not current_visibility)
        self.visibility_control.setText("Hide Chat History" if not current_visibility else "Show Chat History")

        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            if not current_visibility:
                main_window.setFixedHeight(350)
            else:
                main_window.setFixedHeight(180)

    def RefreshConversation(self):
        global previous_message_content
        try:
            with open(BuildStoragePath('Responses.data'), "r", encoding='utf-8') as data_file:
                current_messages = data_file.read()

            if current_messages and current_messages != previous_message_content:
                self.conversation_display.clear()
                self.AppendMessageToDisplay(message_content=current_messages, text_color='#e0e0e0')
                previous_message_content = current_messages

                if self.conversation_display.isVisible():
                    self.conversation_display.verticalScrollBar().setValue(
                        self.conversation_display.verticalScrollBar().maximum()
                    )
        except Exception as e:
            logging.error(f"Error refreshing conversation: {e}")

    def RefreshBotState(self):
        try:
            with open(BuildStoragePath('Status.data'), "r", encoding='utf-8') as data_file:
                current_state = data_file.read()
            audio_state = RetrieveAudioDeviceState()
            logging.debug(f"UI Status: {current_state}, Audio: {audio_state}")
            if audio_state == "True":
                self.info_symbol.setPixmap(QIcon.fromTheme("audio-input-microphone").pixmap(16, 16))
            else:
                self.info_symbol.setPixmap(QIcon.fromTheme("microphone-sensitivity-muted").pixmap(16, 16))
            self.info_text.setText(current_state)
        except Exception as e:
            logging.error(f"Error refreshing bot state: {e}")

    def AppendMessageToDisplay(self, message_content, text_color):
        text_cursor = self.conversation_display.textCursor()
        char_formatting = QTextCharFormat()
        block_formatting = QTextBlockFormat()
        block_formatting.setTopMargin(5)
        block_formatting.setLeftMargin(5)
        char_formatting.setForeground(QColor(text_color))
        text_cursor.setCharFormat(char_formatting)
        text_cursor.setBlockFormat(block_formatting)
        text_cursor.insertText(message_content)
        self.conversation_display.setTextCursor(text_cursor)

class AudioInputControl(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.activation_state = False
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                border-radius: 20px;
                border: 2px solid #5a5a5a;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

        self.audio_symbol = QIcon.fromTheme("microphone-sensitivity-muted")
        self.setIcon(self.audio_symbol)
        self.setIconSize(QSize(24, 24))

        self.clicked.connect(self.switch_audio_state)
        InitializeAudioDevice()

    def switch_audio_state(self):
        self.activation_state = not self.activation_state
        if self.activation_state:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1e88e5;
                    border-radius: 20px;
                    border: 2px solid #42a5f5;
                }
                QPushButton:hover {
                    background-color: #2196f3;
                }
            """)
            self.setIcon(QIcon.fromTheme("audio-input-microphone"))
            ActivateAudioDevice()
            logging.debug("Audio activated")
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3a3a3a;
                    border-radius: 20px;
                    border: 2px solid #5a5a5a;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
            """)
            self.setIcon(QIcon.fromTheme("microphone-sensitivity-muted"))
            InitializeAudioDevice()
            logging.debug("Audio deactivated")

class StreamlinedBotInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(f"{bot_identifier}")
        self.setupInterface()
        self.drag_active = False
        self.drag_offset = QPoint()
        self.setFixedWidth(450)
        self.adjustSize()
        self.setFixedHeight(self.sizeHint().height())

        self.move(20, 20)

        self.previous_command = ""
        self.monitoring_timer = QTimer(self)
        self.monitoring_timer.timeout.connect(self.monitor_commands)
        self.monitoring_timer.start(1000)  # Increased from 500ms

    def setupInterface(self):
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)

        container_layout = QVBoxLayout(self.main_container)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0, 0, 0, 0)

        header_section = QWidget()
        header_section.setFixedHeight(30)
        header_arrangement = QHBoxLayout(header_section)
        header_arrangement.setContentsMargins(10, 0, 5, 0)
        header_arrangement.setSpacing(5)

        self.header_symbol = QLabel()
        self.header_symbol.setPixmap(QIcon.fromTheme("microphone-sensitivity-muted").pixmap(16, 16))

        header_text = QLabel(f"{bot_identifier}")
        header_text.setStyleSheet("""
            color: #ffffff;
            font-weight: bold;
            font-size: 12px;
        """)

        exit_control = QPushButton("✕")
        exit_control.setFixedSize(20, 20)
        exit_control.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaaaaa;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff5555;
                background-color: #444444;
                border-radius: 10px;
            }
        """)
        exit_control.clicked.connect(self.close)

        header_arrangement.addWidget(self.header_symbol)
        header_arrangement.addWidget(header_text)
        header_arrangement.addStretch(1)
        header_arrangement.addWidget(exit_control)

        header_section.setStyleSheet("background-color: #1e88e5;")

        header_section.mousePressEvent = self.headerMousePressed
        header_section.mouseMoveEvent = self.headerMouseMoved
        header_section.mouseReleaseEvent = self.headerMouseReleased

        content_area = QWidget()
        content_arrangement = QVBoxLayout(content_area)
        content_arrangement.setContentsMargins(0, 0, 0, 0)
        content_arrangement.setSpacing(0)

        self.conversation_panel = CompactConversationPanel()

        control_bar = QFrame()
        control_bar.setFrameShape(QFrame.StyledPanel)
        control_bar.setFixedHeight(60)
        control_arrangement = QHBoxLayout(control_bar)
        control_arrangement.setContentsMargins(15, 5, 15, 5)

        self.audio_control = AudioInputControl()

        control_arrangement.addStretch(1)
        control_arrangement.addWidget(self.audio_control)
        control_arrangement.addStretch(1)

        content_arrangement.addWidget(self.conversation_panel)
        content_arrangement.addWidget(control_bar)

        content_area.setStyleSheet("background-color: #252525;")

        container_layout.addWidget(header_section)
        container_layout.addWidget(content_area)

        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.refreshInterfaceState)
        self.state_timer.start(500)  # Increased from 200ms

    def refreshInterfaceState(self):
        try:
            current_state = RetrieveBotOperationalState()
            audio_state = RetrieveAudioDeviceState()
            if audio_state == "True":
                self.header_symbol.setPixmap(QIcon.fromTheme("audio-input-microphone").pixmap(16, 16))
            else:
                self.header_symbol.setPixmap(QIcon.fromTheme("microphone-sensitivity-muted").pixmap(16, 16))
        except Exception as e:
            logging.error(f"Error refreshing interface state: {e}")

    def monitor_commands(self):
        try:
            with open(BuildStoragePath('Database.data'), "r", encoding='utf-8') as data_file:
                file_content = data_file.read().strip()

            if file_content:
                content_lines = file_content.split('\n')
                if content_lines:
                    latest_line = content_lines[-1].lower()

                    if latest_line != self.previous_command:
                        self.previous_command = latest_line

                        if "jarvis" in latest_line and any(keyword in latest_line for keyword in ["wake", "are you there", "you there", "hello", "hi", "wake up"]):
                            greeting_response = SelectRandomGreeting()
                            updated_content = file_content + f"\n{bot_identifier} : {greeting_response}"
                            DisplayContentOnScreen(updated_content)

                            self.audio_control.activation_state = True
                            self.audio_control.setStyleSheet("""
                                QPushButton {
                                    background-color: #1e88e5;
                                    border-radius: 20px;
                                    border: 2px solid #42a5f5;
                                }
                                QPushButton:hover {
                                    background-color: #2196f3;
                                }
                            """)
                            self.audio_control.setIcon(QIcon.fromTheme("audio-input-microphone"))
                            ActivateAudioDevice()
                            logging.debug("Wake command detected")

                        elif "jarvis" in latest_line and any(keyword in latest_line for keyword in ["sleep", "mute", "stop", "quiet"]):
                            self.audio_control.activation_state = False
                            self.audio_control.setStyleSheet("""
                                QPushButton {
                                    background-color: #3a3a3a;
                                    border-radius: 20px;
                                    border: 2px solid #5a5a5a;
                                }
                                QPushButton:hover {
                                    background-color: #4a4a4a;
                                }
                            """)
                            self.audio_control.setIcon(QIcon.fromTheme("microphone-sensitivity-muted"))
                            InitializeAudioDevice()
                            logging.debug("Sleep command detected")

                            sleep_response = f"Entering sleep mode. Wake me when needed, {user_identifier}."
                            updated_content = file_content + f"\n{bot_identifier} : {sleep_response}"
                            DisplayContentOnScreen(updated_content)
        except Exception as e:
            logging.error(f"Error monitoring commands: {e}")

    def headerMousePressed(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_active = True
            self.drag_offset = event.pos()

    def headerMouseMoved(self, event):
        if self.drag_active and event.buttons() & Qt.LeftButton:
            self.move(self.mapToGlobal(event.pos() - self.drag_offset))

    def headerMouseReleased(self, event):
        self.drag_active = False

def InitializeGraphicalInterface():
    try:
        application = QApplication(sys.argv)
        application.setStyle('Fusion')

        theme_palette = application.palette()
        theme_palette.setColor(theme_palette.Window, QColor(37, 37, 37))
        theme_palette.setColor(theme_palette.WindowText, QColor(220, 220, 220))
        theme_palette.setColor(theme_palette.Base, QColor(45, 45, 45))
        theme_palette.setColor(theme_palette.AlternateBase, QColor(53, 53, 53))
        theme_palette.setColor(theme_palette.ToolTipBase, QColor(60, 60, 60))
        theme_palette.setColor(theme_palette.ToolTipText, QColor(220, 220, 220))
        theme_palette.setColor(theme_palette.Text, QColor(220, 220, 220))
        theme_palette.setColor(theme_palette.Button, QColor(53, 53, 53))
        theme_palette.setColor(theme_palette.ButtonText, QColor(220, 220, 220))
        theme_palette.setColor(theme_palette.BrightText, QColor(255, 0, 0))
        theme_palette.setColor(theme_palette.Highlight, QColor(30, 136, 229))
        theme_palette.setColor(theme_palette.HighlightedText, QColor(255, 255, 255))
        application.setPalette(theme_palette)

        interface_window = StreamlinedBotInterface()
        interface_window.show()
        sys.exit(application.exec_())
    except Exception as e:
        logging.error(f"Error initializing graphical interface: {e}")

if __name__ == "__main__":
    InitializeGraphicalInterface()