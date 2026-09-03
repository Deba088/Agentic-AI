# AGENTS.md — AI Agent Workflow & Python Development Rules

This file guides AI coding agents (Claude Code, Cursor, Copilot) when working in this repository. Follow these constraints strictly.

## 1. Project Overview & Tech Stack
This project is an AI Agent system built using Python. It relies on an event-driven workflow loop consisting of Planning, Execution, Tool Usage, and Self-Correction.

- **Python Version:** 3.11+
- **Dependency Manager:** Poetry (Use `poetry run python` and `poetry add`)
- **Core Frameworks:** LangGraph / CrewAI / Autogen (Adapt to existing imports)
- **Primary LLM Provider:** Anthropic Claude (via `anthropic` Python SDK)

## 2. Core Python Architecture Rules
- **Async First:** All network calls, LLM invocations, and tool activities must use async/await patterns (`asyncio`).
- **Strict Typing:** Every function signature must contain Type Hints. Use `typing.Protocol` for agent tools.
- **State Management:** Agent state must be immutable. Use Pydantic v2 BaseModels for state payload transitions.
- **Dependency Injection:** Pass clients (e.g., Anthropic client) into agent classes via `__init__`; do not instantiate clients globally.

## 3. Specific AI Agent Workflow Constraints
When writing or modifying agent loop workflows, you MUST enforce the following architecture:
- **Tool Call Safety:** Never allow an agent to execute raw shell commands or raw SQL directly without a deterministic regex or Pydantic validation gate.
- **Token Control:** Always implement a max-turn limit (e.g., max 10 loops) inside `while` loops or agent execution graphs to prevent runaway token spend.
- **Fallbacks:** Every LLM API call must use an explicit exception handler fallback (e.g., switch from `claude-3-5-sonnet` to `claude-3-haiku` if a rate limit or 5xx occurs).

## 4. Coding Conventions & Code Quality Gates
- **Formatting:** Code must comply with Black formatting and Ruff linting rules. 
- **Documentation:** Every class and public method requires a Google-style docstring explaining parameters, return types, and agent intent.
- **Idiomatic Style:** Prefer functional composition and standard library implementations over pulling in minor third-party micro-dependencies.

## 5. Development & Test Commands
Always run validation gates before marking a task complete:
- **Install Dependencies:** `poetry install`
- **Format Check:** `poetry run ruff check .`
- **Run Agent Tests:** `poetry run pytest tests/`
- **Run Live Mock Loop:** `poetry run python -m src.main --mock`

## 6. Execution Constraints (Do Not Violate)
- **NEVER** edit or alter `.env` or configurations containing API keys directly.
- **NEVER** write endless loop logic without an explicit break threshold or timeout flag.
- **NEVER** drop or skip test assertions (`assert response is not None`).