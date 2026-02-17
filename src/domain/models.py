from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyzeRequest:
    text: str
    rdf: str


@dataclass(frozen=True)
class AnalyzeResponse:
    text: str
    rdf: str
    generated_text: str
    bleurt: float

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "rdf": self.rdf,
            "generated_text": self.generated_text,
            "bleurt": self.bleurt,
        }
