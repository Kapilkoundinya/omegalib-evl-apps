/*=========================================================================
 
 Program:   Visualization Toolkit
 Module:    vtkInteractorStyleTerrain.cxx
 
 Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
 All rights reserved.
 See Copyright.txt or http://www.kitware.com/Copyright.htm for details.
 
 This software is distributed WITHOUT ANY WARRANTY; without even
 the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 PURPOSE.  See the above copyright notice for more information.
 
 =========================================================================*/
#include "vtkInteractorStyleMyTrackball.h"

#include <vtkActor.h>
#include <vtkActorCollection.h>
#include <vtkCamera.h>
#include <vtkCallbackCommand.h>
#include <vtkCellPicker.h>
#include <vtkExtractEdges.h>
#include <vtkExtractSelection.h>
#include <vtkFloatArray.h>
#include <vtkIntArray.h>
#include <vtkMath.h>
#include <vtkObjectFactory.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkProp.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSelection.h>
#include <vtkSelectionNode.h>


vtkStandardNewMacro(vtkInteractorStyleMyTrackball);

//----------------------------------------------------------------------------
vtkInteractorStyleMyTrackball::vtkInteractorStyleMyTrackball()
{
	this->MotionFactor = 10.0;
}

//----------------------------------------------------------------------------
vtkInteractorStyleMyTrackball::~vtkInteractorStyleMyTrackball()
{
	
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnMouseMove() 
{ 
	int x = this->Interactor->GetEventPosition()[0];
	int y = this->Interactor->GetEventPosition()[1];
	
	switch (this->State) 
    {
		case VTKIS_ROTATE:
			this->FindPokedRenderer(x, y);
			this->Rotate();
			this->InvokeEvent(vtkCommand::InteractionEvent, NULL);
			break;
			
		case VTKIS_PAN:
			this->FindPokedRenderer(x, y);
			this->Pan();
			this->InvokeEvent(vtkCommand::InteractionEvent, NULL);
			break;
			
		case VTKIS_DOLLY:
			this->FindPokedRenderer(x, y);
			this->Dolly();
			this->InvokeEvent(vtkCommand::InteractionEvent, NULL);
			break;
    }
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnLeftButtonDown () 
{ 	
	int x = this->Interactor->GetEventPosition()[0];
	int y = this->Interactor->GetEventPosition()[1];
	
	this->FindPokedRenderer(x, y);
	if (this->CurrentRenderer == NULL)
	{
		return;
	}
	
	// left click while not holding SHIFT key
	if(!this->Interactor->GetShiftKey())
	{
		this->GrabFocus(this->EventCallbackCommand);
		this->StartRotate();
	}
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnLeftButtonUp ()
{
	switch (this->State) 
    {
		case VTKIS_ROTATE:
			this->EndRotate();
			if ( this->Interactor )
			{
				this->ReleaseFocus();
			}
			break;
    }
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnRightButtonDown () 
{
	this->FindPokedRenderer(this->Interactor->GetEventPosition()[0], 
							this->Interactor->GetEventPosition()[1]);
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	this->GrabFocus(this->EventCallbackCommand);
	this->StartPan();
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnRightButtonUp ()
{
	switch (this->State) 
    {
		case VTKIS_PAN:
			this->EndPan();
			if ( this->Interactor )
			{
				this->ReleaseFocus();
			}
			break;
    }
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnMouseWheelForward () 
{
	this->FindPokedRenderer(this->Interactor->GetEventPosition()[0], 
							this->Interactor->GetEventPosition()[1]);
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	this->GrabFocus(this->EventCallbackCommand);
	this->StartDolly();
	double factor = this->MotionFactor * 0.2 * this->MouseWheelMotionFactor;
	this->Dolly(pow(1.1, factor));
	this->EndDolly();
	this->ReleaseFocus();
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnMouseWheelBackward ()
{
	this->FindPokedRenderer(this->Interactor->GetEventPosition()[0], 
							this->Interactor->GetEventPosition()[1]);
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	this->GrabFocus(this->EventCallbackCommand);
	this->StartDolly();
	double factor = this->MotionFactor * -0.2 * this->MouseWheelMotionFactor;
	this->Dolly(pow(1.1, factor));
	this->EndDolly();
	this->ReleaseFocus();
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::Rotate()
{
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	vtkRenderWindowInteractor *rwi = this->Interactor;
	
	int dx = rwi->GetEventPosition()[0] - rwi->GetLastEventPosition()[0];
	int dy = rwi->GetEventPosition()[1] - rwi->GetLastEventPosition()[1];
	
	int *size = this->CurrentRenderer->GetRenderWindow()->GetSize();
	
	double delta_elevation = -20.0 / size[1];
	double delta_azimuth = -20.0 / size[0];
	
	double rxf = dx * delta_azimuth * this->MotionFactor;
	double ryf = dy * delta_elevation * this->MotionFactor;
	
	vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
	camera->Azimuth(rxf);
	camera->Elevation(ryf);
	camera->OrthogonalizeViewUp();
	
	if (this->AutoAdjustCameraClippingRange)
    {
		this->CurrentRenderer->ResetCameraClippingRange();
    }
	
	if (rwi->GetLightFollowCamera()) 
    {
		this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
    }
	
	rwi->Render();
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::Pan()
{
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	vtkRenderWindowInteractor *rwi = this->Interactor;
	
	// Get the vector of motion
	
	double fp[3], focalPoint[3], pos[3], v[3], p1[4], p2[4];
	
	vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
	camera->GetPosition( pos );
	camera->GetFocalPoint( fp );
	
	this->ComputeWorldToDisplay(fp[0], fp[1], fp[2], 
								focalPoint);
	
	this->ComputeDisplayToWorld(rwi->GetEventPosition()[0], 
								rwi->GetEventPosition()[1],
								focalPoint[2],
								p1);
	
	this->ComputeDisplayToWorld(rwi->GetLastEventPosition()[0],
								rwi->GetLastEventPosition()[1], 
								focalPoint[2], 
								p2);
    
	for (int i=0; i<3; i++)
    {
		v[i] = p2[i] - p1[i];
		pos[i] += v[i];
		fp[i] += v[i];
    }
	
	camera->SetPosition( pos );
	camera->SetFocalPoint( fp );
    
	if (rwi->GetLightFollowCamera()) 
    {
		this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
    }
    
	rwi->Render();
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::Dolly()
{
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	vtkRenderWindowInteractor *rwi = this->Interactor;
	double *center = this->CurrentRenderer->GetCenter();
	int dy = rwi->GetEventPosition()[1] - rwi->GetLastEventPosition()[1];
	double dyf = this->MotionFactor * dy / center[1];
	this->Dolly(pow(1.1, dyf));
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::Dolly(double factor)
{
	if (this->CurrentRenderer == NULL)
    {
		return;
    }
	
	vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
	
	camera->SetParallelScale(camera->GetParallelScale() / factor);
	camera->Dolly(factor);
	if (this->AutoAdjustCameraClippingRange)
	{
		this->CurrentRenderer->ResetCameraClippingRange();
	}
	
	if (this->Interactor->GetLightFollowCamera()) 
    {
		this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
    }
	
	this->Interactor->Render();
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::OnChar()
{	
	vtkRenderWindowInteractor *rwi = this->Interactor;
	
	printf("KEY PRESSED - \'%c\':  ", rwi->GetKeyCode());
	
	switch (rwi->GetKeyCode())
	{
		case 'r':
		case 'R':
			this->CurrentRenderer->GetActiveCamera()->SetPosition(0, 0, 1);
			this->CurrentRenderer->GetActiveCamera()->SetFocalPoint(0, 0, 0);
			this->CurrentRenderer->GetActiveCamera()->SetViewUp(0, 1, 0);
			this->CurrentRenderer->ResetCamera();
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Reset Camera\n");
			rwi->Render();
			break;
		case 'p':
		case 'P':
			if(this->CurrentRenderer->GetActiveCamera()->GetParallelProjection() == 0){
				this->CurrentRenderer->GetActiveCamera()->ParallelProjectionOn();
				printf("Parallel Projection\n");
			}
			else{
				this->CurrentRenderer->GetActiveCamera()->ParallelProjectionOff();
				printf("Perspective Projection\n");
			}
			rwi->Render();
			break;
		case 'a':
		{
			vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
			camera->Azimuth(10);
			camera->OrthogonalizeViewUp();
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Rotate Left\n");
			rwi->Render();
			break;
		}
		case 'A':
		{
			vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
			camera->Azimuth(-10);
			camera->OrthogonalizeViewUp();
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Rotate Right\n");
			rwi->Render();
			break;
		}
		case 'e':
		{
			vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
			camera->Elevation(10);
			camera->OrthogonalizeViewUp();
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Rotate Down\n");
			rwi->Render();
			break;
		}
		case 'E':
		{
			vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
			camera->Elevation(-10);
			camera->OrthogonalizeViewUp();
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Rotate Up\n");
			rwi->Render();
			break;
		}
		case 'z':
		{
			vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
			camera->SetParallelScale(camera->GetParallelScale() / 1.21);
			camera->Dolly(1.21);
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Zoom In\n");
			rwi->Render();
			break;
		}
		case 'Z':
		{
			vtkCamera *camera = this->CurrentRenderer->GetActiveCamera();
			camera->SetParallelScale(1.21 / camera->GetParallelScale());
			camera->Dolly(1.0/1.21);
			this->CurrentRenderer->ResetCameraClippingRange();
			this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
			printf("Zoom Out\n");
			rwi->Render();
			break;
		}
			
		default:
			//this->Superclass::OnChar();
			printf("\n");
			break;
    }
}

//----------------------------------------------------------------------------
void vtkInteractorStyleMyTrackball::PrintSelf(ostream& os, vtkIndent indent)
{
	this->Superclass::PrintSelf(os,indent);
	
}


