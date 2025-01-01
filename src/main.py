from grabber import Grabber

if __name__ == "__main__":
    try:
        # Initialize Grabber
        api_key = "YOUR_API_KEY"
        grabber = Grabber(api_key)

        # Capture a screenshot
        screenshot_path = grabber.capture_screenshot()
        print(f"Screenshot saved at: {screenshot_path}")

        # Example prompt
        prompt = "Analyze this question: What is 2+2?"
        response = grabber.send_prompt_to_chatgpt(prompt)
        print(f"ChatGPT Response: {response}")

        # Process the response
        question_type, content = grabber.process_response(response)
        if question_type == "letter":
            print(f"Multiple-choice question detected. Answer: {content}")
        elif question_type == "code":
            print(f"Programming question detected. Code: {content}")
            # Send email
            grabber.send_email(
                to_email="recipient@example.com",
                subject="Programming Test Answer",
                body=content,
                from_email="your_email@example.com",
                from_password="your_password"
            )
        else:
            print(f"Unrecognized question type: {content}")

        # Clean up
        grabber.cleanup(screenshot_path)

    except Exception as e:
        print(f"An error occurred: {e}")
