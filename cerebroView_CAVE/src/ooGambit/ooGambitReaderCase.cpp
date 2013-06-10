#include <iostream>

#include "ooGambitReaderCase.h"
#include "ooGambitReaderSource.cpp"


/*** Helper Classes ***/
class vecProp {
private:
	string propName;
	vector<double> values;
	double* range;
	
public:
	vecProp(string s) {
		propName = s;
		range = new double[2];
		range[0] =  9.9e12;
		range[1] = -9.9e12;
	}
	string getPropertyName() {
		return propName;
	}
	double getValue(int idx) {
		return values[idx];
	}
	double* getRange() {
		return range;
	}
	void setValue(int idx, double v) {
		if(idx >= values.size()) values.resize(idx+1);
		values[idx] = v;
		if(v < range[0]) range[0] = v;
		if(v > range[1]) range[1] = v;
	}
};

class timeProp {
private:
	string propName;
	vector< vector<double> > values;
	double* range;
	
public:
	timeProp(string s) {
		propName = s;
		range = new double[2];
		range[0] =  9.9e12;
		range[1] = -9.9e12;
	}
	string getPropertyName() {
		return propName;
	}
	int getNumberOfTimeSteps() {
		return (values[1].size()-1);
	}
	double getValue(int idx, int t) {
		return values[idx][t];
	}
	double* getRange() {
		return range;
	}
	void setValue(int idx, int t, double v) {
		if(idx >= values.size()) values.resize(idx+1);
		if(t >= values[idx].size()) values[idx].resize(t+1);
		values[idx][t] = v;
		if(v < range[0]) range[0] = v;
		if(v > range[1]) range[1] = v;
	}
};



/*** Constructor ***/
ooGambitReaderCase::ooGambitReaderCase(string exec) {
	exePath = exec;
	nwkReader = NULL;
}
/*** Destructor ***/
ooGambitReaderCase::~ooGambitReaderCase() {}

/*** Methods - Public ***/
// create flat (primitive data types only)
void ooGambitReaderCase::createFlat(string FName) {
	int i;
	
	ifstream fileIn;
	fileIn.open(FName.c_str());
	
	// exit if file does not exist
	if(!fileIn.is_open()){
		printf("The selected casefile: \"%s\" does not exist. Please check file.\n", FName.c_str());
		//cout << "The selected casefile: \"" << FName << "\" does not exist. Please check file." << endl;
		return;
	}
	

	// begin reading Case file
	printf("\n<===============================================================>\n");
	printf("STARTED READING \"%s\"\n\n", FName.c_str());
	// start timer
	unsigned int start = clock();

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
	IdxS1 = findIndexWithSubstringBetweenElements("meshfile=", 0, LinesInFile.size()-1);
	IdxS2 = findIndexWithSubstringBetweenElements("(vector=", 0, LinesInFile.size()-1);
	if(IdxS1 == -1){
		printf("\"%s\" is not a proper Case file\n", FName.c_str());
		return;
	}
	
	// read meshfile
	if(nwkReader != NULL){
		delete nwkReader;
	}
	
	string nwkFile = exePath + readMeshfileName(IdxS1);
	int nPoints, dims, nFaces, iFaces, bFaces, ptsPerFace, nGroups;
	nwkReader = new ooGambitReaderSource();
	nwkReader->createFlat(nwkFile);
	nwkReader->GetPointFieldDimensions(nPoints, dims);
	nwkReader->GetFaceFieldDimensions(nFaces, iFaces, bFaces, ptsPerFace, nGroups);

	ptConnectDegree.clear();     ptConnectDegree.resize(nPoints+1, 0);
	ptAvgRadii.clear();          ptAvgRadii.resize(nPoints+1, 0.0);
	faceRadii.clear();           faceRadii.resize(nFaces+1, 0.0);
	
	// read face section
	printf("Adding radii and property information...\n");
	readFaceRadiiAndProperties();
	for(i=0; i<vectorProperty.size(); i++){
		printf("  %s\n", vectorProperty[i]->getPropertyName().c_str());
	}
	for(i=0; i<timeProperty.size(); i++){
		printf("  %s: %d time steps\n", timeProperty[i]->getPropertyName().c_str(), timeProperty[i]->getNumberOfTimeSteps());
	}
	
	// clear string list containing entire file
	LinesInFile.clear();
	
	// end timer
	double readTime = ((double)(clock() - start) / (double)CLOCKS_PER_SEC);
	
	// finished
	printf("\nFINISHED READING \"%s\" in %lf seconds\n", FName.c_str(), readTime);
	printf("<===============================================================>\n\n");
}
// read meshfile name
string ooGambitReaderCase::readMeshfileName(int idx) {
	int pos;
	pos = LinesInFile[idx].find("=");
	
	return LinesInFile[idx].substr(pos+1, LinesInFile[idx].length()-pos-1); 
}

