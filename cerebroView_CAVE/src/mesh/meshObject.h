/*************************************************
 ****                                         ****
 ****               Mesh Object               ****
 ****                                         ****
 *************************************************/

#ifndef MESH_OBJECT_H
#define MESH_OBJECT_H

#include "../ooGambit/ooGambitReaderCase.h"


enum {X_AXIS, Y_AXIS, Z_AXIS};
enum {MIN, MAX};

using namespace std;

// mesh object class
class meshObject {
private:
	// point info
	vector<double*> pointMx;
	vector<double> ptAvgRadii;
	double ptRange[3][2];
	double* radiiRange; 
	int nrOfPoints;
	int ptDims;
	
	// face info
	vector<int*> faceMx;
	vector<double> faceRadii;
	vector<vecProp*> vectorProperties;
	vector<timeProp*> timeProperties;
	int nrOfFaces;
	int ptsPerFace;
	
	// group info
	vector<int*> groupMx;
	int nrOfGroups;
	
	// cell info
	vector< vector<int> > cellMx;
	int nrOfCells;
	vector<vecProp*> cellVectorProperties;
	vector<timeProp*> cellTimeProperties;
	
	// point connectivity info
	vector< vector<int> > pt2ptMx;
	vector< vector<int> > pt2faceMx;
	int maxConnect;

public:	
	// Constructor/Destructor
	meshObject();
	~meshObject() {};
	
	// Methods
	void setObjectFromGambitReader(ooGambitReaderCase *reader);
	void calculateRange();
	void generateCellMatrix();
	void reset();
	void normalize();
	void setFaceRadius(int idx, double value);
	void setAvgPtRadius(int idx, double value);
	void deleteFace(int idx);
	int getNumberOfPoints();
	int getNumberOfFaces();
	int getNumberOfGroups();
	int getNumberOfVolumes();
	int getPtDimensions();
	int getPtsPerFace();
	int getMaxConnectivity();
	double getRange(int axis, int min_max);
	double getAvgPointRadius(int idx);
	double getAvgPointVectorProp(int propIdx, int idx);
	double getAvgPointTimeProp(int propIdx, int time, int idx);
	double getTubeRadius(int idx);
	double* getRadiiRange();
	double* getPoint(int idx);
	int* getFace(int idx);
	int* getGroup(int idx);
	int* getPointsForCell(int idx);
	vector<double*> getPointMx();
	vector<int*> getFaceMx();
	vector<int*> getGroupMx();
	vector< vector<int> > getCellMx();
	vector<double> getFaceRadii();
	vector<vecProp*> getVectorProperties();
	vector<timeProp*> getTimeProperties();
	vector<vecProp*> getCellVectorProperties();
	vector<timeProp*> getCellTimeProperties();
	vector<int> getPointConnections(int idx);
	vector<int> getPointFaces(int idx);
	
};

#endif // MESH_OBJECT_H
