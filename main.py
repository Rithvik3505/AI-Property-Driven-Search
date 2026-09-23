#version 2: all cases handled, location detection, budget req, 
# import os
# import re
# from docx import Document
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
# from langchain.chat_models import ChatOpenAI

# # === 🔑 Set your OpenAI API key here ===
# os.environ["OPENAI_API_KEY"] = ""  # Replace with your actual key

# # === 📄 Load .docx table and map prompts to responses ===
# def load_prompt_response_table(docx_path):
#     doc = Document(docx_path)
#     prompt_map = {}

#     for table in doc.tables:
#         for row in table.rows[1:]:
#             prompt = row.cells[0].text.strip().lower()
#             response = "\n".join(
#                 para.text.strip() for para in row.cells[1].paragraphs if para.text.strip()
#             )
#             prompt_map[prompt] = response

#     return prompt_map

# # === 🤖 Create OpenAI LLM chatbot with memory ===
# def create_llm_chatbot():
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
#     memory = ConversationBufferMemory()
#     return ConversationChain(llm=llm, memory=memory, verbose=False)

# # === 🧠 Fuzzy matching to known prompt using LLM ===
# def classify_to_prompt(user_input, prompt_map, llm):
#     prompt_text = (
#         "You are an assistant that classifies user input into one of the following known prompts.\n"
#         "Known prompts:\n" +
#         "\n".join(f"- {p}" for p in prompt_map.keys()) +
#         f"\n\nUser input: {user_input}\n\n"
#         "Return ONLY the exact matching prompt from the list, or 'unknown' if it doesn't match.\n"
#         "If the user enters a location such as a city, locality, or pin code, ask for their budget."
#     )

#     try:
#         result = llm.invoke(prompt_text)
#         matched_prompt = result.content.strip().lower()
#         return prompt_map.get(matched_prompt, None)
#     except Exception as e:
#         print("❌ LLM Classification Error:", str(e))
#         return None

# # === 🏙️ Basic city/locality/pincode detector ===
# def is_location_input(text):
#     text = text.strip().lower()

#     # Match 6-digit Indian pincode
#     if re.match(r"^\d{6}$", text):
#         return True

#     # Match common location-like patterns (contains 'nagar', 'layout', 'city', etc.)
#     location_keywords = ["nagar", "layout", "road", "colony", "area", "block", "sector", "town", "village", "locality", "place", "city"]
#     if any(kw in text for kw in location_keywords):
#         return True

#     # Match known cities using a preloaded list
#     known_cities = {"bengaluru", "bangalore", "mumbai", "delhi", "chennai", "hyderabad", "pune", "kolkata", "ahmedabad", "noida", "gurgaon", "mysuru", "nagpur", "kochi", "indore"}
#     for word in text.split():
#         if word in known_cities:
#             return True

#     return False

# def is_budget_input(text):
#     text = text.lower().replace(",", "").replace(" ", "")
#     # Match common ₹ formats: ₹50k, ₹80L, 80000, etc.
#     if re.search(r"(₹)?(\d{2,6})(k|l|lakhs|crore|cr)?", text):
#         return True
#     return False


# # === 💬 Main chatbot loop ===
# def hybrid_chatbot(prompt_map, conversation, llm):
#     print("Type a known prompt, ask anything else, or type 'exit' to quit.\n")

#     while True:
#         user_input = input("\nYou: ").strip()
#         user_input_clean = user_input.lower()

#         if user_input_clean == "exit":
#             print("Bot: Goodbye!")
#             break

#         # Case 1: Exact match
#         response = prompt_map.get(user_input_clean)
#         if response:
#             print("\nBot:\n" + response)
#             continue

#         # 🆕 Case 1.5: If location detected, ask for budget
#         if is_location_input(user_input):
#             print("\nBot: Got it! Could you also share your budget range for this location?")
#             continue

#         # 🆕 Case 1.6: Budget detected → ask about bedroom requirement
#         if is_budget_input(user_input):
#             print("\nBot: How many bedrooms or rooms do you need?")
#             print("1. 1 BHK / 1 Room\n2. 2 BHK\n3. 3 BHK\n4. 4 BHK or more\n5. Open layout / Not applicable")
#             continue



#         # Case 2: Fuzzy match using LLM
#         response = classify_to_prompt(user_input, prompt_map, llm)
#         if response:
#             print("\nBot:\n" + response)
#             continue

#         # Case 3: Default to open chat
#         try:
#             llm_response = conversation.predict(input=user_input)
#             print("\nBot:", llm_response.strip())
#         except Exception as e:
#             print("❌ LLM Chat Error:", str(e))
#             print("Bot: Sorry, something went wrong.")

