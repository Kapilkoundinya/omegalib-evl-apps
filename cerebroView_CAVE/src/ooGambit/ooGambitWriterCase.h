#ifndef OO_GAMBIT_WRITER_CASE_H
#define OO_GAMBIT_WRITER_CASE_H


#include <ctime>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

#include "ooGambitWriterSource.h"
#include "ooGambitConstants.h"


using namespace std;

class ooGambitWriterCase {
	
public:
	// Constructor & Destructor
	ooGambitWriterCase(string exec, char sep);
	~ooGambitWriterCase();
	
	// Methods - Public
	void createFlat(string FName, vector<double*> aPtCoordMx, vector<int*> aFaceMx,
					vector<int*> aGroupMx, vector<double> aFaceRadii, int aPtDims, int aPtsPerFace);
	
	
private:
	// Methods - Private
	void writeGroupDiameter(int grIdx);
	
	// Members
	string exePath;
	string separator;
	ofstream fileOut;
	ooGambitWriterSource *nwkWriter;
	vector<int*> groupMx;
	vector<double> faceRadii;

};

#endif // OO_GAMBIT_WRITER_CASE_H



