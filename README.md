# Бот для подготовки к ЕГЭ по физике

Бот предназначен для помощи школьникам в подготовке к Единому Государственному Экзамену (ЕГЭ) по физике. Он предоставляет задачи, теорию и автоматическую проверку ответов.

---

## Возможности бота

### 1. **Классификация задач по темам**
   - Поддержка всех разделов физики из кодификатора ЕГЭ: механика, термодинамика, электродинамика, оптика, квантовая физика и др.
   - Возможность запроса задач в формате, аналогичном экзаменационным бланкам (с кратким или развернутым ответом).

### 2. **Теоретические материалы**
   - Краткие конспекты по каждой теме с формулами, графиками и схемами.

### 3. **Проверка ответов**
   - Автоматическая верификация числовых ответов (с учетом погрешности) и текстовых вариантов (множественный выбор).
   - Пояснения к решениям с подробными комментариями.

### Дополнительные функции:
- Планировщик занятий с рекомендациями по расписанию.
- Визуализация прогресса (графики и диаграммы).
- Уведомления о повторении тем.
- Поддержка русского и английского языков (опционально).

---

## Техническая реализация

### Используемые технологии
- **Язык программирования:** Python 3.11+.
- **Фреймворк:** PyTelegramBotAPI (telebot-4.26.0) (для интеграции с Telegram).
- **База данных:** JSON (хранение задач, теорий).

### Архитектура
1. **Модуль взаимодействия с пользователем:**
   - Обработка команд Telegram.
   - Валидация ввода.
   - Генерация клавиатур и интерактивных кнопок.

2. **Модуль задач:**
   - Парсинг задач из открытых банков ФИПИ.
   - Классификация по темам и сложности.
   - Алгоритм выдачи задач на основе прогресса пользователя.

3. **Модуль теории:**
   - Хранение структурированных материалов в формате Markdown.
   - Поиск по ключевым словам.

4. **Аналитический модуль:**
   - Сбор статистики (правильные/неправильные ответы, время решения).
   - Формирование персональных рекомендаций.

### Структура проекта
```bash
├── src/
│   ├── electrodynamics/
│   │   ├── electric-field/
│   │   │   ├── tasks/     # директория с задачами
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── electric-field.pdf  # файл с теорией
│   │   ├── electromagnetic-induction/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── electromagnetic-induction.pdf
│   │   ├── electromagnetic-oscillations-and-waves/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── electromagnetic-oscillations-and-waves.pdf
│   │   ├── fundamentals-of-the-special-theory-of-relativity/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── fundamentals-of-the-special-theory-of-relativity.pdf
│   │   ├── laws-of-direct-curent/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── laws-of-direct-curent.pdf
│   │   └──  magnetic-field/
│   │       ├── tasks/
│   │       │   ├── task-1.md
│   │       │   ├── task-2.md
│   │       │   ├── ...
│   │       │   └── task-n.md
│   │       └── magnetic-field.pdf
│   ├── mechanics/
│   │   ├── conversation-law-in-mechanics/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── theory.pdf
│   │   ├── dynamics/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── theory.pdf
│   │   ├── kinematics/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── kinematics.pdf
│   │   └── mechanical-vibrations-and-waves/
│   │       ├── tasks/
│   │       │   ├── task-1.md
│   │       │   ├── task-2.md
│   │       │   ├── ...
│   │       │   └── task-n.md
│   │       └── mechanical-vibrations-and-waves.pdf
│   ├── quantum-physics/
│   │   ├── wave-particle-duality
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── wave-particle-duality.pdf
│   │   ├── atomic-physics/
│   │   │   ├── tasks/
│   │   │   │   ├── task-1.md
│   │   │   │   ├── task-2.md
│   │   │   │   ├── ...
│   │   │   │   └── task-n.md
│   │   │   └── atomic-physics.pdf
│   │   └── physics-of-the-atomic-nucleus/
│   │       ├── tasks/
│   │       │   ├── task-1.md
│   │       │   ├── task-2.md
│   │       │   ├── ...
│   │       │   └── task-n.md
│   │       └── physics-of-the-atomic-nucleus.pdf
│   └── thermodynamics/
│       ├── molecular-physics-and-thermodynamics/
│       │   ├── tasks/
│       │   │   ├── task-1.md
│       │   │   ├── task-2.md
│       │   │   ├── ...
│       │   │   └── task-n.md
│       │   └── molecular-physics-and-thermodynamics.pdf
│       └── thermodynamics-theme/
│           ├── tasks/
│           │   ├── task-1.md
│           │   ├── task-2.md
│           │   ├── ...
│           │   └── task-n.md
│           └── thermodynamics-theme.pdf
├── themes.json        # JSON-файл с темами
├── config.json        # JSON-файл с конфигом бота (создать)
├── scripts.json       # файл для изменения скриптованных фраз
└── main.py            # основной файл проекта
```