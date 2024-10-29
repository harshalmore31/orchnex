# src/orchnex/orchestrator.py
from typing import Dict
from .config import LLMConfig
from .templates import PromptTemplates
from .providers.base import LLMProvider
from .providers.llama_provider import LlamaProvider
from .providers.gemini_provider import GeminiProvider

class MultiLLMOrchestrator:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.templates = PromptTemplates()
        self.providers: Dict[str, LLMProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all LLM providers"""
        try:
            # Initialize Llama provider
            llama_provider = LlamaProvider()
            llama_provider.initialize(
                api_key=self.config.nvidia_api_key,
                model_name=self.config.llama_model
            )
            self.providers['llama'] = llama_provider

            # Initialize Gemini provider
            gemini_provider = GeminiProvider()
            gemini_provider.initialize(
                api_key=self.config.gemini_api_key,
                model_name=self.config.gemini_model,
                generation_config={
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "max_output_tokens": self.config.max_tokens
                },
                system_instruction=self.templates.get_phoenix_instructions()
            )
            self.providers['gemini'] = gemini_provider
            
        except Exception as e:
            raise RuntimeError(f"Error initializing providers: {str(e)}")

    def enhance_prompt_with_promptmaster(self, input_prompt: str) -> str:
        """Use PromptMaster 3.0 to enhance the input prompt"""
        template = self.templates.get_promptmaster_template()
        
        enhancement_prompt = template.format(
            input_prompt=input_prompt,
            core_objective="Identify user's main goal and requirements",
            context="Add relevant background and scope",
            clarity="Improve precision and break down complex elements",
            format="Specify desired output structure",
            bias="Ensure neutral language",
            constraints="Define response parameters",
            optimization="Adapt for Gemini's capabilities"
        )
        
        return self.providers['llama'].generate_response(
            enhancement_prompt, 
            temperature=0.2
        )

    def process_input(self, user_input: str, verbose: bool = False) -> str:
        """Process user input through the multi-LLM pipeline"""
        try:
            # 1. Enhance prompt
            enhanced_prompt = self.enhance_prompt_with_promptmaster(user_input)
            if verbose:
                print(f"\nEnhanced Prompt:\n{enhanced_prompt}\n")

            # 2. Generate initial response
            initial_result = self.providers['gemini'].generate_response(enhanced_prompt)
            if verbose:
                print(f"Initial Result:\n{initial_result}\n")

            current_result = initial_result
            
            # 3. Iterative feedback loop
            for iteration in range(self.config.max_iterations):
                # Get feedback using template
                feedback_prompt = self.templates.get_feedback_template().format(
                    user_input=user_input,
                    enhanced_prompt=enhanced_prompt,
                    current_result=current_result
                )
                
                feedback = self.providers['llama'].generate_response(feedback_prompt)
                
                if verbose:
                    print(f"\nIteration {iteration + 1} Feedback:\n{feedback}\n")

                if feedback.strip().upper() == "TERMINATE":
                    break

                # Refine response using template
                refinement_prompt = self.templates.get_refinement_template().format(
                    previous_response=current_result,
                    feedback=feedback
                )
                
                current_result = self.providers['gemini'].generate_response(refinement_prompt)
                
                if verbose:
                    print(f"Refined Result (Iteration {iteration + 1}):\n{current_result}\n")

            return current_result
            
        except Exception as e:
            raise RuntimeError(f"Error processing input: {str(e)}")