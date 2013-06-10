#ifndef OO_GAMBIT_READER_CASE_H
#define OO_GAMBIT_READER_CASE_H


#include <ctime>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

#include "ooGambitReaderSource.h"
#include "ooGambitConstants.h"


using namespace std;

class vecProp;
class timeProp;

class ooGambitReaderCase {
	
public:
	// Constructor & Destructor
	ooGambitReaderCase(string exec);
	~ooGambitReaderCase();
	
	// Methods - Public
	void createFlat(string FName);
	vector<double> getPtAvgRadii();
	vector<double> getFaceRadii();
	vector<vecProp*> getVectorProperties();
	vector<timeProp*> getTimeProperties();
	vector<vecProp*> getCellVectorProperties();
	vector<timeProp*> getCellTimeProperties();
	ooGambitReaderSource* getSource();
	
private:
	// Methods - Private
	string readMeshfileName(int idx);
	void readFaceRadiiAndProperties();
	int readRadiiHeader(int idx);
	void readFaceRadiiFlat(int fromIdx, int startIdx, int endIdx);
	int readVectorPropertyHeader(vector<vecProp*> vProp, int idx, string prop);
	int readTimePropertyHeader(vector<timeProp*> tProp, int idx, int time, string prop);
	int findStringBetweenLines(int idx1, int idx2, string aString);
	vector<int> parseLineForIntegersNew(string aLine);
	string Clean(string aLine);
	int findIndexWithSubstringBetweenElements(string searchFor, int startIdx, int endIdx);
	
	// Members
	string exePath;
	int IdxS1, IdxS2;
	ooGambitReaderSource *nwkReader;
	vector<string> LinesInFile;
	int NPoints, NFaces;
	vector<int> ptConnectDegree;
	vector<double> ptAvgRadii;
	vector<double> faceRadii;
	vector<vecProp*> vectorProperty;
	vector<timeProp*> timeProperty;
	vector<vecProp*> cellVectorProperty;
	vector<timeProp*> cellTimeProperty;

};

#endif // OO_GAMBIT_READER_CASE_H



