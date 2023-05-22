import json
import requests
from defines import INSTRUCT_GPT_PROMPT_ANSWER_OPENING, INSTRUCT_GPT_PROMPT_HEADER
from errors import RequestToAiModelFailedError


def request_response_from_ai_model(prompt):
    """Tries to get a response from GPT

    Args:
        prompt (str): the prompt that will be sent to GPT

    Returns:
        str: either a valid response or None
    """
    # Read API key from file
    with open("api_key.txt", "r", encoding="utf8") as file:
        api_key = file.read().strip()

    api_endpoint = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    model = "gpt-4"
    temperature = 1
    max_tokens = None

    prompt = INSTRUCT_GPT_PROMPT_HEADER + prompt + INSTRUCT_GPT_PROMPT_ANSWER_OPENING

    request = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": temperature,
    }

    if max_tokens is not None:
        request["max_tokens"] = max_tokens

    retry_limit = 3

    response = None

    for i in range(retry_limit):
        try:
            response = requests.post(
                api_endpoint, headers=headers, data=json.dumps(request), timeout=15
            )

            # If we made it here, the request was successful, so break out of the loop
            break
        except requests.exceptions.ReadTimeout as exception:
            if i == retry_limit - 1:  # We're on the last retry
                raise RequestToAiModelFailedError(
                    f"Request to '{model}' failed due to ReadTimeout: {exception}"
                ) from exception
            # If we're not on the last retry, continue to the next iteration of the loop
            continue

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    if response.status_code == 400:
        raise RequestToAiModelFailedError(
            f"Request to '{model}' failed due to BadRequestError: {response.text}"
        )
    if response.status_code == 401:
        raise RequestToAiModelFailedError(
            f"Request to '{model}' failed due to UnauthorizedError: {response.text}"
        )
    if response.status_code == 403:
        raise RequestToAiModelFailedError(
            f"Request to '{model}' failed due to ForbiddenError: {response.text}"
        )
    if response.status_code == 404:
        raise RequestToAiModelFailedError(
            f"Request to '{model}' failed due to NotFoundError: {response.text}"
        )
    if response.status_code == 429:
        raise RequestToAiModelFailedError(
            f"Request to '{model}' failed due to NotFoundError: {response.text}"
        )
    if response.status_code == 502:
        raise RequestToAiModelFailedError(
            f"Request to '{model}' failed due to ModelOverloadedError: {response.text}"
        )

    return None
