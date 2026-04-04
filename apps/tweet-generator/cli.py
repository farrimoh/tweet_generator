from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import json

def generate_tweets(text, num_tweets):
    # Initialize Ollama
    llm = OllamaLLM(model="llama3")
    
    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=["text", "num_tweets"],
        template="""Based on the following text, generate {num_tweets} engaging tweets. 
        Make them concise, informative, and engaging. Each tweet should be under 280 characters.
        Format the response as a JSON array of strings.
        
        Text: {text}
        
        Tweets:"""
    )
    
    try:
        # Generate the prompt
        prompt = prompt_template.format(text=text, num_tweets=num_tweets)
        
        # Generate response
        response = llm.invoke(prompt)
        
        # Clean up the response to ensure it's valid JSON
        generated_text = response.strip('[]').split('\n')
        tweets = [tweet.strip().strip('"') for tweet in generated_text if tweet.strip()]
        
        return tweets
    except Exception as e:
        print(f"Error generating tweets: {str(e)}")
        return []

def get_valid_number():
    while True:
        try:
            num = int(input("How many tweets would you like to generate? (1-5): "))
            if 1 <= num <= 5:
                return num
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("\n=== Tweet Generator using Llama 3 ===\n")
    
    # Get input text
    print("Enter your text (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        elif lines:
            break
    
    text = "\n".join(lines).strip()
    
    if not text:
        print("Input text cannot be empty")
        return
    
    # Get number of tweets
    num_tweets = get_valid_number()
    
    print(f"\nGenerating {num_tweets} tweets from the following text:\n")
    print("-" * 50)
    print(text)
    print("-" * 50)
    print("\nGenerating tweets...\n")
    
    tweets = generate_tweets(text, num_tweets)
    
    if tweets:
        print("Generated Tweets:")
        print("-" * 50)
        for i, tweet in enumerate(tweets, 1):
            print(f"{i}. {tweet}")
    else:
        print("No tweets were generated.")
    
    # Ask if user wants to generate more tweets
    while True:
        again = input("\nWould you like to generate more tweets? (y/n): ").lower()
        if again in ['y', 'n']:
            break
        print("Please enter 'y' or 'n'")
    
    if again == 'y':
        main()
    else:
        print("\nThank you for using Tweet Generator!")

if __name__ == "__main__":
    main() 