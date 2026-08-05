Contract: brand-contract v1

# Interface strings

A **decision registry**, not a message catalog. It holds no translations and
does not replace i18n keys. It records which strings have been reconciled
with the voice, which scenario each serves, and where each one lives.

This is what makes "one action, two names" (`B020`) checkable at all. Without
it, that defect is only findable by reading the entire interface — which is
why it survives in every product that has not written one down.

Populated by an inventory sweep at init, not by hand.

| Key | Text (primary) | Location | Scenario | Status |
|---|---|---|---|---|
| <action.project.publish> | <Publish> | <src/ui/ProjectBar.tsx:47> | <SCN-014> | <agreed> |

## Columns

- **Key** — dot-separated, stable, names the action rather than the screen.
  Two rows sharing a `Key` with different `Text` is `B020`.
- **Text (primary)** — the string in the primary locale. Other locales live
  in the project's own i18n files; parity is computed against this column.
- **Location** — `file:line`. A location that no longer resolves is `B023`.
- **Scenario** — the `SCN-NNN` this string serves. A string serving no
  scenario is a question for `ux-scenarios`, not a copy problem.
- **Status** — `agreed` · `proposed` · `drifted` · `orphan`.

## Statuses

| Status | Means |
|---|---|
| `agreed` | reconciled with the voice and approved |
| `proposed` | written, not yet approved |
| `drifted` | the code no longer matches this row (`B021`) |
| `orphan` | in the registry, no longer in the code |

A string found in code with no row here is `B022` — a warning, not an error,
so adopting this registry on an existing product does not block from day one.
It becomes an error only once someone agrees the row.
