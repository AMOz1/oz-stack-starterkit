# Oz Stack Starter Kit

A lightweight web application starter kit built with:

- **Backend**: FastAPI (Python)
- **Frontend**: HTMX
- **Styling**: Tailwind CSS + DaisyUI
- **Optional JS**: Hyperscript

## Setup

### 1. Install Python dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install Node.js dependencies

```bash
npm install
```

### 3. Build CSS

```bash
npm run build:css
```

## Development

### Run the development server

```bash
npm run dev
```

Or manually:

```bash
python -m src.main
```

### Watch for CSS changes

```bash
npm run watch:css
```

## Project Structure

```
├── src/
│   ├── static/
│   │   ├── css/
│   │   │   ├── app.css         # Tailwind CSS source file
│   │   │   └── output.css      # Generated CSS (git-ignored)
│   │   └── js/                 # JavaScript files (if needed)
│   ├── templates/              # Jinja2 templates
│   │   ├── components/         # Reusable UI components
│   │   ├── base.html           # Base template
│   │   └── index.html          # Main page template
│   └── main.py                 # FastAPI application
├── .gitignore
├── package.json
├── README.md
└── requirements.txt
```
