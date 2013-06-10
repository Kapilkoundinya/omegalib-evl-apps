#include "cerebroView_CAVE.h"

#include "src/mesh/meshObject.cpp"
#include "src/ooGambit/ooGambitWriterCase.cpp"

/*** Auxillary Functions ***/
double remap(double val, double minV, double maxV, double minM, double maxM) {
	return (val-minV) * ((maxM-minM)/(maxV-minV)) + minM;
}

/*** Constructor ***/
cerebroView_CAVE::cerebroView_CAVE(): EngineModule("cerebroView_CAVE") {
	// Create and register the omegalib vtk module
	myVtkModule = new VtkModule();
	ModuleServices::addModule(myVtkModule);

	// define resource path
	resrcPath = "/data/evl/omegalib/apps/cerebroView_CAVE/resrc/";

	// Create object for a network
	nwk = new meshObject();

	// Create color lookup table
	colLUT = vtkLookupTable::New();
	colorTF = vtkColorTransferFunction::New();
	opacityTF = vtkPiecewiseFunction::New();
}

/*** Class Methods ***/
void cerebroView_CAVE::initialize() {
	// Set up colormap
	//colorMap[0][0] = 0.10; colorMap[0][1] = 0.10; colorMap[0][2] = 0.90; // Blue
	//colorMap[1][0] = 0.78; colorMap[1][1] = 0.78; colorMap[1][2] = 1.00; // Blue-White
	//colorMap[2][0] = 1.00; colorMap[2][1] = 0.78; colorMap[2][2] = 0.78; // Red-White
	//colorMap[3][0] = 0.90; colorMap[3][1] = 0.10; colorMap[3][2] = 0.10; // Red

	colorMap[0][0] = 0.05; colorMap[0][1] = 0.15; colorMap[0][2] = 0.95; // Blue
	colorMap[1][0] = 0.50; colorMap[1][1] = 0.05; colorMap[1][2] = 0.95; // Blue-Purple
	colorMap[2][0] = 0.95; colorMap[2][1] = 0.05; colorMap[2][2] = 0.50; // Red-Purple
	colorMap[3][0] = 0.95; colorMap[3][1] = 0.15; colorMap[3][2] = 0.05; // Red

	// Initialize data variables
	cProp = 0;
	orient = false;

	// Load NWK from file and create VTK objects
	loadFile(resrcPath+"Data/case/New_Brain_V7.allProperties.cs31", true); // Full Brain File
	//loadFile(resrcPath+"Data/case/FBU_MK7.V5.pressflow.cs31", true); // FBU File


	// Create an omegalib scene node. We will attach our vtk objects to it
	for(int i=0; i<nwk->getNumberOfGroups(); i++){
		String name = ostr("vtkRoot%02i", %i);
		SceneNode *node = new SceneNode(getEngine(), name);
		getEngine()->getScene()->addChild(node);
		node->setPosition(0.0, 1.6, -4.0);
		node->setScale(1.0, 1.0, 1.0);
		node->setBoundingBoxVisible(false);		
		mySceneNode.push_back(node);
	}
	
	printf("Finished adding scene nodes\n");
	
	initNWK();

	// Create an omegalib menu
	myMenuManager = MenuManager::createAndInitialize();
	Menu* menu = myMenuManager->createMenu("menu");
	myMenuManager->setMainMenu(menu);
	printf("Finished creating menu\n");

	for(int i=0; i<nwk->getNumberOfGroups(); i++){
		String grNum = ostr("%04i", %nwk->getGroup(i)[0]);
		String text = "Group: " + grNum;
		bool display = true;
		if(grNum[3] == '2' || grNum == "0187" || grNum == "2830") display = false;
		MenuItem* myEditorMenuItem = menu->addItem(MenuItem::Checkbox);
		myEditorMenuItem->setText(text);
		myEditorMenuItem->setUserData(mySceneNode[i]);
		myEditorMenuItem->setChecked(display);
		myEditorMenuItem->setListener(this);
		mySceneNode[i]->setVisible(display);
	}
}

void cerebroView_CAVE::update(const UpdateContext& context) {
	int i;

	for(i=0; i<mySceneNode.size(); i++){
		if(orient){
			mySceneNode[i]->resetOrientation();
			mySceneNode[i]->setOrientation(orientation);
		}
	}
}

