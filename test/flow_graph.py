#!/usr/bin/env python3
"""The bounded scenario graph validator — executable half of
`plugins/super-ux/skills/references/interactive-flow-prototypes.md` (CTX-03.01).

`validate_graph(graph)` returns a list of problems, empty when the graph is
sound. Each problem names its IFP rule, so a refusal is a pointer into the
contract rather than a shrug. Python stdlib only.
"""
KINDS = {"happy", "error", "recovery", "back", "cancel", "returning", "external"}
STATUS_SMUGGLE = ("status", "implemented", "product")


def validate_graph(graph):
    problems = []
    if not isinstance(graph, dict):
        return ["graph: not an object"]

    def smuggled(obj, where):
        for f in STATUS_SMUGGLE:
            if isinstance(obj, dict) and f in obj:
                problems.append(f"IFP-06 {where}: carries `{f}` — a preview "
                                "raises no status; that axis lives in "
                                "docs/ux/scenarios.md and moves by its own rules")

    smuggled(graph, "graph")
    screens = graph.get("screens", [])
    transitions = graph.get("transitions", [])
    scenarios = graph.get("scenarios", [])
    externals = graph.get("external", [])
    entry = graph.get("entry")

    screen_ids = set()
    for i, s in enumerate(screens):
        where = f"screens[{i}]"
        if not isinstance(s, dict) or not s.get("id"):
            problems.append(f"IFP-02 {where}: screen without an id")
            continue
        smuggled(s, where)
        if s["id"] in screen_ids:
            problems.append(f"IFP-02 {where}: duplicate screen id {s['id']!r}")
        screen_ids.add(s["id"])

    ext_ids = set()
    for i, e in enumerate(externals):
        where = f"external[{i}]"
        eid = e.get("id") if isinstance(e, dict) else None
        if not eid or not str(eid).startswith("external:"):
            problems.append(f"IFP-05 {where}: an external destination is named "
                            "`external:<name>`, explicitly")
            continue
        if e.get("mock") != "explicit":
            problems.append(f"IFP-05 {where}: {eid} without `mock: explicit` — "
                            "a stand-in that does not declare itself is a "
                            "functional claim the preview cannot back")
        ext_ids.add(eid)

    if entry not in screen_ids:
        problems.append(f"IFP-03 graph: entry {entry!r} is not a declared screen")

    targets = screen_ids | ext_ids
    outgoing, incoming = {}, set()
    for i, t in enumerate(transitions):
        where = f"transitions[{i}]"
        if not isinstance(t, dict):
            problems.append(f"IFP-01 {where}: not an object")
            continue
        smuggled(t, where)
        missing = [f for f in ("origin", "action", "result") if not t.get(f)]
        if missing:
            problems.append(f"IFP-01 {where}: missing {'/'.join(missing)} — a "
                            "transition is origin/action/result, all three")
            continue
        if t["origin"] not in screen_ids:
            problems.append(f"IFP-02 {where}: origin {t['origin']!r} is not a "
                            "declared screen")
        if t["result"] not in targets:
            problems.append(f"IFP-02 {where}: result {t['result']!r} resolves to "
                            "no declared screen or external destination")
        if t.get("kind") not in KINDS:
            problems.append(f"IFP-04 {where}: kind {t.get('kind')!r} is not one "
                            f"of {sorted(KINDS)}")
        outgoing.setdefault(t["origin"], []).append(t["result"])
        incoming.add(t["result"])

    if entry in screen_ids:
        seen, stack = set(), [entry]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(r for r in outgoing.get(cur, []) if r in screen_ids)
        for sid in sorted(screen_ids - seen):
            problems.append(f"IFP-03 graph: {sid} is unreachable from {entry} — "
                            "a declared screen no path enters")
        for sid in sorted(screen_ids):
            terminal = sid in {t.get("result") for t in transitions
                               if isinstance(t, dict)} and not outgoing.get(sid)
            if terminal and graph.get("terminal") != sid \
                    and sid not in set(graph.get("terminals", [])):
                problems.append(f"IFP-03 graph: {sid} has no way out and is not "
                                "declared terminal — a dead end the demo path "
                                "would hide")

    covered = {t.get("kind") for t in transitions if isinstance(t, dict)}
    covered |= {s.get("kind") for s in scenarios if isinstance(s, dict)}
    declared_absent = set(graph.get("absent", []))
    for kind in sorted(KINDS - covered - declared_absent):
        problems.append(f"IFP-04 graph: kind {kind!r} has no coverage and is "
                        "not declared absent — silence is not a coverage state")

    for i, s in enumerate(scenarios):
        where = f"scenarios[{i}]"
        if isinstance(s, dict):
            smuggled(s, where)
            tids = {t.get("id") for t in transitions if isinstance(t, dict)}
            for step in s.get("path", []):
                if step not in tids:
                    problems.append(f"IFP-02 {where}: path step {step!r} names "
                                    "no declared transition")
    return problems
