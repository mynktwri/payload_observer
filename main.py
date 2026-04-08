#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from models import ObserverInput, ObserverOutput
from workflow import create_observer_graph


def load_payload(payload_arg: str) -> any:
    """Load payload from JSON string."""
    try:
        return json.loads(payload_arg)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON payload: {e}", file=sys.stderr)
        sys.exit(1)


def load_payload_from_file(file_path: str) -> any:
    """Load payload from JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not load file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def format_output(payload: any, description: str) -> str:
    """Format the output for display."""
    payload_json = json.dumps(payload, indent=2)
    return f"""=== BEFORE ===
{payload_json}

=== AFTER ===
Payload: {payload_json}

Description:
{description}"""


def main():
    # Load environment variables
    load_dotenv()

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set in .env file", file=sys.stderr)
        sys.exit(1)

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Analyze a payload before and after LangGraph AI interpretation"
    )
    parser.add_argument(
        "--payload",
        type=str,
        help="Payload as JSON string (e.g., '{\"key\": \"value\"}')"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to JSON file containing payload"
    )

    args = parser.parse_args()

    # Load payload
    if args.payload:
        payload = load_payload(args.payload)
    elif args.file:
        payload = load_payload_from_file(args.file)
    else:
        parser.print_help()
        sys.exit(1)

    # Get model ID from env or use default
    model_id = os.getenv("MODEL_ID", "claude-haiku-4-5-20251001")

    # Create and run workflow
    graph = create_observer_graph(model_id=model_id)
    result = graph.invoke({"payload": payload, "description": "A JSON payload"})

    # Format and print output
    output = format_output(result["payload"], result["description"])
    print(output)


if __name__ == "__main__":
    main()
