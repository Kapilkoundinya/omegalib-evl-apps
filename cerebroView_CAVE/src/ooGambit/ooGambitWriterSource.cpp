#include <iostream>

#include "ooGambitWriterSource.h"

/*** Constructor ***/
ooGambitWriterSource::ooGambitWriterSource() {}
/*** Destructor ***/
ooGambitWriterSource::~ooGambitWriterSource() {}

/*** Methods - Public ***/
// create flat (primitive data types only)
void ooGambitWriterSource::createFlat(string FName, vector<double*> aPtCoordMx, vector<int*> aFaceMx, vector<int*> aGroupMx, int aPtDims, int aPtsPerFace) {
	fileName = FName;
	ptCoordMx = aPtCoordMx;
	faceMx = aFaceMx;
	groupMx = aGroupMx;
	ptDims = aPtDims;
	ptsPerFace = aPtsPerFace;
	
	writeReport();
}

void ooGambitWriterSource::writeReport() {
	int i;
	LinesInFile.push_back(GambitHeader);
	LinesInFile.push_back("(0 \"Flat GRID for Generated Networks in Gambit FORMAT - Model Generator A. Linninger, 3/4/2010\")");
	LinesInFile.push_back(GambitBlank);
	LinesInFile.push_back(GambitDim);
	LinesInFile.push_back("(2 2)");
	LinesInFile.push_back(GambitBlank);
	
	addPointSection();
	LinesInFile.push_back(GambitBlank);
	
	addFaceSections();
	LinesInFile.push_back(GambitBlank);
	
	addFinalSection();
	
	ofstream fileOut;
	fileOut.open(fileName.c_str());
	for(i=0; i<LinesInFile.size(); i++){
		fileOut << LinesInFile[i] << endl;
	}
}

void ooGambitWriterSource::addPointSection() {
	int i, j;
	int lastPtIdx = ptCoordMx.size()-1;
	char aLine[30];
	
	sprintf(aLine, "(10 (0 1 1 1 %X))", ptDims);
	string line = aLine;
	LinesInFile.push_back(line);
	sprintf(aLine, "(10 (0 1 %X 1 %X)(", lastPtIdx, ptDims);
	line = aLine;
	LinesInFile.push_back(line);
	
	for(i=1; i<=lastPtIdx; i++){
		line = "";
		for(j=0; j<ptDims; j++){
			sprintf(aLine, "   %15.10e ", ptCoordMx[i][j]);
			string ln = aLine;
			line = line + ln;
		}
		LinesInFile.push_back(line);
	}
	LinesInFile.push_back("))");
}

void ooGambitWriterSource::addFaceSections() {
	int i, j;
	int NFaces = faceMx.size()-1;
	char aLine[30];
	
	LinesInFile.push_back(GambitFaces);
	
	sprintf(aLine, "(13(0 1 %X 0))", NFaces);
	string line = aLine;
	LinesInFile.push_back(line);
	for(i=0; i<groupMx.size(); i++){
		// write one face subSection
		sprintf(aLine, "(13(%X %X %X %X %X)(", groupMx[i][0], groupMx[i][1], groupMx[i][2], 0, 0);
		line = aLine;
		LinesInFile.push_back(line);
		for(j=groupMx[i][1]; j<=groupMx[i][2]; j++){
			line = writeFace(faceMx[j]);
			LinesInFile.push_back(line);
		}
		LinesInFile.push_back("))");
	}
}

string ooGambitWriterSource::writeFace(int* aFaceInfo) {
	int i;
	char aLine[30];
	sprintf(aLine, "%X  ", ptsPerFace);
	string line = aLine;
	
    for(i=0; i<(ptsPerFace+2); i++){
        sprintf(aLine, "%X  ", aFaceInfo[i]);
		string ln = aLine;
		line = line + ln;
    }
	
    return line;
}

void ooGambitWriterSource::addFinalSection() {
	string line;
	
	// Cells info
	LinesInFile.push_back(GambitCells);
	
	line = "(12 (0 1 1 0))";
	LinesInFile.push_back(line);
	
	line = "(12 (0 1 1 1 3))";
	LinesInFile.push_back(line);
	LinesInFile.push_back(GambitBlank);
	
	// zones info
	LinesInFile.push_back(GambitZones);
	LinesInFile.push_back(GambitZ1);
}

