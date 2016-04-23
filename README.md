#Author: Gregory Miles
Purpose: CS332L CSULA

This game was made using the pygame library.  All code was written by
Gregory Miles.  The background sprites and fonts are from Kenny Vleugels website
www.kenney.nl the monsters, player and items and attack(s) are from
the TomeTik website:
http://pousse.rapiere.free.fr/tome/
All resoures are from links provided on the CS332L course website.
All maps were made with Tiled:
http://www.mapeditor.org/

Tiled maps can be made and relativly easily implemented into the game,
because they an be exported as json files and json files are really just
python data structures (a combination of dictionaries and lists).

So it is possible to add your own maps to a certain extent, although
the warping from one map to the next needs more work.

The initial inspiration is from a turn based game known as NetHack:
http://www.nethack.org/
NetHack is called "Net" because players can telnet into a NetHack server and
Hack because it is a Hack and Slash.

To start the game start "client.py", requires python 3.5

##Direction controls are:
 y  k  u           
  \ | /               
 h- . -l             
  / | \               
 b  j  n

Space Bar attacks, to attack in a specific direction first press the
key for that direction, then attack.

Monsters will give exp which then levels the player up and restores his life.

If you die you have to start all over again.

Outside the castle, to enter you must go along the right inner wall of the,
castle entrance, this is a bit of a bug, but if I had more time I would
probably reimplement the warps as being colliable rectangles instead of
attempting to check if the player is within a certain distance from the
tiled object square.

The end game is when the player gets the "Sceptre of Yendor".  This either
ends the game or lets the player continue playing, although he can not escape,
the castle...yet.
