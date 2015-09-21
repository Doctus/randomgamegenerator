class GlobalState(object):
	"""A state class build to avoid all these global statements."""

	session = None#Session()

	alert = True

	pogSelection = set()
	pogHover = None

	mouseButton = None
	mousePosition = (0, 0)

	pogPlacement = False
	pogPath = "path"

	previousLinePlacement = None #(0, 0) expected
	nextLinePlacement = None

	thickness = 1
	linecolour = [1.0, 1.0, 1.0]
	drawmode = "Freehand"

	GM = None

	storedMessages = []

	moveMode = "free"
	moveablePogs = []

	cameraPog = None
	pogmove = [0, 0]

	dreams = {}

	@staticmethod
	def incrementDreams(target, amount):
		if target not in _state.dreams:
			_state.dreams[target] = 0
		_state.dreams[target] += amount

	@staticmethod
	def getDreams(target):
		if target not in _state.dreams:
			return 0
		return _state.dreams[target]

	@staticmethod
	def initialize(mainApp):
		GlobalState.App = mainApp
