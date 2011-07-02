RGG v.099 "Curses from all directions"

http://code.google.com/p/randomgamegenerator/

Introduction
  RGG is a whiteboad client, primarily designed to facilitate play of 
  traditional pen-and-paper role-playing games online, although it's 
  usable for a variety of other types of board games and similar purposes. 

  You need an open port to host. Look up your firewall/router information
  or search for tutorials on port forwarding. You don't need to worry
  about this if you're just joining a friend's game; only one person
  has to have the port open so s/he can host. The default port is 6812.

  You'll probably want to place some of your own "pogs" (images) in
  the data/pogs folder for use during the game. Most file types are
  supported, although jpg may not be under Windows. Be aware also that
  automatic file transfer to other users is still somewhat buggy. You 
  might need to send them your images some other way. Similarly, you can 
  put portrait images in data/portraits - the same disclaimers apply.

  If you have any questions or comments, you can probably get a hold
  of us most easily in one of these places:
    http://momm.seiken.co.uk/forum
    irc.darkmyst.org#attercop

Coded by:
  Doctus (kirikayuumura.noir@gmail.com)
  NagelBagel (nagelbagel@gmail.com)
  Oipo (kingoipo@gmail.com)

Art by:
  Garrick (earthisthering@gmail.com)

Special Thanks:
  Kaijyuu and Antistone for suggestions and testing
  Everyone from MoMM and #attercop

Changelog:

  v0.99 "Curses from all directions"
    * Pogs and lines are no longer limited to maps. Instead, you can
      place them freely and save a "game session" to store all maps,
      pogs, and lines. (Beware: saving maps does NOT save pogs and lines
      on them now!)
    * Fixed some graphical issues relating to tile edges.
    * Added compressed texture support for increased drawing speed.
    * Added graphics configuration dialog.
    * The game window will try to get the user's attention if it's
      not the active window and the user's name is mentioned in
      OOC chat.
    * Added two generators: food and artifood (artifact food).
    * Restored /proll (private dice roll) functionality.
    * Fixed an issue with IC chat portrait loading.
    * Fixed several bugs relating to lines and erasing.
    * Added a new "celtic" interface theme.
    * Fixed a longstanding issue that was preventing file transfer
      from working correctly in many situations.
    * Fixed transfer of large files.
    * Fixed issues relating to opening multiple maps.
    * Synchronized pog resizing across the network.
    * Added indicator of area being erased with eraser.

  v0.98 "The doom of a planet"
    * "RGG in Space": Massive overhaul of underlying graphics code;
      greatly improves FPS among other optimizations. Renderer now
      uses newer opengl extensions if present and supports mipmapping.
    * Added space tiles.
    * Added more default pogs/portraits.
    * Added ability to open multiple maps at once.
    * Pog plugin commands now work on all selected pogs.
    * Removed some redundant map loading.
    * Fixed a bug involving sending data to an empty group of users.
    * Added circles to show which pogs are selected.
    * Added support for stylesheets.
    * Replaced the dubious plugin loading system with a different, 
      possibly more dubious system.
    * Line-drawing now has more thickness options. (Some may be buggy.)
    * Lines can now be drawn in colour.
    * Added a list of current users.
    * Portrait selection now provides a list of files in the folder.
    * Host dialog now also remembers inputs.
    * Made certain buttons behave more normally.

  v0.97 "Armor won't help the heart stay sharp!"
    * Created this readme
    * Improved map editor interface
    * Restructured save folders: everything now goes in save/
    * Made join dialog remember last inputs