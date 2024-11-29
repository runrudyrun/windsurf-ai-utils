# Windsurf AI Utils

A collection of secure utilities for Cascade AI to interact with various services and APIs. This repository provides tools for managing credentials, interacting with databases, and integrating with external services.

## Features

- **Secure Credential Management**
  - Environment-based configuration using `python-dotenv`
  - Secure handling of sensitive data using JWT encryption
  - Credential masking capabilities
  - Type-safe settings using Pydantic
  - Comprehensive configuration validation

- **ClickHouse Integration**
  - Secure database connection management
  - Query execution with parameter substitution
  - Support for streaming large result sets
  - Connection health checks
  - Validated configuration setup

- **Miro Integration**
  - Board item management (cards, connectors)
  - Create and update cards
  - Manage relationships between items
  - Secure API token handling
  - Comprehensive error handling
  - Detailed API documentation

- **Testing and Quality**
  - Extensive unit test coverage
  - Configuration validation tests
  - Mock-based service testing
  - Integration test examples

- **Documentation**
  - Detailed service-specific documentation
  - Usage examples and best practices
  - Known issues and troubleshooting guides
  - API reference documentation

## Project Structure

```
windsurf-ai-utils/
├── core/
│   ├── config.py        # Configuration and environment management
│   ├── security.py      # JWT-based security utilities
│   └── validation.py    # Configuration validation
├── services/
│   ├── clickhouse/
│   │   └── client.py    # ClickHouse database client
│   └── miro/
│       └── client.py    # Miro API client
├── docs/                # Detailed documentation
│   └── services/
│       ├── clickhouse/  # ClickHouse client docs
│       └── miro/        # Miro client docs
├── tests/               # Unit tests
│   ├── core/           # Core module tests
│   └── services/       # Service client tests
├── utils/              # Helper utilities
└── examples/           # Usage examples
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/windsurf-ai-utils.git
cd windsurf-ai-utils
```

2. Configure environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
pip install -r requirements.txt
```

3. Set up credentials:
```bash
cp .env.example .env
# Configure your credentials in .env
```

4. Validate configuration:
```python
from core.validation import validate_all

# Check all configurations
results = validate_all()
for service, result in results.items():
    if not result["valid"]:
        print(f"Invalid {service} configuration:")
        print(f"Errors: {result['errors']}")
        print(f"Warnings: {result['warnings']}")
```

## Testing

Run the test suite:
```bash
# Install test dependencies
pip install pytest pytest-mock

# Run all tests
pytest

# Run specific test file
pytest tests/services/miro/test_client.py

# Run with coverage
pytest --cov=.
```

## Usage Examples

### ClickHouse Client

```python
from services.clickhouse.client import clickhouse_client

# Execute a query with parameters
results = clickhouse_client.execute_query(
    "SELECT * FROM table WHERE date >= {date}",
    params={"date": "2024-01-01"}
)

# Stream large result sets
for row in clickhouse_client.execute_query_stream(
    "SELECT * FROM large_table"
):
    process_row(row)
```

### Miro Client

```python
from services.miro.client import miro_client

# Create a card
card = miro_client.create_card(
    content="Task Description",
    position={"x": 0, "y": 0}
)

# Update card content
miro_client.update_card(
    card_id=card["id"],
    content="Updated Task Description"
)

# Get board items
items = miro_client.get_board_items(item_type="card")
```

### Security Manager

```python
from core.security import security_manager

# Encrypt sensitive data
encrypted = security_manager.encrypt_sensitive_data({
    "api_key": "sensitive_value"
})

# Mask sensitive strings
masked = security_manager.mask_sensitive_string("1234567890", visible_chars=4)
# Output: '******7890'
```

## Security Considerations

- All sensitive data is stored in environment variables
- Sensitive values are handled as `SecretStr` using Pydantic
- JWT encryption for additional data protection
- Secure parameter substitution in database queries
- Configuration validation before service initialization
- Comprehensive error handling with secure error messages
- No hardcoded credentials
- Regular security audits through automated testing

## Requirements

- Python 3.8+
- ClickHouse database
- Miro account with API access
- Required Python packages:
  - `python-dotenv`: Environment variable management
  - `pydantic`: Data validation and settings management
  - `clickhouse-driver`: ClickHouse database connectivity
  - `requests`: HTTP client for API interactions
  - `python-jose[cryptography]`: JWT handling
  - `pytest`: Testing framework
  - `pytest-mock`: Mocking for tests
  - `pytest-cov`: Test coverage reporting

## Development

### Running Tests
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=. --cov-report=term-missing

# Run specific test module
pytest tests/services/miro/test_client.py -v
```

### Documentation
Detailed documentation for each service is available in the `docs/` directory:
- [Miro Service Documentation](docs/services/miro/README.md)
- [ClickHouse Service Documentation](docs/services/clickhouse/README.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
