# Feature Specification: Advanced Scheduling Features for In-Memory Python Console Todo App

**Feature Branch**: `004-advanced-scheduling`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Advanced Features for In-Memory Python Console Todo App - Enhancing the in-memory console todo app with recurring tasks and due date reminders. Target audience: Developers adding intelligent scheduling features to a console-based todo app."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Due Date to Todos (Priority: P1)

As a user, I want to assign a due date and time to each todo so I can track when tasks need to be completed and prioritize work based on deadlines.

**Why this priority**: Due dates are the foundation of time-based task management. Without due dates, recurring tasks and overdue notifications cannot function. This is the most critical feature that enables all other scheduling capabilities.

**Independent Test**: Can be fully tested by creating a todo with a specific due date, viewing it in the list to confirm the due date is displayed, and verifying that the due date persists in memory throughout the session.

**Acceptance Scenarios**:

1. **Given** the console app is running, **When** I add a new todo and enter a due date "2026-02-15 14:00", **Then** the todo is created with the due date displayed alongside other attributes
2. **Given** I have an existing todo without a due date, **When** I update it to add due date "2026-02-20 09:30", **Then** the todo displays the new due date
3. **Given** the console app is running, **When** I add a new todo and press Enter to skip the due date prompt, **Then** the todo is created with no due date (None)
4. **Given** the console app is running, **When** I enter an invalid due date format "tomorrow" or "15/02/2026", **Then** the system displays an error message and prompts for a valid format (YYYY-MM-DD HH:MM)
5. **Given** I have an existing todo with a due date, **When** I view all todos, **Then** todos are displayed with their due dates in a human-readable format (e.g., "2026-02-15 14:00" or "in 7 days")

---

### User Story 2 - View Upcoming and Overdue Todos (Priority: P1)

As a user, I want to see which todos are due soon or overdue so I can focus on the most time-sensitive tasks first.

**Why this priority**: Displaying upcoming and overdue todos is the immediate value delivery from due dates. Users need to quickly identify what requires urgent attention. This complements US1 and provides actionable insights without additional features.

**Independent Test**: Can be fully tested by creating todos with various due dates (past, today, future), viewing the list, and confirming that overdue tasks are visually distinguished (e.g., marked with a warning indicator) and upcoming tasks within the next 7 days are highlighted.

**Acceptance Scenarios**:

1. **Given** I have 5 todos with varying due dates, **When** I view all todos, **Then** overdue todos are marked with a visual indicator (e.g., "⚠ OVERDUE") and displayed first in the list
2. **Given** I have todos due today, tomorrow, and next week, **When** I view all todos, **Then** todos due within the next 7 days show a "📅 DUE SOON" indicator
3. **Given** the console app is running, **When** I select "View Upcoming Todos", **Then** the system displays only todos due within the next 7 days, sorted by due date (earliest first)
4. **Given** the console app is running, **When** I select "View Overdue Todos", **Then** the system displays only todos with due dates in the past that are not yet complete, sorted by how overdue they are (most overdue first)
5. **Given** a todo becomes overdue (due date passes), **When** I view the list, **Then** the todo automatically appears in the overdue section without requiring manual refresh

---

### User Story 3 - Create Recurring Todos (Priority: P2)

As a user, I want to mark a todo as recurring (daily, weekly, or monthly) so I don't have to manually recreate regular tasks.

**Why this priority**: Recurring tasks automate repetitive todo creation. This is the second most valuable feature after due dates, as many users have routine tasks. However, it depends on US1 (due dates) to determine when the next occurrence should be scheduled.

**Independent Test**: Can be fully tested by creating a recurring todo (e.g., "daily"), marking it complete, and verifying that a new instance of the todo is automatically created with the next due date (e.g., tomorrow for daily recurrence).

**Acceptance Scenarios**:

1. **Given** the console app is running, **When** I add a new todo and select recurrence type "daily", **Then** the todo is created as a recurring task with the next due date set to tomorrow
2. **Given** I have a recurring todo with recurrence "weekly", **When** I mark it as complete, **Then** a new instance of the todo is automatically created with the due date set to 7 days from the original due date
3. **Given** I have a recurring todo with recurrence "monthly", **When** I mark it as complete, **Then** a new instance is created with the due date set to the same day next month
4. **Given** the console app is running, **When** I add a new todo and press Enter to skip the recurrence prompt, **Then** the todo is created as a one-time (non-recurring) task
5. **Given** I have a recurring todo, **When** I update it to change recurrence from "daily" to "weekly", **Then** the recurrence type is updated and the next due date is recalculated accordingly

