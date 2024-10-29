# src/orchnex/utils/output_manager.py
import os
from datetime import datetime
from typing import Optional
import json

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
        # Create a safe filename from the prompt
        safe_prompt = "".join(x for x in prompt[:30] if x.isalnum() or x in " -_").strip()
        safe_prompt = safe_prompt.replace(" ", "_")
        
        self.current_interaction = f"{timestamp}_{safe_prompt}"
        interaction_dir = self._get_interaction_dir()
        self._ensure_directory(interaction_dir)
        
        # Save original prompt
        self.save_output("original_prompt.md", prompt)
        
        return self.current_interaction

    def save_output(self, filename: str, content: str, metadata: dict = None) -> str:
        """
        Save output to file with optional metadata
        
        Args:
            filename (str): Name of the output file
            content (str): Content to save
            metadata (dict, optional): Additional metadata to save
            
        Returns:
            str: Path to saved file
        """
        if not self.current_interaction:
            raise RuntimeError("No active interaction")
            
        output_dir = self._get_interaction_dir()
        
        # Prepare content with metadata
        final_content = content
        if metadata:
            metadata_content = f"---\n{json.dumps(metadata, indent=2)}\n---\n\n"
            final_content = metadata_content + content
        
        # Save file
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        return filepath

    def save_summary(self, summary_data: dict) -> str:
        """Save interaction summary"""
        if not self.current_interaction:
            raise RuntimeError("No active interaction")
            
        summary_file = os.path.join(self._get_interaction_dir(), "summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, indent=2, default=str, f)
            
        return summary_file

    def _get_interaction_dir(self) -> str:
        """Get current interaction directory"""
        if not self.current_session or not self.current_interaction:
            raise RuntimeError("No active session or interaction")
        return os.path.join(self.base_dir, self.current_session, self.current_interaction)

    @staticmethod
    def _ensure_directory(directory: str) -> None:
        """Ensure directory exists"""
        os.makedirs(directory, exist_ok=True)