/*** Methods - Private ***/
// reads face and group matrices
void ooGambitReaderCase::readFaceRadiiAndProperties() {
	int idx = IdxS2;
	
	while(idx > 0){
		int pos1, pos2, startSearch;
		pos1 = LinesInFile[idx].find("=Dia");
		if(pos1 >= 0){
			startSearch = readRadiiHeader(idx+1);
		}
		else{
			pos1 = LinesInFile[idx].find("=");
			pos2 = LinesInFile[idx].find(" ");
			string property = LinesInFile[idx].substr(pos1+1, pos2-pos1-1);
			string type = LinesInFile[idx].substr(pos2+1, LinesInFile[idx].length()-pos2-2);
			pos1 = property.find("|");
			if(type.substr(0,5) == "group"){
				if(pos1 >= 0){
					int i;
					int timeStep = atoi(property.substr(pos1+1, property.length()-pos1-1).c_str());
					property = property.substr(0, pos1);
					bool inList = false;
					for(i=0; i<timeProperty.size(); i++){
						if(timeProperty[i]->getPropertyName() == property){
							inList = true;
						}
					}
					if(inList == false){
						timeProp *newTimeProp = new timeProp(property);
						timeProperty.push_back(newTimeProp);
					}
					startSearch = readTimePropertyHeader(timeProperty, idx+1, timeStep, property);
				}
				else{
					
					int i;
					bool inList = false;
					for(i=0; i<vectorProperty.size(); i++){
						if(vectorProperty[i]->getPropertyName() == property){
							inList = true;
						}
					}
					if(inList == false){
						vecProp *newVectorProp = new vecProp(property);
						vectorProperty.push_back(newVectorProp);
					}
					startSearch = readVectorPropertyHeader(vectorProperty, idx+1, property);
				}
			}
			else if(type.substr(0,4) == "cell"){
				if(pos1 >= 0){
					int i;
					int timeStep = atoi(property.substr(pos1+1, property.length()-pos1-1).c_str());
					property = property.substr(0, pos1);
					bool inList = false;
					for(i=0; i<cellTimeProperty.size(); i++){
						if(cellTimeProperty[i]->getPropertyName() == property){
							inList = true;
						}
					}
					if(inList == false){
						timeProp *newTimeProp = new timeProp(property);
						cellTimeProperty.push_back(newTimeProp);
					}
					startSearch = readTimePropertyHeader(cellTimeProperty, idx+1, timeStep, property);
				}
				else{
					
					int i;
					bool inList = false;
					for(i=0; i<cellVectorProperty.size(); i++){
						if(cellVectorProperty[i]->getPropertyName() == property){
							inList = true;
						}
					}
					if(inList == false){
						vecProp *newVectorProp = new vecProp(property);
						cellVectorProperty.push_back(newVectorProp);
					}
					startSearch = readVectorPropertyHeader(cellVectorProperty, idx+1, property);
				}
			}
		}
		idx = findIndexWithSubstringBetweenElements("(vector=", startSearch, LinesInFile.size()-1);
	}
}

// reads radii header
int ooGambitReaderCase::readRadiiHeader(int idx) {
	int i, pos1, pos2, pos3;
	pos1 = LinesInFile[idx].find("type=");
	pos2 = LinesInFile[idx].find("value=");
	pos3 = LinesInFile[idx].find(")");
	
	string type = LinesInFile[idx].substr(pos1+5, 5);
	
	if(type == "const"){
		double value = atof(LinesInFile[idx].substr(pos2+6, pos3-pos2-6).c_str()) / 2.0;
		vector<int> ptArray;
		ptArray = parseLineForIntegersNew(Clean(LinesInFile[idx+1]));
		
		vector<int*> faceMx = nwkReader->getFaceMatrix();
		for(i=ptArray[1]; i<=ptArray[2]; i++){
			faceRadii[i] = value;
			int p1_idx = faceMx[i][0];
			int p2_idx = faceMx[i][1];
			ptAvgRadii[p1_idx] = ((ptAvgRadii[p1_idx]*ptConnectDegree[p1_idx]) + value) / (ptConnectDegree[p1_idx]+1);
			ptConnectDegree[p1_idx] += 1;
			ptAvgRadii[p2_idx] = ((ptAvgRadii[p2_idx]*ptConnectDegree[p2_idx]) + value) / (ptConnectDegree[p2_idx]+1);
			ptConnectDegree[p2_idx] += 1;
		}
		
		return (idx+1);
	}
	else{
		vector<int> ptArray;
		ptArray = parseLineForIntegersNew(Clean(LinesInFile[idx+1]));
		readFaceRadiiFlat(idx+2, ptArray[1], ptArray[2]);
		
		return ((idx+2) + (ptArray[2]-ptArray[1]));
	}
}

// reads one face section
void ooGambitReaderCase::readFaceRadiiFlat(int fromIdx, int startIdx, int endIdx) {
	int i;
	
	vector<int*> faceMx = nwkReader->getFaceMatrix();
	for(i=startIdx; i<=endIdx; i++){
		double value = atof(LinesInFile[fromIdx+(i-startIdx)].c_str()) / 2.0;
		faceRadii[i] = value;
		int p1_idx = faceMx[i][0];
		int p2_idx = faceMx[i][1];
		ptAvgRadii[p1_idx] = ((ptAvgRadii[p1_idx]*ptConnectDegree[p1_idx]) + value) / (ptConnectDegree[p1_idx]+1);
		ptConnectDegree[p1_idx] += 1;
		ptAvgRadii[p2_idx] = ((ptAvgRadii[p2_idx]*ptConnectDegree[p2_idx]) + value) / (ptConnectDegree[p2_idx]+1);
		ptConnectDegree[p2_idx] += 1;
	}
}

