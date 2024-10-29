# src/orchnex/orchestrator.py
from typing import Dict
from .config import LLMConfig
from .templates import PromptTemplates
from .providers.base import LLMProvider
from .providers.llama_provider import LlamaProvider
from .providers.gemini_provider import GeminiProvider
from .output_manager import OutputManager

class MultiLLMOrchestrator:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.templates = PromptTemplates()
        self.providers: Dict[str, LLMProvider] = {}
        self.output_manager = OutputManager()
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

# In your orchestrator's process_input method:
    def process_input(self, prompt: str, verbose: bool = False) -> str:
        """Process user input through the multi-LLM pipeline"""
        # Start new interaction
        self.output_manager.start_interaction(prompt)
        
        try:
            # 1. Enhance prompt
            enhanced_prompt = self.enhance_prompt_with_promptmaster(prompt)
            self.output_manager.save_step_output(
                "enhanced_prompt",
                enhanced_prompt,
                "Enhanced Prompt"
            )

            # 2. Generate initial response
            initial_result = self.providers['gemini'].generate_response(enhanced_prompt)
            self.output_manager.save_step_output(
                "initial_response",
                initial_result,
                "Initial Gemini Response"
            )

            current_result = initial_result
            
            # 3. Iterative feedback loop
            for iteration in range(self.config.max_iterations):
                feedback = self.providers['llama'].generate_response(
                    f"Analyze this response for improvements:\n{current_result}"
                )
                
                if "TERMINATE" in feedback.upper():
                    break

                current_result = self.providers['gemini'].generate_response(
                    f"Refine based on feedback:\n{feedback}\n\nPrevious response:\n{current_result}"
                )
                
                self.output_manager.save_iteration_output(
                    iteration + 1,
                    feedback,
                    current_result
                )

            # Save final summary
            self.output_manager.save_final_summary(
                prompt,
                enhanced_prompt,
                current_result
            )

            return current_result

        except Exception as e:
            error_msg = f"Error in processing input: {str(e)}"
            self.output_manager.save_step_output(
                "error",
                error_msg,
                "Error"
            )
            raise RuntimeError(error_msg)