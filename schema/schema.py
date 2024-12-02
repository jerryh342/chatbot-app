from dataclasses import dataclass


@dataclass
class Case():
    caseNum: int
    caseDesc: str
    maxStage: int
    questions: dict
