# email_app.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTextEdit, QLineEdit, QPushButton,
    QSplitter, QFrame, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDialog, QFormLayout, QStyleFactory, QStatusBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPalette, QColor, QAction

# --- Main Application Window ---

class EmailApp(QMainWindow):
    """
    Main application window for the Email client.
    Inherits from QMainWindow to provide standard window features like menus, toolbars, and a status bar.
    """
    def __init__(self):
        super().__init__()
        self.dummy_data = {}  # To store simulated email data
        self._initUI()

    def _initUI(self):
        """Initializes the main user interface components."""
        self.setWindowTitle("PyQt6 Email Client")
        self.setGeometry(100, 100, 1200, 800)

        # Set the application icon (uses a standard Qt icon as a fallback)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        # --- Load Data ---
        self._load_dummy_data()

        # --- Create UI Components ---
        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_central_widget()
        self._create_status_bar()

        # --- Initial State ---
        self.folder_list.setCurrentRow(0) # Select "Inbox" by default

    def _create_actions(self):
        """Create QAction objects for menus and toolbars."""
        # --- File Actions ---
        self.new_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "&New Message...", self)
        self.new_action.triggered.connect(self._compose_email)
        self.new_action.setShortcut("Ctrl+N")

        self.exit_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton), "&Exit", self)
        self.exit_action.triggered.connect(self.close)
        self.exit_action.setShortcut("Ctrl+Q")

        # --- Edit Actions ---
        self.reply_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_MailReply), "&Reply", self)
        self.reply_action.triggered.connect(self._reply_email)
        self.reply_action.setShortcut("Ctrl+R")
        self.reply_action.setEnabled(False) # Disabled until an email is selected

        self.forward_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_MailForward), "&Forward", self)
        self.forward_action.triggered.connect(self._forward_email)
        self.forward_action.setShortcut("Ctrl+F")
        self.forward_action.setEnabled(False)

        self.delete_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon), "&Delete", self)
        self.delete_action.triggered.connect(self._delete_email)
        self.delete_action.setShortcut("Delete")
        self.delete_action.setEnabled(False)

        # --- Help Actions ---
        self.about_action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton), "&About", self)
        self.about_action.triggered.connect(self._show_about_dialog)

    def _create_menu_bar(self):
        """Creates the main window's menu bar."""
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.reply_action)
        edit_menu.addAction(self.forward_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.delete_action)

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _create_tool_bar(self):
        """Creates the main toolbar for common actions."""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        
        toolbar.addAction(self.new_action)
        toolbar.addSeparator()
        toolbar.addAction(self.reply_action)
        toolbar.addAction(self.forward_action)
        toolbar.addAction(self.delete_action)

    def _create_status_bar(self):
        """Creates the status bar at the bottom of the window."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _create_central_widget(self):
        """Sets up the main layout of the application using splitters."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5) # Add some padding around the main layout
        main_layout.setSpacing(5)

        # --- Main Splitter (divides folders from email list/view) ---
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Left Pane: Folder List ---
        self.folder_list = QListWidget()
        self.folder_list.setMaximumWidth(200)
        self.folder_list.addItems(self.dummy_data.keys())
        self.folder_list.currentItemChanged.connect(self._folder_changed)
        main_splitter.addWidget(self.folder_list)

        # --- Right Pane: Vertical Splitter ---
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # --- Top-Right Pane: Email List Table ---
        self.email_table = QTableWidget()
        self.email_table.setColumnCount(3)
        self.email_table.setHorizontalHeaderLabels(["From", "Subject", "Date"])
        self.email_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.email_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.email_table.verticalHeader().setVisible(False)
        self.email_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Stretch subject
        self.email_table.itemSelectionChanged.connect(self._email_selected)
        right_splitter.addWidget(self.email_table)

        # --- Bottom-Right Pane: Email Content View ---
        self.email_content_view = QTextEdit()
        self.email_content_view.setReadOnly(True)
        right_splitter.addWidget(self.email_content_view)

        # Set initial sizes for the right splitter
        right_splitter.setSizes([300, 500])

        main_splitter.addWidget(right_splitter)
        
        # Set initial sizes for the main splitter
        main_splitter.setSizes([150, 1050])

        main_layout.addWidget(main_splitter)

    # --- Event Handlers and Functionality ---

    def _load_dummy_data(self):
        """Creates and loads simulated email data."""
        self.dummy_data = {
            "Inbox": [
                {"from": "Alice <alice@example.com>", "subject": "Project Update", "date": "2024-07-28", "body": "Hi Team,\n\nHere is the latest update on the project. Please review the attached document.\n\nBest,\nAlice"},
                {"from": "Bob <bob@example.com>", "subject": "Lunch Today?", "date": "2024-07-28", "body": "Hey, are you free for lunch today at 12:30?"},
                {"from": "Marketing Dept <mktg@corp.com>", "subject": "Weekly Newsletter", "date": "2024-07-27", "body": "Check out our latest news and offers!"},
            ],
            "Sent": [
                {"from": "Me", "to": "Charlie <charlie@example.com>", "subject": "Re: Your Question", "date": "2024-07-26", "body": "Hi Charlie,\n\nHere's the answer to your question from yesterday.\n\nRegards,\nMe"},
            ],
            "Drafts": [],
            "Trash": [
                 {"from": "Spam Service <spam@junk.com>", "subject": "You've Won!", "date": "2024-07-25", "body": "Click here to claim your prize!"},
            ]
        }
        # Add a folder icon to each folder name
        for folder in self.dummy_data.keys():
            item = QListWidgetItem(folder)
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
            item.setIcon(icon)


    def _folder_changed(self, current, previous):
        """Slot for when the selected folder in the QListWidget changes."""
        if not current:
            return
            
        folder_name = current.text()
        self.email_table.setRowCount(0) # Clear the table
        self.email_content_view.clear()
        self._update_action_states(email_selected=False)

        emails = self.dummy_data.get(folder_name, [])
        self.email_table.setRowCount(len(emails))

        for row, email in enumerate(emails):
            self.email_table.setItem(row, 0, QTableWidgetItem(email["from"]))
            self.email_table.setItem(row, 1, QTableWidgetItem(email["subject"]))
            self.email_table.setItem(row, 2, QTableWidgetItem(email["date"]))

        self.status_bar.showMessage(f"Loaded {len(emails)} emails from '{folder_name}'")

    def _email_selected(self):
        """Slot for when an email in the QTableWidget is selected."""
        selected_rows = self.email_table.selectionModel().selectedRows()
        if not selected_rows:
            self.email_content_view.clear()
            self._update_action_states(email_selected=False)
            return

        selected_row = selected_rows[0].row()
        current_folder = self.folder_list.currentItem().text()
        
        try:
            email = self.dummy_data[current_folder][selected_row]
            self.email_content_view.setText(f"From: {email['from']}\n"
                                            f"Subject: {email['subject']}\n"
                                            f"Date: {email['date']}\n"
                                            f"--------------------------------\n\n"
                                            f"{email['body']}")
            self._update_action_states(email_selected=True)
            self.status_bar.showMessage(f"Viewing email: '{email['subject']}'")
        except (KeyError, IndexError):
            # Error handling in case of data inconsistency
            self.email_content_view.setText("Error: Could not load email content.")
            self._update_action_states(email_selected=False)
            self.status_bar.showMessage("Error loading email", 5000)

    def _update_action_states(self, email_selected):
        """Enables or disables actions based on whether an email is selected."""
        self.reply_action.setEnabled(email_selected)
        self.forward_action.setEnabled(email_selected)
        self.delete_action.setEnabled(email_selected)

    def _compose_email(self):
        """Opens the compose email dialog."""
        dialog = ComposeEmailDialog(self)
        if dialog.exec():
            # In a real app, you would send the email and move it to the "Sent" folder
            QMessageBox.information(self, "Email Sent", "Your message has been 'sent' successfully!")
            self.status_bar.showMessage("Email composed and sent.", 5000)
    
    def _reply_email(self):
        """Opens compose dialog pre-filled for a reply."""
        selected_rows = self.email_table.selectionModel().selectedRows()
        if not selected_rows:
            self._show_error_message("No Email Selected", "Please select an email to reply to.")
            return

        selected_row = selected_rows[0].row()
        current_folder = self.folder_list.currentItem().text()
        email = self.dummy_data[current_folder][selected_row]

        dialog = ComposeEmailDialog(self)
        dialog.to_field.setText(email['from'])
        dialog.subject_field.setText(f"Re: {email['subject']}")
        dialog.body_field.setText(f"\n\n--- On {email['date']}, {email['from']} wrote: ---\n> " + email['body'].replace('\n', '\n> '))
        dialog.body_field.moveCursor(dialog.body_field.textCursor().Start)
        
        if dialog.exec():
            QMessageBox.information(self, "Reply Sent", "Your reply has been 'sent' successfully!")
            self.status_bar.showMessage("Replied to email.", 5000)


    def _forward_email(self):
        """Opens compose dialog pre-filled for a forward."""
        selected_rows = self.email_table.selectionModel().selectedRows()
        if not selected_rows:
            self._show_error_message("No Email Selected", "Please select an email to forward.")
            return

        selected_row = selected_rows[0].row()
        current_folder = self.folder_list.currentItem().text()
        email = self.dummy_data[current_folder][selected_row]

        dialog = ComposeEmailDialog(self)
        dialog.subject_field.setText(f"Fwd: {email['subject']}")
        dialog.body_field.setText(f"\n\n--- Forwarded message ---\n"
                                 f"From: {email['from']}\n"
                                 f"Date: {email['date']}\n"
                                 f"Subject: {email['subject']}\n\n"
                                 f"{email['body']}")
        dialog.body_field.moveCursor(dialog.body_field.textCursor().Start)

        if dialog.exec():
            QMessageBox.information(self, "Email Forwarded", "Your message has been 'forwarded' successfully!")
            self.status_bar.showMessage("Forwarded email.", 5000)


    def _delete_email(self):
        """Deletes the selected email (simulates moving to Trash)."""
        selected_rows = self.email_table.selectionModel().selectedRows()
        if not selected_rows:
            self._show_error_message("No Email Selected", "Please select an email to delete.")
            return

        selected_row = selected_rows[0].row()
        current_folder = self.folder_list.currentItem().text()

        # Confirmation dialog
        reply = QMessageBox.question(self, "Delete Email", 
                                     "Are you sure you want to delete this email?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Simulate moving to trash
                email_to_move = self.dummy_data[current_folder].pop(selected_row)
                if 'Trash' in self.dummy_data:
                    self.dummy_data['Trash'].append(email_to_move)
                
                # Refresh the current folder view
                self._folder_changed(self.folder_list.currentItem(), None)
                self.status_bar.showMessage("Email moved to Trash.", 5000)
            except (KeyError, IndexError):
                self._show_error_message("Error", "Could not delete the selected email.")


    def _show_about_dialog(self):
        """Displays the 'About' dialog box."""
        QMessageBox.about(self, "About PyQt6 Email Client",
                          "<b>PyQt6 Email Client</b><br>"
                          "A simple email application example.<br><br>"
                          "Created using PyQt6 and modern Python.<br>"
                          "Version 1.0")
                          
    def _show_error_message(self, title, message):
        """Utility function to show a standardized error message box."""
        QMessageBox.warning(self, title, message)

    def closeEvent(self, event):
        """Overrides the default close event to ask for confirmation."""
        reply = QMessageBox.question(self, 'Exit Confirmation',
                                     "Are you sure you want to exit?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()  # Proceed with closing
        else:
            event.ignore()  # Cancel the close


# --- Compose Email Dialog ---

class ComposeEmailDialog(QDialog):
    """
    A dialog window for composing a new email.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compose New Message")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))

        # --- Layout ---
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # --- Widgets ---
        self.to_field = QLineEdit()
        self.subject_field = QLineEdit()
        self.body_field = QTextEdit()

        form_layout.addRow("To:", self.to_field)
        form_layout.addRow("Subject:", self.subject_field)

        layout.addLayout(form_layout)
        layout.addWidget(self.body_field)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.send_button = QPushButton("Send")
        self.send_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.send_button.clicked.connect(self.accept) # `accept()` closes the dialog with a "success" result

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.cancel_button.clicked.connect(self.reject) # `reject()` closes with a "failure" result

        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

# --- Main Execution ---

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    
    # Apply a modern, dark theme for a professional look
    app.setStyle(QStyleFactory.create("Fusion"))
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(127, 127, 127))
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(127, 127, 127))
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(127, 127, 127))
    
    app.setPalette(dark_palette)
    
    window = EmailApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()