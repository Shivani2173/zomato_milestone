---
name: Zomato AI Design System
colors:
  surface: '#1e0f0e'
  surface-dim: '#1e0f0e'
  surface-bright: '#473533'
  surface-container-lowest: '#180a09'
  surface-container-low: '#271716'
  surface-container: '#2c1b1a'
  surface-container-high: '#372624'
  surface-container-highest: '#43302f'
  on-surface: '#fadcd9'
  on-surface-variant: '#e4beba'
  inverse-surface: '#fadcd9'
  inverse-on-surface: '#3e2c2b'
  outline: '#ab8986'
  outline-variant: '#5b403e'
  surface-tint: '#ffb3ae'
  primary: '#ffb3ae'
  on-primary: '#68000b'
  primary-container: '#ff5352'
  on-primary-container: '#5c0008'
  inverse-primary: '#ba1724'
  secondary: '#ffb68d'
  on-secondary: '#532200'
  secondary-container: '#ae4f00'
  on-secondary-container: '#ffe7dc'
  tertiary: '#60dac4'
  on-tertiary: '#003730'
  tertiary-container: '#0ba38f'
  on-tertiary-container: '#003029'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad7'
  primary-fixed-dim: '#ffb3ae'
  on-primary-fixed: '#410004'
  on-primary-fixed-variant: '#930014'
  secondary-fixed: '#ffdbc9'
  secondary-fixed-dim: '#ffb68d'
  on-secondary-fixed: '#331200'
  on-secondary-fixed-variant: '#763300'
  tertiary-fixed: '#7ef7e0'
  tertiary-fixed-dim: '#60dac4'
  on-tertiary-fixed: '#00201b'
  on-tertiary-fixed-variant: '#005046'
  background: '#1e0f0e'
  on-background: '#fadcd9'
  surface-variant: '#43302f'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
---

## Brand & Style
The design system is engineered to evoke a sense of premium, high-performance intelligence. It caters to a tech-savvy audience that demands speed, accuracy, and aesthetic sophistication in food-discovery and logistics.

The visual style is a blend of **Modern Minimalism** and **High-Contrast Glassmorphism**. By utilizing a deep, near-black foundation with vibrant coral-to-orange accents, the interface feels energetic yet sophisticated. The aesthetic focuses on "dark-mode first" principles, ensuring that data-heavy interfaces remain legible and reduce eye strain while maintaining a high-fashion, editorial quality. Elements are polished with subtle glows and smooth transitions to reinforce the "AI" narrative of fluid, real-time processing.

## Colors
The palette is rooted in a deep-space grayscale to provide maximum contrast for the AI's core actions. 

- **Primary & Accent:** A "Rich Coral" gradient is the signature mark of the system. It is used sparingly for primary actions, progress indicators, and active states to guide the user's eye.
- **Neutrals:** The background uses a pure #0D0D0F to ensure OLED blacks. Surface tiers (#16171A and #1E1F24) create a logical hierarchy for information containment.
- **Functional:** Success states use a vibrant emerald to indicate connectivity and completion, while muted grays handle secondary metadata and taglines to maintain a clean visual hierarchy.

## Typography
The typographic system utilizes a dual-font approach to balance personality with utility.

- **Headlines (Outfit):** Chosen for its geometric clarity and modern character. Bold and Semi-Bold weights are used to create a strong editorial structure. 
- **Body & UI (Inter):** Used for all functional text, data, and long-form content. Its high x-height and neutral tone ensure legibility against dark backgrounds.
- **Scale:** Large display sizes use tighter letter-spacing for a more "locked-in" appearance, while smaller labels use increased tracking to prevent character blurring on low-brightness screens.

## Layout & Spacing
The spacing rhythm is based on a **4px baseline grid**, ensuring mathematical harmony across all components.

- **Grid System:** A 12-column fluid grid for desktop with 24px gutters. On mobile, the system transitions to a 4-column grid with 16px margins.
- **Content Density:** High-density data areas (like menu lists) utilize `sm` spacing, while immersive AI chat interfaces or hero sections utilize `xl` and `2xl` spacing to create "breathable" luxury.
- **Safe Areas:** All interactive targets maintain a minimum 44px hit-zone, even if the visual container is smaller.

## Elevation & Depth
Depth in this design system is achieved through **Tonal Layering** supplemented by subtle **Ambient Shadows**.

- **Z-Index 0 (Background):** #0D0D0F - The infinite base.
- **Z-Index 1 (Surface):** #16171A - Used for primary card containers. Includes a 1px inner border (stroke) of #FFFFFF at 5% opacity to define edges against the black background.
- **Z-Index 2 (Elevated):** #1E1F24 - Used for hover states, tooltips, and floating menus.
- **Shadows:** A soft `rgba(0, 0, 0, 0.4)` shadow with a 12px blur and 4px offset is applied to elevated elements to create a natural separation from the base surface.
- **Glows:** Primary buttons may use a soft coral outer glow (8px blur, 10% opacity) to simulate a light-emitting interface.

## Shapes
The shape language is "Rounded-Modern," avoiding sharp clinical corners in favor of approachable, organic curves.

- **Cards:** 16px radius creates a friendly, containment-focused look for restaurant tiles and AI summaries.
- **Interactive Elements:** Buttons and inputs use a slightly tighter 12px radius, providing a distinct "utility" feel compared to content cards.
- **Badges/Tags:** 8px radius or full-pill shapes are used for metadata like "Fast Delivery" or "Trending" to make them instantly recognizable as secondary indicators.

## Components
Consistent component behavior is critical for the premium feel of the design system.

- **Buttons:** Primary buttons use the `Accent Gradient`. Text is white with a slight drop shadow for legibility. Secondary buttons use a ghost style with a #1E1F24 background and a subtle white border.
- **Inputs:** Base state is #16171A with a 1px #1E1F24 border. On focus, the border transitions to the primary coral color with a 2px outer glow.
- **Chips/Badges:** Small, high-contrast elements. Use #1E1F24 for the background with the text in `text_muted` (#9CA3AF) or the primary coral for active filtering.
- **Cards:** Utilize the 16px radius. Image headers should have a subtle bottom-to-top black gradient overlay to ensure white text overlay remains readable.
- **AI Feedback Indicator:** A specialized component—a pulsating 4px ring using the Accent Gradient—is used to signal when the AI is "thinking" or processing a request.
- **Lists:** Clean dividers using #1E1F24 at 0.5px thickness. Interactive list items should have a transition duration of 200ms easing into the `surface_elevated` color on hover.