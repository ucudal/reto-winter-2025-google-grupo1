from pydantic.dataclasses import dataclass

from env import Environment


@dataclass
class Dependencies:
    env: Environment
    pass
