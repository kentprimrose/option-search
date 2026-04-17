# Design System Documentation: The Quantitative Edge

## 1. Overview & Creative North Star
**Creative North Star: The Sovereign Analyst**
This design system is built to evoke the feeling of a high-end, private trading floor. It rejects the cluttered, chaotic nature of legacy financial tools in favor of "The Sovereign Analyst"—an aesthetic that prioritizes clarity, tonal depth, and editorial authority. 

We move beyond the "template" look by utilizing intentional asymmetry and high-contrast typography. Instead of crowding the screen with lines and borders, we use breathing room and varying depths of navy to guide the eye. The UI is not a flat grid; it is an atmospheric space where data feels illuminated and curated.

## 2. Colors
Our palette is rooted in the deep reaches of the night. By using a monochromatic navy foundation with electric blue accents, we create a high-performance environment that reduces eye strain while maintaining a "premium" feel.

### Surface Hierarchy & Nesting
We achieve depth through "Tonal Layering." The UI should be treated as a series of physical layers:
*   **Base:** `surface` (#0c1322) is the canvas.
*   **Sections:** Use `surface_container_low` (#151b2b) for large layout areas.
*   **Cards/Interactive Elements:** Use `surface_container_highest` (#2e3545) to make actionable items "rise" toward the user.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders for sectioning or row separation. Boundaries must be defined solely through background color shifts. For example, a `surface_container_high` card sitting on a `surface` background provides all the definition needed. 

### The "Glass & Gradient" Rule
To elevate the system from "standard" to "bespoke":
*   **Glassmorphism:** For floating menus or high-level filters, use semi-transparent `surface_variant` colors with a 12px-20px `backdrop-blur`.
*   **Signature Gradients:** Primary Action Buttons should not be flat. Use a subtle linear gradient from `primary` (#adc6ff) to `primary_container` (#4d8eff) at a 135-degree angle to provide a "glow" that feels professional and polished.

## 3. Typography
This design system uses a dual-typeface strategy to balance editorial sophistication with data density.

*   **Display & Headlines (Manrope):** Use Manrope for all `display-` and `headline-` scales. Its geometric construction feels modern and authoritative. Headers should use `on_surface` (#dce2f8) for maximum contrast against the navy background.
*   **Data & UI (Inter):** Use Inter for `title-`, `body-`, and `label-` scales. Inter’s tall x-height and clear apertures are essential for the legibility of ticker symbols, strike prices, and complex data tables.
*   **Contrast as Hierarchy:** Maintain a strict contrast ratio. Important financial figures (like Mark or Bid/Ask) should always use `on_surface`, while labels and secondary metadata use `on_surface_variant` (#c2c6d6).

## 4. Elevation & Depth
Depth in this system is a product of light and tone, not structure.

*   **The Layering Principle:** Stack containers to create hierarchy. A `surface_container_lowest` card placed inside a `surface_container_low` section creates a natural "recessed" look, perfect for input groups or data buckets.
*   **Ambient Shadows:** When an element must "float" (like a tooltip or modal), use a shadow with a 32px blur and 6% opacity. The shadow color should be `#000000` to ground it in the deep navy environment.
*   **The "Ghost Border" Fallback:** If a boundary is strictly required for accessibility, use a "Ghost Border." Apply the `outline_variant` (#424754) at **15% opacity**. Never use a 100% opaque outline.

## 5. Components

### Buttons
*   **Primary:** Gradient of `primary` to `primary_container`. Roundedness: `md` (0.375rem). High-contrast `on_primary` text.
*   **Tertiary/Icon:** Use `on_primary_container` icons. Backgrounds should be transparent unless hovered, where they shift to `surface_bright`.

### Interactive Filter Cards
*   **Container:** `surface_container_highest`. Roundedness: `lg` (0.5rem).
*   **Checkboxes:** When checked, use `primary` fill with `on_primary` checkmarks. When unchecked, use a 1px `ghost border` of the `outline` token.
*   **Action Triggers:** Use the `primary_fixed` color for small "play" or "execute" buttons within cards to signify their high-priority status.

### Data Tables
*   **Forbid Dividers:** Do not use horizontal lines between rows.
*   **Zebra Striping:** Use a subtle shift between `surface_container` and `surface_container_low` to distinguish rows.
*   **Highlight State:** On hover, a row should transition to `surface_bright` or `surface_container_highest` with a 200ms ease-in-out.
*   **Typography:** Column headers use `label-md` in `on_surface_variant` with 5% letter spacing for an editorial, "pro-terminal" feel.

### Input Fields
*   **Surface:** Use `surface_container_lowest` to create a "punched-out" effect.
*   **Focus State:** A 2px `primary` ghost border (40% opacity) indicates focus, alongside a subtle `surface_bright` background shift.

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical layouts (e.g., a wide table next to a narrow filter stack) to create visual interest.
*   **Do** use `tertiary` (#ffb782) sparingly for warnings or "puts" to provide a warm counter-point to the cool navy.
*   **Do** maximize whitespace between data modules to prevent the "spreadsheet fatigue" common in financial apps.

### Don't
*   **Don't** use pure black (#000000). Always use the `surface` navy tokens to maintain tonal depth.
*   **Don't** use 1px dividers. If you feel the need for a line, try an 8px or 16px gap instead.
*   **Don't** use standard "Success Green" unless it is specifically mapped to the `secondary` or `primary` blue tones to maintain the monochromatic signature of the system. Use `on_surface` white for positive numbers to keep the editorial feel.