#include <iostream>

#include "ooGambitReaderSource.h"

/*** Constructor ***/
ooGambitReaderSource::ooGambitReaderSource() {}
/*** Destructor ***/
ooGambitReaderSource::~ooGambitReaderSource() {}

/*** Methods - Public ***/
// create flat (primitive data types only)
void ooGambitReaderSource::createFlat(string FName) {
	int fromIdx, toIdx; 
	
	fstream fileIn;
	fileIn.open(FName.c_str());
	
	// exit if file does not exist
	if(!fileIn.is_open()){
		printf("The selected meshfile: \"%s\" does not exist. Please check file.\n", FName.c_str());
		//cout << "The selected meshfile: \"" << FName << "\" does not exist. Please check file." << endl;
		return;
	}
	
	// store each line of file into an Array List
	int lnNo = 0;
	string aLine;
	LinesInFile.resize(10000);
	while(getline(fileIn, aLine)){
		if(lnNo >= LinesInFile.size()) LinesInFile.resize(2*LinesInFile.size());
		if(aLine.length() > 0 && aLine[aLine.length()-1] == '\r') aLine.erase(aLine.length()-1, 1);
		LinesInFile[lnNo] = aLine;
		lnNo++;
	}
	LinesInFile.resize(lnNo);
	
	// reject file if it does not have proper format
	IdxS1 = findIndexWithSubstringBetweenElements(LinesInFile, GambitDim, 0, LinesInFile.size()-1);
	IdxS2 = findIndexWithSubstringBetweenElements(LinesInFile, GambitFaces, 0, LinesInFile.size()-1);
	IdxS3 = findIndexWithSubstringBetweenElements(LinesInFile, GambitZones, 0, LinesInFile.size()-1);
	if(IdxS1 == -1){
		printf("\"%s\" is not a proper Gambit file\n", FName.c_str());
		//cout << "\"" << FName << "\" is not a proper Gambit file" << endl;
		return;
	}
	
	// begin read proper Gambit file
	// read points section
	printf("Adding point information... "); fflush(stdout);
	//cout << "Adding point information... ";
	readPointSectionHeader(NPoints, fromIdx, toIdx);
	ptCoordMx.clear();  ptCoordMx.resize(NPoints+1);
	readPointCoordinates(fromIdx, toIdx);
	printf("read in %d points\n", NPoints);
	//cout << "read in " << NPoints << " points" << endl;
	
	// read face section
	printf("Adding face and group information... "); fflush(stdout);
	//cout << "Adding face and group information... ";
	readFaceMatrixAndGroups();
	printf("read in %d faces and %d groups\n", NFaces, nrOfGroups);
	//cout << "read in " << NFaces << " faces and " << nrOfGroups << " groups" << endl;
	
	// clear string list containing entire file
	LinesInFile.clear();
}

// gets point dimension information
void ooGambitReaderSource::GetPointFieldDimensions(int& aNPoints, int& dims) {
	aNPoints = NPoints;
	dims = dimensions;
}

// gets face dimension information
void ooGambitReaderSource::GetFaceFieldDimensions(int& aNFaces, int& aIFaces, int& aBFaces, int& ptsPerFace,  int& numGroups) {
	aNFaces = NFaces;
	aIFaces = iNFaces;
	aBFaces = bNFaces;
	ptsPerFace = nrOfPointsPerFace;
	numGroups = nrOfGroups;
}

// gets volume dimension information
void ooGambitReaderSource::GetVolumeFieldDimensions(int& aNVolumes, int& aINVolumes, int& aBNVolumes) {
	aNVolumes = NVolumes;
	aINVolumes = iNVolumes;
	aBNVolumes = bNVolumes;
}

/*** Methods - Private ***/
// reads the point section header
void ooGambitReaderSource::readPointSectionHeader(int& nrPoints, int& fromIdx, int& toIdx) {
	int idx;
	string aLine;
	vector<int> ptArray;
	
	// find first point block
	idx = findIndexWithSubstringBetweenElements(LinesInFile, GambitPtBegin, IdxS1, IdxS2);
	aLine = LinesInFile[idx+1]; // skip a line
	ptArray = parseLineForIntegersNew(Clean(aLine));
	
	fromIdx = idx + 1 + ptArray[1];
	toIdx   = idx + 1 + ptArray[2];
	dimensions = ptArray[4]; // 2 => 2D points (x,y), 3=> 3D points (x,y,z)
	nrPoints = toIdx - fromIdx + 1;
}

