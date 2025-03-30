import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv
import sys
from pathlib import Path
import logging

# Add parent directory to path so we can import our own modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import database models (only when needed)
# from src.database import models, crud, db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("oz-stack.desktop")

# Load environment variables
load_dotenv()

# Get app settings from environment variables
APP_NAME = os.getenv("APP_NAME", "Oz Stack Desktop")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Set CustomTkinter appearance
ctk.set_appearance_mode(os.getenv("CTK_APPEARANCE", "System"))  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme(os.getenv("CTK_THEME", "blue"))    # Options: "blue", "green", "dark-blue"


class OzDesktopApp(ctk.CTk):
    """Main desktop application window using CustomTkinter"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Initialize UI
        self.create_menu()
        self.create_widgets()
        
        # Log application start
        logger.info(f"Desktop application started: {APP_NAME} v{APP_VERSION}")

    def create_menu(self):
        """Create the application menu"""
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Help menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        """Create the main application UI elements"""
        # Create a container frame with grid layout
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid layout (4x4)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=3)
        self.container.grid_rowconfigure(0, weight=1)
        
        # Create the sidebar frame
        self.sidebar = ctk.CTkFrame(self.container, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text=APP_NAME, font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.home_button = ctk.CTkButton(
            self.sidebar, text="Home", command=self.show_home_frame
        )
        self.home_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.data_button = ctk.CTkButton(
            self.sidebar, text="Data", command=self.show_data_frame
        )
        self.data_button.grid(row=2, column=0, padx=20, pady=10)
        
        # Appearance mode selector
        self.appearance_label = ctk.CTkLabel(self.sidebar, text="Appearance:")
        self.appearance_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_option = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode
        )
        self.appearance_option.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.appearance_option.set(ctk.get_appearance_mode())
        
        # Create the main content area
        self.content_frame = ctk.CTkFrame(self.container)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        
        # Initialize frames
        self.home_frame = None
        self.data_frame = None
        
        # Show default frame
        self.show_home_frame()

    def show_home_frame(self):
        """Show the home content frame"""
        # Hide other frames
        if self.data_frame:
            self.data_frame.grid_forget()
            
        # Create home frame if it doesn't exist
        if not self.home_frame:
            self.home_frame = ctk.CTkFrame(self.content_frame)
            self.home_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Add content to home frame
            welcome_label = ctk.CTkLabel(
                self.home_frame, 
                text="Welcome to Oz Stack Desktop!",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            welcome_label.pack(pady=(20, 10))
            
            description = ctk.CTkLabel(
                self.home_frame,
                text="This is a modern desktop application built with CustomTkinter.",
                font=ctk.CTkFont(size=14)
            )
            description.pack(pady=10)
            
            # Sample button
            sample_button = ctk.CTkButton(
                self.home_frame,
                text="Say Hello",
                command=lambda: messagebox.showinfo("Hello", "Hello, World!")
            )
            sample_button.pack(pady=20)
        else:
            self.home_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_data_frame(self):
        """Show the data content frame"""
        # Hide other frames
        if self.home_frame:
            self.home_frame.pack_forget()
            
        # Create data frame if it doesn't exist
        if not self.data_frame:
            self.data_frame = ctk.CTkFrame(self.content_frame)
            self.data_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Add content to data frame
            data_label = ctk.CTkLabel(
                self.data_frame, 
                text="Data Management",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            data_label.pack(pady=(20, 20))
            
            # Demo data entry form
            form_frame = ctk.CTkFrame(self.data_frame)
            form_frame.pack(fill="x", padx=20, pady=10)
            
            # Name field
            name_label = ctk.CTkLabel(form_frame, text="Name:")
            name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            
            self.name_entry = ctk.CTkEntry(form_frame, width=300)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)
            
            # Description field
            desc_label = ctk.CTkLabel(form_frame, text="Description:")
            desc_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            
            self.desc_entry = ctk.CTkTextbox(form_frame, width=300, height=100)
            self.desc_entry.grid(row=1, column=1, padx=10, pady=10)
            
            # Status field
            status_label = ctk.CTkLabel(form_frame, text="Status:")
            status_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            
            self.status_var = ctk.StringVar(value="Pending")
            self.status_combo = ctk.CTkComboBox(
                form_frame, 
                values=["Pending", "In Progress", "Completed"],
                variable=self.status_var,
                width=300
            )
            self.status_combo.grid(row=2, column=1, padx=10, pady=10)
            
            # Buttons
            button_frame = ctk.CTkFrame(self.data_frame)
            button_frame.pack(fill="x", padx=20, pady=(10, 20))
            
            save_button = ctk.CTkButton(
                button_frame, 
                text="Save", 
                command=self.save_data
            )
            save_button.pack(side="right", padx=10)
            
            clear_button = ctk.CTkButton(
                button_frame, 
                text="Clear", 
                command=self.clear_form,
                fg_color="transparent", 
                border_width=2,
                text_color=("gray10", "gray90")
            )
            clear_button.pack(side="right", padx=10)
        else:
            self.data_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def save_data(self):
        """Save form data to database (demo function)"""
        # Get form data
        name = self.name_entry.get()
        description = self.desc_entry.get("0.0", "end").strip()
        status = self.status_var.get()
        
        # Validate
        if not name:
            messagebox.showwarning("Validation Error", "Name is required")
            return
        
        # Normally, you would save to the database here
        # Example:
        # db = db.SessionLocal()
        # try:
        #     new_task = crud.create_task(db, schemas.TaskCreate(
        #         name=name,
        #         description=description,
        #         status=status
        #     ))
        #     messagebox.showinfo("Success", f"Task created with ID: {new_task.id}")
        # except Exception as e:
        #     messagebox.showerror("Error", f"Failed to save: {str(e)}")
        # finally:
        #     db.close()
        
        # For now, just show a message
        messagebox.showinfo("Data Saved", 
                            f"Name: {name}\nDescription: {description}\nStatus: {status}")
        self.clear_form()

    def clear_form(self):
        """Clear the data entry form"""
        self.name_entry.delete(0, "end")
        self.desc_entry.delete("0.0", "end")
        self.status_var.set("Pending")

    def open_settings(self):
        """Open settings dialog"""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("500x300")
        settings_window.transient(self)  # Make window modal
        
        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            settings_frame, 
            text="Application Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Add settings options here
        # ...
        
        # Sample setting
        theme_label = ctk.CTkLabel(settings_frame, text="Color Theme:")
        theme_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        theme_option = ctk.CTkOptionMenu(
            settings_frame, 
            values=["blue", "green", "dark-blue"],
            command=self.change_color_theme
        )
        theme_option.pack(anchor="w", padx=20, pady=(5, 10))
        theme_option.set(ctk.get_default_color_theme())
        
        # Close button
        close_button = ctk.CTkButton(
            settings_frame, 
            text="Close", 
            command=settings_window.destroy
        )
        close_button.pack(pady=20)

    def show_about(self):
        """Show the about dialog"""
        messagebox.showinfo(
            "About",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "A modern desktop application built with CustomTkinter\n"
            "Part of the Oz Stack Starter Kit"
        )

    def change_appearance_mode(self, new_appearance_mode: str):
        """Change the application appearance mode"""
        ctk.set_appearance_mode(new_appearance_mode)

    def change_color_theme(self, new_color_theme: str):
        """Change the application color theme"""
        ctk.set_default_color_theme(new_color_theme)
        messagebox.showinfo(
            "Theme Changed", 
            "The new theme will be fully applied the next time you start the application."
        )


def run_desktop_app():
    """Run the desktop application"""
    app = OzDesktopApp()
    app.mainloop()


if __name__ == "__main__":
    run_desktop_app()