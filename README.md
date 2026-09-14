# Demo: Issue-to-PR Agent (background color fix)

A minimal end-to-end test case for the AI-103 project's core loop:
**GitHub issue → agent edits code in a sandbox → tests run → PR opened.**

## What's in here

- `index.html`, `style.css` — the tiny "codebase" being fixed
- `test_style.py` — the test the agent must make pass (checks background color)
- `ISSUE.md` — the sample issue text used as the agent's task
- `mini_agent_config.yaml` — points mini-SWE-agent at Azure OpenAI (via litellm)
- `Dockerfile` — the sandbox image agent actions run inside
- `run_agent.py` — the orchestrator: webhook → sandboxed run → test gate → PR

## Try it locally (before wiring up the real webhook)

```bash
pip install requirement.txt
export GROQ_API_KEY="<your-groq-key>"
python run_local_test.py
pytest test_style.py -v 
```

> Currently wired to **Groq** (fast, free-tier friendly) for local testing,
> and running **without Docker** (`LocalEnvironment`) for a quick first pass —
> the agent's bash commands run directly on your machine. That's fine
> against this throwaway test repo, but never point the no-sandbox mode at a
> repo with real credentials or data nearby. Swap to `DockerEnvironment` +
> the `Dockerfile` here (see `mini_agent_config.yaml`) once you're past
> initial testing, and swap to Azure OpenAI before the actual submission.

## Full pipeline

Run `uvicorn run_agent:app --reload` and point a GitHub webhook (issue
`opened` event) at `/webhook`. On a real issue, it clones the repo, runs the
agent in the sandbox, gates on the test suite, and — only if tests pass —
pushes to `agent/issue-<n>` and opens a PR. Nothing is ever pushed to `main`
or merged automatically; a human reviews and merges.

## Acknowledgment

This project uses [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent)
(MIT License) by the SWE-agent team (Princeton/Stanford) as the core
issue-resolution loop.

> Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated
> Software Engineering," NeurIPS 2024. https://arxiv.org/abs/2405.15793

Everything else — the webhook, sandboxing, test-gating, and PR creation — is
original work built for this project.