void cerebroView_CAVE::handleEvent(const Event& e) {
	// Wand
	if(e.getServiceType() == Service::Wand){
		// Button Up :: Scale Larger
		bool cameraEnabled = getEngine()->getDefaultCamera()->isControllerEnabled();
		if(e.isButtonDown(Event::ButtonUp) && cameraEnabled){
			for(int i=0; i<mySceneNode.size(); i++) {
				mySceneNode[i]->scale(1.2000, 1.2000, 1.2000);
			}
		}
		// Button Up :: Scale Smaller
		if(e.isButtonDown(Event::ButtonDown) && cameraEnabled){
			for(int i=0; i<mySceneNode.size(); i++) {
				mySceneNode[i]->scale(0.8333, 0.8333, 0.8333);
			}
		}
		// Button Left :: Change Color Property
		if(e.isButtonDown(Event::ButtonLeft)){
			if(cProp > 0) cProp--;
			printf("left-color: %d\n", cProp);
			switch(cProp){
				case 0:
					changeColorProperty("Diameter");
					break;
				case 1:
					changeColorProperty("Pressure");
					break;
				case 2:
					changeColorProperty("Flow");
					break;
			}
		}
		// Button Right :: Change Color Property
		if(e.isButtonDown(Event::ButtonRight)){
			if(cProp < 2) cProp++;
			printf("right-color: %d\n", cProp);
			switch(cProp){
				case 0:
					changeColorProperty("Diameter");
					break;
				case 1:
					changeColorProperty("Pressure");
					break;
				case 2:
					changeColorProperty("Flow");
					break;
			}
		}
		// Button 5 (Back Bumper) :: Lock/Release Orientation
		orient = e.isFlagSet(Event::Button5);
		// Ratation of Wand :: Update Orientation
		orientation = e.getOrientation();
	}

	// Keyboard
	if(e.getServiceType() == Service::Keyboard && e.getType() == Event::Down){
		int key = e.getSourceId();
		printf("Key: %c | %d\n", key, key);
		switch(key){
			case 'n':
				if(cProp > 0) cProp--;
				switch(cProp){
					case 0:
						changeColorProperty("Diameter");
						break;
					case 1:
						changeColorProperty("Pressure");
						break;
					case 2:
						changeColorProperty("Flow");
						break;
				}
				break;
			case 'm':
				if(cProp < 2) cProp++;
				switch(cProp){
					case 0:
						changeColorProperty("Diameter");
						break;
					case 1:
						changeColorProperty("Pressure");
						break;
					case 2:
						changeColorProperty("Flow");
						break;
				}
				break;
		}
	}
}

void cerebroView_CAVE::onMenuItemEvent(MenuItem* mi) {
	printf("Menu Item Selected\n");
	SceneNode* aNode = (SceneNode*) mi->getUserData();
	if(aNode != NULL){
		aNode->setVisible(mi->isChecked());
	}
}

void cerebroView_CAVE::loadFile(string fileName, bool normalize) {
	ooGambitReaderCase *reader = new ooGambitReaderCase(resrcPath);
	reader->createFlat(fileName);
	nwk->setObjectFromGambitReader(reader);
	if(normalize) nwk->normalize();
	else nwk->calculateRange();
	delete reader;

	printf("NWK Range: %.3e %.3e %.3e %.3e %.3e %.3e\n", nwk->getRange(X_AXIS, MIN), nwk->getRange(X_AXIS, MAX), 
		nwk->getRange(Y_AXIS, MIN), nwk->getRange(Y_AXIS, MAX), nwk->getRange(Z_AXIS, MIN), nwk->getRange(Z_AXIS, MAX));
}

