# How to make a Multi-Model AI

import openai
import google.generativeai as genai
# you can import other AI also..

# Initalize specific LLM's and their config, below is the OpenAI example, which is LLM-1

# Initialize OpenAI Client (for Llama 2)
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="nvapi-lc_Mxxxxxxxxxxxxxxxxxxxxxxxxxxx30xX"
)

# Initialize Google Generative AI (for Gemini)
genai.configure(api_key="AIxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7s")
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Same intialize LLM-2


