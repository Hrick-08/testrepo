"""
Run mini-SWE-agent locally (no Docker) against ISSUE.md.
Use this instead of the inline `python -c "..."` one-liner on Windows,
since cmd.exe doesn't handle multi-line quoted strings like bash does.

Run with: python run_local_test.py
"""
from run_agent import create_model
from minisweagent.agents.default import DefaultAgent
from minisweagent.environments.local import LocalEnvironment

model = create_model()
env = LocalEnvironment(cwd=".")
agent = DefaultAgent(model, env)
agent.run(open("ISSUE.md").read())