void cerebroView_CAVE::initNWK() {
	int i, j, k, l, m;
	
	// update data points
	vtkPoints* nwkPoints = vtkPoints::New();
	vtkFloatArray* nwkRadii = vtkFloatArray::New();
	nwkRadii->SetName("Radii");
	
	nwkPoints->InsertNextPoint(nwk->getPoint(1));
	nwkRadii->InsertNextValue(nwk->getAvgPointRadius(1));
	for(i=1; i<=nwk->getNumberOfPoints(); i++){
		nwkPoints->InsertNextPoint(nwk->getPoint(i));
		nwkRadii->InsertNextValue(nwk->getAvgPointRadius(i));
	}
	
	vector<vecProp*> vectorProperties = nwk->getVectorProperties();
	vector<timeProp*> timeProperties = nwk->getTimeProperties();
	
	// dummy points for invalid lines
	double *bounds = nwkPoints->GetBounds();
	double *radRange = nwk->getRadiiRange();
	double centerX = (bounds[0]+bounds[1])/2.0;
	double centerY = (bounds[2]+bounds[3])/2.0;
	double centerZ = (bounds[4]+bounds[5])/2.0;
	double lengthX = bounds[1]-bounds[0];
	double lengthY = bounds[3]-bounds[2];
	double lengthZ = bounds[5]-bounds[4];
	nwkPoints->InsertNextPoint(centerX, centerY, centerZ);
	nwkPoints->InsertNextPoint(centerX+(0.00001*lengthX), centerY+(0.00001*lengthY), centerZ+(0.00001*lengthZ));
	nwkRadii->InsertNextValue(radRange[0]);
	nwkRadii->InsertNextValue(radRange[0]);
	
	// update color table
	updateColorTable(radRange[0], radRange[1]);

	// initialize by group
	int nGroups = nwk->getNumberOfGroups();
	for(i=0; i<nGroups; i++){
		// initialize group names and all properties that can be used for color 
		char grNum[5];
		sprintf(grNum, "%04d", nwk->getGroup(i)[0]);
		
		vtkCellArray* nwkLines = vtkCellArray::New();
		
		vector<vtkFloatArray*> nwkVectorProps;
		vector<vtkFloatArray**> nwkTimeProps;
		vector<vtkFloatArray*> nwkVectorProps2;
		vector<vtkFloatArray**> nwkTimeProps2;
		
		// allocate space for simulated properties
		for(j=0; j<vectorProperties.size(); j++){
			vtkFloatArray* vProp = vtkFloatArray::New();
			vProp->SetName(vectorProperties[j]->getPropertyName().c_str());
			nwkVectorProps.push_back(vProp);
			vtkFloatArray* vProp2 = vtkFloatArray::New();
			vProp2->SetName(vectorProperties[j]->getPropertyName().c_str());
			nwkVectorProps2.push_back(vProp2);
		}
		for(j=0; j<timeProperties.size(); j++){
			vtkFloatArray** tProp  = new vtkFloatArray*[timeProperties[j]->getNumberOfTimeSteps()+1];
			vtkFloatArray** tProp2 = new vtkFloatArray*[timeProperties[j]->getNumberOfTimeSteps()+1];
			for(k=1; k<=timeProperties[j]->getNumberOfTimeSteps(); k++){
				char tName[50];
				sprintf(tName, "%s|%d", timeProperties[j]->getPropertyName().c_str(), k);
				tProp[k] = vtkFloatArray::New();
				tProp[k]->SetName(tName);
				tProp2[k] = vtkFloatArray::New();
				tProp2[k]->SetName(tName);
			}
			nwkTimeProps.push_back(tProp);
			nwkTimeProps2.push_back(tProp2);
		}
		
		// insert data for each property at each face
		int startIdx = nwk->getGroup(i)[1];
		int endIdx = nwk->getGroup(i)[2];
		
		vector<int> shownPointIdx;
		
		for(j=startIdx; j<=endIdx; j++){
			int *ptIdx = nwk->getFace(j);
			
			double rad1 = nwk->getAvgPointRadius(ptIdx[0]);
			double rad2 = nwk->getAvgPointRadius(ptIdx[1]);
			
			double *pt1c = nwk->getPoint(ptIdx[0]);
			double *pt2c = nwk->getPoint(ptIdx[1]);
			
			// add line if points are not the same as each other
			if(pt1c[0] != pt2c[0] || pt1c[1] != pt2c[1] || pt1c[2] != pt2c[2]){
				nwkLines->InsertNextCell(2);
				nwkLines->InsertCellPoint(ptIdx[0]);
				nwkLines->InsertCellPoint(ptIdx[1]);
				
				for(k=0; k<nwkVectorProps.size(); k++){
					nwkVectorProps[k]->InsertNextValue(vectorProperties[k]->getValue(j));
				}
				for(k=0; k<nwkTimeProps.size(); k++){
					for(m=1; m<=timeProperties[k]->getNumberOfTimeSteps(); m++){
						nwkTimeProps[k][m]->InsertNextValue(timeProperties[k]->getValue(j, m));
					}
				}
				
				// add points for displaying spheres at the tube joints
				if(grNum[3] != '2'){
					if(std::find(shownPointIdx.begin(), shownPointIdx.end(), ptIdx[0]) == shownPointIdx.end()){
						shownPointIdx.push_back(ptIdx[0]);
					}
					if(std::find(shownPointIdx.begin(), shownPointIdx.end(), ptIdx[1]) == shownPointIdx.end()){
						shownPointIdx.push_back(ptIdx[1]);
					}
				}
			}
			// otherwise add dummy line
			else{
				nwkLines->InsertNextCell(2);
				nwkLines->InsertCellPoint(nwkPoints->GetNumberOfPoints()-2);
				nwkLines->InsertCellPoint(nwkPoints->GetNumberOfPoints()-1);
			}
		}
		
		// add tubes to be drawn
		vtkPolyData* nwkPolyData = vtkPolyData::New();
		nwkPolyData->SetPoints(nwkPoints);
		nwkPolyData->SetLines(nwkLines);
		nwkPolyData->GetPointData()->AddArray(nwkRadii);
		nwkPolyData->GetPointData()->SetActiveScalars("Radii");
		for(j=0; j<nwkVectorProps.size(); j++){
			nwkPolyData->GetCellData()->AddArray(nwkVectorProps[j]);
		}
		for(j=0; j<nwkTimeProps.size(); j++){
			for(k=1; k<=timeProperties[j]->getNumberOfTimeSteps(); k++){
				nwkPolyData->GetCellData()->AddArray(nwkTimeProps[j][k]);
			}
		}
		nwkPolyLines.push_back(nwkPolyData);
		
		vtkTubeFilter* nwkTubes = vtkTubeFilter::New();
		nwkTubes->SetInput(nwkPolyData);
		nwkTubes->SetNumberOfSides(6);
		nwkTubes->SetVaryRadiusToVaryRadiusByAbsoluteScalar();
		nwkTubes->Update();
		
		vtkPolyDataMapper* nwkMapper = vtkPolyDataMapper::New();
		nwkMapper->SetInputConnection(nwkTubes->GetOutputPort());
		//nwkMapper->ScalarVisibilityOff();
		nwkMapper->ScalarVisibilityOn();
		nwkMapper->SetScalarModeToUsePointFieldData();  // Color by Radii
		nwkMapper->SetColorModeToMapScalars();          // Color by Radii
		nwkMapper->SelectColorArray("Radii");           // Color by Radii
		nwkMapper->SetScalarRange(colLUT->GetTableRange());
		nwkMapper->SetLookupTable(colLUT);
		
		vtkActor* nwkActor = vtkActor::New();
		nwkActor->SetMapper(nwkMapper);
		nwkActor->GetProperty()->SetSpecularColor(1.0, 1.0, 1.0);
		nwkActor->GetProperty()->SetSpecular(0.7);
		nwkActor->GetProperty()->SetSpecularPower(72);
		nwkActor->GetProperty()->BackfaceCullingOn();
		nwkActor->GetProperty()->SetLineWidth(1);
		nwkActor->VisibilityOn();
		
		nwkTubeActor.push_back(nwkActor);
		
		// add spheres to be drawn
		vtkPoints* spherePoints = vtkPoints::New();
		vtkFloatArray* sphereRadii = vtkFloatArray::New();
		sphereRadii->SetName("SphereRadii");
		for(j=0; j<shownPointIdx.size(); j++){
			double *pt = nwk->getPoint(shownPointIdx[j]);
			double rad = nwk->getAvgPointRadius(shownPointIdx[j]);
			spherePoints->InsertNextPoint(pt);
			sphereRadii->InsertNextValue(rad);
			for(k=0; k<nwkVectorProps2.size(); k++){
				double vecVal = nwk->getAvgPointVectorProp(k, shownPointIdx[j]);
				nwkVectorProps2[k]->InsertNextValue(vecVal);
			}
			for(k=0; k<nwkTimeProps2.size(); k++){
				for(l=1; l<=timeProperties[k]->getNumberOfTimeSteps(); l++){
					double timeVal = nwk->getAvgPointTimeProp(k, l, shownPointIdx[j]);
					nwkTimeProps2[k][l]->InsertNextValue(timeVal);
				}
			}
		}
		
		vtkPolyData* spherePolyData = vtkPolyData::New();
		spherePolyData->SetPoints(spherePoints);
		spherePolyData->GetPointData()->AddArray(sphereRadii);
		spherePolyData->GetPointData()->SetActiveScalars("SphereRadii");
		for(j=0; j<nwkVectorProps2.size(); j++){
			spherePolyData->GetPointData()->AddArray(nwkVectorProps2[j]);
		}
		for(j=0; j<nwkTimeProps2.size(); j++){
			for(k=1; k<=timeProperties[j]->getNumberOfTimeSteps(); k++){
				spherePolyData->GetPointData()->AddArray(nwkTimeProps2[j][k]);
			}
		}
		
		vtkSphereSource* sphere = vtkSphereSource::New();
		sphere->SetThetaResolution(6); 
		sphere->SetPhiResolution(6);
		
		vtkGlyph3D* sphereGlyph = vtkGlyph3D::New();
		sphereGlyph->SetSourceConnection(sphere->GetOutputPort());
		sphereGlyph->SetInput(spherePolyData);
		sphereGlyph->ScalingOn();
		sphereGlyph->SetScaleModeToScaleByScalar();
		sphereGlyph->SetRange(radRange[0], radRange[1]);
		sphereGlyph->SetScaleFactor(2.0);
		
		vtkPolyDataMapper* sphereMapper = vtkPolyDataMapper::New();
		sphereMapper->SetInputConnection(sphereGlyph->GetOutputPort());
		//sphereMapper->ScalarVisibilityOff();
		sphereMapper->ScalarVisibilityOn();
		sphereMapper->SetScalarModeToUsePointFieldData();
		sphereMapper->SetColorModeToMapScalars();
		sphereMapper->SelectColorArray("SphereRadii");
		sphereMapper->SetScalarRange(colLUT->GetTableRange());
		sphereMapper->SetLookupTable(colLUT);
		
		vtkActor* sphereActor = vtkActor::New();
		sphereActor->SetMapper(sphereMapper); 
		sphereActor->GetProperty()->SetSpecularColor(1.0, 1.0, 1.0);
		sphereActor->GetProperty()->SetSpecular(0.7);
		sphereActor->GetProperty()->SetSpecularPower(72);
		sphereActor->GetProperty()->BackfaceCullingOn();
		sphereActor->VisibilityOn();
		
		nwkJointActor.push_back(sphereActor);
	}
	
	for(i=0; i<nwkTubeActor.size(); i++){
		myVtkModule->attachProp(nwkTubeActor[i], mySceneNode[i]);
	}
	for(i=0; i<nwkJointActor.size(); i++){
		myVtkModule->attachProp(nwkJointActor[i], mySceneNode[i]);
	}
}

