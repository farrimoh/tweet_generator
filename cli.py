from models import TweetGenerator
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_valid_number():
    while True:
        try:
            num = int(input("How many tweets would you like to generate? (1-5): "))
            if 1 <= num <= 5:
                return num
            console.print("[red]Please enter a number between 1 and 5.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

def get_model_choice():
    while True:
        console.print("\nChoose your model type:")
        console.print("1. Ollama (local)")
        console.print("2. Hugging Face (cloud)")
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice in [1, 2]:
                return "ollama" if choice == 1 else "huggingface"
            console.print("[red]Please enter 1 or 2.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

def get_model_name(model_type):
    if model_type == "ollama":
        return "llama3"
    else:
        return "meta-llama/Llama-2-7b-chat-hf"

def main():
    console.print(Panel.fit(
        "[bold blue]Tweet Generator 🐦[/bold blue]",
        title="Welcome"
    ))
    
    # Get model choice
    model_type = get_model_choice()
    model_name = get_model_name(model_type)
    
    # Get input text
    console.print("\nEnter your text (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        elif lines:
            break
    
    text = "\n".join(lines).strip()
    
    if not text:
        console.print("[red]Input text cannot be empty[/red]")
        return
    
    # Get number of tweets
    num_tweets = get_valid_number()
    
    console.print(f"\nGenerating {num_tweets} tweets from the following text using {model_type.title()} model:\n")
    console.print(Panel(text, title="Input Text"))
    
    try:
        with console.status("[bold green]Generating tweets...[/bold green]"):
            generator = TweetGenerator(model_type=model_type, model_name=model_name)
            tweets = generator.generate_tweets(text, num_tweets)
        
        if tweets:
            console.print("\n[bold green]Generated Tweets:[/bold green]")
            for i, tweet in enumerate(tweets, 1):
                console.print(Panel(tweet, title=f"Tweet {i} 🐦"))
        else:
            console.print("[red]No tweets were generated.[/red]")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if model_type == "huggingface":
            console.print("[yellow]Note: Make sure you have set up your Hugging Face API token in the .env file[/yellow]")
    
    # Ask if user wants to generate more tweets
    while True:
        again = input("\nWould you like to generate more tweets? (y/n): ").lower()
        if again in ['y', 'n']:
            break
        console.print("[red]Please enter 'y' or 'n'[/red]")
    
    if again == 'y':
        main()
    else:
        console.print("\n[bold blue]Thank you for using Tweet Generator![/bold blue]")

if __name__ == "__main__":
    main() 