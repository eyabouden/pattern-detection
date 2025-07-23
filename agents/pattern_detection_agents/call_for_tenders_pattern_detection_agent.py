import os
import json
from collections import Counter
from typing import Tuple, Dict, Any

# Simulated MCP and A2A protocols
class MCPProtocol:
    def use_tool(self, tool_name, params):
        return f"[MCP] Tool '{tool_name}' used with params: {params}"

class A2AProtocol:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent

    def send_message(self, from_agent, to_agent, message):
        agent = self.agents.get(to_agent)
        return agent.receive_message(from_agent, message) if agent else f"Agent '{to_agent}' not found."


class CallForTendersPatternDetectionAgent:
    def __init__(self, data_dir="data/companies/our_company/synthetic_internal/call_for_tenders", mcp=None, a2a=None):
        self.agent_name = "CallForTendersPatternDetectionAgent"
        self.data_dir = data_dir
        self.mcp = mcp or MCPProtocol()
        self.a2a = a2a
        self.tenders, self.responses = self._load_data()

    def _load_data(self) -> Tuple[list, list]:
        tenders, responses = [], []
        for year_folder in os.listdir(self.data_dir):
            tender_path = os.path.join(self.data_dir, year_folder, "call_for_tenders.json")
            response_path = os.path.join(self.data_dir, year_folder, "tender_responses.json")
            if os.path.exists(tender_path):
                with open(tender_path, encoding="utf-8") as f:
                    tenders += json.load(f)
            if os.path.exists(response_path):
                with open(response_path, encoding="utf-8") as f:
                    responses += json.load(f)
        return tenders, responses

    def detect_patterns(self, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower().strip()
        tool_response = self.mcp.use_tool("PatternAnalysisTool", {"query": prompt})

        handlers = {
            "success rate": self._tender_success_rates,
            "tender success": self._tender_success_rates,
            "bid amount": self._bid_amount_statistics,
            "bids": self._bid_amount_statistics,
            "responder activity": self._responder_activity_patterns,
            "responder patterns": self._responder_activity_patterns,
            "status distribution": self._tender_status_distribution,
            "tender status": self._tender_status_distribution
        }

        for keyword, handler in handlers.items():
            if keyword in prompt_lower:
                result = handler()
                break
        else:
            result = {
                "error": "Pattern not recognized. Try one of: 'success rate', 'bid amount', 'responder activity', or 'status distribution'."
            }

        result["tool_response"] = tool_response
        return result

    def _tender_success_rates(self) -> Dict[str, Any]:
        awarded = [t for t in self.tenders if t.get("status", "").lower() == "awarded"]
        success_rate = len(awarded) / len(self.tenders) if self.tenders else 0
        success_by_type = Counter(t.get("tender_type", "Unknown") for t in awarded)
        return {
            "pattern": "tender_success_rates",
            "overall_success_rate": round(success_rate, 3),
            "success_by_type": dict(success_by_type),
            "total_tenders": len(self.tenders),
            "awarded_tenders": len(awarded)
        }

    def _bid_amount_statistics(self) -> Dict[str, Any]:
        bid_amounts = [r["bid_amount"] for r in self.responses if "bid_amount" in r]
        if not bid_amounts:
            return {"pattern": "bid_amount_statistics", "error": "No bid amounts available."}
        return {
            "pattern": "bid_amount_statistics",
            "average_bid": round(sum(bid_amounts) / len(bid_amounts), 2),
            "max_bid": max(bid_amounts),
            "min_bid": min(bid_amounts),
            "num_bids": len(bid_amounts)
        }

    def _responder_activity_patterns(self) -> Dict[str, Any]:
        all_counts = Counter(r.get("responder", "Unknown") for r in self.responses)
        accepted_counts = Counter(r["responder"] for r in self.responses if r.get("status", "").lower() == "accepted")
        return {
            "pattern": "responder_activity_patterns",
            "total_responders": len(all_counts),
            "bids_per_responder": dict(all_counts),
            "accepted_bids_per_responder": dict(accepted_counts)
        }

    def _tender_status_distribution(self) -> Dict[str, Any]:
        status_counts = Counter(t.get("status", "Unknown") for t in self.tenders)
        return {
            "pattern": "tender_status_distribution",
            "status_counts": dict(status_counts)
        }

    def receive_message(self, from_agent: str, message: str) -> str:
        return f"[{self.agent_name}] Received message from {from_agent}: {message}"


# Optional script to demonstrate usage
if __name__ == "__main__":
    mcp = MCPProtocol()
    a2a = A2AProtocol()
    agent = CallForTendersPatternDetectionAgent(mcp=mcp, a2a=a2a)
    a2a.register_agent(agent.agent_name, agent)

    example_prompts = [
        "Show tender success rate",
        "Give me bid amount stats",
        "Analyze responder activity",
        "Display tender status distribution",
        "What’s the win rate by type?",
        "How many responses had high bids?"
    ]

    for prompt in example_prompts:
        print(f"\nPrompt: {prompt}")
        print(json.dumps(agent.detect_patterns(prompt), indent=2))

    print("\nA2A example:")
    print(a2a.send_message("TestAgent", agent.agent_name, "Ping?"))
