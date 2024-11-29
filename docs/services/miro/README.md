# Miro Service

The Miro service provides a client for interacting with the Miro API v2, allowing you to create and manage cards on Miro boards.

## Configuration

The service requires the following environment variables:

```env
MIRO_ACCESS_TOKEN="your_access_token"  # OAuth 2.0 access token
MIRO_BOARD_ID="board_id"               # Board ID with trailing equals sign if present
```

## Usage

### Basic Usage

```python
from services.miro.client import miro_client

# Check access
if miro_client.check_token():
    print("Token is valid")

# Create a card
card = miro_client.create_card(
    title="My Card",
    description="Card description",
    style={"cardTheme": "#2196f3"},  # Material Design Blue
    position={"x": 0, "y": 0, "origin": "center"}
)

# Get card URL
url = miro_client.get_card_url(card["id"])
```

### API Methods

#### `create_card`
Creates a new card on the board.

```python
card = miro_client.create_card(
    title="My Card",
    description="Description",
    style={"cardTheme": "#2196f3"},
    position={"x": 0, "y": 0, "origin": "center"}
)
```

**Parameters:**
- `title`: Card title
- `description`: Card description
- `style`: Optional card style (e.g. `{"cardTheme": "#2196f3"}`)
- `position`: Optional card position

#### `update_card`
Updates an existing card.

```python
miro_client.update_card(
    card_id="card_id",
    title="New Title",
    description="New Description",
    style={"cardTheme": "#f44336"}
)
```

#### `delete_card`
Deletes a card from the board.

```python
miro_client.delete_card("card_id")
```

## Known Issues

1. Board ID Format
   - Some board IDs include a trailing equals sign (`=`)
   - Always use the full board ID as shown in the Miro URL

2. Card Styling
   - Only `cardTheme` is supported for styling (not `fillColor`)
   - Use hex color codes (e.g. `#2196f3`)

## Error Handling

The client provides detailed error logging:
- API request details (URL, headers)
- Request payload for POST/PATCH requests
- Error responses from the API

Example error handling:

```python
try:
    card = miro_client.create_card(...)
except Exception as e:
    print(f"Error creating card: {e}")
```

## Development

### Running Tests
TODO: Add test instructions

### Adding New Features
1. Update the client in `services/miro/client.py`
2. Add documentation for new methods
3. Update known issues if relevant
4. Add example usage in `examples/`
