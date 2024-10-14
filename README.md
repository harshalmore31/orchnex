# Orchnex AI (Experimental)

**Revolutionizing Generative AI Through Orchestrated Multi-Agent Collaboration**

> **[WARNING]**
> Orchnex AI is currently an experimental project exploring the power of multi-agent systems in generative AI. It is not intended for production use and therefore has no official support at this time. 

**Project Goals:**

* Develop a multi-model LLM architecture with specialized AI agents for enhanced accuracy, relevance, and user experience.
* Implement an iterative feedback loop between agents to refine and optimize outputs.
* Demonstrate the effectiveness of this approach across various domains and use cases.

## Getting Started

**Prerequisites:**

* Python 3.8+
* OpenAI API key
* Google Generative AI API key

**Installation:**

```bash
pip install openai google-generativeai
```

## Usage Example

The package isn't ready yet, consider it as an example of our project

Here is an Example:
[Multi-Model using Meta3.1:8b and Gemini1.5pro-exp](./meta_x_Gemini.py)

## Architecture

![Orchnex AI Architecture](./assets/Architecture.jpg) (Include a diagram if available)

Orchnex AI employs a unique three-agent architecture:

* **LLM-UI (User Interface Agent):** Receives the initial user input, interprets intent, and translates it into a structured prompt optimized for a specific domain expert. 
* **LLM-Expert (Domain Expert Agent):** Possesses specialized knowledge in a particular domain (e.g., medicine, law, technology) and generates an initial response based on the LLM-UI's prompt.
* **LLM-Verifier (Verification and Refinement Agent):**  Analyzes the initial response using chain-of-thought reasoning and self-prompting, ensuring accuracy and alignment with user expectations. It provides iterative feedback to LLM-Expert to refine the output.

## Iterative Refinement

A key feature of Orchnex AI is its iterative feedback loop. LLM-Verifier critically assesses LLM-Expert's response and provides specific, actionable feedback for improvement. LLM-Expert incorporates this feedback to generate a refined response, and the loop continues until a satisfactory output is achieved.

## Potential Applications

Orchnex AI's multi-agent architecture holds promise for a wide range of applications, including:

* Personalized Education
* Content Creation 
* Customer Service
* Scientific Research 
* And more...

## Contributing

Orchnex AI is currently an experimental project. We are not accepting contributions at this time, but we appreciate your interest! 

## Future Work

* Implement a unified API endpoint with single API key access for greater usability.
* Expand the range of supported domain experts and refine the iterative feedback mechanisms.
* Explore new applications and evaluate Orchnex AI's performance on various benchmarks.

## Core Contributors 

* Harshal More 

## License
