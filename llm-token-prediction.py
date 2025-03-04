import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time
import sys
import threading
import numpy as np
from colorama import Fore, Style, init
# Using readline for input handling instead of keyboard
import readline
import os

# Initialize colorama for colored terminal output
init()

class TokenGenerationVisualizer:
    def __init__(self, model_name="gpt2"):
        """Initialize the visualizer with a specified model."""
        print(f"Loading {model_name} model and tokenizer...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name, cache_dir=os.path.expanduser("~/.cache/huggingface/"))
        self.model = GPT2LMHeadModel.from_pretrained(model_name, cache_dir=os.path.expanduser("~/.cache/huggingface/"))
        
        # Set padding side to the left so that padding tokens are ignored
        self.tokenizer.padding_side = "left"
        # Set pad token to eos token for GPT2 (which doesn't have a pad token)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Set device (cuda if available, else cpu)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"Model loaded on {self.device}.")
        
        # Generation parameters
        self.stop_generation = False
        self.delay = 0.5  # Default delay between tokens (seconds)
        
        # No need for keyboard hook, we'll use a different approach for interruption
        self.stop_animation = False
    
    def check_for_interrupt(self):
        """Check if user wants to interrupt by pressing Enter"""
        print(f"{Fore.YELLOW}Press Enter at any time to stop generation.{Style.RESET_ALL}")
        
        def input_thread():
            input()
            self.stop_generation = True
            print(f"\n{Fore.YELLOW}Generation stopped by user.{Style.RESET_ALL}")
        
        t = threading.Thread(target=input_thread)
        t.daemon = True
        t.start()
    
    def _clear_line(self):
        """Clear the current line in the terminal."""
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        sys.stdout.flush()
    
    def generate_next_token(self, input_text, top_k=5):
        """Generate the next token for input text and show probabilities."""
        # Encode the input text
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        
        # Get model's output logits
        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits
        
        # Get probabilities for next token
        next_token_logits = logits[0, -1, :]
        probs = torch.nn.functional.softmax(next_token_logits, dim=-1)
        
        # Get top-k token ids and probabilities
        topk_probs, topk_indices = torch.topk(probs, top_k)
        
        # Print the top token probabilities
        print(f"{Fore.CYAN}Top {top_k} next token predictions:{Style.RESET_ALL}")
        for i, (idx, prob) in enumerate(zip(topk_indices, topk_probs)):
            token = self.tokenizer.decode([idx])
            prob_percent = prob.item() * 100
            
            # Use different colors for the top prediction vs others
            if i == 0:
                color = Fore.GREEN
                selected_marker = "✓"
            else:
                color = Fore.WHITE
                selected_marker = " "
                
            # Print token info with bar visualization
            bar_length = int(prob_percent / 5)  # Scale to reasonable length
            bar = "█" * bar_length
            print(f"{color}{selected_marker} {token!r:<15} {prob_percent:5.2f}% {bar}{Style.RESET_ALL}")
        
        # Return the most likely next token
        next_token_id = topk_indices[0].item()
        next_token = self.tokenizer.decode([next_token_id])
        
        return next_token, next_token_id
    
    def generate_text(self, prompt, max_length=50, temperature=2.0):
        """Generate text token by token with visualization."""
        current_text = prompt
        generated_tokens = []
        
        print(f"\n{Fore.BLUE}Starting text generation from prompt:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
        # Set up input thread to check for interruption
        self.check_for_interrupt()
        
        try:
            for _ in range(max_length):
                if self.stop_generation:
                    break
                
                # Show thinking animation
                thinking_thread = threading.Thread(target=self._thinking_animation)
                thinking_thread.daemon = True
                thinking_thread.start()
                
                # Generate next token
                next_token, _ = self.generate_next_token(current_text)
                
                # Stop the thinking animation
                self.stop_animation = True
                thinking_thread.join(timeout=0.1)
                self._clear_line()
                
                # Add token to the generated text
                generated_tokens.append(next_token)
                current_text += next_token
                
                # Show progress
                print(f"\n{Fore.GREEN}Current text:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{prompt}{Fore.MAGENTA}{' '.join(generated_tokens)}{Style.RESET_ALL}")
                
                # Pause to make the generation visible
                print(f"\n{Fore.YELLOW}Waiting {self.delay}s before next token...{Style.RESET_ALL}")
                time.sleep(self.delay)
                
                # Check if we should stop based on the generated token
                if next_token == self.tokenizer.eos_token or next_token == '\n\n':
                    print(f"\n{Fore.YELLOW}Generation stopped: End of sequence token generated.{Style.RESET_ALL}")
                    break
                
                # Clear screen for next token
                print("\n" + "-" * 50 + "\n")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Generation stopped by user.{Style.RESET_ALL}")
        
        # Final output
        final_text = prompt + ''.join(generated_tokens)
        print(f"\n{Fore.GREEN}Final generated text:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{final_text}{Style.RESET_ALL}")
        
        return final_text
    
    def _thinking_animation(self):
        """Display a thinking animation while processing."""
        self.stop_animation = False
        chars = "|/-\\"
        i = 0
        while not self.stop_animation:
            sys.stdout.write(f'\r{Fore.CYAN}Thinking {chars[i % len(chars)]}{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def interactive_mode(self):
        """Run in interactive mode, allowing user to input prompts."""
        print(f"{Fore.GREEN}=" * 50)
        print(f"LLM Token Generation Visualizer")
        print(f"=" * 50)
        print(f"This tool demonstrates how GPT-2 predicts tokens one by one.")
        print(f"You'll see the token probabilities and generation process in real-time.")
        print(f"{Style.RESET_ALL}")
        
        while True:
            print(f"\n{Fore.CYAN}Settings:{Style.RESET_ALL}")
            print(f"  - Model: GPT-2")
            print(f"  - Delay between tokens: {self.delay}s")
            
            # Reset stop flag
            self.stop_generation = False
            
            # Get user prompt
            prompt = input(f"\n{Fore.YELLOW}Enter a prompt (or 'q' to quit, 'config' to change settings):{Style.RESET_ALL} ")
            
            if prompt.lower() == 'q':
                print("Exiting...")
                break
            elif prompt.lower() == 'config':
                self._configure_settings()
                continue
            elif not prompt:
                print(f"{Fore.RED}Please enter a valid prompt.{Style.RESET_ALL}")
                continue
                
            # Generate text from prompt
            self.generate_text(prompt)
    
    def _configure_settings(self):
        """Allow user to configure generation settings."""
        print(f"\n{Fore.CYAN}Configuration:{Style.RESET_ALL}")
        
        try:
            delay = input(f"Enter delay between tokens in seconds (current: {self.delay}): ")
            if delay:
                self.delay = float(delay)
                print(f"Delay set to {self.delay}s")
        except ValueError:
            print(f"{Fore.RED}Invalid value, keeping current settings.{Style.RESET_ALL}")


if __name__ == "__main__":
    # Check if the required packages are installed
    try:
        import torch
        import transformers
        import colorama
    except ImportError:
        print("Some required packages are missing. Installing now...")
        os.system("pip install torch transformers colorama")
        print("Packages installed. Please restart the script.")
        sys.exit()
    
    # cached_dir = os.path.expanduser("~/.cache/huggingface/")
    # Create visualizer and run in interactive mode
    visualizer = TokenGenerationVisualizer()
    visualizer.interactive_mode()