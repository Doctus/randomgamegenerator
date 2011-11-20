RGG v.0992b "Share lives with all things in nature"

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
  Some portraits from:
     http://www5f.biglobe.ne.jp/~itazu/etolier/index.html
     Thank you!

Special Thanks:
  Kaijyuu and Antistone for suggestions and testing
  Everyone from MoMM and #attercop

Changelog:
  v0.992b "Share lives with all things in nature"
    * Fixed some critical bugs with session and map loading.
    * Added a number of default portraits.
    * Added relationship generator.
    * Expanded space tiles slightly.
    * Fixed some issues relating to incorrectly transferred files.

  v0.992 "Share lives with all things in nature"
    * Fixed an issue with map placement when loading sessions.
    * Added language-switching capability.
    * Added language support for Dutch, German, and Japanese.
    * Fixed an issue with setting pog layers.
    * Made pog naming dialog default to pog's current name if
      it has one.
    * Improved transfer socket initialization.
    * Added a Pog Editor plugin through which images can be
      easily edited and saved as pogs.
    * Added several features to assist hosting.
    * Reduced texture "bleed" on tile edges.
    * Added backup controls for zoom and pan in the map window.
    * The IC chat widget now scrolls automatically to a new character.
    * Fixed center-on-pog command.
    * Fixed an issue involving layers and deleting pogs.
    * Added timestamps in OOC chat (can be toggled off).

  v0.991 "Underground souls, rumble"
    * The game window now remembers its last arrangement.
    * Very long text (e.g. in pog names) now tries to wrap.
    * Allowed negative layers for pogs.
    * Added password system to limit who can join a game.
    * Added GM designation.
    * Added music player.
    * Added dance terms to technique generator.

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