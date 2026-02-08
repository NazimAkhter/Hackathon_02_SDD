# Quickstart Guide: Advanced Scheduling Features

**Feature**: 004-advanced-scheduling
**Purpose**: Quick examples and usage patterns for due dates and recurring tasks

## Basic Usage

### Adding a Todo with Due Date

```
$ python -m todo_app

========== Todo App Menu ==========
1. Add Todo
...
===================================

Enter your choice (1-9): 1

--- Add New Todo ---
Enter title: Submit quarterly report
Enter description (optional, press Enter to skip): Q4 financials to CFO
Enter priority (high/medium/low, press Enter for medium): high
Enter tags (comma-separated, press Enter to skip): work, deadline
Enter due date (YYYY-MM-DD HH:MM, press Enter to skip): 2026-02-15 17:00

✓ Todo added successfully! (ID: 1)
```

**Result**: Todo created with due date Feb 15, 2026 at 5:00 PM

---

### Viewing Todos with Due Dates

```
--- All Todos ---

 ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence
----+--------+----------+--------------------------+----------------------+-----------------------+-------------
  1 | [ ]    | HIGH     | Submit quarterly report  | work, deadline       | 📅 2026-02-15 17:00  |
  2 | [ ]    | MEDIUM   | Buy groceries            | home, errands        | (no due date)        |
  3 | [ ]    | LOW      | Old task from Jan        | admin                | ⚠ 2026-01-20 10:00  |

Total: 3 todos (0 completed, 3 incomplete)
```

**Indicators**:
- `📅` = Due within next 7 days
- `⚠` = Overdue (past due date, not complete)
- `(no due date)` = No due date set

---

### Creating a Recurring Todo

```
Enter your choice (1-9): 1

--- Add New Todo ---
Enter title: Daily standup meeting
Enter description (optional, press Enter to skip): Team sync at 9 AM
Enter priority (high/medium/low, press Enter for medium): medium
Enter tags (comma-separated, press Enter to skip): work, meetings
Enter due date (YYYY-MM-DD HH:MM, press Enter to skip): 2026-02-09 09:00
Enter recurrence (none/daily/weekly/monthly, press Enter for none): daily

✓ Todo added successfully! (ID: 4)
```

**Result**: Recurring todo created. When marked complete, it will automatically reschedule for tomorrow.

---

### Marking a Recurring Todo Complete

```
Enter your choice (1-9): 5

--- Mark Todo as Complete ---
Enter todo ID: 4

Todo marked as complete!
  Title: Daily standup meeting
  Description: Team sync at 9 AM

✓ Next occurrence created automatically! (ID: 5, Due: 2026-02-10 09:00)
```

**Behavior**:
- Original todo (ID 4) marked complete
- New todo (ID 5) created with same title, description, priority, tags
- Due date automatically set to tomorrow (for daily recurrence)

---

### Viewing Upcoming Todos

```
Enter your choice (1-9): 6

--- View Upcoming Todos ---

 ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence
----+--------+----------+--------------------------+----------------------+-----------------------+-------------
  1 | [ ]    | HIGH     | Submit quarterly report  | work, deadline       | 📅 2026-02-15 17:00  |
  5 | [ ]    | MEDIUM   | Daily standup meeting    | work, meetings       | 📅 2026-02-10 09:00  | 🔁 daily

Found 2 upcoming todo(s) due within the next 7 days.
```

**Filter**: Shows only todos due within next 7 days (and not complete)

---

### Viewing Overdue Todos

```
Enter your choice (1-9): 7

--- View Overdue Todos ---

 ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence
----+--------+----------+--------------------------+----------------------+-----------------------+-------------
  3 | [ ]    | LOW      | Old task from Jan        | admin                | ⚠ 2026-01-20 10:00  |
  8 | [ ]    | HIGH     | Missed deadline          | urgent               | ⚠ 2026-02-05 14:00  |

Found 2 overdue todo(s).
```

**Filter**: Shows only todos past their due date (and not complete), sorted by most overdue first

---

### Updating a Todo's Due Date

```
Enter your choice (1-9): 3

--- Update Todo ---
Enter todo ID: 1

Current Todo:
  ID: 1
  Title: Submit quarterly report
  Description: Q4 financials to CFO
  Status: Incomplete
  Priority: HIGH
  Tags: work, deadline
  Due Date: 2026-02-15 17:00
  Recurrence: none

Enter new title (press Enter to keep current):
Enter new description (press Enter to keep current):
Enter new priority (high/medium/low, press Enter to keep current):
Enter new tags (comma-separated, press Enter to keep current):
Enter new due date (YYYY-MM-DD HH:MM, press Enter to keep current): 2026-02-18 12:00
Enter new recurrence (none/daily/weekly/monthly, press Enter to keep current):

✓ Todo updated successfully!
```

**Result**: Due date changed to Feb 18, 2026 at noon

---

### Disabling Recurrence

```
Enter your choice (1-9): 3

--- Update Todo ---
Enter todo ID: 5

Current Todo:
  ID: 5
  Title: Daily standup meeting
  Description: Team sync at 9 AM
  Status: Incomplete
  Priority: MEDIUM
  Tags: work, meetings
  Due Date: 2026-02-10 09:00
  Recurrence: daily

Enter new title (press Enter to keep current):
Enter new description (press Enter to keep current):
Enter new priority (high/medium/low, press Enter to keep current):
Enter new tags (comma-separated, press Enter to keep current):
Enter new due date (YYYY-MM-DD HH:MM, press Enter to keep current):
Enter new recurrence (none/daily/weekly/monthly, press Enter to keep current): none

✓ Todo updated successfully!
```

