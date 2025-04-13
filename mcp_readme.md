# Model Control Protocol (MCP)

A simple framework that allows multiple models (Claude, Gemini 2.5 Pro, and ChatGPT) to interact, share data, and collaborate using Python and SQLite.

## Overview

This implementation provides a basic system for message passing between language models. The key features include:

1. **Message Passing Between Models**: Models can send and receive messages to each other.
2. **Shared Data Management via SQLite**: All interactions and data shared between models are tracked.
3. **Model Coordination (Sequential Execution)**: Models work in sequence to avoid running in parallel.
4. **Simple Interface for Interactions**: A command-line interface to control and initiate communication.
5. **Data Integrity (Basic Data Logging)**: All messages get stored in the SQLite database for tracking.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- SQLite3 (included in Python standard library)

### Installation

1. Clone or download the repository
2. No additional dependencies are required

### Running the Program

You can run the program directly from the command line:

```bash
python mcp_implementation.py
```

This will start the command-line interface, allowing you to control model interactions.

## Usage

The command-line interface provides the following options:

1. **Start a new conversation**: Begin a new interaction sequence with an initial message
2. **Continue existing conversation**: Continue an ongoing conversation with another turn
3. **View message history**: See all past messages exchanged between models
4. **Clear database**: Reset the database to start fresh
5. **Exit**: Quit the program

## How It Works

1. The system initializes a SQLite database to store all messages and interactions
2. Models take turns sending and receiving messages in a predetermined sequence
3. Each message is stored in the database with metadata about the sender and receiver
4. In this demonstration, we simulate model responses, but in a real implementation, this would connect to actual API endpoints

## Example Usage

See the `mcp_example_usage.py` file for a demonstration of how to use the MCP system programmatically.

## Database Schema

The SQLite database consists of two main tables:

1. **messages**: Stores message content with metadata
   - `id`: Unique message identifier
   - `model_id`: The model that sent the message
   - `message_type`: Type of message (e.g., "text")
   - `message_content`: The actual message content
   - `timestamp`: When the message was sent

2. **model_interactions**: Tracks the sequence of interactions
   - `interaction_id`: Unique interaction identifier
   - `model1_id`: The sender model
   - `model2_id`: The receiver model
   - `message_id`: Reference to the message sent
   - `timestamp`: When the interaction occurred

## Extending the System

To extend this basic implementation:

1. Replace the simulated model responses with actual API calls to language models
2. Add more sophisticated message processing logic
3. Implement a web interface instead of a command-line interface
4. Add support for parallel processing or more complex interaction patterns
5. Enhance the database schema to store additional metadata

## Limitations

This is a simplified implementation meant for demonstration purposes:

- No actual API integration with language models
- Basic error handling
- No authentication or security features
- Limited to sequential processing only
