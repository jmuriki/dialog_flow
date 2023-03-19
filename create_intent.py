import os
import json
import requests

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, theme, questions, answer):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for question in questions:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=question
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=answer)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=theme,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def get_training_phrases(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    json_url = os.getenv("JSON_URL")
    json_path = os.getenv("JSON_PATH")
    training_phrases_payload = {}
    if json_url:
        training_phrases_payload.update(get_training_phrases(json_url))
    if json_path:
        with open(json_path, "r") as file:
            payload = json.load(file)
        training_phrases_payload.update(payload)
    for theme, payload in training_phrases_payload.items():
        create_intent(
            project_id,
            theme,
            payload['questions'],
            [payload['answer']]
        )


if __name__ == '__main__':
    main()