**Result**: Todo converted from recurring to one-time task. When marked complete, it will NOT reschedule.

---

## Recurrence Examples

### Daily Recurrence

```
Original due date: 2026-02-09 09:00
Mark complete → Next due date: 2026-02-10 09:00 (+1 day)
Mark complete → Next due date: 2026-02-11 09:00 (+1 day)
```

### Weekly Recurrence

```
Original due date: 2026-02-09 14:00 (Sunday)
Mark complete → Next due date: 2026-02-16 14:00 (next Sunday, +7 days)
Mark complete → Next due date: 2026-02-23 14:00 (next Sunday, +7 days)
```

### Monthly Recurrence

```
Original due date: 2026-02-15 10:00
Mark complete → Next due date: 2026-03-15 10:00 (same day next month)
Mark complete → Next due date: 2026-04-15 10:00 (same day next month)
```

### Monthly Recurrence with Non-Existent Date

```
Original due date: 2026-01-31 12:00 (Jan 31)
Mark complete → Next due date: 2026-02-28 12:00 (Feb has no 31st, uses last day)
Mark complete → Next due date: 2026-03-31 12:00 (March 31 exists)
Mark complete → Next due date: 2026-04-30 12:00 (April has no 31st, uses last day)
```

---

## Filtering and Sorting with Due Dates

### Sort by Due Date

```
Enter your choice (1-9): 8

--- Sort Todos ---
1. Sort by Priority (high → medium → low)
2. Sort by Date (newest first)
3. Sort by Date (oldest first)
4. Sort by Title (A-Z)
5. Sort by Due Date (earliest first)
6. Sort by Due Date (latest first)

Enter sort type (1-6): 5

--- Sorted Todos ---

 ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence
----+--------+----------+--------------------------+----------------------+-----------------------+-------------
  3 | [ ]    | LOW      | Old task from Jan        | admin                | ⚠ 2026-01-20 10:00  |
  5 | [ ]    | MEDIUM   | Daily standup meeting    | work, meetings       | 📅 2026-02-10 09:00  | 🔁 daily
  1 | [ ]    | HIGH     | Submit quarterly report  | work, deadline       | 📅 2026-02-15 17:00  |
  2 | [ ]    | MEDIUM   | Buy groceries            | home, errands        | (no due date)        |

Total: 4 todo(s).
```

**Sorting**: Todos with due dates first (earliest to latest), followed by todos without due dates

---

## Error Handling

### Invalid Due Date Format

```
Enter due date (YYYY-MM-DD HH:MM, press Enter to skip): tomorrow

✗ Error: Invalid date format. Please use YYYY-MM-DD HH:MM (e.g., 2026-02-15 14:00)
```

### Invalid Recurrence for Non-Due-Date Todo

```
Enter due date (YYYY-MM-DD HH:MM, press Enter to skip): [Enter pressed]
Enter recurrence (none/daily/weekly/monthly, press Enter for none): daily

✗ Error: Recurring todos require a due date. Please enter a due date or set recurrence to 'none'.
```

### Invalid Recurrence Type

```
Enter recurrence (none/daily/weekly/monthly, press Enter for none): biweekly

✗ Error: Invalid recurrence type. Please enter 'none', 'daily', 'weekly', or 'monthly'.
```

---

## Common Workflows

### Morning Review Workflow

1. View overdue todos: Check what you missed
2. View upcoming todos: See what's due this week
3. Prioritize: Update priorities based on urgency
4. Complete tasks: Mark done, recurring tasks auto-reschedule

### Weekly Planning Workflow

1. Sort by due date: See all deadlines in order
2. Filter by priority + due date: Focus on high-priority upcoming tasks
3. Add recurring tasks: Set up weekly meetings or routines
4. Review and adjust: Update due dates as plans change

### End-of-Day Workflow

1. Mark completed tasks: Triggers auto-rescheduling for recurring tasks
2. Check overdue: Decide whether to reschedule or delete
3. Add tomorrow's tasks: Set due dates for next day
4. Exit: All data saved in memory during session (lost on exit)

---

## Tips

1. **Use Enter to skip**: Quickly add todos without due dates or recurrence
2. **Relative time awareness**: "📅 DUE SOON" indicator helps spot urgent tasks
3. **Disable recurring anytime**: Convert recurring to one-time by updating recurrence to "none"
4. **Delete recurring series**: Delete current instance to stop future rescheduling
5. **Past due dates OK**: System accepts past dates (useful for tracking missed deadlines)
6. **24-hour time format**: Always use HH:MM in 24-hour format (e.g., 14:00 not 2:00 PM)

---

## Limitations

- **In-memory only**: All data lost on exit (no persistence)
- **Session-scoped recurring**: Recurring tasks only reschedule when marked complete during session
- **No natural language**: "tomorrow" or "next week" not supported - use YYYY-MM-DD HH:MM format
- **Simple recurrence only**: Daily, weekly, monthly only - no "every other day" or custom patterns
- **Local time only**: No timezone support - uses system local time
- **Single recurrence per todo**: Cannot set multiple recurrence patterns (e.g., "daily and weekly")

---

## Next Phase Preview (Phase III - Persistence)

Coming in Phase III:
- Due dates and recurring tasks persist across sessions
- Database storage for historical recurring instances
- Due date reminders via notifications
- Calendar view of scheduled tasks
- Timezone support for due dates
