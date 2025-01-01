from grabber import Grabber
from config import CONFIG
import keyboard  # To listen for key presses
import time

def execute_task():
    """
    Function to execute the screenshot and send task.
    """
    grabber = Grabber()
    
    try:
        # Capture a screenshot
        screenshot_path = grabber.capture_screenshot()
        print(f"Screenshot saved at: {screenshot_path}")

        # Example prompt to ChatGPT
        prompt = "Analyze this question: What is 2+2?"
        response = grabber.send_prompt_to_chatgpt(prompt)
        print(f"ChatGPT Response: {response}")

        # Process the response
        question_type, content = grabber.process_response(response)
        if question_type == "letter":
            print(f"Multiple-choice question detected. Answer: {content}")
        elif question_type == "code":
            print(f"Programming question detected. Code: {content}")
            # Send email with the code response
            grabber.send_email(
                to_email=CONFIG['email'],  # Use email from config
                subject="Programming Test Answer",
                body=content
            )
        else:
            print(f"Unrecognized question type: {content}")

        # Clean up the screenshot
        grabber.cleanup(screenshot_path)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("TestHelper is running in the background. Press 'Ctrl+Shift+S' to execute the task, or 'Ctrl+Shift+Q' to quit.")

    # Listen for the key combinations
    while True:
        try:
            # Execute task when 'Ctrl+Shift+S' is pressed
            if keyboard.is_pressed('ctrl+shift+s'):
                print("Executing the task...")
                execute_task()
                time.sleep(1)  # Prevent duplicate execution

            # Exit the program when 'Ctrl+Shift+Q' is pressed
            if keyboard.is_pressed('ctrl+shift+q'):
                print("Exiting TestHelper. Goodbye!")
                break
        except KeyboardInterrupt:
            print("Program interrupted. Exiting...")
            break
