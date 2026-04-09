import inspect

print("=" * 60)

# ToolRegistry
try:
    from vanna.core.registry import ToolRegistry
    methods = [m for m in dir(ToolRegistry) if not m.startswith("_")]
    print("ToolRegistry methods:", methods)
    print("ToolRegistry.__init__:", inspect.signature(ToolRegistry.__init__))
except Exception as e:
    print("ToolRegistry ERROR:", e)

print()

# RunSqlTool
try:
    from vanna.tools import RunSqlTool
    print("RunSqlTool.__init__:", inspect.signature(RunSqlTool.__init__))
except Exception as e:
    print("RunSqlTool ERROR:", e)

print()

# VisualizeDataTool
try:
    from vanna.tools import VisualizeDataTool
    print("VisualizeDataTool.__init__:", inspect.signature(VisualizeDataTool.__init__))
except Exception as e:
    print("VisualizeDataTool ERROR:", e)

print()

# DemoAgentMemory
try:
    from vanna.integrations.local.agent_memory import DemoAgentMemory
    methods = [m for m in dir(DemoAgentMemory) if not m.startswith("_")]
    print("DemoAgentMemory methods:", methods)
    print("DemoAgentMemory.__init__:", inspect.signature(DemoAgentMemory.__init__))
except Exception as e:
    print("DemoAgentMemory ERROR:", e)

print()

# Agent
try:
    from vanna import Agent
    print("Agent.__init__:", inspect.signature(Agent.__init__))
except Exception as e:
    print("Agent ERROR:", e)

print()

# AgentConfig
try:
    from vanna import AgentConfig
    print("AgentConfig.__init__:", inspect.signature(AgentConfig.__init__))
except Exception as e:
    print("AgentConfig ERROR:", e)

print()

# SaveQuestionToolArgsTool
try:
    from vanna.tools.agent_memory import SaveQuestionToolArgsTool
    print("SaveQuestionToolArgsTool.__init__:", inspect.signature(SaveQuestionToolArgsTool.__init__))
except Exception as e:
    print("SaveQuestionToolArgsTool ERROR:", e)

print()

# SearchSavedCorrectToolUsesTool
try:
    from vanna.tools.agent_memory import SearchSavedCorrectToolUsesTool
    print("SearchSavedCorrectToolUsesTool.__init__:", inspect.signature(SearchSavedCorrectToolUsesTool.__init__))
except Exception as e:
    print("SearchSavedCorrectToolUsesTool ERROR:", e)

print()

# GeminiLlmService
try:
    from vanna.integrations.google import GeminiLlmService
    print("GeminiLlmService.__init__:", inspect.signature(GeminiLlmService.__init__))
except Exception as e:
    print("GeminiLlmService ERROR:", e)

print("=" * 60)