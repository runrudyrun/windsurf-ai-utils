# Windsurf AI Utils

A collection of secure utilities for Cascade AI to interact with various services and APIs. This repository provides tools for managing credentials, interacting with databases, and integrating with external services.

## Features

- **Secure Credential Management**
  - Environment-based configuration using `python-dotenv`
  - Secure handling of sensitive data using JWT encryption
  - Credential masking capabilities
  - Type-safe settings using Pydantic

- **ClickHouse Integration**
  - Secure database connection management
  - Query execution with parameter substitution
  - Support for streaming large result sets
  - Connection health checks

- **Miro Integration**
  - Board item management (cards, connectors)
  - Create and update cards
  - Manage relationships between items
  - Secure API token handling

## Project Structure

```
windsurf-ai-utils/
├── core/
│   ├── config.py        # Configuration and environment management
│   └── security.py      # JWT-based security utilities
├── services/
│   ├── clickhouse/
│   │   └── client.py    # ClickHouse database client
│   └── miro/
│       └── client.py    # Miro API client
├── utils/               # Helper utilities
└── examples/            # Usage examples
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
- No hardcoded credentials

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Requirements

- Python 3.8+
- ClickHouse database
- Miro account with API access
- Required Python packages:
  - `python-dotenv`
  - `pydantic`
  - `clickhouse-driver`
  - `requests`
  - `python-jose[cryptography]`
