# Super Martian - Platformer Game

## Features

- **Special Items**: Includes a `SpecialBox` that spawns a `RotatingKey` when hit from below. The key allows the player to win the level.
- **Custom Transitions**: Smooth fade-in and fade-out transitions between levels.
- **Player Animations**: Corrected animations for the player when interacting with the `SpecialBox` and other objects.
- **Level Progression**: Transition logic to move to the next level after completing the current one.
- **Timer System**: Integrated timer system for countdowns and animations using the `Timer` utility.

## Recent Updates

### Special Items
- Added a `SpecialBox` that reacts to player collisions:
  - If the player hits the box from below, it jumps and spawns a `RotatingKey`.
  - The box becomes inactive (gray texture) after being hit.
- The `RotatingKey` rotates smoothly and can be collected by the player to trigger level completion.

### Transitions
- Implemented fade-in and fade-out transitions for smoother level changes.
- Fixed an issue where the transition would get stuck during the fade-out phase.

### Player Animations
- Fixed animation bugs when the player interacts with the `SpecialBox`:
  - The player now correctly switches between `idle` and `walk` states when standing on the box.
  - Adjusted collision logic to ensure the player does not clip through the box.

### Level Progression
- Added logic to transition to the next level after collecting the `RotatingKey`.
- Ensured that the game pauses and transitions smoothly when a level is completed.

### Create new Level
- Integrated new level for enjoy when you take the special key, after transition you going to stay in new level with new tricks.

## How to use new Mechanics

1. **Interact with SpecialBox**: Jump and hit the `SpecialBox` from below to spawn the `RotatingKey`.
2. **Collect Items**: Collect coins and the `RotatingKey` to progress.
3. **Win the Level**: Collect the `RotatingKey` to trigger the level transition.
