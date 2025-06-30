import sys
from PyQt6.QtCore import QUrl, QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QLineEdit, 
                             QPushButton, QVBoxLayout, QWidget, QTabWidget, 
                             QStatusBar, QStyle, QMessageBox)
from PyQt6.QtGui import QIcon, QAction, QPalette, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile

# Custom WebEnginePage class to handle new window requests (_blank links)
class CustomWebEnginePage(QWebEnginePage):
    """
    Custom WebEnginePage to handle requests for opening links in a new window.
    This class emits a signal that the main browser window can catch to create a new tab
    instead of opening a new OS-level window.
    """
    # Signal that emits the QWebEnginePage of the new window
    new_window_requested = pyqtSignal(QWebEnginePage)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Use a unique, off-the-record profile for each page to enhance isolation
        self.profile = QWebEngineProfile(self)

    def createWindow(self, _type):
        """
        Handles requests to create a new window (e.g., from target='_blank' links).
        Instead of creating a new window, it creates a new page and emits a signal.
        """
        # Create a new page with its own isolated profile
        new_page = CustomWebEnginePage()
        self.new_window_requested.emit(new_page)
        return new_page

# Main Application Class
class Browser(QMainWindow):
    """
    Main browser application window. Inherits from QMainWindow.
    This class sets up the UI, manages tabs, and handles all browser functionalities.
    """
    def __init__(self):
        super().__init__()

        # --- Window Properties ---
        self.setWindowTitle("PyQt6 Modern Web Browser")
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)))
        self.setMinimumSize(QSize(1024, 768))

        # --- Central Widget: Tab Widget ---
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)  # Makes tabs look more like browser tabs
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        # --- Signal/Slot Connections for Tabs ---
        self.tabs.tabBarDoubleClicked.connect(lambda i: self.add_new_tab(label="New Tab"))
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_ui_on_tab_change)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # --- Navigation Toolbar ---
        nav_toolbar = QToolBar("Navigation")
        nav_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(nav_toolbar)

        # --- Menu Bar ---
        self.setup_menu()

        # --- Navigation Actions ---
        # Back Button
        self.back_btn_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)), "Back", self)
        self.back_btn_action.setStatusTip("Go to the previous page")
        self.back_btn_action.triggered.connect(self.navigate_back)
        nav_toolbar.addAction(self.back_btn_action)

        # Forward Button
        self.forward_btn_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)), "Forward", self)
        self.forward_btn_action.setStatusTip("Go to the next page")
        self.forward_btn_action.triggered.connect(self.navigate_forward)
        nav_toolbar.addAction(self.forward_btn_action)

        # Reload Button
        reload_btn_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)), "Reload", self)
        reload_btn_action.setStatusTip("Reload the current page")
        reload_btn_action.triggered.connect(self.reload_page)
        nav_toolbar.addAction(reload_btn_action)

        # Home Button
        home_btn_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)), "Home", self)
        home_btn_action.setStatusTip("Go to the home page")
        home_btn_action.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_btn_action)

        nav_toolbar.addSeparator()

        # --- URL Bar ---
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("QLineEdit { border-radius: 10px; padding: 5px; }")
        nav_toolbar.addWidget(self.url_bar)

        # --- Initial Tab ---
        self.add_new_tab(QUrl("http://www.google.com"), "Homepage")

        self.show()

    def setup_menu(self):
        """Creates and sets up the main menu bar."""
        menu_bar = self.menuBar()

        # --- File Menu ---
        file_menu = menu_bar.addMenu("&File")
        
        new_tab_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        file_menu.addSeparator()

        exit_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton)), "Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # --- Help Menu ---
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("About", self)
        about_action.setStatusTip("Show application information")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def add_new_tab(self, url=None, label="New Tab"):
        """Adds a new tab to the browser."""
        if url is None:
            url = QUrl("about:blank")
        
        # Create the web engine view
        browser_view = QWebEngineView()
        
        # Use the custom page class to handle new window requests
        custom_page = CustomWebEnginePage(browser_view)
        custom_page.new_window_requested.connect(self.handle_new_window_request)
        browser_view.setPage(custom_page)

        browser_view.setUrl(url)
        
        # Add the new view as a tab
        index = self.tabs.addTab(browser_view, label)
        self.tabs.setCurrentIndex(index)

        # --- Connect signals for the new tab's browser view ---
        browser_view.urlChanged.connect(lambda q, browser=browser_view: self.update_url_bar(q, browser))
        browser_view.loadFinished.connect(lambda _, browser=browser_view, i=index: self.update_tab_title(browser, i))
        browser_view.loadProgress.connect(lambda progress: self.status_bar.showMessage(f"Loading... {progress}%"))
        browser_view.loadFinished.connect(lambda: self.status_bar.showMessage("Load finished.", 3000)) # Message disappears after 3s

    def handle_new_window_request(self, page):
        """Creates a new tab for a page requested by createWindow."""
        # This is a bit of a workaround to get the intended URL
        page.urlChanged.connect(lambda url: self.add_new_tab(url=url, label="New Tab"), Qt.ConnectionType.SingleShotConnection)
        
    def close_current_tab(self, index):
        """Closes the tab at the given index."""
        if self.tabs.count() < 2:
            # If it's the last tab, close the entire application
            self.close()
        else:
            widget = self.tabs.widget(index)
            if widget:
                # Disconnect signals to prevent issues
                widget.deleteLater()
            self.tabs.removeTab(index)
            
    def update_tab_title(self, browser, index):
        """Updates the tab's title to the webpage's title."""
        if browser == self.tabs.widget(index):
            title = browser.page().title()
            if len(title) > 30:
                title = title[:27] + "..."
            self.tabs.setTabText(index, title)
            self.tabs.setTabToolTip(index, browser.page().title())
    
    def update_ui_on_tab_change(self, index):
        """Updates the URL bar and navigation buttons when the current tab changes."""
        if index == -1: # No tabs left
            return
            
        browser_view = self.tabs.currentWidget()
        if browser_view:
            self.update_url_bar(browser_view.url(), browser_view)

    def navigate_to_url(self):
        """Navigates the current tab to the URL in the URL bar."""
        text = self.url_bar.text()
        if not text.startswith(('http://', 'https://')):
            url = QUrl("http://" + text)
        else:
            url = QUrl(text)
        
        if url.isValid():
            self.tabs.currentWidget().setUrl(url)
        else:
            self.status_bar.showMessage("Error: Invalid URL", 3000)

    def update_url_bar(self, url, browser=None):
        """Updates the URL bar with the current page's URL."""
        # Only update if the browser view causing the signal is the current one
        if browser is not None and browser != self.tabs.currentWidget():
            return
            
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)
        
        # Update Back/Forward button state
        current_browser = self.tabs.currentWidget()
        if current_browser:
            history = current_browser.page().history()
            self.back_btn_action.setEnabled(history.canGoBack())
            self.forward_btn_action.setEnabled(history.canGoForward())

    def navigate_home(self):
        """Navigates the current tab to the default homepage."""
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_back(self):
        """Navigates the current tab back."""
        self.tabs.currentWidget().back()

    def navigate_forward(self):
        """Navigates the current tab forward."""
        self.tabs.currentWidget().forward()

    def reload_page(self):
        """Reloads the current page."""
        self.tabs.currentWidget().reload()

    def show_about_dialog(self):
        """Displays the 'About' dialog with application information."""
        QMessageBox.about(self, "About PyQt6 Web Browser",
                          "This is a modern web browser created using PyQt6 and QtWebEngine.\n\n"
                          "Developed as a demonstration of a professional desktop application.")

    def closeEvent(self, event):
        """Handles the window close event."""
        reply = QMessageBox.question(self, 'Confirm Exit',
                                     "Are you sure you want to exit the browser?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    
    # --- Modern Styling ---
    app.setStyle("Fusion")

    # Create a dark theme palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.darkGray)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.darkGray)

    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    # Instantiate and show the main window
    window = Browser()
    
    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()