void cerebroView_CAVE::changeColorProperty(string colorProp) {
	int i,j;

	vector<vecProp*> vectorProperties = nwk->getVectorProperties();
	vector<timeProp*> timeProperties = nwk->getTimeProperties();

	// Color by Diameter
	if(colorProp == "Diameter"){
		double *range = nwk->getRadiiRange();
		updateColorTable(range[0], range[1]);
		for(i=0; i<nwkTubeActor.size(); i++){
			nwkTubeActor[i]->GetMapper()->SetScalarModeToUsePointFieldData();  // Color by Radii
			nwkTubeActor[i]->GetMapper()->SetColorModeToMapScalars();          // Color by Radii
			nwkTubeActor[i]->GetMapper()->SelectColorArray("Radii");           // Color by Radii
			nwkTubeActor[i]->GetMapper()->SetScalarRange(colLUT->GetTableRange());
			nwkTubeActor[i]->GetMapper()->SetLookupTable(colLUT);
		}
		for(i=0; i<nwkJointActor.size(); i++){
			nwkJointActor[i]->GetMapper()->SetScalarModeToUsePointFieldData();  // Color by Radii
			nwkJointActor[i]->GetMapper()->SetColorModeToMapScalars();          // Color by Radii
			nwkJointActor[i]->GetMapper()->SelectColorArray("SphereRadii");     // Color by Radii
			nwkJointActor[i]->GetMapper()->SetScalarRange(colLUT->GetTableRange());
			nwkJointActor[i]->GetMapper()->SetLookupTable(colLUT);
		}
	}
	// Color by Vector Property
	for(i=0; i<vectorProperties.size(); i++){
		if(colorProp == vectorProperties[i]->getPropertyName()){
			double *range = vectorProperties[i]->getRange();
			updateColorTable(range[0], range[1]);
			for(j=0; j<nwkTubeActor.size(); j++){
				nwkTubeActor[j]->GetMapper()->SetScalarModeToUseCellFieldData();
				nwkTubeActor[j]->GetMapper()->SetColorModeToMapScalars();
				nwkTubeActor[j]->GetMapper()->SelectColorArray(colorProp.c_str());
				nwkTubeActor[j]->GetMapper()->SetScalarRange(colLUT->GetTableRange());
				nwkTubeActor[j]->GetMapper()->SetLookupTable(colLUT);
			}
			for(j=0; j<nwkJointActor.size(); j++){
				nwkJointActor[j]->GetMapper()->SetScalarModeToUsePointFieldData();
				nwkJointActor[j]->GetMapper()->SetColorModeToMapScalars();
				nwkJointActor[j]->GetMapper()->SelectColorArray(colorProp.c_str());
				nwkJointActor[j]->GetMapper()->SetScalarRange(colLUT->GetTableRange());
				nwkJointActor[j]->GetMapper()->SetLookupTable(colLUT);
			}
		}
	}
	// Color by Time Property
}

