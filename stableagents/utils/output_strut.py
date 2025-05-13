
## Sample Code to get a start and see how Stable Agents work

import json
from pydantic import BaseModel
from typing import Any, Callable

class OutputParserError(Exception):
    """
    Exception raised when the output parser fails to parse the output
    """

    def __init__(self, message, output=None):
        self.message = message
        self.output = output
        super().__init__(self.message)
    
    def __str__(self):
        if self.output:
           return f"{self.message}\nProblematic output: {self.output}"
        return self.message
    
 