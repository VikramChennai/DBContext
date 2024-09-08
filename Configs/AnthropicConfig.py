import anthropic

AnthropicClient = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)


# Test the Anthropic setup with a simple call
def test_anthropic_setup():
    try:
        # Create a simple completion request
        completion = AnthropicClient.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt="Human: Hello, Claude! Can you hear me?\n\nAssistant: Yes, I can hear you! How can I assist you today?",
        )
        
        # Print the response
        print("Anthropic API test response:")
        print(completion.completion)
        print("\nAPI call successful!")
    except Exception as e:
        print(f"Error occurred while testing Anthropic API: {str(e)}")

# 