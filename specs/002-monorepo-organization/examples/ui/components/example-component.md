# Example Component Specification

**Component**: ExampleCard
**Type**: Presentational

## Purpose

Display example data in card format.

## Props

- title: string (required)
- description: string (optional)
- onAction: () => void (required)

## Behavior

- Clicking card triggers onAction callback
- Hover shows shadow effect
- Responsive: Full width on mobile, fixed width on desktop

## Styling

- Background: white (light mode), gray-800 (dark mode)
- Border radius: 8px
- Padding: 16px
- Shadow on hover: lg

## Accessibility

- ARIA label for interactive elements
- Keyboard navigation support
- Focus indicators
