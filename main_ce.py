# VERSION 2: CASE 1 AND 2 HANDLED
# import os
# from docx import Document
# from langchain_cohere import ChatCohere

# # === 🔑 SET YOUR COHERE API KEY HERE ===
# os.environ["COHERE_API_KEY"] = "Cohere API key"

# # Load docx prompt-response table
# def load_prompt_response_table(docx_path):
#     doc = Document(docx_path)
#     prompt_map = {}

#     for table in doc.tables:
#         for row in table.rows[1:]:
#             prompt = row.cells[0].text.strip()
#             response = row.cells[1].text.strip()
#             prompt_map[prompt.lower()] = response

#     return prompt_map

# # Initialize Cohere LLM via LangChain
# llm = ChatCohere(model="command-r", temperature=0.3)

# # Use Cohere to infer closest matching prompt
# def llm_match_prompt(user_input, prompt_map):
#     prompt_text = (
#         "You are an assistant that matches user prompts to known prompt options. "
#         "Here are the known prompts:\n\n"
#         + "\n".join(f"- {p}" for p in prompt_map.keys())
#         + f"\n\nUser input: {user_input}\n\n"
#         "Return exactly one of the known prompt strings that best matches the user's intent. "
#         "If no match is found, respond with 'unknown'."
#     )

#     try:
#         matched_prompt = llm.invoke(prompt_text).content.strip().lower()
#         return prompt_map.get(matched_prompt, "Sorry, I don’t understand that prompt yet.")
#     except Exception as e:
#         print("🔴 LLM Error:", str(e))
#         return "Sorry, the LLM couldn't be reached. Please try again later."

# # Chatbot loop
# def chatbot(prompt_map):
#     print("📢 Chatbot (Cohere) is live. Type your prompt or 'exit' to quit.\n")
#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() == 'exit':
#             print("Bot: Goodbye!")
#             break

#         response = prompt_map.get(user_input.lower())
#         if response:
#             print("Bot:", response)
#         else:
#             response = llm_match_prompt(user_input, prompt_map)
#             print("Bot:", response)

# if __name__ == "__main__":
#     path = "prompt_table.docx"
#     prompts = load_prompt_response_table(path)
#     chatbot(prompts)


#VERSION 3: ALL 3 CASES HANDLED
import os
from docx import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_cohere import ChatCohere

# === 🔑 SET YOUR COHERE API KEY HERE ===
os.environ["COHERE_API_KEY"] = "Cohere API Key"  # Replace with your actual Cohere key

# === 🔍 Load prompt-response table from the Word document ===
def load_prompt_response_table(docx_path):
    doc = Document(docx_path)
    prompt_map = {}

    for table in doc.tables:
        for row in table.rows[1:]:  # Skip header row
            prompt = row.cells[0].text.strip()
            response = row.cells[1].text.strip()
            prompt_map[prompt.lower()] = response

    return prompt_map

# === 💬 Create LLM-powered conversational chatbot (Cohere) ===
def create_llm_chatbot():
    llm = ChatCohere(model="command-r", temperature=0.5)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    return conversation

# === 🧠 Main hybrid chatbot loop ===
def hybrid_chatbot(prompt_map, conversation):
    print("\n🤖 Chatbot (Cohere) is live!")
    print("Type a known prompt, ask anything else, or type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        # Step 1: Try exact match in docx prompt map
        response = prompt_map.get(user_input.lower())
        if response:
            print("Bot:", response)
        else:
            # Step 2: Let the Cohere LLM generate a natural response
            try:
                llm_response = conversation.predict(input=user_input)
                print("Bot:", llm_response.strip())
            except Exception as e:
                print("❌ LLM Error:", str(e))
                print("Bot: Sorry, something went wrong with the chatbot.")

# === 🔁 Entry point ===
if __name__ == "__main__":
    docx_path = "prompt_table.docx"  # Make sure this file is in your folder
    prompt_map = load_prompt_response_table(docx_path)
    conversation = create_llm_chatbot()
    hybrid_chatbot(prompt_map, conversation)
