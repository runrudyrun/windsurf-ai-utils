# Windsurf AI Utils

A collection of secure utilities for interacting with various services and APIs, designed specifically for AI assistants.

## Features

- **Secure Credential Management**
  - Environment variables-based configuration
  - Encrypted storage for sensitive data
  - Safe credential handling patterns

- **ClickHouse Integration**
  - Secure database connections
  - Efficient query execution
  - Stream processing support
  - Query parameter sanitization

- **Miro API Integration**
  - Board management
  - Card creation and updates
  - Connector management (relationships between items)
  - Task progress tracking
  - Batch operations support

## Project Structure

```
windsurf-ai-utils/
├── core/                      # Core components
│   ├── config.py             # Configuration and environment management
│   └── security.py           # Security utilities for credential handling
├── services/                  # Service integrations
│   ├── clickhouse/           # ClickHouse database client
│   │   ├── __init__.py
│   │   └── client.py
│   └── miro/                 # Miro API integration
│       ├── __init__.py
│       └── client.py
├── utils/                    # Helper utilities
└── examples/                 # Usage examples
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/windsurf-ai-utils.git
cd windsurf-ai-utils
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Linux/macOS
source venv/bin/activate
# On Windows
.\venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Usage Examples

### ClickHouse Client

```python
from services.clickhouse.client import clickhouse_client

# Execute a query
results = clickhouse_client.execute_query(
    "SELECT * FROM your_table WHERE date >= {date}",
    params={"date": "2024-01-01"}
)

# Stream large results
for row in clickhouse_client.execute_query_stream(
    "SELECT * FROM large_table"
):
    process_row(row)
```

### Miro Client

```python
from services.miro.client import miro_client

# Create connected cards
cards = miro_client.create_related_cards([
    {
        "content": "Task 1",
        "position": {"x": 0, "y": 0}
    },
    {
        "content": "Task 2",
        "position": {"x": 200, "y": 0}
    }
], connection_type="curved")

# Create custom connector
miro_client.create_connector(
    start_item_id=cards[0]["id"],
    end_item_id=cards[1]["id"],
    connector_type="straight",
    style={
        "strokeColor": "#ff0000",
        "strokeWidth": 2,
        "strokeStyle": "dashed"
    }
)
```

## Security

- All sensitive data is stored in environment variables
- `.env` file is excluded from version control
- Additional encryption layer for sensitive data
- Secure credential handling patterns implemented
- No hardcoded credentials or sensitive information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Requirements

- Python 3.8+
- ClickHouse database
- Miro account with API access
- Required Python packages (see requirements.txt)
