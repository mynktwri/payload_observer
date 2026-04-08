#!/usr/bin/env python3

import json
import os
import sys

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory

from workflow import create_observer_graph


def main():
    # Load environment variables
    load_dotenv()

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set in .env file", file=sys.stderr)
        sys.exit(1)

    # Create Flask app
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    # Get model ID from env or use default
    model_id = os.getenv("MODEL_ID", "claude-haiku-4-5-20251001")

    # Create workflow graph once
    graph = create_observer_graph(model_id=model_id)

    @app.route("/")
    def index():
        return send_from_directory("static", "index.html")

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        try:
            data = request.get_json()
            payload = data.get("payload")
            original_input = data.get("original_input", "")

            if payload is None:
                return jsonify({"error": "Missing payload"}), 400

            # Run workflow
            result = graph.invoke({"payload": payload, "original_input": original_input, "description": ""})

            return jsonify({
                "payload": result["payload"],
                "description": result["description"],
                "similarity": round(result.get("similarity", 0.0), 2),
                "intersection": result.get("intersection", 0),
                "union": result.get("union", 0),
            })
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Invalid JSON: {e}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Run Flask server
    port = 8000
    print(f"Starting Payload Observer at http://localhost:{port}")
    app.run(debug=True, port=port)


if __name__ == "__main__":
    main()
