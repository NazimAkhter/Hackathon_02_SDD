---
description: "Task list for In-Memory Python Console Todo App implementation"
---

# Tasks: In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md
**Created**: 2026-01-02

**Tests**: Unit tests and integration tests are included in this task breakdown as specified in the plan.md testing strategy.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. User Stories 1-2 are P1 (MVP), User Story 3 is P2, User Stories 4-5 are P3.

---

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- All tasks include exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per research.md and plan.md

- [X] T001 Initialize UV project with pyproject.toml at repository root
- [X] T002 Create directory structure: src/todo_app/, tests/unit/, tests/integration/
- [X] T003 [P] Create __init__.py files in src/todo_app/, tests/, tests/unit/, tests/integration/
- [X] T004 [P] Add pytest, pytest-cov, pytest-mock as dev dependencies via UV
- [X] T005 [P] Create .gitignore with Python/UV ignores (.venv, __pycache__, *.pyc, .pytest_cache, htmlcov/)
- [X] T006 Configure pyproject.toml with project metadata (name: todo-app, version: 0.1.0, requires-python: >=3.13)

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain model that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Todo dataclass in src/todo_app/models.py with attributes (id, title, description, completed, created_at)
- [X] T008 Add __post_init__ validation to Todo model (title non-empty, trim whitespace, max 200 chars)
- [X] T009 Add description length validation to Todo model (max 1000 chars)
- [X] T010 Implement Todo.mark_complete() method in src/todo_app/models.py
- [X] T011 [P] Implement Todo.is_complete() method in src/todo_app/models.py
- [X] T012 [P] Implement Todo.__str__() method for CLI display format in src/todo_app/models.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Todo Items (Priority: P1) 🎯 MVP

**Goal**: Users can create new todo items with title and description

**Independent Test**: Launch app, add todo with title and description, verify it appears with unique ID

**Acceptance Scenarios**:
- Add todo with title and description → creates with unique ID
- Add todo with title only → creates with empty description
- Add todo with empty title → displays error "Title is required"

### Unit Tests for User Story 1

> **RED PHASE**: Write these tests FIRST, ensure they FAIL before implementation

- [ ] T013 [P] [US1] Write test_todo_creation_with_defaults in tests/unit/test_models.py
- [ ] T014 [P] [US1] Write test_todo_creation_with_all_fields in tests/unit/test_models.py
- [ ] T015 [P] [US1] Write test_todo_title_validation_empty in tests/unit/test_models.py
- [ ] T016 [P] [US1] Write test_todo_title_validation_whitespace in tests/unit/test_models.py
- [ ] T017 [P] [US1] Write test_todo_title_trimming in tests/unit/test_models.py
- [ ] T018 [P] [US1] Write test_todo_title_max_length in tests/unit/test_models.py
- [ ] T019 [P] [US1] Write test_todo_description_max_length in tests/unit/test_models.py

### Service Layer for User Story 1

- [ ] T020 [US1] Create TodoService class with __init__ and empty todos dict in src/todo_app/service.py
- [ ] T021 [US1] Implement _generate_id() method in TodoService (returns max(keys)+1 or 1)
- [ ] T022 [US1] Implement add_todo(title, description) method in TodoService

### Service Tests for User Story 1

- [ ] T023 [P] [US1] Write test_add_todo_creates_with_id in tests/unit/test_service.py
- [ ] T024 [P] [US1] Write test_add_todo_increments_ids in tests/unit/test_service.py
- [ ] T025 [P] [US1] Write test_add_todo_trims_title in tests/unit/test_service.py

### CLI Layer for User Story 1

- [ ] T026 [US1] Implement add_todo_flow() in src/todo_app/cli.py with input prompts and validation
- [ ] T027 [US1] Implement display_menu() function in src/todo_app/cli.py
- [ ] T028 [US1] Implement get_user_choice() function with validation (1-6) in src/todo_app/cli.py

### Entry Point for User Story 1

- [ ] T029 [US1] Create main() function in src/todo_app/__main__.py with menu loop
- [ ] T030 [US1] Add KeyboardInterrupt handling (Ctrl+C) in __main__.py
- [ ] T031 [US1] Add welcome message and exit option (6) in __main__.py

