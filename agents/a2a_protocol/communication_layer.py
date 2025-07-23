class CommunicationLayer:
    def __init__(self, agent_registry):
        self.agent_registry = agent_registry

    def send(self, message):
        agent = self.agent_registry.get(message.receiver)
        if agent:
            return agent.handle_message(message)
        else:
            return {"error": "Agent not found"} 