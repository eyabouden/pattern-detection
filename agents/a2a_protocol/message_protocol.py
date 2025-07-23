class AgentMessage:
    def __init__(self, sender, receiver, type, payload=None):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.payload = payload 