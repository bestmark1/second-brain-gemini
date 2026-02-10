# Todoist Integration

<!--
╔══════════════════════════════════════════════════════════════════╗
║  КАК НАСТРОИТЬ ЭТОТ ФАЙЛ                                         ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Замените [Your Clients] на имена ваших клиентов              ║
║  2. Замените [Your Company] на название вашей компании           ║
║  3. Замените [@your_channel] на ваш Telegram-канал               ║
║  4. Измените примеры задач на релевантные для вас                ║
║  5. Удалите этот комментарий после настройки                     ║
╚══════════════════════════════════════════════════════════════════╝
-->

## Available MCP Tools

### Reading Tasks
- `get-overview` — all projects with hierarchy
- `find-tasks` — search by text, project, section
- `find-tasks-by-date` — tasks by date range

### Writing Tasks
- `add-tasks` — create new tasks
- `complete-tasks` — mark as done
- `update-tasks` — modify existing

---

## Pre-Creation Checklist

### 1. Check Workload (REQUIRED)

```
find-tasks-by-date:
  startDate: "today"
  daysCount: 7
  limit: 50
```

Build workload map:
```
Mon: 2 tasks
Tue: 4 tasks  ← overloaded
Wed: 1 task
Thu: 3 tasks  ← at limit
Fri: 2 tasks
Sat: 0 tasks
Sun: 0 tasks
```

### 2. Check Duplicates (REQUIRED)

```
find-tasks:
  searchText: "key words from new task"
```

If similar exists → mark as duplicate, don't create.

---

## Priority by Domain

Based on user's work context (see [ABOUT.md](ABOUT.md)):

| Domain | Default Priority | Override |
|--------|-----------------|----------|
| Client Work | p1-p2 | — |
| Agency Ops (urgent) | p2 | — |
| Agency Ops (regular) | p3 | — |
| Content (with deadline) | p2-p3 | — |
| Product/R&D | p4 | масштабируемость → p3 |
| AI & Tech | p4 | автоматизация → p3 |

### Priority Keywords

| Keywords in text | Priority |
|-----------------|----------|
| срочно, критично, дедлайн клиента | p1 |
| важно, приоритет, до конца недели | p2 |
| нужно, надо, не забыть | p3 |
| (strategic, R&D, long-term) | p4 |

### Apply Decision Filters for Priority Boost

If entry matches 2+ filters → boost priority by 1 level:
- Это масштабируется?
- Это можно автоматизировать?
- Это усиливает экспертизу/бренд?
- Это приближает к продукту/SaaS?

---

## Date Mapping

| Context | dueString |
|---------|-----------|
| **Client deadline** | exact date |
| **Urgent ops** | today / tomorrow |
| **This week** | friday |
| **Next week** | next monday |
| **Strategic/R&D** | in 7 days |
| **Not specified** | in 3 days |

### Russian → dueString

| Russian | dueString |
|---------|-----------|
| сегодня | today |
| завтра | tomorrow |
| послезавтра | in 2 days |
| в понедельник | monday |
| в пятницу | friday |
| на этой неделе | friday |
| на следующей неделе | next monday |
| через неделю | in 7 days |
| 15 января | January 15 |

---

## Task Creation

```
add-tasks:
  tasks:
    - content: "Task title"
      dueString: "friday"  # MANDATORY
      priority: "p4"       # based on domain
      projectId: "..."     # if known
```

### Task Title Style

User prefers: прямота, ясность, конкретика

<!-- Замените примеры на релевантные для вас -->
✅ Good:
- "Отправить презентацию клиенту"
- "Созвон с командой по проекту"
- "Написать пост про [тема]"

❌ Bad:
- "Подумать о презентации"
- "Что-то с клиентом"
- "Разобраться с AI"

### Workload Balancing

If target day has 3+ tasks:
1. Find next day with < 3 tasks
2. Use that day instead
3. Mention in report: "сдвинуто на {day} (перегрузка)"

---

## Project Detection

<!--
Настройте под свои проекты в Todoist.
Замените примеры клиентов и название канала.
-->

| Keywords | Project |
|----------|---------|
| [Your Client Names], клиент, бренд | Client Work |
| [Your Company], команда, найм, процессы | Company Ops |
| продукт, SaaS, MVP | Product |
| пост, [@your_channel], контент | Content |

If unclear → use Inbox (no projectId).

---

## Anti-Patterns (НЕ СОЗДАВАТЬ)

Based on user preferences:

- ❌ "Подумать о..." → конкретизируй действие
- ❌ "Разобраться с..." → что именно сделать?
- ❌ Абстрактные задачи без Next Action
- ❌ Дубликаты существующих задач
- ❌ Задачи без дат

---

## Error Handling

CRITICAL: Никогда не предлагай "добавить вручную".

If `add-tasks` fails:
1. Include EXACT error message in report
2. Continue with next entry
3. Don't mark as processed
4. User will see error and can debug

WRONG output:
  "Не удалось добавить (MCP недоступен). Добавь вручную: Task title"

CORRECT output:
  "Ошибка создания задачи: [exact error from MCP tool]"
