# src/demo.py
from rich.console import Console
from rich.prompt import Prompt
from orchnex import LLMConfig, MultiLLMOrchestrator
import os

def run_interactive_demo():
    console = Console()
    
    # ASCII Art Header
    console.print("""
    ╔═══════════════════════════════════════════╗
    ║            🌟 ORCHNEX DEMO 🌟             ║
    ║    Multi-LLM Orchestration Platform       ║
    ╚═══════════════════════════════════════════╝
    """, style="bold blue")
    
    # Initialize configuration
    config = LLMConfig(
        gemini_api_key=os.getenv("GEMINI_API_KEY") or input("Enter GEMINI_API_KEY : "),
        nvidia_api_key=os.getenv("NVIDIA_API_KEY") or input("Enter NVIDIA_API_KEY : ")
    )
    
    orchestrator = MultiLLMOrchestrator(config)
    
    # Show capabilities
    console.print("\n🔥 Available Capabilities:", style="bold yellow")
    capabilities = [
        "✨ Prompt Enhancement via PromptMaster 3.0",
        "🤖 Multi-LLM Processing Pipeline",
        "📊 Quality Analysis and Refinement",
        "🔄 Iterative Improvement Loop",
        "📈 Performance Metrics"
    ]
    for cap in capabilities:
        console.print(f"  {cap}")
    
    # Interactive demo
    while True:
        try:
            prompt = Prompt.ask("\n\n💭 Enter your prompt (or 'quit' to exit)")
            
            if prompt.lower() == 'quit':
                break
                
            console.print("\n🎯 Processing your request through the orchestration pipeline...\n")
            result = orchestrator.process_input(prompt, verbose=True)
            
        except KeyboardInterrupt:
            console.print("\n\n❌ Demo interrupted by user")
            break
        except Exception as e:
            console.print(f"\n❌ Error: {str(e)}", style="bold red")

if __name__ == "__main__":
    run_interactive_demo()