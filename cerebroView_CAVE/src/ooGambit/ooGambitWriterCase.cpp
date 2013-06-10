#include <iostream>

#include "ooGambitWriterCase.h"
#include "ooGambitWriterSource.cpp"


/*** Constructor ***/
ooGambitWriterCase::ooGambitWriterCase(string exec, char sep) {
	exePath = exec;
	separator = " ";
	separator[0] = sep;
	nwkWriter = NULL;
}
/*** Destructor ***/
ooGambitWriterCase::~ooGambitWriterCase() {}

/*** Methods - Public ***/
// create flat (primitive data types only)
void ooGambitWriterCase::createFlat(string FName, vector<double*> aPtCoordMx, vector<int*> aFaceMx, vector<int*> aGroupMx, vector<double> aFaceRadii, int aPtDims, int aPtsPerFace) {
	int i, pos;
	
	fileOut.open(FName.c_str());
	
	groupMx = aGroupMx;
	faceRadii = aFaceRadii;
	
	// begin writing Case file
	printf("\n<===============================================================>\n");
	printf("STARTED WRITING \"%s\"\n\n", FName.c_str());
	
	// start timer
	unsigned int start = clock();
	
	// write meshfile
	if(nwkWriter != NULL){
		delete nwkWriter;
	}
	
	pos = FName.rfind(separator);
	string meshFile = FName.substr(pos+1, FName.length()-pos-1);
	pos = meshFile.rfind(".");
	meshFile.replace(pos, 5, ".nw31");
	
	nwkWriter = new ooGambitWriterSource();
	nwkWriter->createFlat((exePath+"Data"+separator+"nwk"+separator+meshFile), aPtCoordMx, aFaceMx, aGroupMx, aPtDims, aPtsPerFace);
	
	// header info
	fileOut << "<model header=\"3d network Tube Flow with variabel diameter\" author=\"Andreas A Linninger\" date=\"4/16/2011\" ProblemType=\"LienarTubeFlow\" Equation1=Nabla PP = alfa F" << endl;
	fileOut << "Comments=\"Add user defined comments here...\">" << endl;
	fileOut << "problemtype=LinearVascaultureApplication" << endl;
	fileOut << "meshfile=Data/nwk/" << meshFile << endl;
	fileOut << "<constants>" << endl;
	fileOut << "MY=4.0E-3" << endl;
	fileOut << "P1=13300" << endl;
	fileOut << "PN=266" << endl;
	fileOut << "</constants>" << endl;
	fileOut << endl;
	
	// diameter by group
	for(i=0; i<groupMx.size(); i++){
		writeGroupDiameter(i);
	}
	
	
	
	// end timer
	double readTime = ((double)(clock() - start) / (double)CLOCKS_PER_SEC);
	
	// finished
	printf("\nFINISHED WRITING \"%s\" in %lf seconds\n", FName.c_str(), readTime);
	printf("<===============================================================>\n\n");
}

void ooGambitWriterCase::writeGroupDiameter(int grIdx) {
	int i;
	char aLine[50];
	bool variableDiameters = false;
	double constDiameter = -1.0;
	vector<double> diameters;
	
	for(i=groupMx[grIdx][1]; i<=groupMx[grIdx][2]; i++){
		if(constDiameter == -1.0) constDiameter = faceRadii[i]*2;
		if((faceRadii[i]*2) != constDiameter){
			variableDiameters = true;
		}
		diameters.push_back(faceRadii[i]*2);
	}
	
	
	sprintf(aLine, "(vector=Dia group=%X)", groupMx[grIdx][0]);
	fileOut << aLine << endl;
	
	int numFacesInGroup = groupMx[grIdx][2]-groupMx[grIdx][1] + 1;
	if(variableDiameters){
		sprintf(aLine, "(N=%d type=variable)", numFacesInGroup);
		fileOut << aLine << endl;
		
		sprintf(aLine, "(13(%X %X %X 0 0)(", groupMx[grIdx][0], groupMx[grIdx][1], groupMx[grIdx][2]);
		fileOut << aLine << endl;
		
		for(i=0; i<diameters.size(); i++){
			sprintf(aLine, "%.10lf", diameters[i]);
			fileOut << aLine << endl;
		}
	}
	else{
		sprintf(aLine, "(N=%d type=const value=%.10lf)", numFacesInGroup, constDiameter);
		fileOut << aLine << endl;
		
		sprintf(aLine, "(13(%X %X %X 0 0)(", groupMx[grIdx][0], groupMx[grIdx][1], groupMx[grIdx][2]);
		fileOut << aLine << endl;
	}
	
	fileOut << endl;
}



