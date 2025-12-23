# Translator Module Examples

This directory contains examples for using the Query Translator module.
The translator converts Chinese queries to English for semantic search in English-language documents.

## Prerequisites

Make sure you have:
- Installed the project dependencies: `pip install -r requirements.txt`
- Set up your `.env` file with `OPENAI_API_KEY` (see `.env.example`)

## Examples

### 01_basic_usage.py
**Basic Query Translation**

Demonstrates the core translation functionality:
- How to initialize QueryTranslator
- Translating simple Chinese queries to English
- Handling queries with technical terms

```bash
python -m query.examples.translator.01_basic_usage
```

**Use case**: Best starting point for understanding basic translation.

---

### 02_mixed_language_handling.py
**Translating Queries with Professional Vocabulary**

Shows how the translator handles Chinese queries that mix natural language with technical terms and acronyms:
- Preserves technical terms (APRA, SIS Act, KYC, AML, ESG, SuperStream)
- Translates natural language portions
- Maintains professional terminology

```bash
python -m query.examples.translator.02_mixed_language_handling
```

**Use case**: Real-world scenarios where Chinese queries contain financial/compliance terminology.

---

## Running All Examples

To run all examples sequentially:

```bash
for example in 01_basic_usage 02_mixed_language_handling; do
    echo "Running $example..."
    python -m query.examples.translator.$example
    echo ""
done
```

Or on Windows:

```bash
@echo off
for %%i in (01_basic_usage 02_mixed_language_handling) do (
    echo Running %%i...
    python -m query.examples.translator.%%i
    echo.
)
```

## How It Works

The `QueryTranslator.translate()` method:
1. Takes a Chinese query as input
2. Sends it to OpenAI with a prompt that specifies technical terms to preserve
3. Returns the English translation
4. Technical terms in `TECHNICAL_TERMS` are explicitly preserved in the prompt

Example:
```python
translator = QueryTranslator()
result = translator.translate("APRA对SIS Act的要求是什么？")
# Returns: "What are APRA's requirements for the SIS Act?"
```

## Troubleshooting

### Error: "No module named 'query'"
Make sure you're running from the project root directory and have installed dependencies.

### Error: "OpenAI API key not found"
Check your `.env` file and ensure `OPENAI_API_KEY` is set correctly. See `.env.example` for format.

## Next Steps

After understanding the Translator module:
- Check Retrieval Examples for search functionality
- Check Ingest Examples for document processing
- Check End-to-End Examples for complete workflows

