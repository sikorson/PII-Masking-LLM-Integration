import pytest


@pytest.fixture
def content():
    def inner(prompt, context):
        return {"prompt": prompt, "context": context}

    return inner


@pytest.fixture
def pii(content):
    def inner(prompt, context):
        from api.mask import PIIMask

        return PIIMask(**content(prompt, context))

    return inner
