import requests

# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values

class Slack:
    
    def __init__(self, channel="#website-order", ) -> None:
        config = dotenv_values()
        apiToken = config['SLACK_API_TOKEN']
        self.SLACK_API_TOKEN = apiToken
        self.API_ENDPOINT = "https://slack.com/api/chat.postMessage"
        
        self.channel = channel                                              # Set the Slack channel or user where you want to send the message
        self.headers = {"Authorization": f"Bearer {self.SLACK_API_TOKEN}",}      # Set up the request headers with the API toke
        
        
    def send_message(self, message: str):
        
        # Set up the request data
        data = {"channel": self.channel,
                "text": message,}

        # Send the POST request to Slack API
        response = requests.post(self.API_ENDPOINT, headers=self.headers, data=data)

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Message sent successfully to Slack!")
        else:
            print(f"Failed to send message. Error: {response.text}")
            
            
            
if __name__ == "__main__":
    slackAPI = Slack()
    slackAPI.send_message("Testing 1st Python Slack message")
