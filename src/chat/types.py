from pydantic.dataclasses import dataclass

from env import Environment

UserId = str

@dataclass
class Dependencies:
    env: Environment
