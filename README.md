# Payload Observer

A web application that analyzes JSON payloads using AI and generates insightful one-sentence descriptions with semantic similarity metrics.

## Overview

Payload Observer accepts any JSON payload and uses Claude AI to generate a concise, human-readable interpretation. It also calculates word-level similarity metrics to measure how well the AI description aligns with the original payload structure.

**Key Features:**
- 🤖 AI-powered payload interpretation using Claude Haiku
- 📊 Word-level Jaccard similarity metrics (0-1 scale)
- 🎨 Clean, minimal HuggingFace Spaces-inspired UI
- ⚡ Real-time analysis with formatted JSON preview
- 📱 Responsive two-column layout (single column on mobile)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (HTML/JS)                 │
│         static/index.html - Two-column UI            │
└──────────────────┬──────────────────────────────────┘
                   │ POST /api/analyze
┌──────────────────▼──────────────────────────────────┐
│              Backend (Flask)                         │
│              app.py - REST API                       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         Workflow (LangGraph)                         │
│  workflow.py - Single-node AI analysis pipeline      │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         Claude API (ChatAnthropic)                   │
│       Generates descriptions & metrics               │
└─────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.10+
- `ANTHROPIC_API_KEY` set in `.env`

### Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd payload_observer
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API key:
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

5. Run the application:
```bash
./start.sh
```

The app will be available at `http://localhost:8000`

## Usage

### Basic Workflow

1. **Enter Payload**: Paste or type any valid JSON in the left input box
2. **Click Analyze**: Submit the payload for AI analysis
3. **View Results**: 
   - Formatted JSON in the output preview
   - AI-generated description in the "AI Description" box
   - Similarity metrics showing word-level overlap

### Example Input

```json
{
  "user": {
    "id": 12345,
    "name": "Alice",
    "email": "alice@example.com"
  },
  "timestamp": "2026-04-07T10:30:00Z",
  "action": "login"
}
```

### Expected Output

- **AI Description**: `User alice@example.com logged in on 2026-04-07 at 10:30 UTC.`
- **Similarity**: `1.0` (perfect match when JSON is consistently formatted)
- **Intersection/Union**: Word counts from similarity calculation

## Configuration

Configure the application via environment variables or code:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Required | Your Anthropic API key |
| `MODEL_ID` | `claude-haiku-4-5-20251001` | Claude model to use for analysis |
| `FLASK_PORT` | `8000` | Port to run the Flask server on |

## Project Structure

```
payload_observer/
├── app.py                 # Flask server and REST API
├── workflow.py            # LangGraph workflow for AI analysis
├── models.py              # Pydantic/dataclass models
├── static/
│   └── index.html         # Frontend UI
├── requirements.txt       # Python dependencies
├── start.sh               # Startup script
├── .env                   # Environment variables (not in repo)
└── .claude_notes          # Project documentation
```

## API Endpoint

### POST `/api/analyze`

Analyzes a JSON payload and returns AI description with metrics.

**Request:**
```json
{
  "payload": { ... },
  "original_input": "JSON string (formatted with 2-space indent)"
}
```

**Response:**
```json
{
  "payload": { ... },
  "description": "One-sentence AI interpretation",
  "similarity": 0.95,
  "intersection": 45,
  "union": 47
}
```

## Similarity Metrics

The app uses **Jaccard Similarity** to measure alignment between the formatted input and re-serialized payload:

```
Jaccard Similarity = |A ∩ B| / |A ∪ B|
```

Where:
- **A** = words in formatted input JSON
- **B** = words in formatted payload JSON
- **Intersection** = common words
- **Union** = total unique words

Since both are formatted consistently, similarity is typically **1.0** (perfect match).

## Styling

- **Background**: Pure black (`#000`)
- **Text**: White (`#fff`)
- **Textbox Background**: Dark gray (`#111`)
- **Borders**: Subtle gray (`#222`, `#333`)
- **Layout**: CSS Grid with two columns (responsive on mobile)

## Development

### Running Tests
```bash
python -m pytest
```

### Modifying the AI Prompt

Edit the system prompt in `workflow.py` to customize how Claude interprets payloads:

```python
# In workflow.py, modify the ChatAnthropic message
response = model.invoke(f"Describe this JSON payload: {json_str}")
```

### Adding Features

- **Custom metrics**: Add new similarity algorithms in `workflow.py`
- **UI enhancements**: Update `static/index.html` for styling or layout
- **New endpoints**: Add routes in `app.py`

## Notes

- ✅ Payload is **never mutated** — the workflow is read-only
- ✅ All formatting is consistent (2-space JSON indentation)
- ✅ Similarity metrics are word-level (not semantic)
- 🔐 API key is stored locally in `.env` (never committed to repo)

## License

[Add your license here]

## Support

For issues or questions, please open an issue on GitHub or contact the maintainer.
