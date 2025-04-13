"""
Example usage of the Model Control Protocol (MCP)

This script demonstrates how to use the MCP system to enable communication
between different language models (Claude, Gemini 2.5 Pro, and ChatGPT).
"""

from mcp_implementation import ModelControlProtocol

def simulate_model_interaction():
    """Simulate a complete interaction between models"""
    # Initialize the MCP
    mcp = ModelControlProtocol("example_session.db")
    
    # Start with a user query
    initial_query = "Compare the approaches to solving climate change"
    print(f"\n[User] Initial query: {initial_query}")
    print("\n=== Starting Model Conversation ===")
    
    # First turn - Claude processes the initial query
    print("\n--- Turn 1 ---")
    responses = mcp.execute_turn(initial_query)
    
    # Second turn - models continue the conversation
    print("\n--- Turn 2 ---")
    responses = mcp.execute_turn()
    
    # Third turn - final responses
    print("\n--- Turn 3 ---")
    responses = mcp.execute_turn()
    
    # Show the message history
    messages = mcp.get_all_messages()
    
    print("\n=== Complete Message History ===")
    for msg in messages:
        msg_id, sender, receiver, content, timestamp = msg
        print(f"[{timestamp}] {sender} → {receiver}: {content}")


if __name__ == "__main__":
    simulate_model_interaction()
    
    # Alternatively, to use the interactive command-line interface:
    # from mcp_implementation import main
    # main()
