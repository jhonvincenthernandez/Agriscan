# Dashboard Design Guidelines

Guidelines for rendering self-contained HTML5 meeting dashboards.

## Core Rules

1. **Zero External Dependencies:**
   - All styles must be inline `<style>` tags.
   - All scripts must be inline `<script>` tags.
   - Do not import CDN stylesheets or scripts (e.g. Bootstrap, Tailwind CDN, Google Fonts).
   - Use system font stacks (`system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`).

2. **Visual Hierarchy:**
   - Header: Meeting title, date, duration, participants.
   - Archetype Viewport: Structured presentation based on classified meeting archetype.
   - Decision Cards: Highlight key outcomes, rationales, and consensus points.
   - Action Items: Clear assignees, deadlines, and status indicators.
   - Verbatim Quotes: Callout cards with attribution.

3. **Accessibility and Contrast:**
   - Enforce WCAG AA contrast ratios (minimum 4.5:1 for normal text).
   - Clean responsive design adapting to mobile and desktop viewports.
