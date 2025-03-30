# Desktop Application Guide

This guide explains how to use the CustomTkinter desktop application capabilities in the Oz Stack Starter Kit.

## Overview

The Oz Stack Starter Kit includes support for creating desktop applications using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), a modern-looking UI library built on top of Tkinter. This allows you to create both web and desktop interfaces for your application using the same codebase.

## Features

- Modern UI with CustomTkinter
- Dark/Light mode support
- Seamless integration with your SQLite database
- Shared business logic between web and desktop interfaces

## Getting Started

### Prerequisites

Ensure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

### Running the Desktop Application

You can run the desktop application in two ways:

1. Via the desktop CLI:

```bash
python -m src.desktop.cli
```

2. By setting the `DESKTOP_MODE` environment variable:

```bash
DESKTOP_MODE=True python -m src.main
```

### Command-line Options

The desktop CLI supports several command-line options:

```bash
python -m src.desktop.cli --help
```

Available options:

- `--version`: Display version information
- `--theme [light/dark/system]`: Set application theme
- `--color [blue/green/dark-blue]`: Set color scheme
- `--debug`: Enable debug logging

## Structure

The desktop application is structured as follows:

```
src/
├── desktop/
│   ├── __init__.py
│   ├── app.py         # Main desktop application
│   └── cli.py         # Command-line interface
```

## Customizing the UI

### Adding New Frames

To add a new frame to the desktop application:

1. Create a new method in the `OzDesktopApp` class in `app.py`:

```python
def show_my_new_frame(self):
    # Hide other frames
    if self.home_frame:
        self.home_frame.pack_forget()
    if self.data_frame:
        self.data_frame.pack_forget()
        
    # Create the new frame
    if not self.my_new_frame:
        self.my_new_frame = ctk.CTkFrame(self.content_frame)
        self.my_new_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add content to the frame
        title = ctk.CTkLabel(
            self.my_new_frame, 
            text="My New Frame",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 20))
        
        # Add more widgets as needed
    else:
        self.my_new_frame.pack(fill="both", expand=True, padx=20, pady=20)
```

2. Add a button to the sidebar:

```python
self.new_button = ctk.CTkButton(
    self.sidebar, text="New Frame", command=self.show_my_new_frame
)
self.new_button.grid(row=3, column=0, padx=20, pady=10)
```

### Using Database Models

To interact with your SQLite database:

```python
from src.database import models, crud, db

def save_data(self):
    # Get form data
    name = self.name_entry.get()
    
    # Save to database
    session = db.SessionLocal()
    try:
        new_task = models.Task(name=name, description="Created from desktop app")
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        messagebox.showinfo("Success", f"Task created with ID: {new_task.id}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {str(e)}")
    finally:
        session.close()
```

## Themes and Appearance

CustomTkinter supports different themes and appearance modes:

### Appearance Modes

- System (default)
- Light
- Dark

Set the appearance mode in code:

```python
ctk.set_appearance_mode("Dark")
```

### Color Themes

- blue (default)
- green
- dark-blue

Set the color theme in code:

```python
ctk.set_default_color_theme("green")
```

## Building Standalone Applications

To create a standalone executable for distribution:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Create the executable:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name=MyApp src/desktop/cli.py
```

For more detailed instructions on packaging, see the [PyInstaller documentation](https://pyinstaller.org/en/stable/).

## Best Practices

1. **Separate logic from UI**
   - Keep business logic in shared modules
   - Use the UI only for display and interaction

2. **Reuse database models**
   - Share the same SQLAlchemy models between web and desktop

3. **Keep UI responsive**
   - Use threading for long-running operations
   - Update the UI in the main thread

4. **Error handling**
   - Always use try/except blocks when working with the database
   - Display user-friendly error messages

## Common Issues

### Window appears blank or empty

- Check for errors in the console
- Ensure all UI elements are properly packed or grid-configured

### Database errors

- Make sure the database file exists and is accessible
- Verify your models are properly defined
- Check connection strings in your environment variables

### Custom widgets or styles not working

- Ensure you're using the correct CTk widget classes
- Check the CustomTkinter documentation for proper usage