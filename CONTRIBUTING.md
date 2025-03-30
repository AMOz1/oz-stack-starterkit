# Contributing to Oz Stack Starter Kit

Thank you for considering contributing to the Oz Stack Starter Kit! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:

1. Check the [Issues](https://github.com/yourusername/oz-stack-starterkit/issues) to see if the bug has already been reported
2. If you're unable to find an open issue addressing the problem, create a new one

When filing a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior and what actually happened
- Screenshots if applicable
- Environment details (OS, browser, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! When suggesting an enhancement:

1. Use a clear and descriptive title
2. Provide a detailed description of the proposed enhancement
3. Explain why it would be useful to most users
4. Describe the current behavior and how it would change

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Run tests and linting
5. Submit a pull request

#### Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update any related documentation
3. Ensure your code follows the existing style guidelines
4. Your PR should include tests if you're adding new functionality
5. The PR will be merged once it receives approval from a maintainer

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

### Setup Instructions

1. Clone your fork of the repository
   ```bash
   git clone https://github.com/yourusername/oz-stack-starterkit.git
   cd oz-stack-starterkit
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. Build CSS
   ```bash
   npm run build:css
   ```

5. Run the development server
   ```bash
   npm run dev
   ```

## Coding Guidelines

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints when appropriate
- Write docstrings for functions and classes
- Organize imports: standard library, third-party packages, local modules

### HTML/CSS

- Use 2-space indentation for HTML and CSS
- Follow Tailwind CSS utility-first approach
- Keep templates clean and focused on presentation
- Extract reusable components to the components directory

### JavaScript

- Use modern ES6+ syntax
- Prefer native browser APIs over adding JavaScript libraries
- Use HTMX and Hyperscript for most interactions
- Add Alpine.js components for more complex client-side logic

## Testing

- Add tests for new features
- Ensure all tests pass before submitting a PR
- Run tests with:
  ```bash
  pytest
  ```

## Documentation

- Update documentation to reflect any changes
- Document new features, components, or APIs
- Follow the existing documentation style

## Community

- Join our [Discord server](#) for questions and discussions
- Follow our [Twitter](#) for announcements
- Subscribe to our [newsletter](#) for updates

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [ISC License](LICENSE).