### Integration Test for User Story 1

- [ ] T032 [US1] Write test_add_todo_flow in tests/integration/test_cli.py (mock input, capture output)
- [ ] T033 [US1] Write test_add_todo_empty_title_error in tests/integration/test_cli.py

**Checkpoint**: User Story 1 complete - users can add todos and see them stored with unique IDs

---

## Phase 4: User Story 2 - View All Todos (Priority: P1) 🎯 MVP

**Goal**: Users can view all todo items in a formatted list with completion status

**Independent Test**: Add several todos (some complete, some not), verify view displays all with status

**Acceptance Scenarios**:
- View 3 todos → displays all with ID, title, description, status
- View when no todos → displays "No todos found"
- View 10 todos (5 complete, 5 incomplete) → clear visual distinction

### Service Layer for User Story 2

- [ ] T034 [P] [US2] Implement get_all_todos() method in TodoService (returns list ordered by created_at)
- [ ] T035 [P] [US2] Implement get_todo_by_id(id) method in TodoService (returns Todo or None)

### Service Tests for User Story 2

- [ ] T036 [P] [US2] Write test_get_all_todos_empty in tests/unit/test_service.py
- [ ] T037 [P] [US2] Write test_get_all_todos_ordered in tests/unit/test_service.py
- [ ] T038 [P] [US2] Write test_get_todo_by_id_found in tests/unit/test_service.py
- [ ] T039 [P] [US2] Write test_get_todo_by_id_not_found in tests/unit/test_service.py

### CLI Layer for User Story 2

- [ ] T040 [US2] Implement view_todos_flow() in src/todo_app/cli.py with table formatting
- [ ] T041 [US2] Add "No todos found" message handling in view_todos_flow()
- [ ] T042 [US2] Implement column truncation (title 30 chars, description 50 chars) in view_todos_flow()

### Integration Test for User Story 2

- [ ] T043 [US2] Write test_view_all_todos_flow in tests/integration/test_cli.py (add 3 todos, verify display)
- [ ] T044 [US2] Write test_view_empty_todos in tests/integration/test_cli.py

**Checkpoint**: User Stories 1 and 2 complete - users can add and view todos (MVP functional!)

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P2)

**Goal**: Users can mark todos as complete to track progress

**Independent Test**: Create todo, mark it complete by ID, verify status changes to complete

**Acceptance Scenarios**:
- Mark incomplete todo → status changes to complete
- Mark already complete todo → displays "already complete"
- Mark non-existent ID → displays "Todo not found"

### Unit Tests for User Story 3

- [ ] T045 [P] [US3] Write test_todo_mark_complete in tests/unit/test_models.py
- [ ] T046 [P] [US3] Write test_todo_mark_complete_idempotent in tests/unit/test_models.py
- [ ] T047 [P] [US3] Write test_todo_is_complete in tests/unit/test_models.py
- [ ] T048 [P] [US3] Write test_todo_str_incomplete in tests/unit/test_models.py
- [ ] T049 [P] [US3] Write test_todo_str_complete in tests/unit/test_models.py

### Service Layer for User Story 3

- [ ] T050 [US3] Implement mark_complete(id) method in TodoService (returns bool)

### Service Tests for User Story 3

- [ ] T051 [P] [US3] Write test_mark_complete_success in tests/unit/test_service.py
- [ ] T052 [P] [US3] Write test_mark_complete_not_found in tests/unit/test_service.py

### CLI Layer for User Story 3

- [ ] T053 [US3] Implement mark_complete_flow() in src/todo_app/cli.py with ID validation
- [ ] T054 [US3] Add "already complete" info message handling in mark_complete_flow()
- [ ] T055 [US3] Add "Todo not found" error handling in mark_complete_flow()

### Integration Test for User Story 3

- [ ] T056 [US3] Write test_mark_complete_flow in tests/integration/test_cli.py
- [ ] T057 [US3] Write test_mark_complete_not_found_error in tests/integration/test_cli.py

**Checkpoint**: User Story 3 complete - users can mark todos as complete and see visual status change

---

## Phase 6: User Story 4 - Update Existing Todos (Priority: P3)

**Goal**: Users can update title or description of existing todos