// read vector propert header
int ooGambitReaderCase::readVectorPropertyHeader(vector<vecProp*> vProp, int idx, string prop) {
	int i, pos1, pos2, pos3;
	pos1 = LinesInFile[idx].find("type=");
	pos2 = LinesInFile[idx].find("value=");
	pos3 = LinesInFile[idx].find(")");
	
	string type = LinesInFile[idx].substr(pos1+5, 5);
	
	vecProp *currentVectorProp = NULL;
	for(i=0; i<vProp.size(); i++){
		if(vProp[i]->getPropertyName() == prop){
			currentVectorProp = vProp[i];
		}
	}
	
	if(type == "const"){
		double value = atof(LinesInFile[idx].substr(pos2+6, pos3-pos2-6).c_str()) / 2.0;
		vector<int> ptArray;
		ptArray = parseLineForIntegersNew(Clean(LinesInFile[idx+1]));

		for(i=ptArray[1]; i<=ptArray[2]; i++){
			currentVectorProp->setValue(i, value);
		}
		
		return (idx+1);
	}
	else{
		vector<int> ptArray;
		ptArray = parseLineForIntegersNew(Clean(LinesInFile[idx+1]));
		for(i=ptArray[1]; i<=ptArray[2]; i++){
			double value = atof(LinesInFile[idx+2+(i-ptArray[1])].c_str());
			currentVectorProp->setValue(i, value);
		}
		
		return ((idx+2) + (ptArray[2]-ptArray[1]));
	}
}

// reads time property header
int ooGambitReaderCase::readTimePropertyHeader(vector<timeProp*> tProp, int idx, int time, string prop) {
	int i, pos1, pos2, pos3;
	pos1 = LinesInFile[idx].find("type=");
	pos2 = LinesInFile[idx].find("value=");
	pos3 = LinesInFile[idx].find(")");
	
	string type = LinesInFile[idx].substr(pos1+5, 5);
	
	timeProp *currentTimeProp = NULL;
	for(i=0; i<tProp.size(); i++){
		if(tProp[i]->getPropertyName() == prop){
			currentTimeProp = tProp[i];
		}
	}
	
	if(type == "const"){
		double value = atof(LinesInFile[idx].substr(pos2+6, pos3-pos2-6).c_str()) / 2.0;
		vector<int> ptArray;
		ptArray = parseLineForIntegersNew(Clean(LinesInFile[idx+1]));
		
		for(i=ptArray[1]; i<=ptArray[2]; i++){
			currentTimeProp->setValue(i, time, value);
		}
		
		return (idx+1);
	}
	else{
		vector<int> ptArray;
		ptArray = parseLineForIntegersNew(Clean(LinesInFile[idx+1]));
		for(i=ptArray[1]; i<=ptArray[2]; i++){
			double value = atof(LinesInFile[idx+2+(i-ptArray[1])].c_str());
			currentTimeProp->setValue(i, time, value);
		}
		
		return ((idx+2) + (ptArray[2]-ptArray[1]));
	}
}

// find line of containing given string between a start and end line
int ooGambitReaderCase::findStringBetweenLines(int idx1, int idx2, string aString) {
	int i;
	int pos;
	
	for(i=idx1; i<=idx2; i++){
		pos = LinesInFile[i].find(aString);
		if(pos >= 0) return i;
	}
	
	return -1;
}

// parses a line for a list of integers
vector<int> ooGambitReaderCase::parseLineForIntegersNew(string aLine) {
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

// removes leading identifiers
string ooGambitReaderCase::Clean(string aLine) {
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

// finds the index in a list that contains the wanted substring
int ooGambitReaderCase::findIndexWithSubstringBetweenElements(string searchFor, int startIdx, int endIdx) {
	int i;
	
	for(i=startIdx; i<=endIdx; i++){
		int pos;
		pos = LinesInFile[i].find(searchFor);
		if(pos >= 0){
			return i;
		}
	}
	
	return -1;
}

// return the average point radii
vector<double> ooGambitReaderCase::getPtAvgRadii() {
	return ptAvgRadii;
}

// return the face radii
vector<double> ooGambitReaderCase::getFaceRadii() {
	return faceRadii;
}

vector<vecProp*> ooGambitReaderCase::getVectorProperties() {
	return vectorProperty;
}

vector<timeProp*> ooGambitReaderCase::getTimeProperties() {
	return timeProperty;
}

vector<vecProp*> ooGambitReaderCase::getCellVectorProperties() {
	return cellVectorProperty;
}

vector<timeProp*> ooGambitReaderCase::getCellTimeProperties() {
	return cellTimeProperty;
}

ooGambitReaderSource* ooGambitReaderCase::getSource() {
	return nwkReader;
}







