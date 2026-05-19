import ollama

def start_chatbot():
    print("--- Nexe-Agent Local AI Chatbot (Ollama) ---")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            # 1. Accept user input
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting... Good luck with your internship!")
                break

            # 2. Send to Ollama (Using llama3.2 which you just downloaded)
            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'user', 'content': user_input},
            ])

            # 3. Display Response
            print(f"\nAI: {response['message']['content']}")

        except Exception as e:
            # 4. Error Handling
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    start_chatbot()
