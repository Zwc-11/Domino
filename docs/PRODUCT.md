# DOMINO Product

Status: foundation document. Product scope is governed by `AGENTS.md` §1–§3 and `docs/PHASES.md`. This file records product intent; it does not describe implemented functionality (see `docs/STATUS.md`).

## What DOMINO is

An interactive economic simulation system. The central product is an **executable representation of economic relationships**: a company or economic system is modeled as variables and deterministic equations, a user changes an assumption, and the consequences propagate through the model with every step explainable and traceable to evidence.

## What DOMINO is not

- a chatbot
- a stock screener or portfolio tracker
- a stock-price prediction product
- a financial-news summarizer
- a generic RAG wrapper
- a graph visualization demo
- a collection of AI agents

## Core loop

```text
EXPLORE → CHANGE → EXECUTE → PROPAGATE → EXPLAIN → VERIFY → MONITOR
```

| Step | User capability | First phase |
|---|---|---|
| Explore | Open an entity, browse its economic dependencies | 4–5 |
| Change | Modify a variable or assumption | 6 |
| Execute | Run a deterministic scenario | 1 (engine), 3 (API), 6 (UI) |
| Propagate | Watch consequences move through the model | 6 |
| Explain | Inspect calculations, assumptions, uncertainty | 6 |
| Verify | Inspect evidence and provenance; reconstruct what was knowable at a date | 7, 12–13 |
| Monitor | Save a thesis and compare it against later evidence | 14 |

## Primary user

A research-oriented user who needs to understand how an economic assumption (e.g. HBM memory price) propagates into a company's unit economics and margins, and why — not an AI summary of it.

## Product principles

1. **Deterministic numbers.** Authoritative results come from the Economic Compiler, never from an LLM (`AGENTS.md` §3, §13).
2. **Evidence first.** Disclosed facts, derived facts, human assumptions, AI-proposed interpretations, and user scenario assumptions stay distinct (`AGENTS.md` §14).
3. **Unknown is not zero; no fake precision** (`AGENTS.md` §17–§18).
4. **Direct manipulation over chat.** The mobile product centers on graph exploration and shock propagation (`AGENTS.md` §37).
5. **Bounded scope.** First domain: semiconductors. First model: synthetic `AcmeGPU` (`AGENTS.md` §39).

## Kill gate

After Phase 6 (Shock Lab), a new user must be able to open AcmeGPU, change a variable, execute, watch propagation, and understand why. If that interaction is not compelling, the core product is improved before any AI or data infrastructure is built (`AGENTS.md` §59).

## Explicit non-goals

Brokerage integration, real-money trading, stock-price prediction, personalized investment recommendations, social feed, chatbot-first UI, 3D globe, thousands of companies (`AGENTS.md` §58).

## Success metrics (measured from Phase 22)

First-scenario completion, scenarios per active user, evidence inspection rate, second-scenario rate, thesis-save rate, returning research users.
