# Contributing to RAT 4.0

Thank you for considering contributing to RAT 4.0! We welcome all contributions, from bug reports to new features and documentation improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

1. **Check for Existing Issues**: Before creating a new issue, please check if a similar issue already exists.
2. **Create an Issue**: If you find a bug, create a detailed issue with:
   - A clear title and description
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Enhancements

1. **Check for Existing Suggestions**: Look for similar enhancement requests.
2. **Create an Enhancement Request**: Include:
   - A clear title and description
   - Why this enhancement would be useful
   - Any alternative solutions
   - Screenshots or mockups if applicable

### Your First Code Contribution

1. **Fork the Repository**: Click the "Fork" button in the top-right corner.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/Devxbu/Educational-RAT.git
   cd Educational-RAT
   ```
3. **Create a New Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Your Changes**: Follow the [Code Style](#code-style) guidelines.
5. **Test Your Changes**:
   ```bash
   python -m unittest discover
   ```
6. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Add: Your feature description"
   ```
7. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Submit the PR

### Pull Requests

- Keep PRs focused on a single feature or bug fix
- Update the CHANGELOG.md with your changes
- Ensure all tests pass
- Update documentation as needed
- Include tests for new features

## Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Devxbu/Educational-RAT.git
   cd Educational-RAT
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run Tests**:
   ```bash
   python -m pytest
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use type hints for all function signatures
- Include docstrings for all public functions and classes
- Keep lines under 100 characters
- Use 4 spaces for indentation
- Write meaningful commit messages

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
