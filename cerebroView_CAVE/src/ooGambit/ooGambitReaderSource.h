#ifndef OO_GAMBIT_READER_SOURCE_H
#define OO_GAMBIT_READER_SOURCE_H


#include <ctime>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

#include "ooGambitConstants.h"


using namespace std;

class ooGambitReaderSource {
	
public:
	// Constructor & Destructor
	ooGambitReaderSource();
	~ooGambitReaderSource();
	
	// Methods - Public
	void createFlat(string FName);
	void GetPointFieldDimensions(int& aNPoints, int& dims);
	void GetFaceFieldDimensions(int& aNFaces, int& aIFaces, int& aBFaces, int& ptsPerFace, int& numGroups);
	void GetVolumeFieldDimensions(int& aNVolumes, int& aINVolumes, int& aBNVolumes);
	vector<double*> getPointMatrix();
	vector<int*> getFaceMatrix();
	vector<int*> getGroupMatrix();
	
private:
	// Methods - Private
	void readPointSectionHeader(int& nrPoints, int& fromIdx, int& toIdx);
	void readPointCoordinates(int fromIdx, int toIdx);
	int readGlobalFaceSectionHeader(int& nrFaces);
	void readFaceMatrixAndGroups();
	bool readFaceSectionFlat(int& startIdx, int& endIdx, int& iFace);
	bool IsThisABoundarySection(int firstLineIdx);
	void swapBoundaryFaceValues(vector<int>& anArray);
	int parseForNrOfInteriorVolumes();
	int findStringBetweenLines(int idx1, int idx2, string aString);
	vector<int> parseLineForIntegersNew(string aLine);
	vector<double> parseLineForDoublesNew(string aLine);
	string Clean(string aLine);
	void StoreSectionInGroupMX(vector<int> aFaceHeader);
	int findIndexWithSubstringBetweenElements(vector<string> list, string searchFor, int startIdx, int endIdx);
	
	// Members
	int IdxS1, IdxS2, IdxS3;
	vector<string> LinesInFile;
	int NPoints;
	int NFaces, iNFaces, bNFaces;
	int NVolumes, iNVolumes, bNVolumes;
	int dimensions, nrOfPointsPerFace, nrOfGroups;
	vector<double*> ptCoordMx;
	vector<int*> faceMx;
	vector<int*> aGrMx;

};

#endif // OO_GAMBIT_READER_SOURCE_H



