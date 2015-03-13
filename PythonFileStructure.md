# Introduction #

List of python files and their purpose as of 2009-24-8.


# Details #

  * **rggViews:** Functions that do things go here
  * **rggChat:** parses chat commands and calls views
  * **rggRemote:** does RPC, calling views to get work done
  * **rggMenu, rggDockWidgets:** Define guis, raising signals when views should chime in
  * **rggDialogs, rggFields:** Used to receive user input and validate it
  * **rggMap, rggPogs, rggTile:** the model, aka the complicated world state
  * **rggRPC:** definitions of serverRPC and clientRPC
  * **rggNet:** low-level networking
  * **rggNameGenerator, rggDice:** Utility functions
  * **rggSystem:** a layer between qt/bmainmod and python
  * **rgg.py:** Entry point; sets up signals and invokes bmainmod