void cerebroView_CAVE::updateColorTable(double min, double max) {
	int i;
	
	printf("Color Range: %.4g, %.4g\n", min, max);
	
	double xLength = nwk->getRange(X_AXIS, MAX) - nwk->getRange(X_AXIS, MIN);
	double yLength = nwk->getRange(Y_AXIS, MAX) - nwk->getRange(Y_AXIS, MIN);
	double zLength = nwk->getRange(Z_AXIS, MAX) - nwk->getRange(Z_AXIS, MIN);
	double maxLength = (xLength > yLength && xLength > zLength) ? xLength : (yLength > zLength ? yLength : zLength);
	
	/* COLOR */
	colorTF->RemoveAllPoints();
	
	// Linear Color
	//colorTF->AddRGBPoint((1.0-(0.0/3.0))*min + (0.0/3.0)*max, colorMap[0][0], colorMap[0][1], colorMap[0][2]);
	//colorTF->AddRGBPoint((1.0-(1.0/3.0))*min + (1.0/3.0)*max, colorMap[1][0], colorMap[1][1], colorMap[1][2]);
	//colorTF->AddRGBPoint((1.0-(2.0/3.0))*min + (2.0/3.0)*max, colorMap[2][0], colorMap[2][1], colorMap[2][2]);
	//colorTF->AddRGBPoint((1.0-(3.0/3.0))*min + (3.0/3.0)*max, colorMap[3][0], colorMap[3][1], colorMap[3][2]);
	
	// Logarithmic Color 1
	colorTF->AddRGBPoint((1.0-(0.00/4.0))*min + (0.00/4.0)*max, colorMap[0][0], colorMap[0][1], colorMap[0][2]);
	colorTF->AddRGBPoint((1.0-(0.25/4.0))*min + (0.25/4.0)*max, colorMap[1][0], colorMap[1][1], colorMap[1][2]);
	colorTF->AddRGBPoint((1.0-(1.00/4.0))*min + (1.00/4.0)*max, colorMap[2][0], colorMap[2][1], colorMap[2][2]);
	colorTF->AddRGBPoint((1.0-(4.00/4.0))*min + (4.00/4.0)*max, colorMap[3][0], colorMap[3][1], colorMap[3][2]);
	
	/* TRANSPARENCY: ALL OPAQUE */
	opacityTF->RemoveAllPoints();
	
	opacityTF->AddPoint(min-0.001, 0.00 / (0.0625*maxLength));
	opacityTF->AddPoint(min,       0.15 / (0.0625*maxLength));
	opacityTF->AddPoint(max,       0.15 / (0.0625*maxLength));
	opacityTF->AddPoint(max+0.001, 0.00 / (0.0625*maxLength));
	
	// build color table
	colLUT->SetTableRange(min, max);
	colLUT->SetNumberOfTableValues(256);
	for(i=0; i<256; i++){
		double col[3];
		double op = opacityTF->GetValue(min + ((double)i/255.0*(max-min)));
		colorTF->GetColor(min + ((double)i/255.0*(max-min)), col);
		colLUT->SetTableValue(i, col[0], col[1], col[2], 1.0);
	}
	colLUT->Build();
}



