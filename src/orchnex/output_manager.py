# src/orchnex/utils/output_manager.py
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json
from rich.console import Console
from rich.panel import Panel

class OutputManager:
    def __init__(self, base_dir: str = "outputs"):
        """
        Initialize OutputManager
        
        Args:
            base_dir (str): Base directory for outputs
        """
        self.base_dir = base_dir
        self.current_session: Optional[str] = None
        self.current_interaction: Optional[str] = None
        self.console = Console()
        self._ensure_directory(self.base_dir)
        
    def start_session(self) -> str:
        """Start a new session with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session = f"session_{timestamp}"
        session_dir = os.path.join(self.base_dir, self.current_session)
        self._ensure_directory(session_dir)
        return self.current_session

    def start_interaction(self, prompt: str) -> str:
        """Start a new interaction within the current session"""
        if not self.current_session:
            self.start_session()
        
        timestamp = datetime.now().strftime("%H%M%S")
        safe_prompt = "".join(x for x in prompt[:30] if x.isalnum() or x in " -_").strip()
        safe_prompt = safe_prompt.replace(" ", "_")
        
        self.current_interaction = f"{timestamp}_{safe_prompt}"
        interaction_dir = self._get_interaction_dir()
        self._ensure_directory(interaction_dir)
        
        # Save and display original prompt
        self.save_step_output("original_prompt", prompt, "Original Prompt")
        return self.current_interaction

    def save_step_output(self, step_name: str, content: str, display_title: str, metadata: Dict[str, Any] = None) -> str:
        """
        Save and display step output
        
        Args:
            step_name (str): Name of the step
            content (str): Content to save
            display_title (str): Title for display panel
            metadata (dict, optional): Additional metadata
        """
        if not self.current_interaction:
            raise RuntimeError("No active interaction")
            
        # Save to file
        output_dir = self._get_interaction_dir()
        timestamp = datetime.now().isoformat()
        
        # Prepare content with metadata
        full_content = f"""Timestamp: {timestamp}
Step: {step_name}

{content}"""

        if metadata:
            metadata_content = "\nMetadata:\n" + "\n".join(f"{k}: {v}" for k, v in metadata.items())
            full_content += metadata_content

        filepath = os.path.join(output_dir, f"{step_name}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        # Display in console
        self.console.print(Panel(
            content,
            title=f"📝 {display_title}",
            style="blue"
        ))
        
        return filepath

    def save_iteration_output(self, iteration: int, feedback: str, refined_response: str) -> None:
        """Save iteration output with feedback and refinement"""
        # Save feedback
        self.save_step_output(
            f"iteration_{iteration}_feedback",
            feedback,
            f"Meta Feedback - Iteration {iteration}",
            {"iteration": iteration}
        )
        
        # Save refined response
        self.save_step_output(
            f"iteration_{iteration}_refinement",
            refined_response,
            f"Refined Response - Iteration {iteration}",
            {"iteration": iteration}
        )

    def save_final_summary(self, original_prompt: str, enhanced_prompt: str, final_result: str) -> None:
        """Save and display final summary"""
        summary_content = f"""Original Prompt:
{original_prompt}

Enhanced Prompt:
{enhanced_prompt}

Final Result:
{final_result}"""

        self.save_step_output(
            "final_summary",
            summary_content,
            "🌟 Final Processing Results",
            {
                "timestamp": datetime.now().isoformat(),
                "processing_complete": True
            }
        )

    def _get_interaction_dir(self) -> str:
        """Get current interaction directory"""
        if not self.current_session or not self.current_interaction:
            raise RuntimeError("No active session or interaction")
        return os.path.join(self.base_dir, self.current_session, self.current_interaction)

    @staticmethod
    def _ensure_directory(directory: str):
        """Ensure directory exists"""
        os.makedirs(directory, exist_ok=True)