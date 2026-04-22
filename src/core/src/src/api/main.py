"""
Cortex AI - Main Entry Point
"""

import asyncio
import logging
from src.core.brain import CortexBrain

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def interactive_mode():
    """Run Cortex AI in interactive CLI mode"""
    print("\n" + "="*50)
    print("🧠 CORTEX AI - Interactive Mode")
    print("="*50)
    print("Type 'exit' to quit\n")
    
    brain = CortexBrain(config={})
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nCortex AI: Goodbye! 👋")
                break
            
            # Process input
            result = await brain.process_input(user_input)
            
            print(f"\nCortex AI: {result['response']}")
            print(f"[Intent: {result['intent']} | Confidence: {result['confidence']:.2f}]\n")
            
        except KeyboardInterrupt:
            print("\n\nCortex AI: Interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError: {e}\n")


async def main():
    """Main function"""
    print("Starting Cortex AI...")
    await interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())
