import sqlite3
import datetime
import time
import os

class ModelControlProtocol:
    def __init__(self, db_path="mcp_database.db"):
        """
        Initialize the Model Control Protocol with a SQLite database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.models = ['Claude', 'Gemini', 'ChatGPT']
        self.current_model_index = 0
        self.setup_database()
    
    def setup_database(self):
        """Create the necessary tables in the SQLite database if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id TEXT NOT NULL,
            message_type TEXT NOT NULL,
            message_content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create model_interactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model1_id TEXT NOT NULL,
            model2_id TEXT NOT NULL,
            message_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"Database initialized at {self.db_path}")
    
    def send_message(self, sender_model, receiver_model, message_content, message_type="text"):
        """
        Send a message from one model to another and store it in the database.
        
        Args:
            sender_model: The model sending the message
            receiver_model: The model receiving the message
            message_content: The content of the message
            message_type: The type of message (default: "text")
            
        Returns:
            message_id: The ID of the stored message
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Store the message
        cursor.execute('''
        INSERT INTO messages (model_id, message_type, message_content)
        VALUES (?, ?, ?)
        ''', (sender_model, message_type, message_content))
        
        message_id = cursor.lastrowid
        
        # Store the interaction
        cursor.execute('''
        INSERT INTO model_interactions (model1_id, model2_id, message_id)
        VALUES (?, ?, ?)
        ''', (sender_model, receiver_model, message_id))
        
        conn.commit()
        conn.close()
        
        print(f"Message sent from {sender_model} to {receiver_model}: {message_content[:50]}...")
        return message_id
    
    def receive_message(self, model_id, message_id=None):
        """
        Retrieve a message for a model from the database.
        
        Args:
            model_id: The model receiving the message
            message_id: Optional specific message ID to retrieve
            
        Returns:
            message: The retrieved message content or None if no message
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if message_id:
            # Retrieve a specific message
            cursor.execute('''
            SELECT m.message_content, m.model_id
            FROM messages m
            JOIN model_interactions mi ON m.id = mi.message_id
            WHERE mi.message_id = ? AND mi.model2_id = ?
            ''', (message_id, model_id))
        else:
            # Retrieve the latest message for this model
            cursor.execute('''
            SELECT m.message_content, m.model_id
            FROM messages m
            JOIN model_interactions mi ON m.id = mi.message_id
            WHERE mi.model2_id = ?
            ORDER BY m.timestamp DESC
            LIMIT 1
            ''', (model_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"{model_id} received message from {result[1]}: {result[0][:50]}...")
            return result[0]
        else:
            print(f"No messages found for {model_id}")
            return None
    
    def execute_turn(self, initial_message=None):
        """
        Execute a turn in the sequence, where each model passes a message to the next.
        
        Args:
            initial_message: Optional starting message for the first model
            
        Returns:
            responses: A list of all model responses in this turn
        """
        responses = []
        current_message = initial_message
        
        # Go through each model in sequence
        for i in range(len(self.models)):
            sender_model = self.models[i]
            receiver_model = self.models[(i + 1) % len(self.models)]
            
            # If this is the first model and an initial message was provided
            if i == 0 and initial_message:
                response = f"INITIAL: {initial_message}"
            else:
                # Process the received message (in a real system, this would call the actual model API)
                received = self.receive_message(sender_model)
                if received:
                    response = f"RESPONSE from {sender_model}: I received '{received}' and my response is..."
                else:
                    response = f"RESPONSE from {sender_model}: No prior message received, starting conversation..."
            
            # Send the processed message to the next model
            self.send_message(sender_model, receiver_model, response)
            responses.append(response)
            
            # In a real system, we might want to pause to simulate API call time
            time.sleep(0.5)
        
        return responses
    
    def get_all_messages(self):
        """Retrieve all messages from the database for display."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT m.id, m.model_id, mi.model2_id, m.message_content, m.timestamp
        FROM messages m
        JOIN model_interactions mi ON m.id = mi.message_id
        ORDER BY m.timestamp ASC
        ''')
        
        messages = cursor.fetchall()
        conn.close()
        
        return messages


def main():
    """Main function to run the command line interface for the MCP."""
    mcp = ModelControlProtocol()
    
    print("\n=== Model Control Protocol (MCP) Command Line Interface ===")
    print("This tool allows models to communicate and collaborate in sequence.")
    
    while True:
        print("\nOptions:")
        print("1. Start a new conversation")
        print("2. Continue existing conversation")
        print("3. View message history")
        print("4. Clear database")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            initial_message = input("Enter an initial message to start the conversation: ")
            print("\nStarting conversation...")
            responses = mcp.execute_turn(initial_message)
            print("\nResponses from this turn:")
            for i, response in enumerate(responses):
                print(f"{mcp.models[i]}: {response}")
        
        elif choice == '2':
            print("\nContinuing conversation...")
            responses = mcp.execute_turn()
            print("\nResponses from this turn:")
            for i, response in enumerate(responses):
                print(f"{mcp.models[i]}: {response}")
        
        elif choice == '3':
            messages = mcp.get_all_messages()
            if not messages:
                print("\nNo messages found in the database.")
            else:
                print("\n=== Message History ===")
                for msg in messages:
                    msg_id, sender, receiver, content, timestamp = msg
                    print(f"[{timestamp}] {sender} -> {receiver}: {content[:50]}...")
        
        elif choice == '4':
            confirm = input("Are you sure you want to clear the database? (y/n): ")
            if confirm.lower() == 'y':
                try:
                    os.remove(mcp.db_path)
                    print(f"Database {mcp.db_path} has been deleted.")
                    mcp.setup_database()
                except FileNotFoundError:
                    print("Database file doesn't exist yet.")
        
        elif choice == '5':
            print("Exiting MCP. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
