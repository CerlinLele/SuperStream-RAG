# SuperStream-RAG Examples

This directory contains comprehensive examples for all modules in SuperStream-RAG.
Each module has its own examples subdirectory with progressively complex examples.

## Quick Start

**First time?** Start with the Translator module:

```bash
python -m query.examples.translator.01_basic_usage
```

## Available Examples

### [Translator Examples](../query/examples/translator/) ✅
Learn how to detect and translate queries between Chinese and English.

**Key examples:**
- `01_basic_usage.py` - Language detection and translation
- `02_custom_api_config.py` - Custom API endpoints
- `03_api_client_config.py` - Fine-grained configuration
- `04_direct_client_creation.py` - Convenience client creation
- `05_mixed_language_handling.py` - Mixed language queries

[View all Translator examples →](../query/examples/translator/README.md)

### Retrieval Examples (Coming Soon)
Learn how to search and retrieve documents from the knowledge base.

### Ingest Examples (Coming Soon)
Learn how to process and ingest documents into the knowledge base.

### End-to-End Examples (Coming Soon)
Complete workflows combining multiple modules.

## Project Structure

```
examples/
├── README.md                # This file

query/
└── examples/
    └── translator/          # Translator module examples
        ├── 01_basic_usage.py
        ├── 02_custom_api_config.py
        ├── 03_api_client_config.py
        ├── 04_direct_client_creation.py
        ├── 05_mixed_language_handling.py
        └── README.md

retrieval/
└── examples/                # Retrieval module examples (future)

ingest/
└── examples/                # Ingest module examples (future)
```

## Running Examples

### Run a single example:
```bash
python -m query.examples.translator.01_basic_usage
```

### Run all examples in a module:
```bash
python -m query.examples.translator  # Requires __main__.py in the module
```

### Interactive exploration:
```bash
python
>>> from query.examples.translator.basic_usage import main
>>> main()
```

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Set `OPENAI_API_KEY` with your actual API key

3. **Verify setup:**
   ```bash
   python -m query.examples.translator.01_basic_usage
   ```

## Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'query'` | Make sure you're running from project root and dependencies are installed |
| `OpenAI API key not found` | Check `.env` file and ensure `OPENAI_API_KEY` is set |
| `Connection error` | Check internet connection and API endpoint availability |

## Adding New Examples

When adding examples for a new module:

1. Create a subdirectory: `examples/module_name/`
2. Create numbered files: `01_basic.py`, `02_advanced.py`, etc.
3. Add `__init__.py` with module docstring
4. Add `README.md` with descriptions and usage instructions
5. Update this main README with links to new module

### Example Template

```python
"""
Example N: Brief Description

Explains what this example demonstrates.
"""

def main():
    """Run the example"""
    # Example code here
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("Example N: Brief Description")
    print("=" * 60)
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
```

## Module Status

- ✅ **Translator** - Complete examples for query translation
- 🔄 **Retrieval** - Examples coming soon
- 🔄 **Ingest** - Examples coming soon
- 🔄 **End-to-End** - Examples coming soon

## Contributing

When adding new examples:
- Keep examples self-contained and runnable
- Include docstrings explaining what's being demonstrated
- Add error handling with helpful messages
- Update the relevant module README
- Number examples to show progression difficulty

## References

- [Project README](../README.md)
- [Translator Module Documentation](../docs/)
- [API Configuration Guide](../docs/api_client_guide.md)
