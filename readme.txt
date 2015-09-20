RGG v1.04 "Fate and Chance cast lots"

https://github.com/Doctus/randomgamegenerator

Introduction

  RGG is a whiteboad client, primarily designed to facilitate play of
  traditional pen-and-paper role-playing games online, although it's
  usable for a variety of other types of board games and similar
  purposes.

  Releases are generally stable. The current development snapshot
  is not guaranteed to be stable, but often fixes bugs present in
  the most recent release, so consider trying it out.

  You need an open port to host. Make sure your firewall and router
  allow inbound connections for RGG's port. You don't need to worry
  about this if you're just joining a friend's game; only one person
  has to have the port open so s/he can host. The default port is 6812.

  You'll probably want to place some of your own "pogs" (images) in
  the data/pogs folder for use during the game. Most file types are
  supported, although jpg may not be under Windows. Similarly, you can
  put portrait images in data/portraits - the same disclaimer applies.
  Pogs you place and portraits you use will automatically be transferred
  to other players to whom you're connected.

  If you have any questions or comments, or if you want to ask about
  contributing to the project, you can probably contact us most easily
  by e-mail or in one of these places:
    http://www.daydreamspiral.com/forum/
    irc.darkmyst.org#attercop

Requirements

  Python2 or Python3
  PyQt4 or PyQt5
  NumPy
  PyOpenGL

  Optional:
    automodinit
    pillow

Credits

  Coded by:
    Doctus (kirikayuumura.noir@gmail.com)
    NagelBagel (nagelbagel@gmail.com)
    Oipo (kingoipo@gmail.com)

  Art and Styles by:
    Garrick (earthisthering@gmail.com)
    Some portraits from:
      http://www5f.biglobe.ne.jp/~itazu/etolier/index.html
      Thank you!

  Special Thanks:
    Kaijyuu, Bardum, Janra, Wallet, and Antistone for suggestions/testing
    Everyone from MoMM and #attercop

Licensing

  RGG's libraries are licensed under the LGPL v3. For more information,
  please see the notice at the top of each source file and the COPYING
  and COPYING.LESSER files in the "doc" folder.

Changelog

v1.04 "Fate and Chance cast lots"               [in dev], 2015

   Fixes
    * Handle now defaults to local OS-level username instead
      of machine name.
    * Authorship of maps now defaults to the current RGG
      handle.
    * Several menu options and buttons now disable themselves
      when appropriate.
    * URLs in chat widgets now open in the user's browser when
      clicked.
    * Fixed an issue that caused non-hosting instances of RGG
      to fail to propagate session loads over the network.

   Features and Changes
    * Added experimental support for Python 3.x and PyQt5.
    * Substantially restructured the folder hierarchy to place
      rgg.py, data/, etc. at the top level.
    * Added option to set in-character portrait display size.
    * Added a "clear all" button for in-character characters.
    * Added "center everyone on pog" command.
    * Added a dark stylesheet.
    * Added a fantasy stylesheet.
    * Missing dependencies should now be detected and warned about.

  ---

v1.03 "The King that was Not"                 January 29, 2013

   Fixes
    * Fixed hidden pogs sometimes being visible.
    * Fixed the "0kb file" issue for good (probably).
    * Fixed several other transfer-related issues.
    * Fixed several dialogs not displaying the correct icon.
    * Some buttons now disable themselves when appropriate
      rather than doing nothing when clicked.
    * IP/version checks will now work consistently.
    * When placing a pog, the drag image now scales properly.

   Features and Changes
    * Added default tilesets suitable to playing Chess and Go.
    * Added a transfer monitor widget.
    * Added two more generators.
    * Added preview when drawing pentagrams and hexagrams.
    * Moved character sheets to their own save folder.
    * Added transfer command for character sheets.
    * Added arbitrary file transfer command.
    * Made the character creator a normal dock widget instead of
      a completely separate window.
    * Added ability to lock camera to a pog and move it with WASD.
    * Greatly improved pog attributes dialog.
    * Added a remove-all-pogs command to the File menu.
    * The map editor now supports undo/redo and copy-paste.
    * Added simultaneous message display.
    * Tileset sizes will now be saved and automatically loaded.

  ---

v1.02b "Of twilight evenings and of long ago" November 4, 2012

   Features and Changes
    * Allowed in-character whispers.

  ---

v1.02  "Of twilight evenings and of long ago" November 3, 2012

   Fixes
    * Fixed several issues with unicode filepaths.

   Features and Changes
    * Added a preview of the currently selected IC portrait.
    * Updated character creator with mech mode.
    * Vastly improved efficiency of the map editor's
      rectangle draw mode.
    * Clicking a player name will now fill in the appropriate
      command to whisper to that player.
    * Reorganized several menus.
    * Added the ability to prompt other players with questions
      and receive responses.

  ---

