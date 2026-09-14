"""
Orchestrator: GitHub issue -> mini-SWE-agent run (sandboxed) -> tests -> PR.

This is the layer YOUR team builds and owns. mini-SWE-agent (cited, MIT
license) only provides the core "edit files via bash until it works" loop.
Everything below — webhook handling, sandboxing, the test gate, and PR
creation — is your technical implementation.

Run: uvicorn run_agent:app --reload
"""
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from fastapi import FastAPI, Request
from github import Github  # PyGithub
from minisweagent.agents.default import DefaultAgent
from minisweagent.models.litellm_model import LitellmModel
from minisweagent.environments.docker import DockerEnvironment

app = FastAPI()

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO_NAME = os.environ["REPO_NAME"]        # e.g. "yourname/demo-repo"
SANDBOX_IMAGE = "demo-agent-sandbox:latest"
FOUNDRY_ENDPOINT = os.environ["AZURE_FOUNDRY_ENDPOINT"].rstrip("/")
FOUNDRY_DEPLOYMENT = os.environ["AZURE_FOUNDRY_DEPLOYMENT"]
FOUNDRY_API_VERSION = os.getenv("AZURE_FOUNDRY_API_VERSION", "2025-04-01-preview")

gh = Github(GITHUB_TOKEN)


def create_model() -> LitellmModel:
    """Create an OpenAI-compatible mini-SWE-agent model for Azure AI Foundry."""
    api_key = os.getenv("AZURE_FOUNDRY_API_KEY")
    if not api_key:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )
        api_key = token_provider()
    api_base = FOUNDRY_ENDPOINT
    if not FOUNDRY_ENDPOINT.endswith("/openai/v1"):
        separator = "&" if "?" in FOUNDRY_ENDPOINT else "?"
        api_base = f"{FOUNDRY_ENDPOINT}{separator}api-version={quote(FOUNDRY_API_VERSION)}"
    return LitellmModel(
        model_name=f"openai/{FOUNDRY_DEPLOYMENT}",
        model_kwargs={
            "api_base": api_base,
            "api_key": api_key,
        },
    )


def clone_repo_to_sandbox(repo_url: str, branch_base: str = "main") -> Path:
    """Clone the target repo into a fresh temp dir that gets mounted into
    the sandbox container. A new checkout per run keeps runs isolated."""
    workdir = Path(tempfile.mkdtemp(prefix="agent-run-"))
    subprocess.run(
        ["git", "clone", "--branch", branch_base, "--depth", "1", repo_url, str(workdir)],
        check=True,
    )
    return workdir


def run_agent_on_issue(issue_title: str, issue_body: str, repo_path: Path) -> bool:
    """Runs mini-SWE-agent inside the Docker sandbox against the issue text.
    Returns True if the agent's changes pass the repo's own test suite."""
    model = create_model()
    env = DockerEnvironment(image=SANDBOX_IMAGE, cwd="/repo", mount={str(repo_path): "/repo"})

    agent = DefaultAgent(model, env)
    task = f"GitHub issue: {issue_title}\n\n{issue_body}\n\nEdit the code to resolve this, then run `pytest` to confirm it passes."
    agent.run(task)

    # Test gate — never trust the agent's own claim that it's done.
    result = subprocess.run(
        ["docker", "run", "--rm", "-v", f"{repo_path}:/repo", SANDBOX_IMAGE, "pytest", "/repo", "-v"],
        capture_output=True, text=True,
    )
    print(result.stdout)
    return result.returncode == 0


def push_branch_and_open_pr(repo_path: Path, issue_number: int, issue_title: str) -> str:
    branch_name = f"agent/issue-{issue_number}"
    subprocess.run(["git", "-C", str(repo_path), "checkout", "-b", branch_name], check=True)
    subprocess.run(["git", "-C", str(repo_path), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo_path), "commit", "-m", f"Fix: {issue_title} (closes #{issue_number})"],
        check=True,
    )
    subprocess.run(["git", "-C", str(repo_path), "push", "origin", branch_name], check=True)

    repo = gh.get_repo(REPO_NAME)
    pr = repo.create_pull(
        title=f"[agent] {issue_title}",
        body=f"Auto-generated fix for #{issue_number}.\n\nTests passed in sandbox before this PR was opened.\n\n**This PR was not merged automatically — please review and test before merging.**",
        head=branch_name,
        base="main",
    )
    return pr.html_url


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    if payload.get("action") != "opened" or "issue" not in payload:
        return {"status": "ignored"}

    issue = payload["issue"]
    repo_path = clone_repo_to_sandbox(payload["repository"]["clone_url"])

    passed = run_agent_on_issue(issue["title"], issue["body"] or "", repo_path)
    if not passed:
        gh.get_repo(REPO_NAME).get_issue(issue["number"]).create_comment(
            "The agent attempted this issue but its changes didn't pass the test suite. No PR was opened."
        )
        return {"status": "failed_tests"}

    pr_url = push_branch_and_open_pr(repo_path, issue["number"], issue["title"])
    return {"status": "pr_opened", "pr_url": pr_url}
