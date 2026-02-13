# Entry Classification

<!--
╔══════════════════════════════════════════════════════════════════╗
║  КАК НАСТРОИТЬ ЭТОТ ФАЙЛ                                         ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Замените [Your Client Names] на имена ваших клиентов        ║
║  2. Замените [Your Company] на название вашей компании          ║
║  3. Замените [@your_channel] на ваш Telegram-канал              ║
║  4. Добавьте свои домены работы, если они отличаются            ║
║  5. Удалите этот комментарий после настройки                    ║
╚══════════════════════════════════════════════════════════════════╝
-->

## Work Domains → Categories

Based on user's work context (see [ABOUT.md](ABOUT.md)):

### Client Work
Брифы, стратегии, креатив, кампании, KPI, предложения

<!-- Добавьте имена ваших клиентов через запятую -->
**Keywords:** [Your Client Names], клиент, бриф, презентация, дедлайн, KPI

**→ Category:** task (p1-p2) → Todoist

### AI & Tech
Инструменты, модели, промпты, пайплайны, агенты

**Keywords:** GPT, Claude, модель, агент, API, пайплайн, автоматизация, интеграция

**→ Category:** learning или project → thoughts/

### Product
Идеи, гипотезы, MVP, юнит-экономика

**Keywords:** продукт, SaaS, MVP, гипотеза, монетизация, юнит-экономика, стартап

**→ Category:** idea или project → thoughts/

### Company Ops
Команда, процессы, автоматизация, найм, управление, финансы

<!-- Замените [Your Company] на название вашей компании/проекта -->
**Keywords:** команда, найм, процесс, HR, финансы, [Your Company]

**→ Category:** task или project (depends on urgency)

### Content
Посты, идеи, тезисы для Telegram и LinkedIn

<!-- Замените [@your_channel] на ваш Telegram-канал или удалите если не нужно -->
**Keywords:** пост, [@your_channel], LinkedIn, контент, тезис, статья

**→ Category:** idea → thoughts/ideas/ или task если с дедлайном

---

## Decision Tree

```
Entry text contains...
│
├─ Client brand or deadline? ────────────────────> TASK (p1-p2)
│  ([Your Clients], клиент, дедлайн, презентация)
│
├─ Operational/urgent? ──────────────────────────> TASK (p2-p3)
│  (нужно сделать, не забыть, позвонить, встреча)
│
├─ AI/tech learning? ────────────────────────────> LEARNING
│  (узнал, модель, агент, интеграция)
│
├─ Product/SaaS idea? ───────────────────────────> IDEA или PROJECT
│  (продукт, MVP, гипотеза, SaaS)
│
├─ Strategic thinking? ──────────────────────────> PROJECT
│  (стратегия, план, R&D, долгосрочно)
│
├─ Personal insight? ────────────────────────────> REFLECTION
│  (понял, осознал, философия)
│
└─ Content idea? ────────────────────────────────> IDEA
   (пост, тезис, контент)
```

## Apply Decision Filters

Перед сохранением спроси:
- Это масштабируется?
- Это можно автоматизировать?
- Это усиливает экспертизу или бренд?
- Это приближает к продукту или SaaS?

Если да на 2+ вопроса → повысить приоритет.

---

## Photo Entries

For `[photo]` entries:

1. Analyze image content via vision
2. Determine domain:
   - Screenshot клиентского материала → Client Work
   - Схема/диаграмма → AI & Tech или Product
   - Текст/статья → Learning
3. Add description to daily file

---

## Output Locations

| Category | Destination | Priority |
|----------|-------------|----------|
| task (client) | Todoist | p1-p2 |
| task (ops) | Todoist | p2-p3 |
| task (content) | Todoist | p3-p4 |
| idea | thoughts/ideas/ | — |
| reflection | thoughts/reflections/ | — |
| project | thoughts/projects/ | — |
| learning | thoughts/learnings/ | — |

---

## File Naming

```
thoughts/{category}/{YYYY-MM-DD}-short-title.md
```

Examples:
```
thoughts/ideas/2024-12-16-saas-pricing-model.md
thoughts/projects/2024-12-16-ai-agents-pipeline.md
thoughts/learnings/2024-12-16-claude-mcp-setup.md
```

---

## Thought Structure

Use preferred format:

```markdown
---
date: {YYYY-MM-DD}
type: {category}
domain: {Client Work|AI & Tech|Product|Agency Ops|Content}
tags: [tag1, tag2]
---

## Context
[Что привело к мысли]

## Insight
[Ключевая идея]

## Implication
<!-- Замените [Your Company] на название вашей компании -->
[Что это значит для [Your Company]/продукта/стратегии]

## Next Action
[Конкретный шаг — не абстрактный]
```

---

## Anti-Patterns (ИЗБЕГАТЬ)

При создании мыслей НЕ делать:
- Абстрактные рассуждения без Next Action
- Академическая теория без применения к вашему проекту/продукту
- Повторы без синтеза (кластеризуй похожие!)
- Хаотичные списки без приоритетов
- Задачи типа "подумать о..." (конкретизируй!)

---

## MOC Updates

After creating thought file, add link to:
```
MOC/MOC-{category}s.md
```

Group by domain when relevant:
```markdown
## AI & Tech
- [[2024-12-16-claude-mcp-setup]] - MCP integration

## Product
- [[2024-12-16-saas-pricing-model]] - Pricing research
```
