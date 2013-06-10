/*************************************************
 ****                                         ****
 ****               Mesh Object               ****
 ****                                         ****
 *************************************************/

#include "meshObject.h"
#include "../ooGambit/ooGambitReaderCase.cpp"

using namespace std;
	
// Constructor
meshObject::meshObject() {
	nrOfPoints = 0;
	ptDims = 0;
	
	nrOfFaces = 0;
	ptsPerFace = 0;
	
	nrOfGroups = 0;
	
	ptRange[X_AXIS][MIN] = 9.9e10; ptRange[X_AXIS][MAX] = -9.9e10;
	ptRange[Y_AXIS][MIN] = 9.9e10; ptRange[Y_AXIS][MAX] = -9.9e10;
	ptRange[Z_AXIS][MIN] = 9.9e10; ptRange[Z_AXIS][MAX] = -9.9e10;
	
	radiiRange = new double[2];
	radiiRange[MIN] =  9.9e10;
	radiiRange[MAX] = -9.9e10;
}

	
// Methods
void meshObject::setObjectFromGambitReader(ooGambitReaderCase *reader) {
	int i, j;
	int inFaces, bnFaces, inVolumes, bnVolumes;
	this->reset();
	
	pointMx = reader->getSource()->getPointMatrix();
	faceMx  = reader->getSource()->getFaceMatrix();
	groupMx = reader->getSource()->getGroupMatrix();
	
	ptAvgRadii = reader->getPtAvgRadii();
	faceRadii  = reader->getFaceRadii();
	
	vectorProperties = reader->getVectorProperties();
	timeProperties = reader->getTimeProperties();
	cellVectorProperties = reader->getCellVectorProperties();
	cellTimeProperties = reader->getCellTimeProperties();
	
	reader->getSource()->GetPointFieldDimensions(nrOfPoints, ptDims);
	reader->getSource()->GetFaceFieldDimensions(nrOfFaces, inFaces, bnFaces, ptsPerFace, nrOfGroups);
	reader->getSource()->GetVolumeFieldDimensions(nrOfCells, inVolumes, bnVolumes);
	
	pt2ptMx.resize(nrOfPoints+1);
	pt2faceMx.resize(nrOfPoints+1);
	
	for(i=1; i<=nrOfFaces; i++){
		for(j=0; j<ptsPerFace; j++){
			pt2ptMx[faceMx[i][j]].push_back(faceMx[i][(j+1)%ptsPerFace]);
			pt2faceMx[faceMx[i][j]].push_back(i);
		}
	}
	maxConnect = 0;
	for(i=1; i<=nrOfPoints; i++){
		int conn = pt2ptMx[i].size();
		if(conn > maxConnect) maxConnect = conn;
	}
	generateCellMatrix();
}
void meshObject::calculateRange() {
	int i, j;

	// reset range
	ptRange[X_AXIS][MIN] = 9.9e10; ptRange[X_AXIS][MAX] = -9.9e10;
	ptRange[Y_AXIS][MIN] = 9.9e10; ptRange[Y_AXIS][MAX] = -9.9e10;
	ptRange[Z_AXIS][MIN] = 9.9e10; ptRange[Z_AXIS][MAX] = -9.9e10;
	
	radiiRange[MIN] =  9.9e10;
	radiiRange[MAX] = -9.9e10;
	
	for(i=1; i<=nrOfPoints; i++){
		for(j=0; j<ptDims; j++){
			double val = pointMx[i][j];
			
			if(val < ptRange[j][MIN]) ptRange[j][MIN] = val;
			if(val > ptRange[j][MAX]) ptRange[j][MAX] = val;
		}
	}
	
	for(i=1; i<faceRadii.size(); i++){
		if(faceRadii[i] < radiiRange[MIN]) radiiRange[MIN] = faceRadii[i];
		if(faceRadii[i] > radiiRange[MAX]) radiiRange[MAX] = faceRadii[i];
	}
}
void meshObject::generateCellMatrix() {
	int i;
	
	cellMx.resize(nrOfCells+1);
	
	for(i=1; i<=nrOfFaces; i++){
		int vol1 = faceMx[i][ptsPerFace+0];
		int vol2 = faceMx[i][ptsPerFace+1];
		if(vol1 > 0) cellMx[vol1].push_back(i);
		if(vol2 > 0) cellMx[vol2].push_back(i);
	}
}
void meshObject::reset() {
	// delete current points, faces, and groups
	pointMx.clear();
	faceMx.clear();
	groupMx.clear();
	cellMx.clear();
	pt2ptMx.clear();
	pt2faceMx.clear();
	
	
	// reset other info
	nrOfPoints = 0;
	ptDims = 0;
	
	nrOfFaces = 0;
	ptsPerFace = 0;
	
	nrOfGroups = 0;
	
	maxConnect = 0;
	
	// reset range
	ptRange[X_AXIS][MIN] = 9.9e10; ptRange[X_AXIS][MAX] = -9.9e10;
	ptRange[Y_AXIS][MIN] = 9.9e10; ptRange[Y_AXIS][MAX] = -9.9e10;
	ptRange[Z_AXIS][MIN] = 9.9e10; ptRange[Z_AXIS][MAX] = -9.9e10;
	
	radiiRange[MIN] =  9.9e10;
	radiiRange[MAX] = -9.9e10;
}	
void meshObject::normalize() {
	int i;

	calculateRange();
	
	double xCenter = (ptRange[X_AXIS][MIN] + ptRange[X_AXIS][MAX]) / 2.0;
	double yCenter = (ptRange[Y_AXIS][MIN] + ptRange[Y_AXIS][MAX]) / 2.0;
	double zCenter = (ptRange[Z_AXIS][MIN] + ptRange[Z_AXIS][MAX]) / 2.0;
	double xLength =  ptRange[X_AXIS][MAX] - ptRange[X_AXIS][MIN];
	double yLength =  ptRange[Y_AXIS][MAX] - ptRange[Y_AXIS][MIN];
	double zLength =  ptRange[Z_AXIS][MAX] - ptRange[Z_AXIS][MIN];
	double maxLength = (xLength > yLength && xLength > zLength) ? xLength : (yLength > zLength ? yLength : zLength);

	for(i=1; i<=nrOfPoints; i++){
		pointMx[i][0] = (pointMx[i][0]-xCenter) / maxLength;
		pointMx[i][1] = (pointMx[i][1]-yCenter) / maxLength;
		pointMx[i][2] = (pointMx[i][2]-zCenter) / maxLength;
		
		ptAvgRadii[i] /= maxLength;
	}
	for(i=1; i<faceRadii.size(); i++){
		faceRadii[i] /= maxLength;
	}

	calculateRange();
}
void meshObject::setFaceRadius(int idx, double value) {
	faceRadii[idx] = value;
}
void meshObject::setAvgPtRadius(int idx, double value) {
	ptAvgRadii[idx] = value;
}
void meshObject::deleteFace(int idx) {
	int i, j;
	
	for(i=0; i <ptsPerFace; i++){
		int point = faceMx[idx][i];
		double sumRad = 0.0;
		for(j=0; j<pt2faceMx[point].size(); j++){
			int face = pt2faceMx[point][j];
			if(face != idx) sumRad += faceRadii[face];
		}
		ptAvgRadii[faceMx[idx][i]] = sumRad/(pt2faceMx[point].size()-1);
	}
	
	faceMx.erase(faceMx.begin() + idx);
	faceRadii.erase(faceRadii.begin() + idx);
	nrOfFaces--;
	
	pt2ptMx.clear();
	pt2faceMx.clear();
	pt2ptMx.resize(nrOfPoints+1);
	pt2faceMx.resize(nrOfPoints+1);
	
	for(i=1; i<=nrOfFaces; i++){
		for(j=0; j<ptsPerFace; j++){
			pt2ptMx[faceMx[i][j]].push_back(faceMx[i][(j+1)%ptsPerFace]);
			pt2faceMx[faceMx[i][j]].push_back(i);
		}
	}
	maxConnect = 0;
	for(i=1; i<=nrOfPoints; i++){
		int conn = pt2ptMx[i].size();
		if(conn > maxConnect) maxConnect = conn;
	}
	
	int groupNum;
	for(i=0; i<nrOfGroups; i++){
		if(idx >= groupMx[i][1] && idx <= groupMx[i][2]) groupNum = i;
	}
	for(i=groupNum+1; i<nrOfGroups; i++){
		groupMx[i][1] -= 1;
		groupMx[i][2] -= 1;
	}
	groupMx[groupNum][2] -= 1;
}
int meshObject::getNumberOfPoints() {
	return nrOfPoints;
}
int meshObject::getNumberOfFaces() {
	return nrOfFaces;
}
int meshObject::getNumberOfGroups() {
	return nrOfGroups;
}
int  meshObject::getNumberOfVolumes() {
	return nrOfCells;
}
int meshObject::getPtDimensions() {
	return ptDims;
}
int meshObject::getPtsPerFace() {
	return ptsPerFace;
}
int meshObject::getMaxConnectivity() {
	return maxConnect;
}
double meshObject::getRange(int axis, int min_max) {
	return ptRange[axis][min_max];
}
double meshObject::getAvgPointRadius(int idx) {
	return ptAvgRadii[idx];
}
double meshObject::getAvgPointVectorProp(int propIdx, int idx){
	int i;
	vector<int> faces = pt2faceMx[idx];
	double value = 0.0;
	for(i=0; i<faces.size(); i++){
		value += vectorProperties[propIdx]->getValue(faces[i]);
	}
	return (value/faces.size());
}
double meshObject::getAvgPointTimeProp(int propIdx, int time, int idx){
	int i;
	vector<int> faces = pt2faceMx[idx];
	double value = 0.0;
	for(i=0; i<faces.size(); i++){
		value += timeProperties[propIdx]->getValue(faces[i],time);
	}
	return (value/faces.size());
}
double meshObject::getTubeRadius(int idx) {
	return faceRadii[idx];
}
double* meshObject::getRadiiRange() {
	return radiiRange;
}
double* meshObject::getPoint(int idx) {	
	return pointMx[idx];
}
int* meshObject::getFace(int idx) {
	return faceMx[idx];
}
int* meshObject::getGroup(int idx) {
	return groupMx[idx];
}
int* meshObject::getPointsForCell(int idx) {
	int* ptIdx = new int[4];
	int face1 = cellMx[idx][0];
	int face2 = cellMx[idx][1];
	
	if(face1 <= 0 || face2 <= 0) return NULL;
	
	ptIdx[0] = faceMx[face1][0];
	ptIdx[1] = faceMx[face1][1];
	ptIdx[2] = faceMx[face1][2];
	ptIdx[3] = faceMx[face2][0];
	if(ptIdx[3] == ptIdx[0] || ptIdx[3] == ptIdx[1] || ptIdx[3] == ptIdx[2]){
		ptIdx[3] = faceMx[face2][1];
		if(ptIdx[3] == ptIdx[0] || ptIdx[3] == ptIdx[1] || ptIdx[3] == ptIdx[2]){
			ptIdx[3] = faceMx[face2][2];
		}
	}
	
	return ptIdx;
}
vector<double*> meshObject::getPointMx() {
	return pointMx;
}
vector<int*> meshObject::getFaceMx() {
	return faceMx;
}
vector<int*> meshObject::getGroupMx() {
	return groupMx;
}
vector< vector<int> > meshObject::getCellMx() {
	return cellMx;
}
vector<double> meshObject::getFaceRadii() {
	return faceRadii;
}
vector<vecProp*> meshObject::getVectorProperties() {
	return vectorProperties;
}
vector<timeProp*> meshObject::getTimeProperties() {
	return timeProperties;
}
vector<vecProp*> meshObject::getCellVectorProperties() {
	return cellVectorProperties;
}
vector<timeProp*> meshObject::getCellTimeProperties() {
	return cellTimeProperties;
}
vector<int> meshObject::getPointConnections(int idx) {
	return pt2ptMx[idx];
}
vector<int> meshObject::getPointFaces(int idx) {
	return pt2faceMx[idx];
}

