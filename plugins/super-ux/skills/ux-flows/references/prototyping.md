# Prototyping — when the answer is not on paper

Split out of `ux-flows/SKILL.md` on 2026-09-10, when its body measured 4809 tokens
past the house working limit of 4750. This is an OPTIONAL step: a run reaches for it
when a static spec cannot settle the question, which is why it reads better as the
thing you open at that moment than as a section carried through every run.

## Contents

- [Prototyping — when the answer is not on paper](#prototyping--when-the-answer-is-not-on-paper)

Between a designed flow and production code sits a question the documents
cannot settle: does this actually feel right? When it comes up — a state
model nobody can reason about, a layout where two options both look
defensible — build a throwaway prototype that answers exactly that question
and nothing else.

- **Logic question** → the smallest runnable thing that drives the state
  machine through the cases that are hard to hold in the head.
- **Look-and-feel question** → the shortlisted variants on one throwaway
  route, switchable, so they are compared side by side rather than in memory.

Rules: it is throwaway from the first line and named so a reader can tell;
no persistence, no tests, no abstractions; one command to run. When it has
answered its question, fold the decision into the chain and keep the
prototype as a primary source — a throwaway branch with a pointer from the
issue. The main branch keeps the decision, not the sketch.

Skip it when the answer is already obvious; the step exists so that "we
weren't sure and shipped anyway" stops being the default.
