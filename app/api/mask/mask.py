import re
from dataclasses import dataclass, field

from faker import Faker
import spacy


PHONE_PATTERN = r"\+?\d{1,3}?[\s.-]?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}"
EMAIL_PATTERN = r"((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])"

pattern_dict = {EMAIL_PATTERN: "email", PHONE_PATTERN: "phone_number"}

faker = Faker()
nlp_model = spacy.load("en_core_web_sm")


@dataclass
class PIIMask:
    context: str
    prompt: str
    replace_map: dict = field(default_factory=dict)

    def _mask_sentence(self, sentence):
        sentence = self._mask_with_nlp(sentence)
        sentence = self._mask_with_regex(sentence)

        return sentence

    def _mask_with_regex(self, sentence):
        for pattern, faker_function in pattern_dict.items():
            for item in re.finditer(pattern, sentence):
                self.replace_map[item.group()] = self.replace_map.get(item.group()) or getattr(faker, faker_function)()
                sentence = sentence.replace(item.group(), self.replace_map[item.group()])

        return sentence

    def _mask_with_nlp(self, sentence):
        doc = nlp_model(sentence)
        for ent in doc.ents:
            match ent.label_:
                case "PERSON":
                    self.replace_map[ent.text] = self.replace_map.get(ent.text, "") or faker.first_name_nonbinary()
                case "ORG":
                    self.replace_map[ent.text] = self.replace_map.get(ent.text, "") or faker.company()
                case "FAC":
                    self.replace_map[ent.text] = self.replace_map.get(ent.text, "") or faker.street_name()
                case "GPE":
                    self.replace_map[ent.text] = self.replace_map.get(ent.text, "") or faker.city()

            sentence = sentence.replace(ent.text, self.replace_map.get(ent.text, ent.text))

        return sentence

    def mask(self) -> dict[str, str]:
        """
        Method for masking user data.

        Returns
        -------
        dict[str, str]
            Masked data in the same structure as input data.

        """
        self.context = self._mask_sentence(self.context)
        self.prompt = self._mask_sentence(self.prompt)

        return {"context": self.context, "prompt": self.prompt}

    def unmask(self, text: str) -> str:
        """
        Method for unmasking answer from LLM.

        Parameters
        ----------
        text : str
            Sentence to be unmasked.

        Returns
        -------
        str
            Unmasked sentence.

        """
        for match, replacement in self.replace_map.items():
            text = text.replace(replacement, match)
        return text
