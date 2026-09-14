"""
Run mini-SWE-agent locally (no Docker) against ISSUE.md.
Use this instead of the inline `python -c "..."` one-liner on Windows,
since cmd.exe doesn't handle multi-line quoted strings like bash does.

Run with: python run_local_test.py
"""
from minisweagent.agents.default import DefaultAgent
from minisweagent.models.litellm_model import LitellmModel
from minisweagent.environments.local import LocalEnvironment

model = LitellmModel(model_name="groq/llama-3.3-70b-versatile")
env = LocalEnvironment(cwd=".")
agent = DefaultAgent(model, env)
agent.run(open("ISSUE.md").read())
