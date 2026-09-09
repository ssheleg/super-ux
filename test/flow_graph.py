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


# --------------------------------------------------------------------------
# CTX-03.03 — coverage and the handoff receipt, on the bounded graph above.

def coverage(graph, walked):
    """Declared vs walked vs NOT_RUN — three states, never two. `walked` is a
    list of {"transition", "from", "to"} records from an actual run."""
    fired = [w.get("transition") for w in walked]
    fired_set = set(fired)
    transitions = {t["id"]: t for t in graph.get("transitions", [])}
    out = {"transitions": {}, "scenarios": {}, "kinds": {}}
    for tid in transitions:
        out["transitions"][tid] = "walked" if tid in fired_set else "NOT_RUN"
    for sc in graph.get("scenarios", []):
        path = sc.get("path", [])
        n = len(path)
        walked_prefix = any(fired[i:i + n] == path for i in range(len(fired) - n + 1))
        out["scenarios"][sc["id"]] = "walked" if walked_prefix else "NOT_RUN"
    declared_absent = set(graph.get("absent", []))
    for kind in sorted(KINDS):
        if kind in declared_absent:
            out["kinds"][kind] = "declared absent"
        elif any(transitions[tid].get("kind") == kind for tid in fired_set
                 if tid in transitions):
            out["kinds"][kind] = "walked"
        else:
            out["kinds"][kind] = "NOT_RUN"
    return out


def smoke(graph, walked):
    """A dead control fails the smoke, by name: a fired transition that moved
    nothing, or a declared transition the smoke never reached."""
    problems = []
    transitions = {t["id"]: t for t in graph.get("transitions", [])}
    for w in walked:
        t = transitions.get(w.get("transition"))
        if t is None:
            problems.append(f"smoke: {w.get('transition')!r} fired but is not "
                            "declared — the page invented a control")
        elif w.get("from") == w.get("to") and t["result"] != t["origin"]:
            problems.append(f"smoke: {t['id']} ({t['action']!r}) is a DEAD "
                            "control — clicked, moved nothing")
    fired = {w.get("transition") for w in walked}
    for tid in sorted(set(transitions) - fired):
        problems.append(f"smoke: {tid} declared but never walked — "
                        "coverage NOT_RUN, and a smoke that skips it is not "
                        "a smoke of this graph")
    return problems


def receipt(graph, walked, artifact_bytes):
    """The persistent handoff record: what was declared, what actually ran,
    pinned to the artifact's exact bytes. It carries NO status axis — a
    preview never upgrades implemented/product evidence — and the production
    gate and the art-direction gate are separate entries a walkthrough
    cannot merge."""
    import hashlib
    for site in (graph, *(w for w in walked if isinstance(w, dict))):
        for f in STATUS_SMUGGLE:
            if f in site:
                raise ValueError(f"receipt: {f!r} has no place here — a preview "
                                 "raises no status (IFP-06)")
    if not walked and artifact_bytes:
        functional = "NOT_RUN — screenshots alone are not a functional pass"
    else:
        functional = "walked" if not smoke(graph, walked) else "FAILED smoke"
    return {
        "artifact_sha256": hashlib.sha256(artifact_bytes or b"").hexdigest(),
        "coverage": coverage(graph, walked),
        "functional": functional,
        "gates": {"production": "separate — code against scenarios (/ux-audit)",
                  "art_direction": "separate — sheleg-design critique"},
    }
