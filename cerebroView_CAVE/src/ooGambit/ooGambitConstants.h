
#define GambitHeader			"(0 \"GRID in GAMBIT FORMAT - Model Generator A. Linninger, 10/10/2005\")"
#define GambitHeaderNW			"(0 \"GRID for Networks in Gambit FORMAT - Model Generator A. Linninger, 12/26/2007\")"
#define GambitBlank				" "

#define GambitDim				"(0 \"Dimension:\")"
#define GambitPixDim			"(0 \"Pixel Dimension:\")"
#define GambitFaces				"(0 \"Faces:\")"
#define GambitProperties		"(0 \"Face Attributes:\")"
#define GambitCells				"(0 \"Cells:\")"
#define GambitZones				"(0 \"Zones:\")"

#define GambitZ1				"(45 (2 fluid fluid) ())"
#define GambitZ2				"(45 (3 wall wall) ())"
#define GambitZ3				"(45 (5 interior default-interior)())"
#define GambitZ4				"(45 (1 All other faces ) ())"

#define GambitPtBegin			"(10 ("     // beginning of points Block
#define GambitCellBegin			"(12 ("     // beginning of Cell Block
#define GambitFaceBegin			"(13("      // beginning of face block
#define GambitPropBegin			"(14("      // beginning of properties block

// domain keywords
#define GambitResults			"(0 \"Results in Domain:\")"
#define volumeResults			"(0 \"Volume Properties\")"
#define faceResults				"(0 \"Face Properties\")"
#define Boundaries				"(0 \"Neumann Boundary Choices\")"


// Network Strings
#define NWResults				"(0 \"Properties and Results of Network Tubes:\")"
#define NWtubeResults			"(0 \"Tube Properties\")"

// Solid Application Keywords
#define TagMeshFile				"Meshfile"
#define TagSolverSelections		"Solver Selections *********************"
#define TagSolverSelectionsEnd	"Solver Selections End******************"

#define TagVarBegin				"//Begin_Variables ***********************"
#define TagVarEnd				"//End_Variables *************************"
#define TagEquBegin				"//Begin_Equations ***********************"
#define TagEquEnd				"//End_Equations *************************"

#define TagBeginTree			"BeginTree"
#define TagEndTree				"EndTree"



