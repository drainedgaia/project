from dataclasses import dataclass
from typing import List

@dataclass
class Course:
    name: str
    grade: str

@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    gpa: float
    courses: List[Course]

