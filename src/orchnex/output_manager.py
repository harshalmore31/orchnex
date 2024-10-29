# src/orchnex/utils/output_manager.py
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class OutputManager:
    def __init__(self, base_dir: str = "outputs"):
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
        
        # Save original prompt
        self.save_output("original_prompt.md", prompt, "Original Prompt")
        return self.current_interaction

    def save_output(self, filename: str, content: str, step_title: str) -> str:
        """Save output to file and display in console"""
        if not self.current_interaction:
            raise RuntimeError("No active interaction")
            
        output_dir = self._get_interaction_dir()
        filepath = os.path.join(output_dir, filename)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Display in console
        self.console.print(Panel(
            Text(content, style="white"),
            title=f"📝 {step_title}",
            border_style="blue"
        ))
        
        return filepath

    def save_iteration(self, iteration: int, feedback: str, refined_result: str) -> None:
        """Save iteration feedback and refined result"""
        # Save feedback
        self.save_output(
            f"feedback_{iteration}.md",
            feedback,
            f"Meta Feedback - Iteration {iteration}"
        )
        
        # Save refined result
        self.save_output(
            f"refined_result_{iteration}.md",
            refined_result,
            f"Refined Result - Iteration {iteration}"
        )

    def save_summary(self, summary_data: dict) -> None:
        """Save interaction summary as JSON"""
        if not self.current_interaction:
            raise RuntimeError("No active interaction")
            
        filepath = os.path.join(self._get_interaction_dir(), "summary.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2)

        # Display summary
        summary_text = "\n".join(f"{k}: {v}" for k, v in summary_data.items())
        self.console.print(Panel(
            Text(summary_text, style="white"),
            title="🌟 Processing Summary",
            border_style="green"
        ))

    def _get_interaction_dir(self) -> str:
        """Get current interaction directory"""
        if not self.current_session or not self.current_interaction:
            raise RuntimeError("No active session or interaction")
        return os.path.join(self.base_dir, self.current_session, self.current_interaction)

    @staticmethod
    def _ensure_directory(directory: str):
        """Ensure directory exists"""
        os.makedirs(directory, exist_ok=True)