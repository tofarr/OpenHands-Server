# Development Guide

This document provides detailed information for developers working on OpenHands Server.

## Development Setup

### Prerequisites
- Python 3.12+
- UV package manager
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/tofarr/OpenHands-Server.git
cd OpenHands-Server

# Install dependencies
make install-dev

# Install pre-commit hooks
make install-pre-commit-hooks
```

## Project Structure

```
OpenHands-Server/
├── openhands_server/          # Main package (currently empty)
│   └── __init__.py
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_dummy.py         # Dummy test
├── .github/                   # GitHub workflows
│   └── workflows/
├── .openhands/               # OpenHands configuration
├── pyproject.toml            # Project configuration
├── Makefile                  # Development commands
├── README.md                 # Project documentation
├── Development.md            # This file
├── LICENSE                   # MIT license
├── .gitignore               # Git ignore rules
└── .pre-commit-config.yaml  # Pre-commit configuration
```

## Development Commands

```bash
# Install dependencies
make install-dev

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run the server
make run

# Clean build artifacts
make clean
```

## Code Quality

This project uses several tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pre-commit**: Git hooks for code quality
- **Pytest**: Testing framework

## Building

### Local Development
```bash
# Run the server locally
make run
```

### Binary Build
```bash
# Build standalone executable
./build.sh --install-pyinstaller
```

## Testing

```bash
# Run all tests
make test

# Run specific test
uv run pytest tests/test_dummy.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## API Development

When implementing the REST/WebSocket interface:

### REST Endpoints
- Use FastAPI for REST endpoints
- Follow RESTful conventions
- Include proper error handling
- Add request/response models with Pydantic

### WebSocket Endpoints
- Use FastAPI WebSocket support
- Handle connection lifecycle properly
- Implement proper error handling
- Consider message queuing for reliability

### Agent Integration
- Use the OpenHands SDK for agent communication
- Handle agent lifecycle properly
- Implement proper error handling and recovery
- Consider async/await patterns for non-blocking operations