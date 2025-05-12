# Introducing Stable Agents

Stable Agents is a Text2Agent SDK that allows you to create agents that can perform complex tasks using natural language.

## Stable Agents vs other Agent Frameworks

Stable Agents is different than other agent frameworks in that it is the only framework that is able to learn from past agentic experiences to improve future agentic experiences.

Here is a code snippet of a Stable Agent in action:

```
from stableagents.agent import Agent
from stableagents.task import Task

# Define a task
task = Task(
    description="Write a blog post about the benefits of using Stable Agents",
    expected_output="A blog post about the benefits of using Stable Agents"
)
```