# # === 🏁 Run the bot ===
# if __name__ == "__main__":
#     docx_path = "prompt_table.docx"
#     prompt_map = load_prompt_response_table(docx_path)
#     conversation = create_llm_chatbot()
#     llm = conversation.llm
#     hybrid_chatbot(prompt_map, conversation, llm)


#version 2: all cases handled, full tree covered, not polished yet
import os
import re
from docx import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "" # Company key

# Case 1 - 2
def load_prompt_response_table(docx_path):
    doc = Document(docx_path)
    prompt_map = {}

    for table in doc.tables:
        for row in table.rows[1:]:
            prompt = row.cells[0].text.strip().lower()
            response = "\n".join(
                para.text.strip() for para in row.cells[1].paragraphs if para.text.strip()
            )
            prompt_map[prompt] = response

    return prompt_map

# Case 3
def create_llm_chatbot():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    memory = ConversationBufferMemory()
    return ConversationChain(llm=llm, memory=memory, verbose=False)

# Case 2
def classify_to_prompt(user_input, prompt_map, llm):
    prompt_text = (
        "You are an assistant that classifies user input into one of the following known prompts.\n"
        "Known prompts:\n" +
        "\n".join(f"- {p}" for p in prompt_map.keys()) +
        f"\n\nUser input: {user_input}\n\n"
        "Return ONLY the exact matching prompt from the list, or 'unknown' if it doesn't match.\n"
        "If the user enters a location such as a city, locality, or pin code, ask for their budget."
    )

    try:
        result = llm.invoke(prompt_text)
        matched_prompt = result.content.strip().lower()
        return prompt_map.get(matched_prompt, None)
    except Exception as e:
        print("❌ LLM Classification Error:", str(e))
        return None

def is_location_input(text):
    text = text.strip().lower()

    if re.match(r"^\d{6}$", text):      # Pin code 
        return True

    location_keywords = ["nagar", "layout", "road", "colony", "area", "block", "sector", "town", "village", "locality", "place", "city"]
    if any(kw in text for kw in location_keywords):
        return True

    known_cities = {"bengaluru", "bangalore", "mumbai", "delhi", "chennai", "hyderabad", "pune", "kolkata", "ahmedabad", "noida", "gurgaon", "mysuru", "nagpur", "kochi", "indore"}
    for word in text.split():
        if word in known_cities:
            return True

    return False

def is_budget_input(text):
    text = text.lower().replace(",", "").strip()

    if any(unit in text for unit in ["sqft", "sq ft", "sqm", "m2", "square", "meter"]):
        return False

    if re.search(r"(₹)?\s?\d{2,7}\s?(k|l|cr|lakhs|crore)?", text):
        return True

    return False

def is_square_footage_input(text):
    text = text.lower().replace(" ", "").strip()

    return bool(re.match(r"^\d{2,5}(sqft|sq\.ft|sqft\.|sqm|m2|m²)$", text))

def hybrid_chatbot(prompt_map, conversation, llm):
    print("Type a known prompt, ask anything else, or type 'exit' to quit.\n")

    while True:
        user_input = input("\nYou: ").strip()
        user_input_clean = user_input.lower()

        if user_input_clean == "exit":
            print("Bot: Goodbye!")
            break

        # Case 1: Exact match
        response = prompt_map.get(user_input_clean)
        if response:
            print("\nBot:\n" + response)
            continue

        # Case 1.1: If location detected, ask for budget
        if is_location_input(user_input):
            print("\nBot: Got it! Could you also share your budget range for this location?")
            continue

        # Case 1.2: If budget detected, ask about bedroom requirement
        if is_budget_input(user_input):
            print("\nBot: How many bedrooms or rooms do you need?")
            print("1. 1 BHK / 1 Room\n2. 2 BHK\n3. 3 BHK\n4. 4 BHK or more\n5. Open layout / Not applicable")
            continue

        # Case 1.3: If square footage, ask about furnishing preference
        if is_square_footage_input(user_input):
            print("\nBot: Do you prefer the property to be:")
            print("1. Fully Furnished\n2. Semi-Furnished\n3. Unfurnished\n4. No preference")
            continue

        # Case 2: prompt has typo match, use LLM to classify
        response = classify_to_prompt(user_input, prompt_map, llm)
        if response:
            print("\nBot:\n" + response)
            continue

        # Case 3: On random input, default to normal chat
        try:
            llm_response = conversation.predict(input=user_input)
            print("\nBot:", llm_response.strip())
        except Exception as e:
            print("❌ LLM Chat Error:", str(e))
            print("Bot: Sorry, something went wrong.")

if __name__ == "__main__":
    docx_path = "prompt_table.docx"
    prompt_map = load_prompt_response_table(docx_path)
    conversation = create_llm_chatbot()
    llm = conversation.llm
    hybrid_chatbot(prompt_map, conversation, llm)
