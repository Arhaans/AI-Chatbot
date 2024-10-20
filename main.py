from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

app = FastAPI()

# Allow CORS for all domains for now (you can restrict it later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the template
template = """
Answer the question below
Here is the conversation history: {context}
Question: {question}

Answer:
"""

# Set up the model and prompt
model = OllamaLLM(model="llama2")
prompt = ChatPromptTemplate.from_template(template)

# Store the conversation context globally
conversation_context = ""

# Pydantic model for request body validation
class UserInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(user_input: UserInput):
    global conversation_context

    user_message = user_input.message

    # Format the prompt with the conversation context and the user's question
    formatted_prompt = prompt.format(context=conversation_context, question=user_message)

    # Get the result from the model
    bot_response = model.invoke(formatted_prompt)

    # Update the conversation context with the new interaction
    conversation_context += f"\nUser: {user_message}\nAI: {bot_response}"

    # Return the bot's response
    return {"reply": bot_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