v1.01c   "Overmuch magic"                     October 13, 2012

   Features and Changes
    * Added an automatic update system for releases.

  ---

v1.01b   "Overmuch magic"                     October 13, 2012

   Fixes
    * The character creator now exports correctly to unicode file
      paths.
    * Lines, circles, and other shapes now synchronize properly
      over the network.
    * Fixed graphical issues relating to NPOT textures on older
      systems.
    * Added sanity checks to ensure placed pogs do not have
      bizarre file paths.

   Features and Changes
    * To avoid some of the HTML-related errors seen in previous
      versions, chat now uses tags like [i]this[/i] instead.
    * The character creator can now save and load character sheets.
    * Added autosaving and autoloading of session data.
    * The GM may prevent players from moving pogs except those
      he or she specifically designates on a per-player basis.
    * RGG will now attempt to purge empty files from the pog,
      portrait, and tileset folders on startup. (These sometimes
      come into existence due to problems with file transfer.)

  ---

  v1.01   "Overmuch magic"                   September 2, 2012

   Fixes
    * Fixed an issue involving hidden images not being reuploaded
      to the GPU.
    * Invalid pogs will now produce an error icon instead of a
      ZeroDivisionError in the console.
    * Style selection now persists when restarting the program.
    * Non-locked pogs are now preferred over locked pogs when
      selecting.
    * File extensions will now be appended consistently when
      saving on any OS.
    * Fixed issues with right-clicking on pogs.

   Features and Changes
    * It is now possible to draw lines, circles, and rectangles
      in addition to freehand mode. Right-click while drawing to
      select a new shape.
    * The map editor is now a base widget instead of a plug-in.
    * Pogs may now be dragged-and-dropped out of the pog palette.
    * Added a preview when selecting portraits.
    * Added an automated ping system to detect connection loss.
    * Added kick command, allowing host to disconnect users.
    * Added ability to ban particualr IPs from connecting.
    * The 0 (zero) key now resets zoom level to the default.
    * Added a "debug console" to the GUI.
    * Added an Inn Name generator.
    * Integrated the character creator as a plug-in.

  ---

  v1.00b  "Pan saw the tomb and laughed"          June 8, 2012

   Fixes
    * Fixed an error with map position after clearing a session.
    * Fixed several sources of graphical problems.
    * Updated IP-checking system.

   Features
    * Savefiles will now be compressed if possible.
    * It is now possible to use pogs and portraits in subfolders.

  ---

  v1.00   "Pan saw the tomb and laughed"          May 12, 2012

   Fixes
    * Disabled Window menu for incompatible old PyQt versions
    * Fixed erronenous retention of deleted lines in saves
    * IC characters now retain order when loaded
    * Removed stray dependency on Phonon

   Features
    * Added command to close specific maps
    * Added command to clear current session entirely
    * Name generators may now be added as individual script files
    * Several new generators added
    * Added option to change draw timer for older systems

  ---

  v0.993b "Shiny crystal light, energize"     January 29, 2012
    * Cleaned up some obsolete material.
    * Added initial documentation.
    * Added About dialog.
    * Dice macros are now automatically saved.
    * Fixed an OS-related issue with the IP translation system.
    * Improved map editor.

  ---

  v0.993 "Shiny crystal light, energize"       January 6, 2012
    * Removed music from repository
    * Made pog palette update itself automagically
    * Reduced loading time of new IC chat character dialog
    * Added a Window menu
    * Allowed pog images to be dragged directly into the main window
    * Likewise for portrait images and the IC Chat window
    * Pog editor now has a "save portrait" button
    * Pogs without a name now display their file path in the pog
      manager for easier identification.
    * All functions of the pog manager and the pog right-click menu
      are now accessible from both locations.

  ---

  v0.992c "Share lives with all things in nature"
    * Fixed a packaging error in the Windows binary release.

  ---

  v0.992b "Share lives with all things in nature"
    * Fixed some critical bugs with session and map loading.
    * Added a number of default portraits.
    * Added relationship generator.
    * Expanded space tiles slightly.
    * Fixed some issues relating to incorrectly transferred files.

  ---

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

  ---

  v0.991 "Underground souls, rumble"
    * The game window now remembers its last arrangement.
    * Very long text (e.g. in pog names) now tries to wrap.
    * Allowed negative layers for pogs.
    * Added password system to limit who can join a game.
    * Added GM designation.
    * Added music player.
    * Added dance terms to technique generator.

  ---

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

  ---

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

  ---

  v0.97 "Armor won't help the heart stay sharp!"
    * Created this readme
    * Improved map editor interface
    * Restructured save folders: everything now goes in save/
    * Made join dialog remember last inputs
