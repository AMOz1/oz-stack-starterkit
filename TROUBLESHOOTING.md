# Troubleshooting Guide

This document provides solutions to common issues you might encounter when setting up or running the Oz Stack Starter Kit.

## Setup Issues

### Python-related Issues

#### "Python command not found"

**Problem:** Running `python` returns a "command not found" error.

**Solution:**
- Ensure Python is installed by running `python3 --version`
- If it's installed as `python3`, create an alias: `alias python=python3`
- On Windows, make sure Python is added to your PATH

#### "Virtual environment not created"

**Problem:** Running `python -m venv venv` fails.

**Solution:**
- Ensure you have the venv module: `python -m pip install --user virtualenv`
- On Ubuntu/Debian: `sudo apt-get install python3-venv`
- On Fedora: `sudo dnf install python3-venv`
- Try using virtualenv instead: `pip install virtualenv && virtualenv venv`

#### "Module not found" errors

**Problem:** Getting `ModuleNotFoundError` when running the application.

**Solution:**
- Ensure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- If a specific module is missing, install it directly: `pip install module_name`

### Node.js-related Issues

#### "npm command not found"

**Problem:** Running `npm` returns a "command not found" error.

**Solution:**
- Ensure Node.js is installed: `node --version`
- If Node.js is installed but npm isn't, reinstall Node.js
- On macOS: `brew install node`
- On Windows: Download and install from nodejs.org

#### "npm install fails"

**Problem:** `npm install` fails with errors.

**Solution:**
- Clear npm cache: `npm cache clean --force`
- Try with a different registry: `npm install --registry=https://registry.npmjs.org/`
- Check Node.js version compatibility: `node --version`
- Make sure you have write permissions in the directory

#### "Wrong Tailwind CSS or DaisyUI versions"

**Problem:** The installed versions of Tailwind CSS or DaisyUI don't match the required versions (Tailwind CSS 4.x and DaisyUI 5.x).

**Solution:**
- Check installed versions with `npm list tailwindcss daisyui`
- Run the provided verification script: `npm run verify-versions`
- Fix the versions automatically: `npm run fix-versions`
- If that doesn't work, manually install the correct versions:
  ```bash
  npm install tailwindcss@^4.0.0 daisyui@^5.0.9 --save
  ```
- Clear npm cache if needed: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

#### "Circular dependency error in Tailwind CSS"

**Problem:** Building CSS fails with a message about circular dependencies.

**Solution:**
- Avoid using `@apply` with component classes like `btn-primary` inside component definitions
- Instead of nesting component classes, extend the base components with more specific utility classes
- Check your app.css file for circular references between component classes
- Simplify complex CSS class hierarchies

### CSS Issues

#### "CSS not being generated"

**Problem:** Running `npm run build:css` doesn't create the output.css file.

**Solution:**
- Check tailwind.config.js for errors
- Ensure the input CSS file exists: `src/static/css/app.css`
- Try installing tailwindcss globally: `npm install -g tailwindcss`
- Run the tailwind CLI directly: `npx tailwindcss -i src/static/css/app.css -o src/static/css/output.css`

#### "CSS changes not reflecting in browser"

**Problem:** Changes to CSS aren't visible in the browser.

**Solution:**
- Make sure you're running the CSS watcher: `npm run watch:css`
- Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
- Check that your HTML is referencing the correct CSS file
- Verify that the output.css file is being updated (check file's modified time)

## Runtime Issues

### Server Issues

#### "Port already in use"

**Problem:** Server fails to start with "Address already in use" error.

**Solution:**
- Change the port in your .env file: `PORT=8001`
- Find and kill the process using the port:
  ```bash
  # On macOS/Linux
  lsof -i :8000
  kill -9 <PID>
  
  # On Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

#### "Connection refused errors"

**Problem:** Browser shows "refused to connect" errors when accessing localhost:8000.

**Solution:**
- Check that the server is actually running
- Verify the HOST setting in your .env file:
  - Try using `127.0.0.1` instead of `0.0.0.0`
  - Some systems may have network interface binding issues with `0.0.0.0`
- Make sure you're using the correct port number
- Check if a firewall is blocking connections
- Try accessing using http://127.0.0.1:8000 explicitly

#### "Server crashes on startup"

**Problem:** Server exits immediately after starting.

**Solution:**
- Check for errors in the console output
- Verify your .env file has correct settings
- Check that required files exist (templates, static files)
- Try running with debug mode: `DEBUG=True python -m src.main`

### HTMX Issues

#### "HTMX requests not working"

**Problem:** HTMX elements don't load or update as expected.

**Solution:**
- Check the browser console for JavaScript errors
- Verify HTMX is properly loaded (check network tab)
- Check attributes: `hx-get`, `hx-target`, and `hx-trigger` are set correctly
- Verify the API endpoints return correct responses (test directly in browser)

#### "HTMX elements don't update"

**Problem:** Content doesn't change when HTMX requests are made.

**Solution:**
- Inspect the network tab to ensure requests are being made
- Check that the server is returning the expected HTML
- Verify target element exists with the correct ID
- Try adding `hx-swap="innerHTML"` to the HTMX element

### Database Issues (if applicable)

#### "Database connection errors"

**Problem:** Application fails with database connection errors.

**Solution:**
- Check database credentials in your .env file
- Ensure the database server is running
- Try connecting to the database with a GUI tool to verify accessibility
- Check for firewall issues that might block connection

## Deployment Issues

### Production Server

#### "Application doesn't work in production"

**Problem:** The application runs locally but not when deployed.

**Solution:**
- Set `DEBUG=False` in your production .env
- Check for environment-specific configuration
- Verify all required dependencies are installed in production
- Check server logs for specific errors
- Ensure static files are properly served

#### "CORS errors in production"

**Problem:** Getting Cross-Origin Resource Sharing (CORS) errors.

**Solution:**
- Configure CORS in your FastAPI application:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://yourdomain.com"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### Docker Issues (if using Docker)

#### "Container fails to start"

**Problem:** Docker container exits immediately after starting.

**Solution:**
- Check Docker logs: `docker logs <container_id>`
- Verify your Dockerfile has correct commands
- Ensure all required environment variables are set
- Try running the container with interactive shell: `docker run -it --rm <image_name> /bin/bash`

## Still Having Issues?

If you're still experiencing problems:

1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Check the [HTMX documentation](https://htmx.org/docs/)
3. Check the [Tailwind CSS documentation](https://tailwindcss.com/docs)
4. Open an issue on the GitHub repository
5. Search for similar issues in the repository's issue tracker
6. Check Stack Overflow for related questions