
import tkinter as tk
import subprocess
import sys
from pathlib import Path
from advanced_database_project.gui.base_page import BasePage
from tkinter import messagebox


class SettingsPage(BasePage):
    """
    GUI Settings Page - Allows for configuration of the database.
    """
    
    def __init__(self, pages, db, user):
        super().__init__(pages, db, user)
        self.configure(bg="#f7f7f7")
        
        self.import_path = tk.StringVar(value="./advanced_database_project/backend/backup/database_backup.xml")
        self.export_confirmation = None
        self.import_entry = None
        
        self.create_settings_page()
        
    def navigate_to(self, page):
        """
        Overide the default naviage_to function from BasePage - Reset the export confirmation message.
        """
        self.export_confirmation.configure(text="")
    
        self.pack_forget()
        page.show()

    def create_settings_page(self):
        """
        Create the widgets for the settings page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew") 
        
        settings_message = tk.Frame(header_frame, bg="#e6e6e6", pady=20)
        settings_message.pack(fill="x")
        settings_message_label = tk.Label(
            settings_message,
            text="Settings",
            font=("Arial", 24, "bold"),
            bg="#e6e6e6",
            fg="#333",
            width=50,
        )
        settings_message_label.pack(pady=10)
        
        settings_frame = tk.Frame(self, bg="#f7f7f7")
        settings_frame.grid(row=2, column=0, padx=(0, 20), pady=10)
        
        reload_label = tk.Label(settings_frame, font=("Arial", 15), bg="#f7f7f7", text="Reload Database: ")
        reload_label.grid(row=0, column=0, pady=(10, 0))
        
        reload_desc = tk.Label(settings_frame, font=("Arial", 12), bg="#f7f7f7", 
                               text="Reloading the database will reset the database back to the original, "
                                    "by using the .sql script to teardown and recreate the database.")
        reload_desc.grid(row=1, column=0, pady=(10, 0))
        
        reload_warn = tk.Label(settings_frame, font=("Arial", 12), bg="#f7f7f7", fg="#ff2e2e",
                               text="YOU WILL LOSE ANY CUSTOM DATA!")
        reload_warn.grid(row=2, column=0, pady=(10, 0))
        
        reload_button = tk.Button(settings_frame, font=("Arial", 12), width=8, text="Reload", command=self.reload_db)
        reload_button.grid(row=3, column=0, pady=(10, 0))

        
        export_label = tk.Label(settings_frame, font=("Arial", 15), bg="#f7f7f7", text="Export Database: ")
        export_label.grid(row=4, column=0, pady=(10, 0))
        
        export_desc = tk.Label(settings_frame, font=("Arial", 12), bg="#f7f7f7", 
                               text="Exporting the database will backup the current database configuration as XML to "
                                    "'./advanced_database_project/backend/backup/database_backup.xml'.")
        export_desc.grid(row=5, column=0, pady=(10, 0))
        
        export_frame = tk.Frame(settings_frame, bg="#f7f7f7") 
        export_frame.grid(row=6, column=0, padx=(490, 20), sticky="w")

        export_button = tk.Button(export_frame, font=("Arial", 12), width=8, text="Export", command=self.export_db)
        export_button.grid(row=0, column=0, pady=(10, 0), padx=(0, 10))

        self.export_confirmation = tk.Label(export_frame, font=("Arial", 12), bg="#f7f7f7", fg="#1aff00")
        self.export_confirmation.grid(row=0, column=1, pady=(10, 0))

    
        import_label = tk.Label(settings_frame, font=("Arial", 15), bg="#f7f7f7", text="Import Database: ")
        import_label.grid(row=7, column=0, pady=(10, 0))
        
        import_desc = tk.Label(settings_frame, font=("Arial", 12), bg="#f7f7f7", 
                               text="Importing the database will restore the database to the XML file defined at the location defined.")
        import_desc.grid(row=8, column=0, pady=(10, 0))
        
        import_warn = tk.Label(settings_frame, font=("Arial", 12), bg="#f7f7f7", fg="#ff2e2e",
                               text="YOU WILL LOSE ANY CUSTOM DATA!")
        import_warn.grid(row=9, column=0, pady=(10, 0))
        
        self.import_entry = tk.Entry(settings_frame, textvariable=self.import_path, width=54, font=("Arial", 12))
        self.import_entry.grid(row=10, column=0, padx=(10, 0), pady=5)
        
        import_button = tk.Button(settings_frame, font=("Arial", 12), width=8, text="Import", command=self.import_db)
        import_button.grid(row=11, column=0, pady=(10, 0))
        
        
        close_label = tk.Label(settings_frame, font=("Arial", 15), bg="#f7f7f7", text="Close Application: ")
        close_label.grid(row=12, column=0, pady=(10, 0))
        
        close_button = tk.Button(settings_frame, font=("Arial", 12), width=8, text="Close", bg="#ff2e2e", command=self.close_application)
        close_button.grid(row=13, column=0, pady=(10, 0))
        
    def close_application(self):
        quit()
        
    def export_db(self):
        self.db.backup_database_to_xml(Path("./advanced_database_project/backend/backup/database_backup.xml"))
        self.export_confirmation.configure(text="Successfully Exported Database!")
        
    def import_db(self):
        result = messagebox.askquestion("Confirmation", "Importing an XML file will restart the application and all unsave data will be lost.\n "
                                        "Are you sure you want to do this?")
        if result == "yes":
            import_path = Path(self.import_path.get())
            if import_path.is_file():
                self.db.restore_database_from_xml(import_path)
                self.restart_application()
            else:
                # self.error_label.configure(text="Username is already taken!")
                self.import_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
        
    def reload_db(self):
        result = messagebox.askquestion("Confirmation", "Reloading the database will restart the application and all unsave data will be lost.\n "
                                        "Are you sure you want to do this?")
        if result == "yes":
            self.db.run_sql_script(Path("create_database_script.sql"))
            for path in Path("./advanced_database_project/assets/").iterdir():
                self.db.insert_image(Path(path))
            
            self.restart_application()
        
    @staticmethod
    def restart_application():
        python = sys.executable
        args = sys.argv
        subprocess.Popen([python] + args)
        sys.exit() 