---

### User Story 4 - Stop or Modify Recurring Todos (Priority: P3)

As a user, I want to disable recurrence for a recurring todo or modify its recurrence pattern so I can adapt to changing routines without deleting and recreating tasks.

**Why this priority**: This is a convenience feature that enhances recurring task management. While valuable, users can work around it by deleting and recreating todos if needed. It's lower priority than core recurring functionality (US3).

**Independent Test**: Can be fully tested by creating a recurring todo, disabling its recurrence, marking it complete, and verifying that no new instance is created. Also test modifying recurrence from daily to weekly and confirming the new pattern takes effect.

**Acceptance Scenarios**:

1. **Given** I have a recurring todo with recurrence "daily", **When** I update it to disable recurrence (set to "none"), **Then** the todo becomes a one-time task and will not reschedule after completion
2. **Given** I have a recurring todo, **When** I delete it, **Then** the recurring series is stopped and no future instances are created
3. **Given** I have a recurring todo with recurrence "weekly", **When** I update it to "monthly", **Then** future instances will be created monthly instead of weekly
4. **Given** I have a recurring todo that has already created multiple instances (original + rescheduled), **When** I disable recurrence on the current instance, **Then** only that instance becomes non-recurring; previously created instances remain as they were

---

### User Story 5 - Filter and Sort by Due Date (Priority: P3)

As a user, I want to filter todos by due date ranges and sort by due date so I can focus on specific timeframes (e.g., "this week" or "next month").

**Why this priority**: This is an enhancement to existing filter/sort capabilities (from Phase I.5), extending them to support the new due date field. It's lower priority because users can already see upcoming/overdue todos (US2), and basic viewing meets most needs.

**Independent Test**: Can be fully tested by creating todos with various due dates, applying a "due this week" filter, and verifying only todos with due dates in the current week are shown. Also test sorting all todos by due date (earliest first) and confirming the correct order.

**Acceptance Scenarios**:

1. **Given** I have 10 todos with varying due dates, **When** I filter by "due this week", **Then** only todos with due dates within the current week are displayed
2. **Given** I have todos with and without due dates, **When** I sort by due date (earliest first), **Then** todos with due dates are displayed first in chronological order, followed by todos without due dates
3. **Given** I have overdue, upcoming, and future todos, **When** I filter by "overdue", **Then** only todos with past due dates (and not complete) are displayed
4. **Given** I have filtered todos by due date, **When** I apply an additional sort (e.g., by priority), **Then** the filtered results are sorted by priority within each due date category

---

### Edge Cases

