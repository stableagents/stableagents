import json
import requests
import uuid
from typing import Dict, Any

# Mock memory store for stable context retention
class StableMemory:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def store(self, session_id: str, context: Dict[str, Any]):
        self.sessions[session_id] = context

    def retrieve(self, session_id: str) -> Dict[str, Any]:
        return self.sessions.get(session_id, {})

    def update(self, session_id: str, key: str, value: Any):
        if session_id in self.sessions:
            self.sessions[session_id][key] = value
        else:
            self.sessions[session_id] = {key: value}

# MCP client to communicate with external tools
class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params
        }
        try:
            response = requests.post(self.server_url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json().get("result", {})
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

# Stable Agent for customer support
class StableAgent:
    def __init__(self, crm_url: str, messaging_url: str):
        self.memory = StableMemory()
        self.crm_client = MCPClient(crm_url)
        self.messaging_client = MCPClient(messaging_url)

    def process_query(self, session_id: str, user_query: str) -> str:
        # Retrieve or initialize session context
        context = self.memory.retrieve(session_id)
        if not context:
            context = {"query_count": 0, "user_id": None, "last_query": ""}
            self.memory.store(session_id, context)

        # Increment query count for tracking
        context["query_count"] += 1
        context["last_query"] = user_query
        self.memory.update(session_id, "last_query", user_query)

        # Step 1: Query CRM for user data
        crm_response = self.crm_client.send_request("get_user_data", {"query": user_query})
        if "error" in crm_response:
            # Handle disruption (e.g., CRM unavailable)
            return "Sorry, I couldn't access user data. Please clarify your request."

        if not crm_response.get("user_id"):
            # Adapt to missing data
            self.memory.update(session_id, "needs_clarification", True)
            return "Please provide your user ID or more details."

        # Update context with user data
        context["user_id"] = crm_response["user_id"]
        self.memory.store(session_id, context)

        # Step 2: Generate response via messaging API
        response_params = {
            "user_id": context["user_id"],
            "query": user_query,
            "context": context
        }
        msg_response = self.messaging_client.send_request("generate_response", response_params)
        if "error" in msg_response:
            return "Sorry, I couldn't generate a response. Try again later."

        # Step 3: Store response in memory for consistency
        self.memory.update(session_id, "last_response", msg_response.get("response", ""))
        return msg_response.get("response", "How can I assist you further?")

# Mock MCP servers (for demonstration)
def mock_crm_server(query: str) -> Dict[str, Any]:
    # Simulate CRM response
    if "user_id" in query.lower():
        return {"user_id": "12345", "name": "John Doe", "history": ["order#001", "order#002"]}
    return {}

def mock_messaging_server(params: Dict[str, Any]) -> Dict[str, Any]:
    # Simulate messaging API response
    query = params.get("query", "")
    user_id = params.get("user_id", "unknown")
    return {"response": f"Hi, user {user_id}! Regarding '{query}', how can I help?"}

# Example usage
if __name__ == "__main__":
    # Initialize agent with mock MCP server URLs
    agent = StableAgent(
        crm_url="http://localhost:8000/crm",
        messaging_url="http://localhost:8001/messaging"
    )

    # Simulate a customer support session
    session_id = str(uuid.uuid4())
    print(agent.process_query(session_id, "What’s my order status?"))
    print(agent.process_query(session_id, "user_id:12345 Check my order."))
    print(agent.process_query(session_id, "Any updates on order#001?"))