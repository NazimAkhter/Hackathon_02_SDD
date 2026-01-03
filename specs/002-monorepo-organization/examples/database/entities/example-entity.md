# Example Entity Specification

**Entity**: Example
**Table**: examples

## Attributes

- id: integer (primary key)
- name: string (required, max 255)
- description: text (optional)
- created_at: timestamp
- updated_at: timestamp

## Relationships

- Belongs to User
- Has many ExampleItems

## Validation

- name: Required, unique
- description: Max 1000 characters

## Indexes

- name (unique)
- created_at
