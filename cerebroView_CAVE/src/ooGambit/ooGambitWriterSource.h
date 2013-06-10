#ifndef OO_GAMBIT_WRITER_SOURCE_H
#define OO_GAMBIT_WRITER_SOURCE_H


#include <ctime>
#include <fstream>
#include <string>
#include <vector>

#include "ooGambitConstants.h"


using namespace std;

class ooGambitWriterSource {
	
public:
	// Constructor & Destructor
	ooGambitWriterSource();
	~ooGambitWriterSource();
	
	// Methods - Public
	void createFlat(string FName, vector<double*> aPtCoordMx, vector<int*> aFaceMx, 
					vector<int*> aGroupMx, int aPtDims, int aPtsPerFace);
	
private:
	// Methods - Private
	void writeReport();
	void addPointSection();
	void addFaceSections();
	string writeFace(int* aFaceInfo);
	void addFinalSection();
	
	
	// Members
	string fileName;
	vector<string> LinesInFile;
	int ptDims;
	int ptsPerFace;
	vector<double*> ptCoordMx;
	vector<int*> faceMx;
	vector<int*> groupMx;

};

#endif // OO_GAMBIT_WRITER_SOURCE_H