// reads 2D or 3D pt coordinates into ptCoordMx
void ooGambitReaderSource::readPointCoordinates(int fromIdx, int toIdx) {
	int i, j;
	int pointIdx;
	vector<double> aPtCoordArray;
	
	pointIdx = 1;
	for(i=fromIdx; i<=toIdx; i++){
		aPtCoordArray = parseLineForDoublesNew(LinesInFile[i]);
		double* ptCoord = new double[dimensions];
		for(j=0; j<dimensions; j++){
			ptCoord[j] = aPtCoordArray[j];
		}
		ptCoordMx[pointIdx] = ptCoord;
		pointIdx++;
	}
}

// reads the global face section header 
int ooGambitReaderSource::readGlobalFaceSectionHeader(int& nrFaces) {
	int idx;
	string aLine;
	vector<int> ptArray;
	
	// read first FaceLine containing the indices of all faces ==> (13(
	idx = findIndexWithSubstringBetweenElements(LinesInFile, GambitFaceBegin, IdxS2, IdxS3);
	
	aLine = LinesInFile[idx];
	
	ptArray = parseLineForIntegersNew(Clean(aLine));
	nrFaces = ptArray[2];  // Total number of faces
	
	aLine = LinesInFile[idx+2]; // first faces start two lines offset
	ptArray = parseLineForIntegersNew(Clean(aLine));
	nrOfPointsPerFace = ptArray[0];
	
	return idx;
}

// reads face and group matrices
void ooGambitReaderSource::readFaceMatrixAndGroups() {
	int fromIdx, toIdx, iFace;
	bool isBoundary;
	
	nrOfGroups = 0;
	
	fromIdx = readGlobalFaceSectionHeader(NFaces);
	faceMx.clear();  faceMx.resize(NFaces+1);
	
	fromIdx++;
	iFace = 1;
	bNFaces = 0;
	while(iFace <= NFaces){
		isBoundary = readFaceSectionFlat(fromIdx, toIdx, iFace);
		if(isBoundary) bNFaces = iFace - 1;
		fromIdx = toIdx;
	}
	
	iNFaces = NFaces - bNFaces;
	iNVolumes = parseForNrOfInteriorVolumes();
	bNVolumes = bNFaces;
	NVolumes = iNVolumes + bNVolumes;
}

// reads one face section
bool ooGambitReaderSource::readFaceSectionFlat(int& startIdx, int& endIdx, int& iFace) {
	int i, j;
	int fromIdx, toIdx;
	vector<int> faceInfo;
	string aLine;
	int sectionIdx;
	
	aLine = LinesInFile[startIdx];
	faceInfo = parseLineForIntegersNew(Clean(aLine));
    
	// Section Index
	sectionIdx = faceInfo[0];
	StoreSectionInGroupMX(faceInfo);
	fromIdx = startIdx + 1;
   
	// read one line less
	toIdx = fromIdx + (faceInfo[2] - faceInfo[1]); // number of new faces
	for(i=fromIdx; i<=toIdx; i++){
		faceInfo = parseLineForIntegersNew(LinesInFile[i]);
		swapBoundaryFaceValues(faceInfo);   // swap if face starts with a zero
		int* face = new int[nrOfPointsPerFace+2];		
		for(j=0; j<nrOfPointsPerFace+2; j++){
			face[j] = faceInfo[j+1];
		}
		faceMx[iFace] = face;
		// faceMx[iFace,_GroupID] = sectionIdx; // what is _GroupID (where is it defined) ???
		iFace++;
	}
	endIdx = toIdx + 2; // push to new face and include one linefeed for '))'
	
	return IsThisABoundarySection(fromIdx);
}

// determines if section is a boundary or not
bool ooGambitReaderSource::IsThisABoundarySection(int firstLineIdx) {
	vector<int> firstFaceInfo;
	
	firstFaceInfo = parseLineForIntegersNew(LinesInFile[firstLineIdx]);
	if((firstFaceInfo[firstFaceInfo.size()-1] = 0) || (firstFaceInfo[firstFaceInfo.size()-2] = 0)){
		return true;
	}
	return false;
}