**Independent Test**: Create todo, update its title/description, verify changes in view

**Acceptance Scenarios**:
- Update title → title changes, description unchanged
- Update description only → description changes, title unchanged
- Update non-existent ID → displays "Todo not found"

### Service Layer for User Story 4

- [ ] T058 [US4] Implement update_todo(id, title, description) method in TodoService (returns bool)

### Service Tests for User Story 4

- [ ] T059 [P] [US4] Write test_update_todo_title in tests/unit/test_service.py
- [ ] T060 [P] [US4] Write test_update_todo_description in tests/unit/test_service.py
- [ ] T061 [P] [US4] Write test_update_todo_not_found in tests/unit/test_service.py

### CLI Layer for User Story 4

- [ ] T062 [US4] Implement update_todo_flow() in src/todo_app/cli.py with current value display
- [ ] T063 [US4] Add "press Enter to keep current" logic for title and description
- [ ] T064 [US4] Add "Todo not found" error handling in update_todo_flow()

### Integration Test for User Story 4

- [ ] T065 [US4] Write test_update_todo_flow in tests/integration/test_cli.py
- [ ] T066 [US4] Write test_update_todo_not_found_error in tests/integration/test_cli.py

**Checkpoint**: User Story 4 complete - users can update existing todos

---

## Phase 7: User Story 5 - Delete Todos (Priority: P3)

**Goal**: Users can delete todos they no longer need

**Independent Test**: Create todo, delete it by ID, verify it no longer appears in view

**Acceptance Scenarios**:
- Delete existing todo → todo removed from list
- Delete non-existent ID → displays "Todo not found"
- Delete ID 3 from 5 todos → only 4 remain

### Service Layer for User Story 5

- [ ] T067 [US5] Implement delete_todo(id) method in TodoService (returns bool)

### Service Tests for User Story 5

- [ ] T068 [P] [US5] Write test_delete_todo_success in tests/unit/test_service.py
- [ ] T069 [P] [US5] Write test_delete_todo_not_found in tests/unit/test_service.py
- [ ] T070 [P] [US5] Write test_id_generation_after_deletion in tests/unit/test_service.py (IDs not reused)

### CLI Layer for User Story 5

- [ ] T071 [US5] Implement delete_todo_flow() in src/todo_app/cli.py with confirmation prompt
- [ ] T072 [US5] Add deletion confirmation (y/n) validation in delete_todo_flow()
- [ ] T073 [US5] Add "Todo not found" error handling in delete_todo_flow()

### Integration Test for User Story 5

- [ ] T074 [US5] Write test_delete_todo_flow in tests/integration/test_cli.py (with confirmation)
- [ ] T075 [US5] Write test_delete_todo_cancelled in tests/integration/test_cli.py
- [ ] T076 [US5] Write test_exit_flow in tests/integration/test_cli.py (menu option 6)

**Checkpoint**: All user stories complete - full CRUD functionality operational

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and validation

- [ ] T077 [P] Create README.md at repository root with project overview and quick start
- [ ] T078 [P] Add docstrings to all public methods in models.py, service.py, cli.py
- [ ] T079 Run full test suite with coverage: `uv run pytest --cov=src/todo_app --cov-report=term-missing`
- [ ] T080 Verify 90%+ coverage for src/todo_app/service.py
- [ ] T081 Test all acceptance scenarios from spec.md manually
- [ ] T082 Validate all functional requirements (FR-001 to FR-012) met
- [ ] T083 Validate all success criteria (SC-001 to SC-007) met
- [ ] T084 Run quickstart.md validation checklist
- [ ] T085 [P] Test Unicode display on different terminals (Windows, Unix)
- [ ] T086 [P] Test edge cases: 100+ todos, long titles/descriptions, special characters

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational (Phase 2) completion
  - User Story 1 (P1): Add todos - no dependencies on other stories
  - User Story 2 (P1): View todos - depends on User Story 1 for data to view (but service method independent)
  - User Story 3 (P2): Mark complete - depends on US1/US2 for todos to exist (but method independent)
  - User Story 4 (P3): Update todos - depends on US1/US2 for todos to exist (but method independent)
  - User Story 5 (P3): Delete todos - depends on US1/US2 for todos to exist (but method independent)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Implementation Order

