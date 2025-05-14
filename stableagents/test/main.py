import json 
import os
import threading
import datetime
import sys
# from stableagents import * 


class StableAgents:

    pass

def local_setup():
    pass

@property
def anonymous_telemetry(self) -> bool:
    return not self.disable_telemetry and not self.offline

@property
def will_contribute(self):
    pass


def agents():
    task = input("What task would you like the agent to perform? ")
    
    if task:
        agent_string = f"Agent will perform the following task: {task}"
    else:
        agent_string = "No task specified for the agent"
        
    return agent_string

print(agents())


def agentstatus():
    status = {
        "status": "inactive",
        "timestamp": None,
        "details": {}
    }
    
    if self is True:
        status["status"] = "active"
        status["timestamp"] = datetime.datetime.now().isoformat()
        status["details"] = {
            "type": "stable_agent",
            "state": "running"
        }
    
    return json.dumps(status, indent=2)

print(agentstatus)




