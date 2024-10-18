from PyQt5.QtWidgets import QApplication, QWidget,QVBoxLayout,QProgressBar, QHBoxLayout, QRadioButton, \
    QLineEdit, QLabel, QPushButton,QFileDialog,QTextEdit,QMessageBox,QComboBox,QInputDialog,QCheckBox,QStyleFactory
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent,QIcon,QFont
import os
import sys
import boto3
import pika
import sqlite3
import ssl
import botocore.exceptions

class SignupLogin(QWidget):
    def __init__(self):
        super().__init__()
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in a PyInstaller bundle
            self.bundle_dir = sys._MEIPASS
        else:
            # Running as a normal script
            self.bundle_dir = os.path.abspath(os.path.dirname(__file__))

        self.set_icons()
        self.create_widgets()
        
    def set_icons(self):
        self.submit = os.path.join(self.bundle_dir, 'icons' ,'upload.png')
        self.clear = os.path.join(self.bundle_dir, 'icons' ,'clear.png')

    def create_widgets(self):
        self.create_buttons()
        self.create_fields()
        self.create_layout()
        self.set_button_cursors()
    
    def create_buttons(self):
        self.clear_button = QPushButton("Clear")
        self.login_button = QPushButton("Login")

        self.clear_button.setIcon(QIcon(self.clear))
        self.login_button.setIcon(QIcon(self.submit))

        self.clear_button.setEnabled(True)
        self.login_button.setEnabled(True)

        #  submit and clear button working
        self.clear_button.clicked.connect(self.on_clear_clicked)
        self.login_button.clicked.connect(lambda: self.sign_up_login())


    def set_button_cursors(self):
        # Set cursor to hand when hovering over buttons
        self.clear_button.setCursor(Qt.PointingHandCursor)

    def create_fields(self):
        self.login_fields()
        self.widget_style()

    def create_layout(self):        

        self.input_layout = self.create_input_layout()
        self.button_layout = self.create_button_layout()
        self.create_main_layout(self.input_layout,self.button_layout)
    
    def fields_layout(self,label_field,input_field):
        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(label_field)
        label_input_layout.addWidget(input_field)

        return label_input_layout
    
    def create_input_layout(self):
        self.input_layout = QVBoxLayout()
        self.file_layout = QHBoxLayout()

        # AWS S3 fileds
        self.fileds_box_layout()
        # Add the file layout to the main layout
        self.input_layout.addLayout(self.file_layout)

        return self.input_layout
    
    def create_button_layout(self):
        # Submit and Clear button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.clear_button)
        button_layout.setAlignment(Qt.AlignLeft)
        return button_layout
    
    def create_main_layout(self,input_layout,button_layout):
        #  all main layout
        self.main_layout = QVBoxLayout(self)

        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(input_layout)

        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(button_layout)

    def show_error(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.addButton(QMessageBox.Ok)
        error_dialog.setDefaultButton(QMessageBox.Ok)
        for button in error_dialog.buttons():
            button.setCursor(Qt.PointingHandCursor)
        error_dialog.exec_()
    
    def show_success(self,message):
        success_popup = QMessageBox(self)
        success_popup.setIcon(QMessageBox.Information)
        success_popup.setWindowTitle("Success")
        success_popup.setText(message)
        success_popup.addButton(QMessageBox.Ok)
        success_popup.setDefaultButton(QMessageBox.Ok)
        success_popup.setModal(True)   

        # Set cursor to hand when hovering over QMessageBox buttons
        for button in success_popup.buttons():
            button.setCursor(Qt.PointingHandCursor)

        success_popup.exec_()

    def sign_up_login(self):
        if not self.login_validate():
            return

        username = self.login_username_input.text()
        password = self.login_password_input.text()
        if username == "admin" and password == "admin":
            window.show()
            signup_login.close()
        else:
            self.show_error("Invalid Credentials")
            self.clear_input_fields()
            return 
       
    def on_clear_clicked(self):
        self.clear_input_fields()

    def clear_input_fields(self):
        self.login_username_input.clear()
        self.login_password_input.clear()

    def create_label_fileds(self,text):
        signup_login_label = QLabel(text, self)
        return signup_login_label

    def create_input_fileds(self):
        signup_login_input = QLineEdit(self)
        return signup_login_input

    def login_fields(self):

        self.login_username_label = self.create_label_fileds('Username:')
        self.login_password_label = self.create_label_fileds('Password:')

        self.login_username_input = self.create_input_fileds()
        self.login_password_input = self.create_input_fileds()
        
    def fileds_box_layout(self):
 
        self.username_layout = QHBoxLayout()
        self.username_layout.addWidget(self.login_username_label)
        self.username_layout.addWidget(self.login_username_input)

        self.input_layout.addLayout(self.username_layout)

        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(self.login_password_label)
        self.password_layout.addWidget(self.login_password_input)

        self.input_layout.addLayout(self.password_layout)  
        
    def login_show_fields(self):
        self.login_username_label.show()
        self.login_username_input.show()

        self.login_password_label.show()
        self.login_password_input.show()
        self.login_button.show()

    def login_validate(self):
        if not self.login_username_input.text():
            self.show_error("Please Fill UserName.")
            return False

        elif not self.login_password_input.text():
            self.show_error("Please Fill Password.")
            return False
        else:
            return True

    def widget_style(self):

        # set the window title
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(os.path.join(self.bundle_dir, 'icons' ,'cloud-uploder.png')))
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        font_size = 10 # You can adjust the font size as needed
        # Labels
        labels = [
            self.login_username_label, self.login_password_label,
            self.login_username_input,self.login_password_input
        ]

        for label in labels:
            label.setFont(QFont('Segoe UI', font_size))
        
        # set fixed lables width
        max_label_width = max(
            self.login_username_label.sizeHint().width(),
            self.login_password_label.sizeHint().width(),
        )
        self.login_username_label.setFixedWidth(max_label_width)
        self.login_password_label.setFixedWidth(max_label_width)

        # Input fields
        inputs = [
            self.login_username_input, self.login_password_input
        ]
        # self.rabbitmq_host_input.setFixedWidth(100)
        for input_field in inputs:
            input_field.setFixedHeight(35)  # Adjust the height as needed

        # Set placeholder text for RabbitMQ input fields
        self.login_username_input.setPlaceholderText("Enter Email")
        self.login_password_input.setPlaceholderText("Enter Password")

        # print(self.submit_button.)
        self.login_button.setFixedHeight(40)
        self.login_button.setFixedWidth(150)

        self.clear_button.setFixedHeight(40)
        self.clear_button.setFixedWidth(150)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in a PyInstaller bundle
            self.bundle_dir = sys._MEIPASS
        else:
            # Running as a normal script
            self.bundle_dir = os.path.abspath(os.path.dirname(__file__))

        self.select_file = "Select Files"
        self.set_icons()
        self.create_database()
        self.create_widgets()
    
    def create_database(self):
        # Connect to SQLite database (creates a new database if it doesn't exist)
        self.connection = sqlite3.connect(".cloud_uploader.db")

        # Create a cursor object to execute SQL commands
        self.cursor = self.connection.cursor()

        # Create a table for RabbitMQ fields
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rabbitmq_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_name TEXT,
                host TEXT,
                username TEXT,
                password TEXT,
                virtualhost TEXT,
                port TEXT,
                queue TEXT,
                files TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # # Create a table for AWS S3 fields
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS aws_s3_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_name TEXT,
                access_key TEXT,
                secret_key TEXT,
                region TEXT,
                bucket_name TEXT,
                folder TEXT,
                files TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # # Commit changes and close the connection
        self.connection.commit()

    def set_icons(self):
        self.rabbitmq_icon = os.path.join(self.bundle_dir, 'icons' ,'rabbitmq_logo.png')
        self.awss3_icon = os.path.join(self.bundle_dir, 'icons' ,'aws.png')
        self.choose_file = os.path.join(self.bundle_dir, 'icons' ,'choose_file.png')
        self.submit = os.path.join(self.bundle_dir, 'icons' ,'upload.png')
        self.clear = os.path.join(self.bundle_dir, 'icons' ,'clear.png')

    def create_widgets(self):
        self.create_radio_buttons()
        self.create_buttons()
        self.create_fields()
        self.load_collections()
        self.toggle_radio()
        self.create_layout()
        self.create_drag_drop_text_edits()
        self.set_button_cursors()

    def create_radio_buttons(self):
        self.rabbitmq_radio = self.create_radio_button("RabbitMQ",self.rabbitmq_icon)
        self.awss3_radio = self.create_radio_button("AWS S3",self.awss3_icon)

    def create_radio_button(self, text,icon):
        radio_button = QRadioButton(text)
        radio_button.setIcon(QIcon(icon))
        radio_button.setStyleSheet("font-size: 14px; padding: 10px; background-color: lightgray;")
        return radio_button
    
    def create_buttons(self):
        self.submit_button = QPushButton("Submit")
        self.clear_button = QPushButton("Clear")
        self.save_and_upload = QPushButton("Save And Upload")

        self.submit_button.setIcon(QIcon(self.submit))
        self.clear_button.setIcon(QIcon(self.clear))
        self.save_and_upload.setIcon(QIcon(self.submit))

        self.submit_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.save_and_upload.setEnabled(True)

        #  submit and clear button working
        self.submit_button.clicked.connect(lambda: self.on_submit_clicked(False))
        self.clear_button.clicked.connect(self.on_clear_clicked)
        self.save_and_upload.clicked.connect(lambda: self.on_submit_clicked(True))

    def set_button_cursors(self):
        # Set cursor to hand when hovering over buttons
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.rabbitmq_file_select_button.setCursor(Qt.PointingHandCursor)
        self.awss3_file_select_button.setCursor(Qt.PointingHandCursor)
        self.awss3_radio.setCursor(Qt.PointingHandCursor)
        self.rabbitmq_radio.setCursor(Qt.PointingHandCursor)
        self.rabbitmq_radio.setCursor(Qt.PointingHandCursor)

    def create_fields(self):
        self.rabbitmq_fileds()
        self.awss3_fileds()
        self.widget_style()

    def create_layout(self):        

        radio_layout = self.create_radio_layout()
        input_layout = self.create_input_layout()
        button_layout = self.create_button_layout()
        self.create_main_layout(radio_layout,input_layout,button_layout)
    
    def create_radio_layout(self):

        # rabbitmq and aws radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.rabbitmq_radio)
        radio_layout.addWidget(self.awss3_radio)
        radio_layout.addWidget(self.aws_s3_collection_names)
        radio_layout.addWidget(self.rabbitmq_collection_names)

        radio_layout.setAlignment(self.rabbitmq_radio,Qt.AlignCenter)
        radio_layout.setAlignment(self.awss3_radio,Qt.AlignCenter)
        return radio_layout

    def fields_layout(self,label_field,input_field):
        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(label_field)
        label_input_layout.addWidget(input_field)

        return label_input_layout
    
    def create_input_layout(self):
        self.input_layout = QVBoxLayout()
        self.file_layout = QHBoxLayout()

        # AWS S3 fileds
        self.fileds_box_layout()
        # Add the file layout to the main layout
        self.input_layout.addLayout(self.file_layout)

        # Connect signals
        self.rabbitmq_file_select_button.clicked.connect(self.rabbitmq_file_select_clicked)
        self.awss3_file_select_button.clicked.connect(self.aws_file_select_clicked)
        return self.input_layout
    
    def create_button_layout(self):
        # Submit and Clear button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.save_and_upload)
        button_layout.setAlignment(Qt.AlignLeft)
        return button_layout
    
    def create_main_layout(self,radio_layout,input_layout,button_layout):
        #  all main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(radio_layout)
        self.main_layout.setAlignment(radio_layout,Qt.AlignLeft)

        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(input_layout)

        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(button_layout)

    def create_drag_drop_text_edits(self):
        # Connect drag and drop events
        self.rabbitmq_drag_drop_text_edit.dragEnterEvent = self.drag_enter_event
        self.rabbitmq_drag_drop_text_edit.dropEvent = self.drop_event

        self.aws_drag_drop_text_edit.dragEnterEvent = self.drag_enter_event
        self.aws_drag_drop_text_edit.dropEvent = self.drop_event

    def toggle_radio(self):
        self.rabbitmq_radio.toggled.connect(self.on_radio_toggled)
        self.awss3_radio.toggled.connect(self.on_radio_toggled)
        self.awss3_radio.setChecked(True)
        self.awss3_show_fileds()

    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_names = [url.toLocalFile() for url in event.mimeData().urls()]
            for file_name in file_names:
                if self.rabbitmq_radio.isChecked():
                    self.rabbitmq_drag_drop_text_edit.append(file_name)
                else:
                    self.aws_drag_drop_text_edit.append(file_name)

            event.acceptProposedAction()

    def show_error(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.addButton(QMessageBox.Ok)
        error_dialog.setDefaultButton(QMessageBox.Ok)
        for button in error_dialog.buttons():
            button.setCursor(Qt.PointingHandCursor)
        error_dialog.exec_()

    def show_success(self):
        success_popup = QMessageBox(self)
        success_popup.setIcon(QMessageBox.Information)
        success_popup.setWindowTitle("Success")
        success_popup.setText("File upload successful!")
        success_popup.addButton(QMessageBox.Ok)
        success_popup.setDefaultButton(QMessageBox.Ok)
        success_popup.setModal(True)   

        # Set cursor to hand when hovering over QMessageBox buttons
        for button in success_popup.buttons():
            button.setCursor(Qt.PointingHandCursor)

        success_popup.exec_()
        self.awss3_progress_bar.setValue(0)
        self.rabbitmq_progress_bar.setValue(0)

    def load_collections(self):
        # Retrieve data from the SQLite database and populate the combobox
        connection = sqlite3.connect('.cloud_uploader.db')  # Replace with your actual database file
        cursor = connection.cursor()

        cursor.execute("SELECT collection_name FROM rabbitmq_config ORDER BY created_at DESC")
        rabbitmq_collection_names = cursor.fetchall()
        
        cursor.execute("SELECT collection_name FROM aws_s3_config ORDER BY created_at DESC")
        awss3_collection_names = cursor.fetchall()
        
        if awss3_collection_names:
            self.aws_s3_collection_names.clear()
            for collection in awss3_collection_names:
                self.aws_s3_collection_names.addItem(f"{collection[0]}")
                                
        if rabbitmq_collection_names:
            self.rabbitmq_collection_names.clear()                
            for collection in rabbitmq_collection_names:
                self.rabbitmq_collection_names.addItem(f"{collection[0]}")            
        
        connection.close()


    def on_previous_config_selected(self):
        # Get the selected configuration from the combobox
        if self.rabbitmq_radio.isChecked():
            service_name = "rabbitmq_config"
            selected_text = self.rabbitmq_collection_names.currentText()
        if self.awss3_radio.isChecked():
            service_name = "aws_s3_config"
            selected_text = self.aws_s3_collection_names.currentText()

        # Retrieve the full configuration data from the database based on the ID
        connection = sqlite3.connect('.cloud_uploader.db')  # Replace with your actual database file
        cursor = connection.cursor()

        # Assuming your table is named 'rabbitmq_config'
        cursor.execute(f"SELECT * FROM {service_name} WHERE collection_name='{selected_text}'")
        config_data = cursor.fetchone()

        if not config_data:
            return False

        connection.close()

        # # Populate your input fields with the retrieved data
        if self.rabbitmq_radio.isChecked():
            self.rabbitmq_host_input.setText(config_data[2])
            self.rabbitmq_username_input.setText(config_data[3])
            self.rabbitmq_password_input.setText(config_data[4])
            self.rabbitmq_virtualhost_input.setText(config_data[5])
            self.rabbitmq_port_input.setText(config_data[6])
            self.rabbitmq_queue_input.setText(config_data[7])

        if self.awss3_radio.isChecked():
            self.awss3_access_key_input.setText(config_data[2])
            self.awss3_secret_key_input.setText(config_data[3])
            self.awss3_region_input.setText(config_data[4])
            self.awss3_bucket_name_input.setText(config_data[5])
            self.awss3_folder_input.setText(config_data[6])
                
    def on_radio_toggled(self):
        if self.rabbitmq_radio.isChecked():
            self.setFixedSize(600, 650)
            self.rabbitmq_show_fields()
            self.awss3_hide_fileds()

        elif self.awss3_radio.isChecked():
            self.setFixedSize(600, 600)
            self.awss3_show_fileds()
            self.rabbitmq_hide_fields()
                    
        self.rabbitmq_collection_names.currentIndexChanged.connect(lambda: self.on_previous_config_selected())
        self.aws_s3_collection_names.currentIndexChanged.connect(lambda: self.on_previous_config_selected())

        self.submit_button.setEnabled(True)
        self.on_previous_config_selected()

    def on_submit_clicked(self, save=None):
        try:
            if self.rabbitmq_radio.isChecked():
                self.handle_rabbitmq_submit(save)
            elif self.awss3_radio.isChecked():
                self.handle_awss3_submit(save)
            else:
                raise ValueError("Invalid radio button selection")

        except Exception:
            error_message = "Failed to connect to the server."
            self.show_error(error_message)
            self.refresh_ui()

    def handle_rabbitmq_submit(self, save):
        if not self.rabbitmq_validate():
            return

        collection_name = self.check_collections() if save else None
        if collection_name is None and save:
            return

        self.publish_files_to_rabbitmq_queue(save, collection_name)
        if save:
            self.refresh_ui()

        self.show_success()

    def handle_awss3_submit(self, save):
        if not self.aws_validate():
            return

        collection_name = self.check_collections() if save else None
        if collection_name is None and save:
            return

        self.upload_files_to_aws_s3_bucket(save, collection_name)
        if save:
            self.refresh_ui()

        self.show_success()

    # def on_submit_clicked(self,save=None):
    #     collection_name = None
    #     if self.rabbitmq_radio.isChecked():
    #         try:
    #             if not self.rabbitmq_validate():
    #                 return

    #             if save:
    #                 collection_name = self.check_collections()
    #                 if collection_name == None:
    #                     return

    #             self.publish_files_to_rabbitmq_queue(save,collection_name)
    #             if save:
    #                 self.refresh_ui()

    #         except Exception as e:
    #             error_message = "Failed to connect to server."
    #             self.show_error(error_message)
    #             self.refresh_ui()

    #     elif self.awss3_radio.isChecked():
    #         try:
    #             if not self.aws_validate():
    #                 return
                
    #             if save:
    #                 collection_name = self.check_collections()
    #                 if collection_name == None:
    #                     return

    #             self.upload_files_to_aws_s3_bucket(save,collection_name)
    #             if save:
    #                 self.refresh_ui()
            
    #         except Exception as e:
    #             error_message = "Failed to connect to server."
    #             self.show_error(error_message)
    #             self.refresh_ui()
        
    #     self.show_success()

    def refresh_ui(self):
        self.load_collections()
        if self.rabbitmq_radio.isChecked():

            if self.rabbitmq_collection_names.count() > 0:
                self.rabbitmq_collection_names.show()
            else:
                self.rabbitmq_collection_names.hide()

        elif self.awss3_radio.isChecked():

            if self.aws_s3_collection_names.count() > 0:
                self.aws_s3_collection_names.show()
            else:
                self.aws_s3_collection_names.hide()
        
    def save_data_to_database(self, table_name, data):
        columns = ", ".join(data.keys())
        placeholders = ":" + ", :".join(data.keys())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, data)
        self.connection.commit()

    def check_collections(self):
        while True:
            collection_name, ok_pressed = QInputDialog.getText(self, 'Collection Name', 'Enter Collection Name:')

            if not collection_name and not ok_pressed:
                return

            if self.validate_collection_name(collection_name, ok_pressed):
                return collection_name

    def validate_collection_name(self, collection_name, ok_pressed):
        if ok_pressed and not collection_name:
            self.show_error("Please Fill Collection Name.")
            return False

        radio = self.awss3_radio if self.awss3_radio.isChecked() else self.rabbitmq_radio
        collection_names = self.get_collection_names(radio)

        if collection_name in collection_names:
            QMessageBox.warning(self, 'Duplicate Collection Name', 'Collection Name already exists!')
            return False

        return True

    def get_collection_names(self, radio):
        if radio == self.awss3_radio:
            return [self.aws_s3_collection_names.itemText(i) for i in range(self.aws_s3_collection_names.count())]
        elif radio == self.rabbitmq_radio:
            return [self.rabbitmq_collection_names.itemText(i) for i in range(self.rabbitmq_collection_names.count())]
        else:
            return []

    # def check_collections(self):

    #     while True:
    #         collection_name, ok_pressed = QInputDialog.getText(self, 'Collection Name', 'Enter Collectin Name:')

    #         if (len(collection_name) == 0) and (not ok_pressed):
    #             return
            

    #         elif collection_name and ok_pressed:
    #             if ok_pressed:
    #                 if not collection_name:
    #                     self.show_error("Please Fill Collection Name.")
    #                     continue

    #             if self.awss3_radio.isChecked():
    #                 if collection_name in [self.aws_s3_collection_names.itemText(i) for i in range(self.aws_s3_collection_names.count())]:
    #                     QMessageBox.warning(self, 'Duplicate Collection Name', 'Collection Name already exists!')
    #                     continue
    #                 else:
    #                     return collection_name

    #             if self.rabbitmq_radio.isChecked():
    #                 if collection_name in [self.rabbitmq_collection_names.itemText(i) for i in range(self.rabbitmq_collection_names.count())]:
    #                     QMessageBox.warning(self, 'Duplicate Collection Name', 'Collection Name already exists!')
    #                     continue
    #                 else:
    #                     return collection_name

    def aws_file_select_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("All Files (*);;Python Files (*.py)")
        file_dialog.setWindowTitle(self.select_file)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_() == QFileDialog.Accepted:
            file_names = file_dialog.selectedFiles()
            for file_name in file_names:
                self.aws_drag_drop_text_edit.append(file_name)

            file_dialog.done(QFileDialog.Accepted)

    def rabbitmq_file_select_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("All Files (*);;Python Files (*.py)")
        file_dialog.setWindowTitle(self.select_file)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_() == QFileDialog.Accepted:
            file_names = file_dialog.selectedFiles()
            for file_name in file_names:
                self.rabbitmq_drag_drop_text_edit.append(file_name)

            file_dialog.done(QFileDialog.Accepted)

    def on_clear_clicked(self):
        self.clear_input_fields()
        self.awss3_progress_bar.setValue(0)
        self.rabbitmq_progress_bar.setValue(0)

    def clear_input_fields(self):
        self.rabbitmq_host_input.clear()
        self.rabbitmq_username_input.clear()
        self.rabbitmq_password_input.clear()
        self.rabbitmq_virtualhost_input.clear()
        self.rabbitmq_port_input.clear()
        self.rabbitmq_queue_input.clear()
        self.rabbitmq_drag_drop_text_edit.clear()

        self.awss3_access_key_input.clear()
        self.awss3_secret_key_input.clear()
        self.awss3_region_input.clear()
        self.awss3_bucket_name_input.clear()
        self.awss3_folder_input.clear()
        self.aws_drag_drop_text_edit.clear()

    def create_label_fileds(self,text):
        rabbitmq_labels = QLabel(text, self)
        return rabbitmq_labels

    def create_input_fileds(self):
        rabbitmq_input = QLineEdit(self)
        return rabbitmq_input 

    def rabbitmq_fileds(self):
        self.rabbitmq_host_label = self.create_label_fileds('Host:')
        self.rabbitmq_host_label.hide()

        self.rabbitmq_username_label = self.create_label_fileds('Username:')
        self.rabbitmq_username_label.hide()                      
        self.rabbitmq_password_label = self.create_label_fileds('Password:')
        self.rabbitmq_password_label.hide()                      
        self.rabbitmq_virtualhost_label = self.create_label_fileds('Virtual Host:')
        self.rabbitmq_virtualhost_label.hide()                      
        self.rabbitmq_port_label = self.create_label_fileds('Port Number:')
        self.rabbitmq_port_label.hide()
        self.rabbitmq_queue_label = self.create_label_fileds('Queue Name:')
        self.rabbitmq_queue_label.hide()

        self.rabbitmq_host_input = self.create_input_fileds()
        self.rabbitmq_host_input.hide()
        self.rabbitmq_username_input = self.create_input_fileds()
        self.rabbitmq_username_input.hide()
        self.rabbitmq_password_input = self.create_input_fileds()
        self.rabbitmq_password_input.hide()
        self.rabbitmq_virtualhost_input = self.create_input_fileds()
        self.rabbitmq_virtualhost_input.hide()
        self.rabbitmq_port_input = self.create_input_fileds()
        self.rabbitmq_port_input.hide()
        self.rabbitmq_queue_input = self.create_input_fileds()
        self.rabbitmq_queue_input.hide()

        self.rabbitmq_file = self.create_label_fileds(self.select_file)
        self.rabbitmq_file.hide()

        self.rabbitmq_file_select_button = QPushButton('Choose File', self)
        self.rabbitmq_file_select_button.setIcon(QIcon(self.choose_file))
        self.rabbitmq_file_select_button.setToolTip(self.select_file) 
        self.rabbitmq_file_select_button.hide()

        self.rabbitmq_drag_drop_text_edit = QTextEdit(self)
        self.rabbitmq_drag_drop_text_edit.setAcceptDrops(True)
        self.rabbitmq_drag_drop_text_edit.setPlaceholderText("Drag and drop files here")
        self.rabbitmq_drag_drop_text_edit.hide()

        self.rabbitmq_progress_bar = QProgressBar(self)
        self.rabbitmq_progress_bar.setFixedHeight(30)
        self.rabbitmq_progress_bar.setValue(0)
        self.rabbitmq_progress_bar.hide()

        self.rabbitmq_collection_names = QComboBox(self)
        self.rabbitmq_collection_names.hide()

        self.is_aws_checkbox = QCheckBox("Is AWS")
        self.is_aws_checkbox.hide()

    def awss3_fileds(self):
        self.awss3_access_key_lable = self.create_label_fileds('Access_key:')
        self.awss3_access_key_lable.hide()
        self.awss3_access_key_input = self.create_input_fileds()
        self.awss3_access_key_input.hide()

        self.awss3_secret_key_lable = self.create_label_fileds('Secret Key:')
        self.awss3_secret_key_lable.hide()
        self.awss3_secret_key_input = self.create_input_fileds()
        self.awss3_secret_key_input.hide()

        self.awss3_region_lable = self.create_label_fileds('Region:')
        self.awss3_region_lable.hide()
        self.awss3_region_input = self.create_input_fileds()
        self.awss3_region_input.hide()

        self.awss3_bucket_name_lable = self.create_label_fileds('Bucket Name:')
        self.awss3_bucket_name_lable.hide()
        self.awss3_bucket_name_input = self.create_input_fileds()
        self.awss3_bucket_name_input.hide()

        self.awss3_folder_lable = self.create_label_fileds('Folder:')
        self.awss3_folder_lable.hide()
        self.awss3_folder_input = self.create_input_fileds()
        self.awss3_folder_input.hide()

        self.awss3_select_files = self.create_label_fileds(self.select_file)
        self.awss3_select_files.hide()

        self.awss3_file_select_button = QPushButton('Choose File', self)
        self.awss3_file_select_button.setIcon(QIcon(self.choose_file))
        self.awss3_file_select_button.setToolTip(self.select_file) 
        self.awss3_file_select_button.hide()

        self.aws_drag_drop_text_edit = QTextEdit(self)
        self.aws_drag_drop_text_edit.setAcceptDrops(True)
        self.aws_drag_drop_text_edit.setPlaceholderText("Drag and drop files here")
        self.aws_drag_drop_text_edit.hide()

        self.awss3_progress_bar = QProgressBar(self)
        self.awss3_progress_bar.setFixedHeight(30)
        self.awss3_progress_bar.setValue(0)
        self.awss3_progress_bar.hide()

        self.aws_s3_collection_names = QComboBox(self)
        self.aws_s3_collection_names.hide()
        
    def fileds_box_layout(self):
 
        self.input_layout.addWidget(self.is_aws_checkbox)

        self.host_layout = QHBoxLayout()
        self.host_layout.addWidget(self.rabbitmq_host_label)
        self.host_layout.addWidget(self.rabbitmq_host_input)

        self.input_layout.addLayout(self.host_layout)

        self.username_layout = QHBoxLayout()
        self.username_layout.addWidget(self.rabbitmq_username_label)
        self.username_layout.addWidget(self.rabbitmq_username_input)

        self.input_layout.addLayout(self.username_layout)

        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(self.rabbitmq_password_label)
        self.password_layout.addWidget(self.rabbitmq_password_input)

        self.input_layout.addLayout(self.password_layout)

        self.virtualhost_layout = QHBoxLayout()
        self.virtualhost_layout.addWidget(self.rabbitmq_virtualhost_label)
        self.virtualhost_layout.addWidget(self.rabbitmq_virtualhost_input)

        self.input_layout.addLayout(self.virtualhost_layout)

        self.port_layout = QHBoxLayout()
        self.port_layout.addWidget(self.rabbitmq_port_label)
        self.port_layout.addWidget(self.rabbitmq_port_input)

        self.input_layout.addLayout(self.port_layout)

        self.queue_layout = QHBoxLayout()
        self.queue_layout.addWidget(self.rabbitmq_queue_label)
        self.queue_layout.addWidget(self.rabbitmq_queue_input)

        self.input_layout.addLayout(self.queue_layout)

        self.input_layout.addWidget(self.rabbitmq_progress_bar)
        self.input_layout.addWidget(self.rabbitmq_file)
        
        self.file_layout.addWidget(self.rabbitmq_file_select_button)
        self.file_layout.addWidget(self.rabbitmq_drag_drop_text_edit)

        self.access_key_layout = QHBoxLayout()
        self.access_key_layout.addWidget(self.awss3_access_key_lable)
        self.access_key_layout.addWidget(self.awss3_access_key_input)

        self.input_layout.addLayout(self.access_key_layout)

        self.secret_key_layout = QHBoxLayout()
        self.secret_key_layout.addWidget(self.awss3_secret_key_lable)
        self.secret_key_layout.addWidget(self.awss3_secret_key_input)

        self.input_layout.addLayout(self.secret_key_layout)

        self.region_layout = QHBoxLayout()
        self.region_layout.addWidget(self.awss3_region_lable)
        self.region_layout.addWidget(self.awss3_region_input)

        self.input_layout.addLayout(self.region_layout)

        self.bucket_layout = QHBoxLayout()
        self.bucket_layout.addWidget(self.awss3_bucket_name_lable)
        self.bucket_layout.addWidget(self.awss3_bucket_name_input)

        self.input_layout.addLayout(self.bucket_layout)

        self.folder_layout = QHBoxLayout()
        self.folder_layout.addWidget(self.awss3_folder_lable)
        self.folder_layout.addWidget(self.awss3_folder_input)

        self.input_layout.addLayout(self.folder_layout)

        self.input_layout.addWidget(self.awss3_progress_bar)
        self.input_layout.addWidget(self.awss3_select_files)
        self.file_layout.addWidget(self.awss3_file_select_button)
        self.file_layout.addWidget(self.aws_drag_drop_text_edit)
    

    def rabbitmq_show_fields(self):
        self.rabbitmq_host_label.show()
        self.rabbitmq_host_input.show()

        self.rabbitmq_username_label.show()
        self.rabbitmq_username_input.show()

        self.rabbitmq_password_label.show()
        self.rabbitmq_password_input.show()

        self.rabbitmq_virtualhost_label.show()
        self.rabbitmq_virtualhost_input.show()

        self.rabbitmq_port_label.show()
        self.rabbitmq_port_input.show()
        self.rabbitmq_queue_label.show()
        self.rabbitmq_queue_input.show()
        self.rabbitmq_file.show()
        self.rabbitmq_file_select_button.show()
        self.rabbitmq_drag_drop_text_edit.show()
        self.rabbitmq_progress_bar.show()
        if self.rabbitmq_collection_names.count() > 0:
            self.rabbitmq_collection_names.show()
        else:
            self.rabbitmq_collection_names.hide()

        self.is_aws_checkbox.show()
    
    def awss3_show_fileds(self):
        self.awss3_access_key_lable.show()
        self.awss3_access_key_input.show()
        self.awss3_secret_key_lable.show()
        self.awss3_secret_key_input.show()
        self.awss3_region_lable.show()
        self.awss3_region_input.show()
        self.awss3_bucket_name_lable.show()
        self.awss3_bucket_name_input.show()
        self.awss3_folder_lable.show()
        self.awss3_folder_input.show()

        self.awss3_select_files.show()
        self.awss3_file_select_button.show()
        self.aws_drag_drop_text_edit.show()
        self.awss3_progress_bar.show()
        if self.aws_s3_collection_names.count() > 0:
            self.aws_s3_collection_names.show()
        else:
            self.aws_s3_collection_names.hide()

    def rabbitmq_hide_fields(self):
        self.rabbitmq_host_label.hide()
        self.rabbitmq_host_input.hide()

        self.rabbitmq_username_label.hide()
        self.rabbitmq_username_input.hide()

        self.rabbitmq_password_label.hide()
        self.rabbitmq_password_input.hide()

        self.rabbitmq_virtualhost_label.hide()
        self.rabbitmq_virtualhost_input.hide()

        self.rabbitmq_port_label.hide()
        self.rabbitmq_port_input.hide()

        self.rabbitmq_queue_label.hide()
        self.rabbitmq_queue_input.hide()

        self.rabbitmq_file.hide()
        self.rabbitmq_file_select_button.hide()
        self.rabbitmq_drag_drop_text_edit.hide()
        self.rabbitmq_progress_bar.hide()
        self.rabbitmq_collection_names.hide()
        self.is_aws_checkbox.hide()
    
    def awss3_hide_fileds(self):
        self.awss3_access_key_lable.hide()
        self.awss3_access_key_input.hide()
        self.awss3_secret_key_lable.hide()
        self.awss3_secret_key_input.hide()
        self.awss3_region_lable.hide()
        self.awss3_region_input.hide()
        self.awss3_bucket_name_lable.hide()
        self.awss3_bucket_name_input.hide()
        self.awss3_folder_lable.hide()
        self.awss3_folder_input.hide()

        self.awss3_select_files.hide()
        self.awss3_file_select_button.hide()
        self.aws_drag_drop_text_edit.hide()
        self.awss3_progress_bar.hide()
        self.aws_s3_collection_names.hide()

    def rabbitmq_validate(self):
        if not self.rabbitmq_host_input.text():
            self.show_error("Please Fill Host Name.")
            return False

        elif not self.rabbitmq_username_input.text():
            self.show_error("Please Fill userName.")
            return False 

        elif not self.rabbitmq_password_input.text():
            self.show_error("Please Fill Password Name.")
            return False 

        elif not self.rabbitmq_virtualhost_input.text():
            self.show_error("Please Fill Virtual Host Name.")
            return False

        elif not self.rabbitmq_port_input.text():
            self.show_error("Please Fill Port Number.")
            return False

        elif not self.rabbitmq_queue_input.text():
            self.show_error("Please Fill Queue Name.")
            return False

        elif not bool(self.rabbitmq_drag_drop_text_edit.toPlainText().strip()):
            self.show_error("Please Add Files.")
            return False
        else:
            return True

    def aws_validate(self):
        if not self.awss3_access_key_input.text():
            self.show_error("Please Fill Access Key.")
            return False
        elif not self.awss3_secret_key_input.text():
            self.show_error("Please Fill secret Key.")
            return False
        elif not self.awss3_region_input.text():
            self.show_error("Please Fill Region.")
            return False
        elif not self.awss3_bucket_name_input.text():
            self.show_error("Please Fill Bucket Name.")
            return False
        elif not bool(self.aws_drag_drop_text_edit.toPlainText().strip()):
            self.show_error("Please Add Files.")
            return False
        else: 
            return True

    def widget_style(self):
        self.setWindowTitle("Cloud Uploader")
        self.setWindowIcon(QIcon(os.path.join(self.bundle_dir, 'icons' ,'cloud-uploder.png')))
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        font_size = 10

        labels = [
            self.rabbitmq_host_label, self.rabbitmq_username_label,
            self.rabbitmq_password_label, self.rabbitmq_virtualhost_label,
            self.rabbitmq_port_label, self.rabbitmq_queue_label,self.awss3_access_key_lable,self.awss3_secret_key_lable,
            self.awss3_region_lable,self.awss3_bucket_name_lable,self.awss3_folder_lable,
            self.awss3_select_files,self.rabbitmq_file,self.awss3_file_select_button,self.rabbitmq_file_select_button,
            self.rabbitmq_host_input, self.rabbitmq_username_input,
            self.rabbitmq_password_input, self.rabbitmq_virtualhost_input,
            self.rabbitmq_port_input, self.rabbitmq_queue_input,
            self.awss3_access_key_input,self.awss3_secret_key_input,self.awss3_region_input,
            self.awss3_bucket_name_input,self.awss3_folder_input,self.submit_button,self.clear_button,self.save_and_upload
        ]

        for label in labels:
            label.setFont(QFont('Segoe UI', font_size))
        
        max_label_width_for_rabbitmq = max(
            self.rabbitmq_host_label.sizeHint().width(),
            self.rabbitmq_username_label.sizeHint().width(),
            self.rabbitmq_queue_label.sizeHint().width(),
        )
        self.rabbitmq_host_label.setFixedWidth(max_label_width_for_rabbitmq)
        self.rabbitmq_username_label.setFixedWidth(max_label_width_for_rabbitmq)
        self.rabbitmq_password_label.setFixedWidth(max_label_width_for_rabbitmq)
        self.rabbitmq_virtualhost_label.setFixedWidth(max_label_width_for_rabbitmq)
        self.rabbitmq_port_label.setFixedWidth(max_label_width_for_rabbitmq)
        self.rabbitmq_queue_label.setFixedWidth(max_label_width_for_rabbitmq)

        max_label_width_for_aws = max(
            self.awss3_access_key_lable.sizeHint().width(),
            self.awss3_secret_key_lable.sizeHint().width(),
            self.awss3_bucket_name_lable.sizeHint().width(),
        )
        self.awss3_access_key_lable.setFixedWidth(max_label_width_for_aws)
        self.awss3_secret_key_lable.setFixedWidth(max_label_width_for_aws)
        self.awss3_region_lable.setFixedWidth(max_label_width_for_aws)
        self.awss3_bucket_name_lable.setFixedWidth(max_label_width_for_aws)
        self.awss3_folder_lable.setFixedWidth(max_label_width_for_aws)

        inputs = [
            self.rabbitmq_host_input, self.rabbitmq_username_input,
            self.rabbitmq_password_input, self.rabbitmq_virtualhost_input,
            self.rabbitmq_port_input, self.rabbitmq_queue_input,
            self.awss3_access_key_input,self.awss3_secret_key_input,self.awss3_region_input,
            self.awss3_bucket_name_input,self.awss3_folder_input
        ]
        for input_field in inputs:
            input_field.setFixedHeight(35) 

        self.rabbitmq_host_input.setPlaceholderText("Enter RabbitMQ Host")
        self.rabbitmq_username_input.setPlaceholderText("Enter RabbitMQ Username")
        self.rabbitmq_password_input.setPlaceholderText("Enter RabbitMQ Password")
        self.rabbitmq_virtualhost_input.setPlaceholderText("Enter RabbitMQ Virtual Host")
        self.rabbitmq_port_input.setPlaceholderText("Enter RabbitMQ Port Number")
        self.rabbitmq_queue_input.setPlaceholderText("Enter RabbitMQ Queue Name")

        self.awss3_access_key_input.setPlaceholderText("Enter AWS S3 Access Key")
        self.awss3_secret_key_input.setPlaceholderText("Enter AWS S3 Secret Key")
        self.awss3_region_input.setPlaceholderText("Enter AWS S3 Region")
        self.awss3_bucket_name_input.setPlaceholderText("Enter AWS S3 Bucket Name")
        self.awss3_folder_input.setPlaceholderText("Enter AWS S3 Folder Path")

        self.awss3_file_select_button.setFixedWidth(150)
        self.awss3_file_select_button.setFixedHeight(150)
        self.rabbitmq_file_select_button.setFixedWidth(150)
        self.rabbitmq_file_select_button.setFixedHeight(150)

        self.rabbitmq_drag_drop_text_edit.setFixedHeight(150)
        self.rabbitmq_drag_drop_text_edit.setFixedWidth(380)
        self.aws_drag_drop_text_edit.setFixedHeight(150)
        self.aws_drag_drop_text_edit.setFixedWidth(380)
        drag_drop_styles = """
            QTextEdit {
                background-color: lightgray;
                border: 1px solid darkgray;
                padding: 10px;
                font-size: 16px; /* Adjust the font size as needed */
            }
        """
        self.rabbitmq_drag_drop_text_edit.setStyleSheet(drag_drop_styles)
        self.aws_drag_drop_text_edit.setStyleSheet(drag_drop_styles)

        self.submit_button.setFixedHeight(40)
        self.submit_button.setFixedWidth(150)

        self.clear_button.setFixedHeight(40)
        self.clear_button.setFixedWidth(150)

        self.save_and_upload.setFixedHeight(40)
        self.save_and_upload.setFixedWidth(200)

        progress_bar_style = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #00FF00;  /* Set the progress bar color to green */
                width: 10px;  /* Set the width of the progress indicator */
            }
        """
        self.rabbitmq_progress_bar.setStyleSheet(progress_bar_style)
        self.awss3_progress_bar.setStyleSheet(progress_bar_style)
    
        radio_buttons = [self.rabbitmq_radio,self.awss3_radio]
        for radio in radio_buttons:
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 14px;
                    padding: 10px;
                    background-color: lightgray;
                    color: black; /* Text color */
                    border-radius: 5px; /* Border radius */
                }

                QRadioButton::indicator {
                    width: 20px; /* Width of the indicator */
                    height: 20px; /* Height of the indicator */
                }

                QRadioButton::indicator:checked {
                    background-color: black; /* Background color when checked */
                    border-radius: 10px; /* Border radius */
                }
            """)
        
        self.aws_s3_collection_names.setFixedHeight(40)
        self.rabbitmq_collection_names.setFixedHeight(40)
        
        self.aws_s3_collection_names.setFixedWidth(200)
        self.rabbitmq_collection_names.setFixedWidth(200)
        
    def publish_files_to_rabbitmq_queue(self,save=None,collection_name=None):
        host_name =  self.rabbitmq_host_input.text()
        username = self.rabbitmq_username_input.text()
        password = self.rabbitmq_password_input.text()
        virtual_host = self.rabbitmq_virtualhost_input.text()
        queue_name = self.rabbitmq_queue_input.text()
        port = self.rabbitmq_port_input.text()
        file_paths = self.rabbitmq_drag_drop_text_edit.toPlainText().split('\n')

        # print(host_name,username,password,virtual_host,queue_name,port,file_paths)

        files = self.rabbitmq_drag_drop_text_edit.toPlainText().split('\n')
        
        # data store in database
        if save:
            self.save_data_to_database("rabbitmq_config", {
                "collection_name": collection_name,
                "host": host_name,
                "username": username,
                "password": password,
                "virtualhost": virtual_host,
                "port": port,
                "queue": queue_name,
                "files": str(file_paths)
            })

        total_files = len(files)

        self.rabbitmq_progress_bar.setMaximum(total_files)
        self.rabbitmq_progress_bar.show()
        self.rabbitmq_progress_bar.setValue(0)

        if self.is_aws_checkbox.isChecked():
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.set_ciphers('ECDHE+AESGCM:!ECDSA')

            url = f"amqps://{username}:{password}@{host_name}:{port}"

            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=context)
            connection = pika.BlockingConnection(parameters)

            channel = connection.channel()
            # channel.queue_declare(queue=queue_name)

        else:
            credentials = pika.PlainCredentials(username, password)
            parameters = pika.ConnectionParameters(host=host_name,
                                            virtual_host=virtual_host,
                                            port=port,
                                            credentials=credentials)
            
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()


        try:
            for file_index, file in enumerate(file_paths, start=1):
                with open(file, 'rb') as file:
                    content = file.read()

                channel.basic_publish(exchange='', routing_key=queue_name, body=content)

                self.rabbitmq_progress_bar.setValue(file_index)
                QApplication.processEvents()

        finally:
            connection.close()

    def upload_files_to_aws_s3_bucket(self, save=None, collection_name=None):
        try:
            access_key, secret_access_key, region, bucket_name, folder_name, file_paths = self.get_aws_s3_parameters()

            # Validate parameters
            self.validate_aws_s3_parameters(access_key, secret_access_key, region, bucket_name, file_paths)

            if save:
                self.save_data_to_database("aws_s3_config", {
                    "collection_name": collection_name,
                    "access_key": access_key,
                    "secret_key": secret_access_key,
                    "region": region,
                    "bucket_name": bucket_name,
                    "folder": folder_name,
                    "files": str(file_paths)
                })

            total_files = len(file_paths)
            self.initialize_aws_s3_progress_bar(total_files)

            s3 = self.create_aws_s3_client(access_key, secret_access_key, region)

            # Ensure folder exists or create it
            self.ensure_s3_folder_exists(s3, bucket_name, folder_name)

            self.upload_files_to_s3(s3, bucket_name, folder_name, file_paths, total_files)

        except Exception as e:
            raise e

    def get_aws_s3_parameters(self):
        access_key = self.awss3_access_key_input.text()
        secret_access_key = self.awss3_secret_key_input.text()
        region = self.awss3_region_input.text()
        bucket_name = self.awss3_bucket_name_input.text()
        folder_name = self.awss3_folder_input.text()
        file_paths = self.aws_drag_drop_text_edit.toPlainText().split("\n")

        return access_key, secret_access_key, region, bucket_name, folder_name, file_paths

    def validate_aws_s3_parameters(self, access_key, secret_access_key, region, bucket_name, file_paths):
        # Add validation logic as needed
        pass

    def initialize_aws_s3_progress_bar(self, total_files):
        self.awss3_progress_bar.setMaximum(total_files)
        self.awss3_progress_bar.setValue(0)
        self.awss3_progress_bar.show()

    def create_aws_s3_client(self, access_key, secret_access_key, region):
        return boto3.client('s3', aws_access_key_id=access_key,
                           aws_secret_access_key=secret_access_key,
                           region_name=region)

    def ensure_s3_folder_exists(self, s3, bucket_name, folder_name):
        if folder_name:
            try:
                s3.head_object(Bucket=bucket_name, Key=f'{folder_name}/')
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    s3.put_object(Bucket=bucket_name, Key=(folder_name if folder_name[-1] == '/' else folder_name+'/'))
                else:
                    raise e

    def upload_files_to_s3(self, s3, bucket_name, folder_name, file_paths, total_files):
        for file_index, file_path in enumerate(file_paths, start=1):
            file_name = os.path.basename(f"{folder_name}{file_path}") if folder_name else os.path.basename(file_path)

            # Upload file to S3
            s3.upload_file(file_path, bucket_name, file_name)

            self.awss3_progress_bar.setValue(file_index)
            QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    signup_login = SignupLogin()
    window = MyWindow()
    signup_login.show()
    sys.exit(app.exec_())