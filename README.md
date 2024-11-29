# Windsurf AI Utilities

Repository with toolkit that I use to simplify the interaction of Cascade AI with external services (such as databases) and APIs. This repository provides the core infrastructure for secure service authentication and data exchange.

## Core Purpose

This toolkit currently provides Cascade AI with:
- Secure service authentication and credential management
- Standardized API clients for external services
- Data querying and transformation utilities

## Key Components

- **Service Clients**
  - Miro API client for visual documentation
  - ClickHouse client for data queries
  - Authentication and token management
  - Error handling and retries

- **Core Utilities**
  - Environment-based configuration
  - Secure credential handling
  - Configuration validation
  - Error management

## Example Use Case: Data Analysis with Visual Documentation

Problem: Analyze data quality issues and create visual documentation of findings.

Tools Used:
- ClickHouse client for data queries
- Native ability of Cascade AI to consume links to locally stored codebase
- Miro client for sending artifacts to my Miro board
- Core utilities for credentials management and error handling

## Project Structure

```
windsurf-ai-utils/
├── core/                # Core utilities
│   ├── config.py       # Configuration management
│   ├── security.py     # Credential handling
│   └── validation.py   # Config validation
├── services/           # Service clients
│   ├── clickhouse/     # ClickHouse client
│   └── miro/          # Miro API client
├── artifacts/           # Folder with task specific artifacts
├── tests/             # Test suite
└── utils/             # Helper utilities
```

## Setup

1. Install:
```bash
pip install -r requirements.txt
```

2. Configure credentials:
```bash
cp .env.example .env
# Add service credentials
```

## Security

- Environment-based credential management
- JWT token handling
- Secure parameter passing
- No hardcoded credentials

## Requirements

- Python 3.8+
- Required packages in requirements.txt

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details
