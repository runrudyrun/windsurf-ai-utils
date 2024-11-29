# AI Guidelines for ClickHouse Integration

This document outlines best practices and guidelines for AI to work with ClickHouse database using the provided utilities.

## 1. Connection Setup

When working with ClickHouse:

1. Always use the existing configuration from `.env` file
   - Do not modify connection settings directly
   - Do not hardcode credentials in scripts
   - Use the provided `clickhouse_client` instance from `services.clickhouse.client`

2. Create example scripts in the `examples/` directory
   - Place new scripts demonstrating specific use cases
   - Include error handling and logging
   - Follow the existing code style and patterns

3. Connection troubleshooting:
   - Use `clickhouse_client.ping()` to test connection
   - Check if ClickHouse server is running
   - Verify credentials in `.env` file
   - Look for connection errors in logs

## 2. Query Execution

When executing queries:

1. Use parameterized queries for safety:
   ```python
   query = "SELECT * FROM table WHERE id = %(id)s"
   params = {"id": user_id}
   results = clickhouse_client.execute_query(query, params)
   ```

2. Handle large result sets with streaming:
   ```python
   for row in clickhouse_client.execute_query_stream(query, params):
       process_row(row)
   ```

3. Always include error handling:
   ```python
   try:
       results = clickhouse_client.execute_query(query)
   except Exception as e:
       handle_error(e)
   ```

## 3. Best Practices

1. Schema handling:
   - Use fully qualified table names when necessary
   - Be aware of the current database context
   - Check table existence before querying

2. Performance considerations:
   - Limit result sets when possible
   - Use appropriate indexes
   - Consider query optimization

3. Security:
   - Never expose credentials in logs or output
   - Use appropriate user permissions
   - Follow the principle of least privilege

## 4. Example Usage

Basic example of working with ClickHouse:

```python
from services.clickhouse.client import clickhouse_client

def analyze_data():
    """Example function demonstrating ClickHouse client usage."""
    if not clickhouse_client.ping():
        print("Failed to connect to ClickHouse")
        return
        
    query = """
    SELECT column1, column2
    FROM your_table
    WHERE condition = %(param)s
    LIMIT 100
    """
    
    try:
        results = clickhouse_client.execute_query(
            query, 
            params={"param": "value"}
        )
        process_results(results)
    except Exception as e:
        handle_error(e)
```

## 5. Common Issues and Solutions

1. Connection Issues:
   - Verify server is running
   - Check port availability
   - Confirm network access
   - Validate credentials

2. Query Issues:
   - Verify table existence
   - Check column names
   - Validate data types
   - Review query syntax

3. Performance Issues:
   - Review query execution plan
   - Check for appropriate indexes
   - Consider query optimization
   - Monitor resource usage

## 6. Development Workflow

1. Create example scripts in `examples/` directory
2. Use existing configuration from `.env`
3. Implement proper error handling
4. Add logging where appropriate
5. Document any special considerations
6. Test thoroughly before deployment
