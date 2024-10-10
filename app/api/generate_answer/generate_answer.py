import os

from flask_restful import Resource
from huggingface_hub import InferenceClient
from flask import json, request

from api.mask.mask import PIIMask

client = InferenceClient(os.environ.get("MODEL"), token=os.environ.get("TOKEN"))

prompt_template = "Answer on a prompt based on context below.\n\n{context}\n\nPrompt: {prompt}"


class GenerateAnswer(Resource):
    """
    Endpoint for generating an answer to a provided question based on context.
    It will mask any PII data and send masked text to the LLM for answer.
    Response will be unmasked after response from LLM and provided to the user.
    """

    def post(self):
        pii = PIIMask(**json.loads(request.data))
        prompt_dict = pii.mask()
        message = {"role": "user", "content": prompt_template.format(**prompt_dict)}
        stream = client.chat.completions.create(messages=[message])
        full_text = "".join(choice.message.content for choice in stream.choices)
        full_text = pii.unmask(full_text)
        return {"response": full_text}
