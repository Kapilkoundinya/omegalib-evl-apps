/**************************************************************************************************
 * THE OMEGA LIB PROJECT
 *-------------------------------------------------------------------------------------------------
 * Copyright 2010-2011		Electronic Visualization Laboratory, University of Illinois at Chicago
 * Authors:										
 *  Alessandro Febretti		febret@gmail.com
 *-------------------------------------------------------------------------------------------------
 * Copyright (c) 2010-2011, Electronic Visualization Laboratory, University of Illinois at Chicago
 * All rights reserved.
 * Redistribution and use in source and binary forms, with or without modification, are permitted 
 * provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice, this list of conditions 
 * and the following disclaimer. Redistributions in binary form must reproduce the above copyright 
 * notice, this list of conditions and the following disclaimer in the documentation and/or other 
 * materials provided with the distribution. 
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR 
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
 * FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR 
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE  GOODS OR SERVICES; LOSS OF 
 * USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *************************************************************************************************/
#include <vtkSmartPointer.h>
#include <cmath>
#include <vtkGlyph3D.h>
#include <vtkLODActor.h>
#include <vtkLODActor.h>
#include <vtkPDBReader.h>
#include <vtkPolyDataMapper.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSphereSource.h>
#include <vtkTubeFilter.h>

#include <omega.h>
#include <omegaToolkit.h>
#include <omegaVtk.h>

using namespace omega;
using namespace omegaToolkit;
using namespace omegaVtk;

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class VtkScene: public EngineModule
{
public:
	VtkScene();
	virtual void initialize();

private:
	VtkModule* myVtkModule;
	SceneNode* mySceneNode;

	vtkSmartPointer<vtkPDBReader> pdb;
	vtkSmartPointer<vtkSphereSource> sphere;
	vtkSmartPointer<vtkGlyph3D> glyph;
	vtkSmartPointer<vtkPolyDataMapper> atomMapper;
	vtkSmartPointer<vtkLODActor> atom;
	vtkSmartPointer<vtkTubeFilter> tube;
	vtkSmartPointer<vtkPolyDataMapper> bondMapper;
	vtkSmartPointer<vtkLODActor> bond;
};

///////////////////////////////////////////////////////////////////////////////////////////////////
VtkScene::VtkScene() 
{
	// Create and register the omegalib vtk module.
	myVtkModule = new VtkModule();
	ModuleServices::addModule(myVtkModule);
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void VtkScene::initialize()
{
	// Create an omegalib scene node. We will attach our vtk objects to it.
	mySceneNode = new SceneNode(getEngine(), "vtkRoot");
	mySceneNode->setPosition(0, 0, -1);
	//mySceneNode->setBoundingBoxVisible(true);
	getEngine()->getScene()->addChild(mySceneNode);

	String filename = "pdbviewer/data/1EAA.pdb";
	String path;
	if(!DataManager::findFile(filename, path))
	{
		ofwarn("could not find %1%", %filename);
		return;
	}

	pdb =	vtkSmartPointer<vtkPDBReader>::New();
	pdb->SetFileName(path.c_str());
	pdb->SetHBScale(1.0);
	pdb->SetBScale(1.0);
	pdb->Update();
	ofmsg("# of atoms is: %1%", %pdb->GetNumberOfAtoms());
 
	double resolution = std::sqrt(100000.0 / pdb->GetNumberOfAtoms());
	if (resolution > 20) resolution = 20;
	if (resolution < 4)	resolution = 4;

	ofmsg("Resolution is: %1%", %resolution);
	sphere = vtkSmartPointer<vtkSphereSource>::New();
	sphere->SetCenter(0, 0, 0);
	sphere->SetRadius(1);
	sphere->SetThetaResolution(static_cast<int>(resolution));
	sphere->SetPhiResolution(static_cast<int>(resolution));
 
	glyph = vtkSmartPointer<vtkGlyph3D>::New();
	glyph->SetInputConnection(pdb->GetOutputPort());
	glyph->SetOrient(1);
	glyph->SetColorMode(1);
	// glyph->ScalingOn();
	glyph->SetScaleMode(2);
	glyph->SetScaleFactor(.25);
	glyph->SetSourceConnection(sphere->GetOutputPort());
 
	atomMapper =	vtkSmartPointer<vtkPolyDataMapper>::New();
	atomMapper->SetInputConnection(glyph->GetOutputPort());
	atomMapper->ImmediateModeRenderingOn();
	atomMapper->UseLookupTableScalarRangeOff();
	atomMapper->ScalarVisibilityOn();
	atomMapper->SetScalarModeToDefault();
 
	atom =	vtkSmartPointer<vtkLODActor>::New();
	atom->SetMapper(atomMapper);
	atom->GetProperty()->SetRepresentationToSurface();
	atom->GetProperty()->SetInterpolationToGouraud();
	atom->GetProperty()->SetAmbient(0.15);
	atom->GetProperty()->SetDiffuse(0.85);
	atom->GetProperty()->SetSpecular(0.1);
	atom->GetProperty()->SetSpecularPower(30);
	atom->GetProperty()->SetSpecularColor(1, 1, 1);
	atom->SetNumberOfCloudPoints(30000);
 
	myVtkModule->attachProp(atom, mySceneNode);
 
	tube = vtkSmartPointer<vtkTubeFilter>::New();
	tube->SetInputConnection(pdb->GetOutputPort());
	tube->SetNumberOfSides(static_cast<int>(resolution));
	tube->CappingOff();
	tube->SetRadius(0.2);
	tube->SetVaryRadius(0);
	tube->SetRadiusFactor(10);
 
	bondMapper =	vtkSmartPointer<vtkPolyDataMapper>::New();
	bondMapper->SetInputConnection(tube->GetOutputPort());
	bondMapper->ImmediateModeRenderingOn();
	bondMapper->UseLookupTableScalarRangeOff();
	bondMapper->ScalarVisibilityOff();
	bondMapper->SetScalarModeToDefault();
 
	bond =	vtkSmartPointer<vtkLODActor>::New();
	bond->SetMapper(bondMapper);
	bond->GetProperty()->SetRepresentationToSurface();
	bond->GetProperty()->SetInterpolationToGouraud();
	bond->GetProperty()->SetAmbient(0.15);
	bond->GetProperty()->SetDiffuse(0.85);
	bond->GetProperty()->SetSpecular(0.1);
	bond->GetProperty()->SetSpecularPower(30);
	bond->GetProperty()->SetSpecularColor(1, 1, 1);
	bond->GetProperty()->SetDiffuseColor(1.0000, 0.8941, 0.70981);

	myVtkModule->attachProp(bond, mySceneNode);

	// Setup the camera
	getEngine()->getDefaultCamera()->focusOn(getEngine()->getScene());
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// Application entry point
int main(int argc, char** argv)
{
	Application<VtkScene> app("pdbviewer");
	return omain(app, argc, argv);
}