**Recommended Sequential Order**:
1. Phase 1 (Setup) → Phase 2 (Foundational)
2. Phase 3 (User Story 1: Add) → Phase 4 (User Story 2: View) ← **MVP COMPLETE**
3. Phase 5 (User Story 3: Mark Complete)
4. Phase 6 (User Story 4: Update)
5. Phase 7 (User Story 5: Delete)
6. Phase 8 (Polish)

**Alternative Parallel Order** (with multiple developers):
- After Phase 2 completes, Phases 3-7 can run in parallel on different branches
- Each user story is independently implementable and testable
- Integration happens at service layer, minimal conflicts

### Within Each User Story

**TDD Flow (Red-Green-Refactor)**:
1. Write unit tests for models/service (should FAIL)
2. Implement models/service methods (tests should PASS)
3. Write integration tests for CLI (should FAIL)
4. Implement CLI flow (tests should PASS)
5. Refactor if needed

**Task Sequence Within Story**:
- Unit tests (parallel) → Service implementation → Service tests (parallel) → CLI implementation → Integration tests

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005 can run in parallel

**Phase 2 (Foundational)**: T011, T012 can run in parallel (different methods)

**User Story 1 Tests**: T013-T019 can run in parallel (different test files/cases)

**User Story 1 Service Tests**: T023-T025 can run in parallel

**User Story 2 Service**: T034, T035 can run in parallel (different methods)

**User Story 2 Service Tests**: T036-T039 can run in parallel

**User Story 3 Unit Tests**: T045-T049 can run in parallel

**User Story 3 Service Tests**: T051, T052 can run in parallel

**User Story 4 Service Tests**: T059-T061 can run in parallel

**User Story 5 Service Tests**: T068-T070 can run in parallel

**Phase 8 (Polish)**: T077, T078, T085, T086 can run in parallel

---

## Parallel Example: User Story 1

```bash
# RED PHASE: Launch all unit tests in parallel
Task T013: "Write test_todo_creation_with_defaults in tests/unit/test_models.py"
Task T014: "Write test_todo_creation_with_all_fields in tests/unit/test_models.py"
Task T015: "Write test_todo_title_validation_empty in tests/unit/test_models.py"
Task T016: "Write test_todo_title_validation_whitespace in tests/unit/test_models.py"
Task T017: "Write test_todo_title_trimming in tests/unit/test_models.py"
Task T018: "Write test_todo_title_max_length in tests/unit/test_models.py"
Task T019: "Write test_todo_description_max_length in tests/unit/test_models.py"

# Verify all tests FAIL

# GREEN PHASE: Implement service (sequential, depends on model validation)
Task T020: "Create TodoService class..."
Task T021: "Implement _generate_id()..."
Task T022: "Implement add_todo()..."

# Launch service tests in parallel
Task T023: "Write test_add_todo_creates_with_id..."
Task T024: "Write test_add_todo_increments_ids..."
Task T025: "Write test_add_todo_trims_title..."

# Verify all tests PASS
```

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T012) ← **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 - Add Todos (T013-T033)
4. Complete Phase 4: User Story 2 - View Todos (T034-T044)
5. **STOP and VALIDATE**: Test adding and viewing todos independently
6. Run tests: `uv run pytest`
7. Manual validation: Add 5 todos, view them, verify display
8. **MVP READY**: Users can add and view todos

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Project structure ready
2. **MVP** (Phases 3-4) → Add + View todos → **DEMO 1**
3. **Enhanced** (Phase 5) → Add Mark Complete → **DEMO 2**
4. **Feature Complete** (Phases 6-7) → Add Update + Delete → **DEMO 3**
5. **Production Ready** (Phase 8) → Polish + validation → **RELEASE**

Each demo is a working increment that delivers user value.

### Parallel Team Strategy

With 3 developers after Phase 2:

- **Developer A**: Phase 3 (User Story 1 - Add)
- **Developer B**: Phase 4 (User Story 2 - View)
- **Developer C**: Phase 5 (User Story 3 - Mark Complete)

