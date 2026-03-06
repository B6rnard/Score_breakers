# Development & Response Guidelines for Score Breakers Project

These instructions outline how GitHub Copilot should approach writing code and responding to requests for the Score Breakers application. They are based on the project description and are intended to keep the development consistent, user-friendly, and in line with the project's theme.

---

# Development & Response Guidelines for Score Breakers Project

These instructions outline how GitHub Copilot should approach writing code and responding to requests for the Score Breakers application. They are based on the project description and are intended to keep the development consistent, user-friendly, and in line with the project's theme.

---

## Project Overview

- **Theme**: Arcade-inspired desktop application using Tkinter
- **Goal**: Allow users to browse and navigate through classic arcade-style games with a retro look and feel in a desktop GUI
- **Core Features**:
  1. User profile management (create, save, and login to profiles via Tkinter forms)
  2. Access to at least three custom-made versions of classic games (e.g., Pac-Man, Tetris, Space Invaders)
  3. Visual design evocative of a traditional arcade hall: vibrant colors, simple menus, clear game choices using Tkinter widgets
  4. High-score tracking per user and ability to compare with others, displayed in Tkinter windows

---

## Skill Level and Code Simplicity

- **Level**: Intermediate
- Keep code simple: avoid overly complex patterns, focus on readability, maintainability, and straightforward implementations suitable for intermediate-level developers.

---

## Coding Approach

1. **Modular Reasoning**
   - Break tasks into small, testable components (e.g., authentication module, game engine, score management).
   - Use meaningful names reflecting arcade theme (e.g., `arcadeMenu`, `highScoreTracker`).

2. **Consistent Style**
   - Follow a clear style guide (indentation, naming conventions, comments) appropriate for Python and Tkinter. Keep code readable.
   - Add simple comments to all parts of the code for easy overview.
   - Add comments where logic may not be immediately obvious, especially for game behavior or scoring.

3. **Retro Aesthetic**
   - When implementing UI with Tkinter, use visuals reflecting the arcade hall: neon colors, pixel fonts, simple navigable menus with Buttons, Labels, and Frames.
   - Keep interactions smooth (e.g., scrollable game list using Listbox or Canvas, responsive login forms with Entry widgets).

4. **Simplified Game Implementations**
   - Each classic game should be our own version with basic functionality only, rendered in Tkinter Canvas.
   - Avoid copyrighted assets or mechanics; focus on recognizable themes.
   - Document any game-specific logic or limitations.

5. **Data Persistence**
   - Use a straightforward storage solution (e.g., JSON files for local storage) for profiles and high scores.
   - Ensure high-score tracking updates correctly and can be queried for comparisons.

6. **User Interaction Flow**
   - Document expected flows: sign-up → login → browse games → play score → update highscores, all within Tkinter windows.
   - Provide clear error handling and validation messages in Tkinter dialogs or labels.

7. **Testing & Validation**
   - Write tests where possible (unit tests for game logic, authentication, score updates).
   - Validate user input and handle edge cases (e.g., duplicate usernames, simultaneous score submissions).

8. **Documentation & Communication**
   - Ask clarifying questions before implementing uncertain features.
   - When delivering code or answers, reference the arcade theme and project goals.
   - Respond with concise explanations, organized sections, and appropriate formatting (headings, lists).

9. **Profile Management**
   - Implement simple profile creation, saving to JSON files, and login validation.
   - Ensure profiles persist across sessions and include basic validation (e.g., unique usernames, required fields).

---

## Response Style for the Assistant

- Provide answers with structured formatting (headings, bullets, numbered steps).
- Keep explanations concise but informative; avoid unnecessary verbosity unless the user requests detailed context.
- When referencing filenames or symbols, wrap them in backticks.
- Use blockquotes for important notes or caveats.

---

**Note:** These guidelines should shape both code contributions and conversational responses, ensuring coherence with the arcade-inspired Score Breakers Tkinter application.