#ifndef __CEREBROVIEW_CAVE_H_
#define __CEREBROVIEW_CAVE_H_

#include <vector>

#include <vtkActor.h>
#include <vtkCellArray.h>
#include <vtkCellData.h>
#include <vtkColorTransferFunction.h>
#include <vtkFloatArray.h>
#include <vtkGlyph3D.h>
#include <vtkLookupTable.h>
#include <vtkPiecewiseFunction.h>
#include <vtkPointData.h>
#include <vtkPoints.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkSphereSource.h>
#include <vtkTubeFilter.h>

#include <omega.h>
#include <omegaToolkit.h>
#include <omegaVtk.h>

#include "src/mesh/meshObject.h"
#include "src/ooGambit/ooGambitReaderCase.h"
#include "src/ooGambit/ooGambitWriterCase.h"

using namespace omega;
using namespace omegaToolkit;
using namespace omegaVtk;
using namespace omegaToolkit::ui;

class cerebroView_CAVE: public EngineModule, IMenuItemListener {
public:
	cerebroView_CAVE();
	virtual void initialize();
	virtual void update(const UpdateContext& context);
	virtual void handleEvent(const Event& e);
	virtual void onMenuItemEvent(MenuItem* mi);

	void loadFile(string fileName, bool normalize);
	void initNWK();
	void changeColorProperty(string colorProp);
	void updateColorTable(double min, double max);

private:
	// OmegaLib Members
	VtkModule* myVtkModule;
	vector<SceneNode*> mySceneNode;
	MenuManager* myMenuManager;

	// Data Members
	string resrcPath;
	meshObject *nwk;
	double colorMap[4][3];
	int cProp;
	bool orient;
	Quaternion orientation;

	// VTK Members
	vector<vtkPolyData*> nwkPolyLines;
	vector<vtkActor*> nwkTubeActor;
	vector<vtkActor*> nwkJointActor;
	vtkLookupTable* colLUT;
	vtkColorTransferFunction* colorTF;
	vtkPiecewiseFunction* opacityTF;

};

#endif // __CEREBROVIEW_CAVE_H_


