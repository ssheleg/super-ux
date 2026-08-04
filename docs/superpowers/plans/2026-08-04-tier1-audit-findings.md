# Plan — тир 1 находок аудита

**Спека:** `docs/superpowers/specs/2026-08-04-tier1-audit-findings-design.md`

Задачи идут строго по порядку: каждая следующая опирается на зелёный результат
предыдущей. Файлы не пересекаются между задачами, кроме отмеченных.

| # | Задача | Файлы | REQ | Definition of done |
|---|---|---|---|---|
| T1 | `validate_catalog()` по TDD | `test/validate.py` | REQ-06 | пять видов подсаженного дефекта дают наблюдаемое падение; на текущем каталоге (146 записей) — зелено |
| T2 | Таксономия и коды источников | `skills/references/best-practices.md` (шапка) | REQ-07 | теги `virality`/`referral`/`auth` в таксономии; `[NIST]`/`[Viral26]` в ключе источников |
| T3 | Кластер виральности BP-147..151 + правка ссылки в BP-067 | `best-practices.md` | REQ-01 | записи есть; BP-067 ссылается на `BP-147..151`; `grep -c "growth loop"` не даёт неразрешённых упоминаний |
| T4 | Пустое состояние BP-152 | `best-practices.md` | REQ-02 | запись есть, три слоя NN/g названы |
| T5 | Пароли и восстановление формы BP-153..156 | `best-practices.md` | REQ-03 | `grep -ci password` > 0; BP-156 ссылается на PRN-09 |
| T6 | Маршрутизация | `skills/references/practice-selection.md` | REQ-05 | диапазон `BP-001..156`; каждая новая запись достижима; `validate_catalog` зелёный |
| T7 | Секция границ охвата | `skills/references/scenario-format.md`, `skills/ux-audit/SKILL.md`, `templates/audit-report.md` | REQ-04 | секция в формате отчёта; скил требует её в DoD; шаблон содержит заготовку |
| T8 | Синк и валидатор | копии в четырёх скилах | REQ-08 | `sync_references.py` затем `validate.py` — оба зелёные |
| T9 | Счётчики | `README.md`, `CHANGELOG.md` | REQ-09 | число практик согласовано везде |
| T10 | Мердж и релиз | `package.json`, `plugin.json`, `marketplace.json`, `CHANGELOG.md` | REQ-10 | четырёхсторонняя сверка; тег `v0.27.0`; рабочее дерево чисто и запушено |
| T11 | Доки, wiki, ретро, приёмка | wiki, `docs/superpowers/retro.md` | REQ-11, REQ-12 | wiki отражает новый счёт; ретро со штампом; обход лестницы по каждому REQ |

## Human steps (единственный блок)

1. `npm publish` — 2FA, выполняется оператором после того, как тег запушен и
   GitHub-релиз собран.

После него автономная часть продолжается: обновление локальных копий (REQ-11).