// swaps boundary face values
void ooGambitReaderSource::swapBoundaryFaceValues(vector<int>& anArray) {
	int anIndex;
	
	if(anArray[4] == 0) return;
	if(anArray[3] == 0){
		// swap point indixes
		anIndex = anArray[1]; 
		anArray[1] = anArray[2];
		anArray[2] = anIndex;
		// swap volume indices
		anIndex = anArray[3];
		anArray[3] = anArray[4];
		anArray[4]= anIndex;
	}
}

// parses for number of interior volumes
int ooGambitReaderSource::parseForNrOfInteriorVolumes() {
	int I1;
	string aLine;
	vector<int> ptArray;
	
    I1 = findStringBetweenLines(0, LinesInFile.size()-1, GambitCellBegin);
    aLine = LinesInFile[I1];
    ptArray = parseLineForIntegersNew(Clean(aLine));
	return ptArray[2];
}

// find line of containing given string between a start and end line
int ooGambitReaderSource::findStringBetweenLines(int idx1, int idx2, string aString) {
	int i;
	int pos;
	
	for(i=idx1; i<=idx2; i++){
		pos = LinesInFile[i].find(aString);
		if(pos >= 0) return i;
	}
	
	return -1;
}

// parses a line for a list of integers
vector<int> ooGambitReaderSource::parseLineForIntegersNew(string aLine) {
	vector<int> result;
	
	stringstream ss;
	ss.str(aLine);
	while(!ss.eof()){
		int val;
		ss >> hex >> val;
		result.push_back(val);
	}
	
	return result;
}

vector<double> ooGambitReaderSource::parseLineForDoublesNew(string aLine) {
	vector<double> result;
	
	stringstream ss;
	ss.str(aLine);
	while(!ss.eof()){
		double val;
		ss >> val;
		result.push_back(val);
	}
	
	return result;
}

// removes leading identifiers
string ooGambitReaderSource::Clean(string aLine) {
	int pos;
	string replaceStr;
	
	// clean point section
	replaceStr = GambitPtBegin;
	pos = aLine.find(replaceStr);
	if(pos >= 0) aLine.replace(pos, replaceStr.length(), "");
	
	// clean face section
	replaceStr = GambitFaceBegin;
	pos = aLine.find(replaceStr);
	if(pos >= 0) aLine.replace(pos, replaceStr.length(), "");
	
	// clean cell section
	replaceStr = GambitCellBegin;
	pos = aLine.find(replaceStr);
	if(pos >= 0) aLine.replace(pos, replaceStr.length(), "");
	
	// remove brackets
	do{
		replaceStr = "(";
		pos = aLine.find(replaceStr);
		if(pos >= 0) aLine.replace(pos, replaceStr.length(), "");
	}while(pos >= 0);
	do{
		replaceStr = ")";
		pos = aLine.find(replaceStr);
		if(pos >= 0) aLine.replace(pos, replaceStr.length(), "");
	}while(pos >= 0);
	
	return aLine;
}

// stores section in the group matrix
void ooGambitReaderSource::StoreSectionInGroupMX(vector<int> aFaceHeader) {
	int* group = new int[3];
	group[0] = aFaceHeader[0];
	group[1] = aFaceHeader[1];
	group[2] = aFaceHeader[2];

	aGrMx.push_back(group);
	
	// increment number of groups
	nrOfGroups++;
}

// finds the index in a list that contains the wanted substring
int ooGambitReaderSource::findIndexWithSubstringBetweenElements(vector<string> list, string searchFor, int startIdx, int endIdx) {
	int i;
	
	for(i=startIdx; i<=endIdx; i++){
		int pos;
		pos = list[i].find(searchFor);
		if(pos >= 0){
			return i;
		}
	}
	
	return -1;
}

// return the point matrix
vector<double*> ooGambitReaderSource::getPointMatrix() {
	return ptCoordMx;
}

// return the face matrix
vector<int*> ooGambitReaderSource::getFaceMatrix() {
	return faceMx;
}

// return the group matrix
vector<int*> ooGambitReaderSource::getGroupMatrix() {
	return aGrMx;
}







