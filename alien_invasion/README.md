Alien Invasion
===
Video game created in Python using pygame and created sprite classes.

Game Description
---

In Alien Invasion, the player controls a rocket ship that appears
at the bottom center of the screen. The player can move the ship
**right** (&rarr;) and **left** ( &larr;) using the arrow keys and shoot bullets using the
**spacebar**. When the game begins, a fleet of aliens fills the sky
and moves across and down the screen. The player shoots and
destroys the aliens. If the player destroys all the aliens, a new fleet
appears that moves faster than the previous fleet. If any alien hits
the player’s ship or reaches the bottom of the screen, the player
loses a ship. If the player loses three ships, the game ends.

To Run Game
---

    python alien_invasion.py

Rules
---

| Controls | Description |
| -------- | ----------- |
| start button | click to begin game. |
| **right** (&rarr;) and **left** ( &larr;) arrow keys | used to move rocket ship along bottom of screen. |
| **spacebar** | used to shoot bullets at alien fleet. Three bullets on board at all times. |
| 'q' key | click 'q' button to quit game and close window.

| On screen | Description |
| --------- | ----------- |
| lives | three lives per round of fleet. Shown in top right corner of screen. |
| alien fleet | rows of alien ships in top half of screen. |
| rocket ship | player icon "flies" across bottom of screen and shoots bullets. |

| Scores | Description |
| ------ | ----------- |
| current score | score for current round or game top left of screen. Score increaes with each round and resets after 3 rounds of alien fleets. |
| high score | overall high score shown in top center of screen. Regularly updates. |

Files 
---

Main:
- **Alien_Invasion:** main run of alien invasion game. Initializes game with defined settings as defined in settings.py (shown below). Runs game from creation of fleets to shooting alien ships and re populating fleet when destroyed for next round.
- **Game_Functions:** refactored code placed here so all game functionality found here and called in alien_invasion.py (shown above). Checks for keyboard/mouse events and conditions for progress in game like bullets hitting ships in fleet or if fleet hits rocket ship.
- **Settings:** predefined settings for bullet, ship and fleet speed as well as lives, bullet width, bullets allowed, and speed up scale for increasing difficulty for level. 

Sprites:
- **Ship:** ship class initializes ships and updates its movements on the screen. Draws ship and centers it with each new round.
- **Bullet:** bullet class initializes bullets and updates its movements on the screen. Draws bullet and updates location as its shot toward alien fleet.
- **Alien:** alien class initializes alien fleet and updates its movement on the screen. Draws fleet and updates movement across screen and down as fleet moves. Checks edge of screen where appropriate. 

Instances:
- **Button:** button class initializes button. Draws button with appropriate message.
- **GameStats:** gamestats class initializes score and level of player. Resets scores as appropriate.
- **Scoreboard:** initialize scoreboard to report scoring information. Draws scoreboard with ships lives, high score, current score and level all across top of screen.

PCC
===

PCC related things found [here](ch12.md)