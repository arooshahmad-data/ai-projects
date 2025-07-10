import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTextEdit, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class ImageViewer(QWidget):
    """
    A PyQt5-based application for browsing images and their associated text files,
    copying them to specified destinations, editing and saving text content, and
    displaying image details.

    Attributes:
    - image_folder_path: Path to the folder containing images.
    - text_folder_path: Path to the folder containing text files associated with images.
    - dest_image_folder_path: Destination path for copying images.
    - dest_text_folder_path: Destination path for copying text files.
    - image_files: List of image filenames in the selected image folder.
    - current_index: Index of the currently displayed image in image_files list.
    """

    def __init__(self):
        """Initialize the ImageViewer widget."""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Set up the user interface."""
        self.image_folder_path = None
        self.text_folder_path = None
        self.dest_image_folder_path = None
        self.dest_text_folder_path = None
        self.image_files = []
        self.current_index = 0

        self.setWindowTitle('Data Verification Tool')
        self.setGeometry(100, 100, 1200, 800)

        # Widgets
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("font-size: 15px;")  # Set default font size to 15px

        self.image_path_edit = QLineEdit(self)
        self.text_path_edit = QLineEdit(self)
        self.dest_image_path_edit = QLineEdit(self)
        self.dest_text_path_edit = QLineEdit(self)

        self.prev_button = QPushButton('Previous', self)
        self.next_button = QPushButton('Next', self)
        self.copy_button = QPushButton('Copy', self)
        self.edit_text_button = QPushButton('Edit Text', self)
        self.save_text_button = QPushButton('Save Text', self)

        # Style Buttons
        self.style_buttons()

        # Message Label
        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)  # Allow text wrapping

        # Count Labels
        self.image_count_label = QLabel('', self)
        self.text_count_label = QLabel('', self)
        self.dest_image_count_label = QLabel('', self)
        self.dest_text_count_label = QLabel('', self)

        # Layouts
        main_layout = QHBoxLayout(self)

        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        path_layout = QVBoxLayout()
        path_layout.addWidget(QLabel('Image Folder: '))
        image_path_layout = QHBoxLayout()
        image_path_layout.addWidget(self.image_path_edit)
        image_path_layout.addWidget(QPushButton('Browse', clicked=self.select_image_folder))
        path_layout.addLayout(image_path_layout)
        path_layout.addWidget(self.image_count_label)

        path_layout.addWidget(QLabel('Text Folder: '))
        text_path_layout = QHBoxLayout()
        text_path_layout.addWidget(self.text_path_edit)
        text_path_layout.addWidget(QPushButton('Browse', clicked=self.select_text_folder))
        path_layout.addLayout(text_path_layout)
        path_layout.addWidget(self.text_count_label)

        image_text_layout = QVBoxLayout()
        image_text_layout.addWidget(self.image_label)
        image_text_layout.addWidget(self.text_edit)

        nav_button_layout = QHBoxLayout()
        nav_button_layout.addWidget(self.prev_button)
        nav_button_layout.addWidget(self.next_button)

        right_panel.addLayout(path_layout)
        right_panel.addWidget(self.message_label)  # Message label added here
        right_panel.addLayout(image_text_layout)
        right_panel.addLayout(nav_button_layout)

        copy_path_layout = QVBoxLayout()
        copy_path_layout.addWidget(QLabel('Destination Image Folder: '))
        dest_image_path_layout = QHBoxLayout()
        dest_image_path_layout.addWidget(self.dest_image_path_edit)
        dest_image_path_layout.addWidget(QPushButton('Browse', clicked=self.select_dest_image_folder))
        copy_path_layout.addLayout(dest_image_path_layout)
        copy_path_layout.addWidget(self.dest_image_count_label)

        copy_path_layout.addWidget(QLabel('Destination Text Folder: '))
        dest_text_path_layout = QHBoxLayout()
        dest_text_path_layout.addWidget(self.dest_text_path_edit)
        dest_text_path_layout.addWidget(QPushButton('Browse', clicked=self.select_dest_text_folder))
        copy_path_layout.addLayout(dest_text_path_layout)
        copy_path_layout.addWidget(self.dest_text_count_label)

        # Create a vertical layout for bottom buttons
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignBottom)  # Align buttons to the bottom
        button_layout.setSpacing(10)  # Set the spacing between buttons

        # Create two horizontal layouts for button groups
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.setSpacing(10)
        nav_buttons_layout.addWidget(self.prev_button)
        nav_buttons_layout.addWidget(self.next_button)

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setAlignment(Qt.AlignCenter)  # Center-align the buttons
        action_buttons_layout.setSpacing(10)
        action_buttons_layout.addWidget(self.copy_button)
        action_buttons_layout.addWidget(self.edit_text_button)
        action_buttons_layout.addWidget(self.save_text_button)

        # Add button groups to the main button layout
        button_layout.addLayout(nav_buttons_layout)
        button_layout.addLayout(action_buttons_layout)

        left_panel.addLayout(copy_path_layout)
        left_panel.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        right_panel.addLayout(button_layout)
        right_panel.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(right_panel)
        main_layout.addLayout(left_panel)

        self.setLayout(main_layout)

        # Connect button signals
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.copy_button.clicked.connect(self.copy_image_and_text)
        self.edit_text_button.clicked.connect(self.edit_text)
        self.save_text_button.clicked.connect(self.save_text)

    def style_buttons(self):
        """Apply styles to buttons."""
        button_style = (
            "background-color: {}; color: white; border-radius: 5px; "
            "padding: 5px; min-width: 100px; max-width: 100px; min-height: 35px; max-height: 35px;"
        )
        self.prev_button.setStyleSheet(button_style.format("#FFA07A"))
        self.next_button.setStyleSheet(button_style.format("#8FBC8F"))
        self.copy_button.setStyleSheet(button_style.format("#1E90FF"))
        self.edit_text_button.setStyleSheet(button_style.format("#FFD700"))
        self.save_text_button.setStyleSheet(button_style.format("#FF6347"))

    def select_image_folder(self):
        """Open a dialog to select the image folder."""
        self.image_folder_path = QFileDialog.getExistingDirectory(self, 'Select Image Folder')
        self.image_path_edit.setText(self.image_folder_path)
        self.load_images()

    def select_text_folder(self):
        """Open a dialog to select the text folder."""
        self.text_folder_path = QFileDialog.getExistingDirectory(self, 'Select Text Folder')
        self.text_path_edit.setText(self.text_folder_path)
        self.load_images()  # Load images after setting text_folder_path

    def select_dest_image_folder(self):
        """Open a dialog to select the destination folder for images."""
        self.dest_image_folder_path = QFileDialog.getExistingDirectory(self, 'Select Destination Image Folder')
        self.dest_image_path_edit.setText(self.dest_image_folder_path)
        self.update_dest_folder_counts()

    def select_dest_text_folder(self):
        """Open a dialog to select the destination folder for text files."""
        self.dest_text_folder_path = QFileDialog.getExistingDirectory(self, 'Select Destination Text Folder')
        self.dest_text_path_edit.setText(self.dest_text_folder_path)
        self.update_dest_folder_counts()

    def update_dest_folder_counts(self):
        """Update labels showing file counts in destination folders."""
        if self.dest_image_folder_path:
            image_count = len([filename for filename in os.listdir(self.dest_image_folder_path)
                               if filename.lower().endswith(('.png', '.jpg', '.jpeg'))])
            self.dest_image_count_label.setText(f'Images: {image_count} files')

        if self.dest_text_folder_path:
            text_count = len([filename for filename in os.listdir(self.dest_text_folder_path)
                              if filename.lower().endswith('.txt')])
            self.dest_text_count_label.setText(f'Text: {text_count} files')

    def load_images(self):
        """Load images from the selected image folder."""
        if self.image_folder_path and self.text_folder_path:
            image_files = [filename for filename in os.listdir(self.image_folder_path)
                           if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.image_files = image_files
            total_images = len(image_files)
            self.image_count_label.setText(f'Images: {total_images} files')

            self.current_index = 0
            self.show_image_and_text()

    def show_image_and_text(self):
        """Display the currently selected image and its associated text."""
        if self.image_files:
            image_filename = self.image_files[self.current_index]
            image_path = os.path.join(self.image_folder_path, image_filename)
            text_filename = os.path.splitext(image_filename)[0] + '.txt'
            if self.text_folder_path:
                text_path = os.path.join(self.text_folder_path, text_filename)
                if os.path.exists(text_path):
                    with open(text_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                        self.text_edit.setPlainText(text_content)
                else:
                    self.text_edit.setPlainText('No text file found for this image.')
            else:
                self.text_edit.setPlainText('Select a text folder to view associated text.')

            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaledToWidth(600))  # Adjust width as needed
            self.image_label.setAlignment(Qt.AlignCenter)

    def show_previous_image(self):
        """Display the previous image in the list."""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image_and_text()

    def show_next_image(self):
        """Display the next image in the list."""
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image_and_text()

    def copy_image_and_text(self):
        """Copy the currently displayed image and its associated text to specified destinations."""
        if self.image_folder_path and self.text_folder_path and self.dest_image_folder_path and self.dest_text_folder_path:
            if self.current_index < len(self.image_files):
                image_filename = self.image_files[self.current_index]
                image_source_path = os.path.join(self.image_folder_path, image_filename)
                text_filename = os.path.splitext(image_filename)[0] + '.txt'
                text_source_path = os.path.join(self.text_folder_path, text_filename)

                dest_image_path = os.path.join(self.dest_image_folder_path, image_filename)
                dest_text_path = os.path.join(self.dest_text_folder_path, text_filename)

                if os.path.exists(dest_image_path) and os.path.exists(dest_text_path):
                    self.show_message('Copy Error', 'Files already exist in the destination directories!', 'darkred')
                elif os.path.exists(dest_image_path):
                    self.show_message('Copy Error', 'Image file already exists in the destination directory!', 'darkred')
                elif os.path.exists(dest_text_path):
                    self.show_message('Copy Error', 'Text file already exists in the destination directory!', 'darkred')
                else:
                    try:
                        # Copy image file
                        shutil.copyfile(image_source_path, dest_image_path)
                        # Copy text file
                        shutil.copyfile(text_source_path, dest_text_path)

                        self.show_message('Copy', 'Image and Text copied successfully!', 'green')
                        self.update_dest_folder_counts()  # Update counts after successful copy
                    except Exception as e:
                        self.show_message('Copy Error', f'Failed to copy files: {str(e)}', 'darkred')
        else:
            self.show_message('Copy Error', 'Select image, text, and destination folders before copying!', 'darkred')

    def edit_text(self):
        """Allow editing of the text content."""
        self.text_edit.setReadOnly(False)

    def save_text(self):
        """Save the edited text content."""
        if self.image_folder_path and self.text_folder_path:
            if self.current_index < len(self.image_files):
                text_filename = os.path.splitext(self.image_files[self.current_index])[0] + '.txt'
                text_path = os.path.join(self.text_folder_path, text_filename)
                new_text_content = self.text_edit.toPlainText()

                try:
                    with open(text_path, 'w', encoding='utf-8-sig') as f:
                        f.write(new_text_content)
                    self.show_message('Save Text', 'Text saved successfully!', 'green')
                    self.text_edit.setReadOnly(True)
                except Exception as e:
                    self.show_message('Save Error', f'Failed to save text: {str(e)}', 'darkred')
        else:
            self.show_message('Save Error', 'Select image and text folders before saving!', 'darkred')

    def show_message(self, title, message, color):
        """Display a message in the message label."""
        style = f'color: {color};'
        self.message_label.setStyleSheet(style)
        self.message_label.setText(f'<b>{title}</b>: {message}')
        QTimer.singleShot(5000, self.clear_message)  # Clear message after 5 seconds

    def clear_message(self):
        """Clear the message label."""
        self.message_label.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
