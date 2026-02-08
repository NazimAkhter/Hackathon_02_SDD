# Feature Specification: Intermediate Features for In-Memory Python Console Todo App

**Feature Branch**: `003-intermediate-todo-features`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Intermediate Features for In-Memory Python Console Todo App - Enhancing the in-memory console todo app with prioritization, categorization, search, filtering, and sorting. Target audience: Developers extending a basic console todo app with organization and usability features."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Assign Priority to Todos (Priority: P1)

As a user, I want to assign a priority level (high, medium, low) to each todo so I can quickly identify which tasks are most urgent and should be tackled first.

**Why this priority**: Priority is the most fundamental organization feature. It transforms a flat list into an actionable, ordered work queue. Without priorities, all other features (sorting, filtering) have less value since there's no key dimension to sort/filter by.

**Independent Test**: Can be fully tested by adding a todo with a specific priority level, viewing it, and verifying the priority is displayed. Can also be tested by updating an existing todo's priority and confirming the change persists in memory.

**Acceptance Scenarios**:

1. **Given** the console app is running, **When** I add a new todo and select priority "high", **Then** the todo is created with priority "high" displayed alongside title and status
2. **Given** I have an existing todo with priority "low", **When** I update its priority to "high", **Then** the todo's priority changes to "high" and the update is reflected in the list view
3. **Given** the console app is running, **When** I add a new todo and skip the priority prompt (press Enter), **Then** the todo is created with a default priority of "medium"
4. **Given** the console app is running, **When** I add a new todo and enter an invalid priority value (e.g., "urgent"), **Then** the system displays an error message and prompts me to choose from high, medium, or low

---

### User Story 2 - Tag Todos with Categories (Priority: P1)

As a user, I want to assign one or more tags/categories (e.g., "work", "home", "errands") to each todo so I can organize tasks by context or area of responsibility.

**Why this priority**: Categories provide the second major dimension of organization. Combined with priorities, they enable meaningful filtering and a structured view of tasks across life/work domains.

**Independent Test**: Can be fully tested by creating a todo with tags, viewing it, and confirming the tags are displayed. Can also test adding/removing tags from an existing todo.

**Acceptance Scenarios**:

1. **Given** the console app is running, **When** I add a new todo and provide tags "work, meeting", **Then** the todo is created with both tags displayed alongside the title
2. **Given** I have an existing todo with tag "work", **When** I update its tags to "work, urgent", **Then** the todo now has both tags displayed
3. **Given** the console app is running, **When** I add a new todo and skip the tags prompt (press Enter), **Then** the todo is created with no tags
4. **Given** the console app is running, **When** I add a todo with tags " Work , HOME ", **Then** the tags are normalized to lowercase and trimmed: "work", "home"

---

### User Story 3 - Search Todos by Keyword (Priority: P2)

As a user, I want to search for todos by typing a keyword so I can quickly find specific tasks without scrolling through the entire list.

**Why this priority**: Search is a key usability feature once the todo list grows beyond a handful of items. It enables fast retrieval without requiring the user to manually scan the list.

**Independent Test**: Can be fully tested by adding several todos with distinct titles/descriptions, searching for a keyword, and verifying only matching todos are returned.

**Acceptance Scenarios**:

1. **Given** I have 5 todos, one with title "Buy groceries" and another with description containing "grocery store", **When** I search for "grocery", **Then** both matching todos are displayed
2. **Given** I have 5 todos, **When** I search for "xyznonexistent", **Then** the system displays "No matching todos found"
3. **Given** I have a todo titled "IMPORTANT Meeting", **When** I search for "important", **Then** the search is case-insensitive and returns the matching todo
4. **Given** the console app is running, **When** I search with an empty keyword, **Then** the system displays an error message prompting me to enter a search term

---

### User Story 4 - Filter Todos by Status, Priority, or Category (Priority: P2)

As a user, I want to filter my todo list by completion status, priority level, or category so I can focus on a specific subset of tasks relevant to my current context.

**Why this priority**: Filtering allows users to reduce information overload and focus on what matters right now. It builds on priority and category data to provide a targeted view.

**Independent Test**: Can be fully tested by creating todos with varying statuses, priorities, and categories, then applying each filter type and verifying only matching results appear.

**Acceptance Scenarios**:

1. **Given** I have 5 todos (3 incomplete, 2 complete), **When** I filter by status "incomplete", **Then** only the 3 incomplete todos are displayed
2. **Given** I have 5 todos with varying priorities, **When** I filter by priority "high", **Then** only the high-priority todos are displayed
3. **Given** I have 5 todos, 2 tagged "work" and 3 tagged "home", **When** I filter by category "work", **Then** only the 2 work-tagged todos are displayed
4. **Given** I apply a filter that matches no todos, **When** the results are displayed, **Then** the system shows "No todos match the selected filter"

---

### User Story 5 - Sort Todos (Priority: P3)

As a user, I want to sort my todo list by priority, creation date, or alphabetically so I can view tasks in the order that best suits my current workflow.

**Why this priority**: Sorting is a convenience feature that enhances readability. It depends on priority and other data being present, so it logically follows the foundational stories.

**Independent Test**: Can be fully tested by creating several todos with different priorities, titles, and timestamps, then applying each sort option and verifying the correct order.

**Acceptance Scenarios**:

1. **Given** I have todos with priorities high, low, and medium, **When** I sort by priority, **Then** todos are displayed in order: high, medium, low
2. **Given** I have todos created at different times, **When** I sort by creation date (newest first), **Then** the most recently created todo appears at the top
3. **Given** I have todos titled "Zebra task", "Apple task", "Mango task", **When** I sort alphabetically, **Then** todos appear in order: Apple task, Mango task, Zebra task
4. **Given** I am viewing a sorted list, **When** I choose a different sort option, **Then** the list re-sorts accordingly

---

### User Story 6 - Combined Filter and Sort (Priority: P3)

As a user, I want to apply a filter and then sort the filtered results so I can find exactly what I need in the order I prefer.

**Why this priority**: This is an advanced usability enhancement that combines two features. It's valuable but only meaningful once both filtering and sorting work independently.

**Independent Test**: Can be fully tested by creating a diverse set of todos, applying a filter (e.g., status: incomplete), then sorting the filtered results (e.g., by priority), and verifying the output is both filtered and sorted correctly.

**Acceptance Scenarios**:

1. **Given** I have 10 todos with mixed statuses and priorities, **When** I filter by status "incomplete" and sort by priority, **Then** only incomplete todos are shown, ordered from high to low priority
2. **Given** I have 10 todos with mixed categories, **When** I filter by category "work" and sort alphabetically, **Then** only work-tagged todos are shown in alphabetical order

---

### Edge Cases

- What happens when a user searches for a keyword that contains special characters (e.g., `@`, `#`, `&`)?
- What happens when a user tries to filter by a category that no todo has been tagged with?
- How does sorting handle todos with the same priority level (stable sort vs. secondary ordering)?
- What happens when a user assigns a very large number of tags (e.g., 50 tags) to a single todo?
- How does filtering by category work when a todo has multiple tags and only one matches?
- What happens when the user provides an invalid sort or filter option from the menu?
- How does the system handle combining filters (e.g., filter by priority AND category simultaneously)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to assign a priority level (high, medium, low) to each todo at creation time
- **FR-002**: System MUST default to "medium" priority when no priority is explicitly chosen
- **FR-003**: System MUST allow users to update the priority of an existing todo
- **FR-004**: System MUST display the priority level alongside each todo in the list view
- **FR-005**: System MUST allow users to assign zero or more tags/categories to each todo at creation time
- **FR-006**: System MUST normalize tags to lowercase and trim whitespace
- **FR-007**: System MUST allow users to update the tags of an existing todo
- **FR-008**: System MUST display tags alongside each todo in the list view
- **FR-009**: System MUST allow users to search todos by keyword across both title and description fields
- **FR-010**: System MUST perform case-insensitive keyword search
- **FR-011**: System MUST display all matching todos when a search is performed, or a "no results" message if none match
- **FR-012**: System MUST allow users to filter todos by completion status (complete/incomplete)
- **FR-013**: System MUST allow users to filter todos by priority level (high, medium, low)
- **FR-014**: System MUST allow users to filter todos by category/tag
- **FR-015**: System MUST display only matching todos when a filter is applied, or a "no results" message if none match
- **FR-016**: System MUST allow users to sort the todo list by priority (high > medium > low)
- **FR-017**: System MUST allow users to sort the todo list by creation date (newest or oldest first)
- **FR-018**: System MUST allow users to sort the todo list alphabetically by title
- **FR-019**: System MUST allow users to apply a filter and then sort the filtered results
- **FR-020**: System MUST present new menu options for Search, Filter, and Sort operations
- **FR-021**: System MUST validate all user inputs for priority, tags, search terms, filter choices, and sort choices with clear error messages
- **FR-022**: System MUST continue to support all existing basic todo operations (add, view, update, delete, mark complete)
- **FR-023**: System MUST store all data in memory only (no file or database persistence)

### Key Entities

- **Todo** (enhanced): Represents a single task item with the following attributes:
  - Unique identifier (auto-generated integer)
  - Title (required text)
  - Description (optional text)
  - Completion status (boolean: complete or incomplete, defaults to incomplete)
  - Priority level (one of: high, medium, low; defaults to medium)
  - Tags/Categories (zero or more text labels, normalized to lowercase)
  - Creation timestamp (for ordering and sort-by-date)

### Assumptions

- This feature builds on top of the existing `001-console-todo` basic app; all CRUD operations from that spec are prerequisites
- Priority levels are limited to exactly three values: high, medium, low (no custom levels)
- Tags are free-form text labels entered as comma-separated values; no predefined list of allowed tags
- Search performs a simple substring match (not fuzzy matching or regex)
- Filtering applies one filter dimension at a time from the menu; combined filtering is achieved by filter + sort
- Sorting is applied to the full list or the currently filtered results
- When todos share the same sort key (e.g., same priority), they retain their original creation order (stable sort)
- The console menu is extended with new numbered options; existing option numbers may shift to accommodate new entries

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can assign a priority to a new todo and see it reflected in the list within 3 seconds
- **SC-002**: Users can tag a todo and later filter by that tag, retrieving only matching items on first attempt
- **SC-003**: Users can search across 100+ todos and receive results within 2 seconds
- **SC-004**: Users can apply any single filter (status, priority, or category) and see the correct subset of todos on first attempt
- **SC-005**: Users can sort their todo list by any of the three criteria (priority, date, alphabetical) and see correctly ordered results on first attempt
- **SC-006**: Users can combine filter and sort in a single workflow, seeing filtered and sorted results correctly
- **SC-007**: All new features work seamlessly alongside existing CRUD operations without breaking any prior functionality
- **SC-008**: Error messages for invalid priority, tag, search, filter, or sort inputs are clear enough that users self-correct without external help
