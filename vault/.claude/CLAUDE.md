# Agent Second Brain

Voice-first personal assistant for capturing thoughts and managing tasks via Telegram.

## EVERY SESSION BOOTSTRAP

**Before doing anything else, read these files in order:**

1. `vault/MEMORY.md` — curated long-term memory (preferences, decisions, context)
2. `vault/daily/YYYY-MM-DD.md` — today's entries
3. `vault/daily/YYYY-MM-DD.md` — yesterday's entries (for continuity)
4. `vault/goals/3-weekly.md` — this week's ONE Big Thing

**Don't ask permission, just do it.** This ensures context continuity across sessions.

---

## SESSION END PROTOCOL

**Before ending a significant session, write to today's daily:**

```markdown
## HH:MM [text]
Session summary: [what was discussed/decided/created]
- Key decision: [if any]
- Created: [[link]] [if any files created]
- Next action: [if any]
```

**Also update `vault/MEMORY.md` if:**
- New key decision was made
- User preference discovered
- Important fact learned
- Active context changed significantly

---

## Mission

Help user stay aligned with goals, capture valuable insights, and maintain clarity.

## Directory Structure

| Folder | Purpose |
|--------|---------|
| `daily/` | Raw daily entries (YYYY-MM-DD.md) |
| `goals/` | Goal cascade (3y → yearly → monthly → weekly) |
| `thoughts/` | Processed notes by category |
| `MOC/` | Maps of Content indexes |
| `attachments/` | Photos by date |

## Current Focus

See [[goals/3-weekly]] for this week's ONE Big Thing.
See [[goals/2-monthly]] for monthly priorities.

## Goals Hierarchy

```
goals/0-vision-3y.md    → 3-year vision by life areas
goals/1-yearly-2025.md  → Annual goals + quarterly breakdown
goals/2-monthly.md      → Current month's top 3 priorities
goals/3-weekly.md       → This week's focus + ONE Big Thing
```

## Entry Format

```markdown
## HH:MM [type]
Content
```

Types: `[voice]`, `[text]`, `[forward from: Name]`, `[photo]`

## Processing Workflow

Run daily processing via `/process` command or automatically at 21:00.

### Process Flow:
1. Read goals/ → understand priorities
2. Check Todoist → know workload
3. Read daily/ → classify entries
4. Create tasks → aligned with goals
5. Save thoughts → build [[links]]
6. Generate HTML report → send to Telegram

## Available Skills

| Skill | Purpose |
|-------|---------|
| `dbrain-processor` | Main daily processing |
| `todoist-ai` | Task management via MCP |
| `graph-builder` | Vault link analysis and building |

## Available Agents

| Agent | Purpose |
|-------|---------|
| `weekly-digest` | Weekly review with goal progress |
| `goal-aligner` | Check task-goal alignment |
| `note-organizer` | Organize vault, fix links |
| `inbox-processor` | GTD-style inbox processing |

## Path-Specific Rules

See `.claude/rules/` for format requirements:
- `daily-format.md` — daily files format
- `thoughts-format.md` — thought notes format
- `goals-format.md` — goals format
- `telegram-report.md` — HTML report format

## MCP Servers

- `todoist` — Task management (add, find, complete tasks)
- `filesystem` — Vault file access

## CRITICAL: Tool Usage Policy

**ТЫ ОБЯЗАН ВЫЗЫВАТЬ MCP TOOLS НАПРЯМУЮ.**

Не существует ситуации, когда MCP tools "недоступны". Если ты получил эту инструкцию — у тебя есть доступ к:

- `todoist__*` — все Todoist операции
- File read/write — все файловые операции

ЗАПРЕЩЁННЫЕ ПАТТЕРНЫ (НИКОГДА не делай это):
- "MCP недоступен в текущем режиме"
- "Не удалось добавить автоматически"
- "Добавь вручную: ..."
- Любые инструкции для ручного выполнения

ПРАВИЛЬНЫЙ ПАТТЕРН:
1. Вызвать todoist__add-tasks tool
2. Получить результат (успех или ошибка)
3. Включить результат в HTML отчёт

При ошибке — показать ТОЧНУЮ ошибку от tool, не придумывать отговорки.

## Report Format

Reports use Telegram HTML:
- `<b>bold</b>` for headers
- `<i>italic</i>` for metadata
- Only allowed tags: b, i, code, pre, a

## Quick Commands

| Command | Action |
|---------|--------|
| `/process` | Run daily processing |
| `/do` | Execute arbitrary request |
| `/weekly` | Generate weekly digest |
| `/align` | Check goal alignment |
| `/organize` | Organize vault |
| `/graph` | Analyze vault links |

## /do Command Context

When invoked via /do, Gemini receives arbitrary user requests. Common patterns:

**Task Management:**
- "перенеси просроченные задачи на понедельник"
- "покажи задачи на сегодня"
- "добавь задачу: позвонить клиенту"
- "что срочного на этой неделе?"

**Vault Queries:**
- "найди заметки про AI"
- "что я записал сегодня?"
- "покажи итоги недели"

**Combined:**
- "создай задачу из первой записи сегодня"
- "перенеси всё с сегодня на завтра"

## MCP Tools Available

**Todoist (todoist__*):**
- `add-tasks` — создать задачи
- `find-tasks` — найти задачи по тексту
- `find-tasks-by-date` — задачи за период
- `update-tasks` — изменить задачи
- `complete-tasks` — завершить задачи
- `user-info` — информация о пользователе

**Filesystem:**
- Read/write vault files
- Access daily/, goals/, thoughts/

## Customization

For personal overrides: create `CLAUDE.local.md`

## Graph Builder

Analyze and maintain vault link structure. Use `/graph` command or invoke `graph-builder` skill.

**Commands:**
- `/graph analyze` — Full vault statistics
- `/graph orphans` — List unconnected notes
- `/graph suggest` — Get link suggestions
- `/graph add` — Apply suggested links

**Scripts:**
- `uv run .claude/skills/graph-builder/scripts/analyze.py` — Graph analysis
- `uv run .claude/skills/graph-builder/scripts/add_links.py` — Link suggestions

See `skills/graph-builder/` for full documentation.

## Learnings (from experience)

1. **Don't rewrite working code** without reason (KISS, DRY, YAGNI)
2. **Don't add checks** that weren't there — let the agent decide
3. **Don't propose solutions** without studying git log/diff first
4. **Don't break architecture** (process.sh → Gemini → skill is correct)
5. **Problems are usually simple** (e.g., sed one-liner for HTML fix)

---

*System Version: 2.3*
*Updated: 2026-02-01*
