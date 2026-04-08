import json
from typing import Any

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph
from typing_extensions import TypedDict


class ObserverState(TypedDict):
    """State for the payload observer workflow."""
    payload: Any
    original_input: str
    description: str
    similarity: float
    intersection: int
    union: int


def create_observer_graph(model_id: str = "claude-haiku-4-5-20251001"):
    """Create and compile the payload observer LangGraph workflow."""

    def interpret_payload(state: ObserverState) -> ObserverState:
        """Read-only node: interpret payload and generate description."""
        payload = state["payload"]
        original_input = state["original_input"]

        # Serialize payload to JSON for analysis
        payload_json = json.dumps(payload, indent=2)

        # Create the prompt
        prompt = f"""Analyze the following payload and provide a one sentence description of what it represents.

Payload:
{payload_json}

Provide a clear, natural language description 1 sentence"""

        # Call Anthropic model
        model = ChatAnthropic(model=model_id)
        response = model.invoke(prompt)

        # Extract text from response
        description = response.content

        # Calculate similarity between original input and serialized payload
        similarity, intersection, union = calculate_string_similarity(original_input, payload_json)

        return {
            "payload": payload,  # Read-only: unchanged
            "original_input": original_input,
            "description": description,
            "similarity": similarity,
            "intersection": intersection,
            "union": union,
        }

    def calculate_string_similarity(str1: str, str2: str) -> tuple:
        """Calculate simple similarity metric between two strings.
        Returns (similarity_score, intersection_count, union_count)
        """
        # Normalize strings
        s1 = str1.lower().split()
        s2 = str2.lower().split()

        # Calculate Jaccard similarity
        set1 = set(s1)
        set2 = set(s2)

        if not set1 and not set2:
            return (1.0, 0, 0)

        intersection = len(set1 & set2)
        union = len(set1 | set2)
        similarity = intersection / union if union > 0 else 0.0

        return (similarity, intersection, union)

    # Build the graph
    graph = StateGraph(ObserverState)
    graph.add_node("interpret", interpret_payload)
    graph.add_edge("__start__", "interpret")
    graph.add_edge("interpret", "__end__")

    return graph.compile()