After initial stories complete:
- **Developer A**: Phase 6 (User Story 4 - Update)
- **Developer B**: Phase 7 (User Story 5 - Delete)
- **Developer C**: Phase 8 (Polish)

Stories can be developed in parallel with minimal conflicts (different methods, different CLI flows).

---

## Testing Strategy Summary

### Total Test Count: 35 tests

**Unit Tests (models.py)**: 12 tests
- T013-T019 (User Story 1): 7 tests
- T045-T049 (User Story 3): 5 tests

**Unit Tests (service.py)**: 15 tests
- T023-T025 (User Story 1): 3 tests
- T036-T039 (User Story 2): 4 tests
- T051-T052 (User Story 3): 2 tests
- T059-T061 (User Story 4): 3 tests
- T068-T070 (User Story 5): 3 tests

**Integration Tests (test_cli.py)**: 8 tests
- T032-T033 (User Story 1): 2 tests
- T043-T044 (User Story 2): 2 tests
- T056-T057 (User Story 3): 2 tests
- T065-T066 (User Story 4): 2 tests
- T074-T076 (User Story 5): 3 tests

### Coverage Target

**Minimum Required**: 90% coverage for `src/todo_app/service.py`

**Command**:
```bash
uv run pytest --cov=src/todo_app --cov-report=term-missing
```

**Success Criteria**: All 35 tests pass, coverage ≥ 90% for service layer

---

## Validation Checklist

After completing all tasks, verify:

### Functional Requirements Coverage

- [ ] FR-001: Add todo with required title ✓ (T022, T026)
- [ ] FR-002: Auto-generated unique ID ✓ (T021)
- [ ] FR-003: Display all todos with status ✓ (T040, T042)
- [ ] FR-004: Mark todo as complete ✓ (T050, T053)
- [ ] FR-005: Update todo title/description ✓ (T058, T062)
- [ ] FR-006: Delete todo by ID ✓ (T067, T071)
- [ ] FR-007: Validate non-empty title ✓ (T008)
- [ ] FR-008: Display error messages ✓ (All CLI flows)
- [ ] FR-009: In-memory storage only ✓ (T020)
- [ ] FR-010: Text-based menu ✓ (T027, T028)
- [ ] FR-011: Run until explicit exit ✓ (T029)
- [ ] FR-012: Boolean completion status ✓ (T010, T050)

### Success Criteria Validation

- [ ] SC-001: Add todo completes in < 5 seconds ✓ (T081)
- [ ] SC-002: Visual distinction for status ✓ (T040, T042)
- [ ] SC-003: All CRUD operations work ✓ (T081)
- [ ] SC-004: Handle 100+ todos without degradation ✓ (T086)
- [ ] SC-005: 90% success rate on valid input ✓ (T079)
- [ ] SC-006: Clear error messages ✓ (T081)
- [ ] SC-007: Code understandable for target audience ✓ (T078)

### User Story Acceptance

- [ ] User Story 1: Add todos (3 scenarios) ✓ (T032, T033)
- [ ] User Story 2: View todos (3 scenarios) ✓ (T043, T044)
- [ ] User Story 3: Mark complete (3 scenarios) ✓ (T056, T057)
- [ ] User Story 4: Update todos (3 scenarios) ✓ (T065, T066)
- [ ] User Story 5: Delete todos (3 scenarios) ✓ (T074, T075, T076)

---

## Notes

- **[P]** tasks = different files, no dependencies, can run in parallel
- **[Story]** label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Follow TDD: Write tests first (RED), implement (GREEN), refactor
- Commit after each task or logical group
- Stop at checkpoints to validate stories independently
- Tasks reference exact file paths from plan.md structure
- All tasks aligned with spec.md requirements and plan.md architecture

---

## References

- **Specification**: `specs/001-console-todo/spec.md` (User Stories, Requirements)
- **Implementation Plan**: `specs/001-console-todo/plan.md` (Architecture, Decisions)
- **Data Model**: `specs/001-console-todo/data-model.md` (Todo Entity)
- **CLI Contract**: `specs/001-console-todo/contracts/cli-interface.md` (Interface Spec)
- **Research**: `specs/001-console-todo/research.md` (Technical Decisions)
- **Quickstart**: `specs/001-console-todo/quickstart.md` (Setup Guide)