- What happens when a user enters a due date in the past for a new todo? (Accept it - may be intentional for tracking overdue items)
- How does the system handle recurring todos when the calculated next due date falls on a non-existent day (e.g., monthly recurrence for Jan 31 → Feb has no 31st)? (Use last day of month as fallback)
- What happens when a user marks a recurring todo complete multiple times in quick succession? (Each completion should create only one next instance; prevent duplicates)
- How does filtering by "due this week" work when the current date is near the end of a week? (Include all days from today through the end of Sunday)
- What happens if a user tries to create a recurring todo without a due date? (Require due date for recurring tasks - show validation error)
- How are time zones handled for due dates? (Use local system time; no timezone conversion needed for console app)
- What happens when viewing todos if the system clock changes (e.g., daylight saving time)? (Recalculate overdue status on each view based on current system time)
- How does the system handle very long recurrence chains (e.g., a daily task running for years)? (In-memory storage - limited by session duration; future instances only created as needed)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to assign a due date and time to each todo at creation
- **FR-002**: Due dates MUST be stored in a structured format (date + time)
- **FR-003**: System MUST accept due dates in YYYY-MM-DD HH:MM format (24-hour time)
- **FR-004**: System MUST allow due date to be optional (todos can exist without due dates)
- **FR-005**: System MUST allow users to update the due date of an existing todo
- **FR-006**: System MUST display due dates in a human-readable format alongside todos
- **FR-007**: System MUST visually distinguish overdue todos (due date in past, not complete)
- **FR-008**: System MUST provide an "overdue" indicator for todos past their due date
- **FR-009**: System MUST provide a "due soon" indicator for todos due within the next 7 days
- **FR-010**: System MUST support filtering todos to show only upcoming tasks (due within next 7 days)
- **FR-011**: System MUST support filtering todos to show only overdue tasks
- **FR-012**: System MUST allow users to mark a todo as recurring at creation time
- **FR-013**: System MUST support three recurrence types: daily, weekly, monthly
- **FR-014**: When a recurring todo is marked complete, system MUST automatically create a new instance with the next due date calculated based on recurrence type
- **FR-015**: System MUST prevent duplicate rescheduling (marking complete twice should not create two new instances)
- **FR-016**: System MUST allow users to update the recurrence type of an existing recurring todo
- **FR-017**: System MUST allow users to disable recurrence on a recurring todo (convert to one-time task)
- **FR-018**: System MUST calculate next due date for daily recurrence as: current due date + 1 day
- **FR-019**: System MUST calculate next due date for weekly recurrence as: current due date + 7 days
- **FR-020**: System MUST calculate next due date for monthly recurrence as: same day next month (or last day of month if day doesn't exist)
- **FR-021**: System MUST validate that recurring todos have a due date (cannot create recurring todo without due date)
- **FR-022**: System MUST display recurrence type alongside recurring todos (e.g., "🔁 Daily")
- **FR-023**: System MUST support sorting todos by due date (earliest first or latest first)
- **FR-024**: System MUST continue to support all existing features (priority, tags, search, filter, sort)
- **FR-025**: System MUST store all data in memory only (no file or database persistence)
- **FR-026**: System MUST update overdue status dynamically based on current system time at view time

### Key Entities

- **Todo** (enhanced): Represents a single task item, now with additional scheduling attributes:
  - All existing attributes (id, title, description, completed, created_at, priority, tags)
  - Due date and time (optional) - when the task should be completed
  - Recurrence type (none, daily, weekly, monthly) - defaults to "none"
  - Recurrence status (boolean) - whether this todo is part of a recurring series

- **Recurrence Pattern**: Represents the recurrence rules for a todo:
  - Recurrence type: daily, weekly, or monthly
  - Next due date calculation: based on current due date and recurrence type
  - Active status: whether recurrence is enabled

### Assumptions

- This feature builds on top of the existing Phase I.5 console todo app; all CRUD operations, priority, tags, search, filter, and sort from prior phases are prerequisites
- Due dates use 24-hour time format (HH:MM) for simplicity
- Due dates are entered manually in YYYY-MM-DD HH:MM format; no natural language parsing (e.g., "tomorrow" not supported)
- Time zones are not handled; all due dates use local system time
- "Overdue" means the current system time is past the due date and the todo is not marked complete
- "Upcoming" means due within the next 7 days from the current date
- Recurring todos create new instances only when marked complete, not automatically by time passing
- Only one recurring series per todo; no support for complex patterns (e.g., "every other day" or "twice weekly")
- Monthly recurrence uses "same day next month" logic; if the day doesn't exist (e.g., Jan 31 → Feb), use the last day of the month
- The console menu is extended with new options for viewing upcoming/overdue todos
- In-memory storage means recurring todo history is lost on app exit; only the current state persists during the session

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a due date to a new todo and see it displayed in the list within 5 seconds
- **SC-002**: Users can view a filtered list of upcoming todos (due within 7 days) with a single menu selection
- **SC-003**: Users can view a filtered list of overdue todos with a single menu selection, and overdue todos are visually distinguished from on-time todos
- **SC-004**: Users can create a recurring todo (daily, weekly, or monthly) and, upon marking it complete, see a new instance automatically created with the correct next due date on first attempt
- **SC-005**: Users can disable recurrence on a recurring todo, mark it complete, and verify that no new instance is created
- **SC-006**: All new scheduling features (due dates, recurring tasks) work seamlessly alongside existing features (priority, tags, search, filter, sort) without breaking any prior functionality
- **SC-007**: Error messages for invalid due date formats or missing due dates (when required) are clear enough that users self-correct without external help
- **SC-008**: 95% of users can successfully create a recurring task and observe it reschedule correctly on first attempt without assistance
