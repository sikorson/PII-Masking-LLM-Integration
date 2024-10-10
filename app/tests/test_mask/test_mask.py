import pytest

from api.mask.mask import PIIMask, faker


class TestPiiMaskHandler:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.context = (
            "Call at 555-123-4567 when you want to call John from Apple Inc."
            " Also John's email address is john.doe@example.com."
            " He lives at 123 Maple Street in San Francisco."
        )
        self.prompt = (
            "Can you confirm that John's number is 555-123-4567"
            " and his email is john.doe@example.com"
            " and he lives at 123 Maple Street in San Francisco"
            " and he work in Apple Inc.?"
        )
        self.pii = PIIMask(context=self.context, prompt=self.prompt)

    @pytest.fixture(autouse=True)
    def mock_faker(self, monkeypatch):
        def mock_phone_number():
            return "123-456-7890"

        def mock_email():
            return "fake@example.com"

        def mock_name():
            return "FakeName"

        def mock_company():
            return "FakeCompany"

        def mock_street_name():
            return "FakeStreet"

        def mock_city():
            return "FakeCity"

        monkeypatch.setattr(faker, "phone_number", mock_phone_number)
        monkeypatch.setattr(faker, "email", mock_email)
        monkeypatch.setattr(faker, "first_name_nonbinary", mock_name)
        monkeypatch.setattr(faker, "company", mock_company)
        monkeypatch.setattr(faker, "street_name", mock_street_name)
        monkeypatch.setattr(faker, "city", mock_city)

    def test_mask(self):
        masked_data = self.pii.mask()

        # If sentences was masked
        assert masked_data["context"] != self.context
        assert masked_data["prompt"] != self.prompt

        # Masking phone number
        assert "123-456-7890" in masked_data["context"]
        assert "123-456-7890" in masked_data["prompt"]

        # Masking email address
        assert "fake@example.com" in masked_data["context"]
        assert "fake@example.com" in masked_data["prompt"]

        # Masking name
        assert "FakeName" in masked_data["context"]
        assert "FakeName" in masked_data["prompt"]
        assert masked_data["context"].count("FakeName") == 2  # Check if all John names are changed properly

        # Masking company
        assert "FakeCompany" in masked_data["context"]
        assert "FakeCompany" in masked_data["prompt"]

        # Masking street
        assert "FakeStreet" in masked_data["context"]
        assert "FakeStreet" in masked_data["prompt"]

        # Masking city
        assert "FakeCity" in masked_data["context"]
        assert "FakeCity" in masked_data["prompt"]

    def test_unmask(self):
        masked_data = self.pii.mask()
        unmasked_context = self.pii.unmask(masked_data["context"])
        unmasked_prompt = self.pii.unmask(masked_data["prompt"])

        assert unmasked_context == self.context
        assert unmasked_prompt == self.prompt
