# from flask import Flask, request, Response
# from twilio.twiml.messaging_response import MessagingResponse
# import main  # This is your chatbot logic

# app = Flask(__name__)

# # Load prompt table and LLM once at startup
# prompt_map = main.load_prompt_response_table("prompt_table.docx")
# conversation = main.create_llm_chatbot()
# llm = conversation.llm

# # Reset state for every new session (optional: improve later for memory)
# def reset_state():
#     main.user_state = {
#         "intent": "buyer",
#         "user_type": None,
#         "looking_to": None,
#         "property_type": None,
#         "sub_type": None,
#         "location": None,
#         "budget": None,
#         "bhk": None,
#         "sqft": None,
#         "furnishing": None,
#         "timeline": None,
#         "current_question": "user_type"
#     }

# @app.route("/whatsapp", methods=["POST"])
# def whatsapp_reply():
#     incoming_msg = request.form.get("Body", "").strip()
#     resp = MessagingResponse()
#     msg = resp.message()

#     # If message is 'reset', start over
#     if incoming_msg.lower() == "reset":
#         reset_state()
#         msg.body("🔄 Chatbot has been reset. Let's start again.")
#         main.ask_question(main.user_state["current_question"], prompt_map)
#         return str(resp)

#     # Simulate one step of hybrid_chatbot
#     q_key = main.user_state["current_question"]
#     user_input = incoming_msg

#     if q_key == "location" and main.is_location_input(user_input):
#         main.user_state[q_key] = user_input

#     elif q_key == "sub_type":
#         property_type = main.user_state.get("property_type", "").lower()
#         if property_type in prompt_map:
#             sub_prompt = prompt_map[property_type]
#             matched = main.match_partial_response(sub_prompt, user_input)
#             main.user_state[q_key] = matched or user_input
#         else:
#             main.user_state[q_key] = user_input

#     elif q_key in ["bhk", "furnishing"]:
#         matched = main.match_partial_response(main.question_prompts[q_key], user_input)
#         main.user_state[q_key] = matched or user_input

#     else:
#         prompt_label = main.question_prompts.get(q_key, "")
#         matched_prompt = main.match_partial_response(prompt_map.get(prompt_label, ""), user_input)
#         main.user_state[q_key] = matched_prompt or user_input

#     next_q = main.get_next_question_key()
#     main.user_state["current_question"] = next_q

#     if next_q:
#         import io
#         from contextlib import redirect_stdout
#         buffer = io.StringIO()
#         with redirect_stdout(buffer):
#             main.ask_question(next_q, prompt_map)
#         bot_reply = buffer.getvalue().strip()
#         msg.body(bot_reply)
#     else:
#         summary = "\n".join(f"- {k.replace('_', ' ').title()}: {v}" for k, v in main.user_state.items() if k != "current_question")
#         msg.body("Thanks! Here's a summary of what you've shared so far:\n" + summary + "\n\nWould you like to proceed to view matching listings or speak with an agent?")

#     return str(resp)

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)  




from fastapi import FastAPI, Request
from pydantic import BaseModel
from main import (
    load_prompt_response_table,
    create_llm_chatbot,
    is_location_input,
    is_budget_input,
    is_square_footage_input,
    classify_to_prompt
)
import uvicorn

app = FastAPI()

# Load once at startup
prompt_map = load_prompt_response_table("prompt_table.docx")

class MessageRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: MessageRequest):
    user_input = req.message.strip()
    
    # Create a fresh LLM instance for stateless call
    conversation = create_llm_chatbot()
    llm = conversation.llm

    # Case 1: Exact match
    if user_input.lower() in prompt_map:
        return { "response": prompt_map[user_input.lower()] }

    # Case 1.1: Location
    if is_location_input(user_input):
        return { "response": "Got it! Could you also share your budget range for this location?" }

    # Case 1.2: Budget
    if is_budget_input(user_input):
        return { "response": "How many bedrooms or rooms do you need?\n1. 1 BHK / 1 Room\n2. 2 BHK\n3. 3 BHK\n4. 4 BHK or more\n5. Open layout / Not applicable" }

    # Case 1.3: Square footage
    if is_square_footage_input(user_input):
        return { "response": "Do you prefer the property to be:\n1. Fully Furnished\n2. Semi-Furnished\n3. Unfurnished\n4. No preference" }

    # Case 2: LLM classification
    classified = classify_to_prompt(user_input, prompt_map, llm)
    if classified:
        return { "response": classified }

    # Case 3: Fallback to chat
    try:
        llm_response = conversation.predict(input=user_input)
        return { "response": llm_response.strip() }
    except Exception as e:
        return { "response": "Bot: Sorry, something went wrong.", "error": str(e) }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
