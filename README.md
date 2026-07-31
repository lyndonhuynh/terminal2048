This project is a recreation of the game '2048' that became very popular some years ago. Here's how the game works:

There is an empty grid to begin with. Then a '2' or '4' will be created randomly on the grid. There's a 90% chance it's a 2. 
Each 'turn' the player can input a direction (up, down, left, and right). Every tile will try to move as far as possible in that direction, stopping when colliding with the outer wall or another tile.
Two tiles with equal value colliding will combine to create one tile with the combined value, so for example, two 512 tiles combine to make a 1024 tile. 
After moving, a new tile is created and it is the player's turn again.

A move cannot be made if that move results in nothing happening (no movement and no merging), and if no moves can be made, the player loses. 
If the player is able to create a '2048' tile before this happens, they win! 
