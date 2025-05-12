# Introducing Stable Agents

Stable Agents is a Text2Agent SDK that allows you to create agents that can perform complex tasks using natural language.

## Stable Agents vs other Agent Frameworks

Stable Agents is different than other agent frameworks in that it is the only framework that is able to learn from past agentic experiences to improve future agentic experiences.

Here is a code snippet of a Stable Agent in action:

```python
from stableagents.agent import Agent
from stableagents.task import Task
from stableagents.tools import *
from stableagents.tools.web_search import WebSearch

# Define a web search tool
web_search = WebSearch()


# Define an agent
agent = Agent(
    name="Stable Agent",
    tools=[web_search],
    task=task
)
```




