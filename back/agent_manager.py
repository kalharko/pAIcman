from back.agent import Agent
from back.action import Action
from back.errors import PacErrUnknownAgentId


class AgentManager():
    _agents: dict[Agent]

    def __init__(self, agents: dict[Agent]) -> None:
        self._agents = []

    def set_agents(self, agents: dict[Agent]) -> None:
        assert isinstance(agents, dict)
        assert len(agents.keys()) > 0
        assert isinstance(agents.values()[0], Agent)

        self._agents = agents

    def apply(self, action: Action) -> bool:
        assert isinstance(action, Action)

        if action.id not in self._agents.keys():
            return PacErrUnknownAgentId(self)

        self._agents[action.id].move((action.direction))

    def get_agent(self, id: str) -> Agent:
        assert isinstance(id, str)

        if id not in self._agents.keys():
            return PacErrUnknownAgentId(self)

        return self._agents[id]

    def get_all_agents(self) -> list[Agent]:
        return self.agents.values()
