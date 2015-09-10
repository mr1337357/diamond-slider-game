Diamond Slider Game
===================

Diamond Slider Game is a shameless knockoff of Bejeweled written in PyGame. It should run on any UNIX system that has pygame, but the controls are aimed at the GCW-Zero. 

Gameplay
--------
Right now gameplay is rather simple. Use the D-Pad to move your cursor around
then use A/B/X/Y to swap the current highlighted gem with another gem in the button's respective direction. If this causes 3 or more gems to line up, the lined up gems will disappear from the map and the gems above them will fall into their place. 

Building
--------
Invoking 
'''
make
'''
will re-create the GCW-Zero's OPK file for the game. Note that this is basically just loading all the files from the game folder into a squashfs volume and then renaming the squashfs volume's file extension to .opk.

