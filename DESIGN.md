# Design Guide

This file defines the visual and interaction rules for Care Overview. Read this before writing or changing frontend code.

## Design Goal

Care Overview should feel like a calm, usable patient portal dashboard. It should be practical, trustworthy, and easy to scan. It should not look like a generic AI-generated SaaS demo.

## Audience

Primary users are patients who need to understand what happened recently, what needs attention, and what actions they should take next. The interface should work for older adults, new portal users, and patients managing several providers or conditions.

## Visual Direction

Use a restrained healthcare product style:

- Quiet and functional
- Clear hierarchy
- Compact but not crowded
- Accessible contrast
- Few decorative elements
- Real data first

Avoid marketing-page design. The first screen should be the dashboard, not a hero section.

## Palette

Use colors by role, not decoration.

- Page background: `#f6f8f7`
- Main surface: `#ffffff`
- Raised surface: `#fbfcfc`
- Text: `#17201d`
- Secondary text: `#5f6f6a`
- Border: `#d9e1de`
- Primary action: `#0f6f68`
- Primary action hover: `#0b5954`
- Link: `#145f8c`
- Success: `#2f7d4f`
- Warning: `#9a6a12`
- Error: `#a33a32`
- Info: `#2d6f94`

Do not use purple-to-blue gradients, glowing borders, glass panels, or decorative color washes.

## Typography

Use the system font stack:

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

Rules:

- Body text: 15px or 16px
- Small labels: 12px or 13px
- Page title: 24px to 30px
- Section headings: 16px to 20px
- Button text: 14px or 15px
- Line height: 1.4 to 1.6
- Letter spacing: 0

Do not use oversized display type inside dashboard panels.

## Layout

Desktop:

- Left navigation rail
- Main content area with a max width around 1180px
- Dashboard summary at the top
- Primary column for recent visit and next steps
- Secondary column for appointments and updates

Mobile:

- Top navigation or compact tab row
- One-column dashboard
- Cards stacked by importance
- Buttons and links at least 44px tall when touchable

Spacing:

- Use 4px increments
- Dense data sections should use 12px to 20px gaps
- Page-level spacing can use 24px to 32px
- Do not use huge empty hero spacing

## Components

Cards:

- Use cards only for real dashboard groups
- Radius: 6px or 8px
- Border: 1px solid `#d9e1de`
- Shadow: none or very subtle
- No nested cards

Buttons:

- Primary buttons are solid teal
- Secondary buttons are bordered
- Destructive buttons use red only for actual destructive actions
- Disabled buttons must visibly look disabled
- Focus state must be visible

Tables and lists:

- Prefer lists for patient tasks and updates
- Use tables only when comparing repeated structured rows
- Keep row actions near the row they affect

Status badges:

- Use muted backgrounds
- Use plain labels like `Open`, `Reviewed`, `Unread`, `Overdue`
- Do not use gradient badges

Forms:

- Labels above fields
- Clear required-field behavior
- Inline error messages near the field
- Keep form controls simple

Empty states:

- Use direct copy
- Explain what is missing
- Offer the next action when useful

Example:

```text
No unread messages
Messages from your care team will appear here.
```

## Interaction Rules

Every interactive element needs:

- Default state
- Hover state
- Focus-visible state
- Disabled state when applicable
- Loading or saving state when applicable
- Error state when applicable

Dashboard counts should update after the user marks a message, result, or task as handled.

## Anti-Generic Checklist

Before merging frontend work, check:

- No purple or violet gradient
- No centered marketing hero
- No three identical feature cards
- No glassmorphism
- No glowing border effects
- No emoji placeholders
- No vague slogan copy
- No oversized whitespace
- No default-looking component dump
- No unreadable gray text
- No missing mobile layout
- No missing focus state
- No missing empty or error state

## Copy Style

Use plain patient-facing language.

Good:

```text
You have 2 tasks due before your next appointment.
```

Avoid:

```text
Transform your healthcare journey with AI-powered insights.
```

The product should summarize existing fictional records only. It should not diagnose, interpret medical meaning, recommend treatment, or label anything as urgent.

## Research Notes

Recent UI design articles describe common generated-looking patterns as vague "modern" prompts, default component libraries, purple or indigo gradients, centered hero layouts, glass cards, identical card grids, generic icons, weak hierarchy, and missing interaction states. This guide avoids those patterns by defining exact colors, layout behavior, component rules, copy style, and review checks.

References:

- https://horizonx.so/blog/ai-generated-ui-looks-generic-ui-specification
- https://cssdna.com/blog/why-ai-generated-uis-look-the-same/
- https://www.joshuasnoddy.com/blog/why-ai-websites-look-the-same/
- https://martecks.com/blog/why-ai-built-apps-look-generic/

