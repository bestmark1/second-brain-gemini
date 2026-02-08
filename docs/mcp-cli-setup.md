# MCP через mcp-cli

Стабильное подключение к MCP серверам через mcp-cli вместо прямого протокола.

## Зачем это нужно

MCP протокол напрямую иногда отваливается. mcp-cli решает эту проблему:

- **Connection pooling** - daemon держит соединения
- **Auto-retry** - автоматические повторы при сетевых ошибках
- **Стабильность** - работа через bash надёжнее чем MCP протокол напрямую

## Как это работает

```
До:
Gemini → MCP Protocol → Todoist MCP Server → Todoist API
         (отваливается)

После:
Gemini → Bash → mcp-cli → Todoist MCP Server → Todoist API
                (daemon, retry, pooling)
```

---

## Установка

### 1. Установите mcp-cli

```bash
curl -fsSL https://raw.githubusercontent.com/philschmid/mcp-cli/main/install.sh | bash
```

Проверка:
```bash
~/.local/bin/mcp-cli --version
# mcp-cli v0.3.0
```

### 2. Создайте конфиг

```bash
mkdir -p ~/.config/mcp
cat > ~/.config/mcp/mcp_servers.json << 'EOF'
{
  "mcpServers": {
    "todoist": {
      "command": "npx",
      "args": ["-y", "@doist/todoist-ai"],
      "env": {
        "TODOIST_API_KEY": "${TODOIST_API_KEY}"
      }
    }
  }
}
EOF
```

### 3. Добавьте токены в shell

```bash
# Добавить в ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export TODOIST_API_KEY="ваш_токен"' >> ~/.bashrc
source ~/.bashrc
```

### 4. Уберите прямое MCP подключение из Gemini

```bash
# Удалить прямое MCP подключение
gemini mcp remove todoist
```

Проверить что удалено:
```bash
gemini mcp list
# todoist НЕ должен быть в списке
```

Теперь Gemini работает через mcp-cli (bash), а не через MCP протокол напрямую.

---

## Проверка

```bash
# Список инструментов (24 шт)
mcp-cli info todoist

# Тест - задачи на сегодня
mcp-cli call todoist find-tasks-by-date '{"startDate": "today"}'

# Обзор всех проектов
mcp-cli call todoist get-overview '{}'
```

---

## Todoist Tools (24)

### Задачи

| Tool | Описание |
|------|----------|
| `add-tasks` | Создать задачи |
| `update-tasks` | Обновить задачи |
| `complete-tasks` | Завершить задачи |
| `find-tasks` | Поиск по тексту/проекту/label |
| `find-tasks-by-date` | Задачи по дате |
| `find-completed-tasks` | Завершённые задачи |

### Проекты и секции

| Tool | Описание |
|------|----------|
| `add-projects` | Создать проекты |
| `update-projects` | Обновить проекты |
| `find-projects` | Поиск проектов |
| `add-sections` | Создать секции |
| `update-sections` | Обновить секции |
| `find-sections` | Секции проекта |

### Комментарии и коллаборация

| Tool | Описание |
|------|----------|
| `add-comments` | Добавить комментарии |
| `update-comments` | Обновить комментарии |
| `find-comments` | Найти комментарии |
| `find-project-collaborators` | Участники проекта |
| `manage-assignments` | Bulk назначение |

### Общее

| Tool | Описание |
|------|----------|
| `get-overview` | Обзор (markdown) |
| `find-activity` | Лог активности |
| `delete-object` | Удалить объект |
| `fetch-object` | Получить объект |
| `user-info` | Инфо о пользователе |
| `search` | Универсальный поиск |
| `fetch` | Получить по ID |

---

## Примеры команд

### Задачи на сегодня
```bash
mcp-cli call todoist find-tasks-by-date '{"startDate": "today"}'
```

### Создать задачу
```bash
mcp-cli call todoist add-tasks '{"tasks": [{"content": "Тест задача", "dueString": "tomorrow", "priority": 2}]}'
```

### Завершить задачу
```bash
mcp-cli call todoist complete-tasks '{"ids": ["task_id_here"]}'
```

### Поиск задач
```bash
mcp-cli call todoist find-tasks '{"searchText": "проект"}'
```

### Обзор проекта
```bash
mcp-cli call todoist get-overview '{"projectId": "project_id"}'
```

### Найти проекты
```bash
mcp-cli call todoist find-projects '{"search": "Work"}'
```

---

## Отладка

```bash
MCP_DEBUG=1 mcp-cli call todoist find-tasks-by-date '{"startDate": "today"}'
```

---

## Требования

- Node.js 18+ (для npx)
- Todoist API Token (Settings → Integrations → Developer)
