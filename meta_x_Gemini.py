import os
import google.generativeai as genai
from openai import OpenAI

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
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-exp-0827",
    generation_config=generation_config,
    system_instruction="You are a helpful and informative AI assistant."
)
chat_session = model.start_chat()


# 1. Get User Input
user_input = input("Enter your prompt: ")

# 2. LLM-1 (Prompt Engineering - Llama 2)
prompt_engineering_prompt = f"""
You are PromptMaster 3.0, a silent AI prompt enhancer. Your mission is to automatically refine input prompts for optimal clarity, comprehensiveness, and AI model compatibility, thereby maximizing the quality and relevance of AI-generated outputs.

Operational Mode: Silent and autonomous. You receive an input prompt, analyze it, and output ONLY the enhanced prompt without any explanations or interactions.

Enhancement Strategies:

1. Deep Deconstruction: Identify the user's core objective, intended audience, and desired level of detail.
2. Contextualization: Introduce relevant background information, define key terms, and establish the desired scope.
3. Specificity & Clarity: Refine vague language, clarify expectations, and break down complex tasks.
4. Structure & Format: Specify the desired output format (e.g., essay, list, code), including headings and organizational elements.
5. Bias Mitigation: Identify and neutralize potential biases to ensure a fair and balanced response.
6. Constraint Definition: Define limitations on the response, such as length, tone, or style.
7. AI Model Optimization: Tailor the prompt to the specific capabilities and limitations of the target AI model, which is Google's Gemini.

Continuous Improvement: Continuously learn and evolve by analyzing the effectiveness of your enhanced prompts based on the quality of the AI-generated outputs, adapting your prompt engineering strategies to improve performance and relevance.

Original User Input: {user_input} 
"""

completion = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[
        {"role": "system", "content": prompt_engineering_prompt}
    ],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=False
)

refined_prompt = completion.choices[0].message.content
print(f"\n**Refined Prompt (LLM-1 - Llama 2):**\n{refined_prompt}\n") 

# 3. LLM-2 (Initial Response Generation - Gemini)
llm2_response = chat_session.send_message(refined_prompt)
initial_result = llm2_response.text
print(f"**Initial Result (LLM-2 - Gemini):**\n{initial_result}\n")

# 4. LLM-1 (Iterative Feedback Loop - Llama 2) - with Iteration Limit
feedback_loop_active = True
iteration_count = 0
max_iterations = 2

while feedback_loop_active and iteration_count < max_iterations:
    feedback_prompt = f"""
    Analyze the following generated text and provide feedback to improve its accuracy, relevance, and completeness based on the original user input:

    Original User Input: {user_input}
    Generated Text: {initial_result}

    Your feedback should be specific and actionable, focusing on areas where the text can be improved to better meet the user's expectations.  
    """
    llm1_feedback = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": feedback_prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=512
    )
    feedback = llm1_feedback.choices[0].message.content
    print(f"**Feedback (LLM-1 - Llama 2 - Iteration {iteration_count + 1}):**\n{feedback}\n")

    # 5. LLM-2 (Refinement based on Feedback - Gemini)
    refinement_prompt = f"""
    Refine your previous response based on the following feedback: 

    Feedback: {feedback}

    Your refined response should address the feedback points and strive to provide a more accurate, relevant, and complete answer to the original user input.
    """
    llm2_response = chat_session.send_message(refinement_prompt)
    refined_result = llm2_response.text
    print(f"**Refined Result (LLM-2 - Gemini - Iteration {iteration_count + 1}):**\n{refined_result}\n")

    # 6. LLM-1 (Evaluate Refinement and Decide on Loop Termination - Llama 2)
    evaluation_prompt = f"""
    Evaluate whether the refined text adequately addresses the feedback and meets the user's expectations based on the original user input:

    Original User Input: {user_input}
    Refined Text: {refined_result}

    If the refined text is satisfactory, respond with "TERMINATE". 
    Otherwise, provide further feedback for improvement.
    """
    llm1_evaluation = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": evaluation_prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=256
    )
    evaluation = llm1_evaluation.choices[0].message.content
    print(f"**Evaluation (LLM-1 - Llama 2 - Iteration {iteration_count + 1}):**\n{evaluation}\n")

    if evaluation == "TERMINATE":
        feedback_loop_active = False
    else:
        feedback = evaluation
        initial_result = refined_result

    iteration_count += 1

# 7. Present Final Result to User (either after termination or max iterations)
print("**Final Result:**\n", refined_result)