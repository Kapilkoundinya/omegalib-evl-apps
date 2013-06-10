/**************************************************************************************************
 * THE OMEGA LIB PROJECT
 *-------------------------------------------------------------------------------------------------
 * Copyright 2010-2013		Electronic Visualization Laboratory, University of Illinois at Chicago
 * Authors:										
 *  Alessandro Febretti		febret@gmail.com
 *-------------------------------------------------------------------------------------------------
 * Copyright (c) 2010-2013, Electronic Visualization Laboratory, University of Illinois at Chicago
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
#include "cyclops/SceneManager.h"

#include <osg/Depth>
#include <osg/ShapeDrawable>
#include <osg/TexEnv>
#include <osg/TexMat>
#include <osg/BlendFunc>
#include <osg/PolygonMode>
#include <osgDB/ReadFile>
#include <osgwTools/Shapes.h>

using namespace cyclops;

///////////////////////////////////////////////////////////////////////////////////////////////
class Pano: public EngineModule, ImageUtils::LoadImageAsyncTask::IAsyncTaskHandler
{
public:
	enum Type { Sphere, Cylinder };

public:
	Pano();
	virtual ~Pano();

	virtual void initialize();
	virtual void dispose();

	void loadPano(Type type, const String& panoName, const String& lString, const String& rString);
	void setPanoDegrees(float horizStart, float vertStart, float horizSpan, float vertSpan);
	void setCylinderOffsetAndHeight(const Vector3f offset, float height);

	void setAlpha(float value);
	float getAlpha();

	Type getType() { return myType; }

	void setLoadCompletedCommand(const String& cmd) { myLoadCompletedCommand = cmd; }
	const String& getLoadCompletedCommand() { return myLoadCompletedCommand; }

	void onTaskCompleted(ImageUtils::LoadImageAsyncTask* data);

private:
	osg::Node* create();
	void update(bool resetGeometry);

private:
	Ref<SceneManager> myScene;

	Ref<osg::Texture> myRTexture;
	Ref<osg::Texture> myLTexture;
	Ref<osg::Node> myNode;
	Ref<osg::Geode> myGeode;
	Ref<osg::Uniform> myTextureUniform;
	Ref<osg::StateSet> myStateSet;
	Ref<osg::Geometry> myGeometry;

	Ref<osg::Uniform> myVertStartDegreesUniform;
	Ref<osg::Uniform> myHorizStartDegreesUniform;
	Ref<osg::Uniform> myVertSpanDegreesUniform;
	Ref<osg::Uniform> myHorizSpanDegreesUniform;

	Ref<osg::Uniform> myAlphaUniform;

	Ref<MoveSkyWithEyePointTransform> myTransform;

	Type myType;

	Vector3f myOffset;
	float myRadius;
	float myHeight;
	float myAlpha;

	String myLoadCompletedCommand;

	Ref<ImageUtils::LoadImageAsyncTask> myLeftTask;
	Ref<ImageUtils::LoadImageAsyncTask> myRightTask;
	bool myNeedUpdateGeometry;
};

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class MoveSkyWithEyePointTransform : public osg::Transform
{
public:
	float pitch;
	osg::Vec3d offset;
public:

    /** Get the transformation matrix which moves from local coords to world coords.*/
    virtual bool computeLocalToWorldMatrix(osg::Matrix& matrix,osg::NodeVisitor* nv) const 
    {
        osgUtil::CullVisitor* cv = dynamic_cast<osgUtil::CullVisitor*>(nv);
        if (cv)
        {
            osg::Vec3 eyePointLocal = cv->getEyeLocal();
            matrix.preMultTranslate(eyePointLocal + offset);
			matrix.preMultRotate(osg::Quat(pitch, osg::Vec3(1, 0, 0)));
        }
        return true;
    }

    /** Get the transformation matrix which moves from world coords to local coords.*/
    virtual bool computeWorldToLocalMatrix(osg::Matrix& matrix,osg::NodeVisitor* nv) const
    {
        osgUtil::CullVisitor* cv = dynamic_cast<osgUtil::CullVisitor*>(nv);
        if (cv)
        {
            osg::Vec3 eyePointLocal = cv->getEyeLocal();
            matrix.postMultTranslate(-eyePointLocal + offset);
	    }
        return true;
    }
};

///////////////////////////////////////////////////////////////////////////////////////////////////
// Python wrapper code.
#ifdef OMEGA_USE_PYTHON
#include "omega/PythonInterpreterWrapper.h"
BOOST_PYTHON_MODULE(pano)
{
	// PanoType
	PYAPI_ENUM(Pano::Type, PanoType)
		PYAPI_ENUM_VALUE(Pano, Cylinder)
		PYAPI_ENUM_VALUE(Pano, Sphere)
		;

	// Pano
	PYAPI_REF_BASE_CLASS_WITH_CTOR(Pano)
		PYAPI_METHOD(Pano, loadPano)
		PYAPI_METHOD(Pano, setPanoDegrees)
		PYAPI_METHOD(Pano, setAlpha)
		PYAPI_METHOD(Pano, getAlpha)
		PYAPI_METHOD(Pano, setCylinderOffsetAndHeight)
		;
}
#endif

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Pano::Pano():
	myRTexture(NULL), myLTexture(NULL), myNode(NULL),
	myRadius(100), myHeight(4), myAlpha(1.0f), myType(Sphere)
{
	// Allocate and delete MoveSkyWithEyePointTransform, since we can't use Ref<> inside the Pano header 
	// (because MoveSkyWithEyePointTransform is defined within this file)
	myTransform = new MoveSkyWithEyePointTransform();
	myScene = SceneManager::instance();

	ModuleServices::addModule(this);
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Pano::~Pano()
{
	myTransform = NULL;
}
	
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::loadPano(Type type, const String& panoName, const String& lString, const String& rString)
{
	myNeedUpdateGeometry = (myType != type);
	myType = type;

	String fileName = StringUtils::replaceAll(panoName, "%1%", lString);
	myLeftTask = ImageUtils::loadImageAsync(fileName);
	myLeftTask->setCompletionHandler(this);

	fileName = StringUtils::replaceAll(panoName, "%1%", rString);
	myRightTask = ImageUtils::loadImageAsync(fileName);
	myRightTask->setCompletionHandler(this);
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::onTaskCompleted(ImageUtils::LoadImageAsyncTask* task)
{
	if(task == myLeftTask)
	{
		osg::Texture2D* panoTex = new osg::Texture2D();
		panoTex->setResizeNonPowerOfTwoHint(false);

		osg::Image* osgImage = omegaOsg::OsgModule::pixelDataToOsg(task->getData().image);
		panoTex->setImage(osgImage);
		myLTexture = panoTex;
	}
	if(task == myRightTask)
	{
		osg::Texture2D* panoTex = new osg::Texture2D();
		panoTex->setResizeNonPowerOfTwoHint(false);

		osg::Image* osgImage = omegaOsg::OsgModule::pixelDataToOsg(task->getData().image);
		panoTex->setImage(osgImage);
		myRTexture = panoTex;
	}
	if(myLeftTask->isComplete() && myRightTask->isComplete())
	{
		myLeftTask = NULL;
		myRightTask = NULL;
		update(myNeedUpdateGeometry);
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::initialize()
{
	myStateSet = new osg::StateSet();

	// Uncomment to draw wireframe skybox.
	//osg::PolygonMode* pm = new osg::PolygonMode();
	//pm->setMode(osg::PolygonMode::FRONT_AND_BACK, osg::PolygonMode::LINE);
	//stateset->setAttribute(pm);

	myStateSet->setMode( GL_LIGHTING, osg::StateAttribute::OFF );
	myStateSet->setMode( GL_CULL_FACE, osg::StateAttribute::OFF );
	myStateSet->setMode( GL_TEXTURE_2D, osg::StateAttribute::ON );

	Ref<osg::Depth> depth = new osg::Depth;
	depth->setWriteMask(false);
	//depth->setRange(1.0,1.0);   
	myStateSet->setAttributeAndModes(depth, osg::StateAttribute::ON );

	myStateSet->setRenderBinDetails(-1,"RenderBin");

	myGeode = new osg::Geode;		
	myGeode->setCullingActive(false);
	myGeode->setStateSet(myStateSet);

	myTransform->setCullingActive(false);
	myTransform->addChild(myGeode);

	ProgramAsset* program = myScene->getProgram("pano", "modules/pano/pano.vert", "modules/pano/pano.frag");
	//osg::StateSet* stateset = myGeode->getOrCreateStateSet();
	myStateSet->setAttributeAndModes(program->program, osg::StateAttribute::ON);

	myStateSet->addUniform( new osg::Uniform("unif_PanoMapL", 0) );
	myStateSet->addUniform( new osg::Uniform("unif_PanoMapR", 1) );

	myVertSpanDegreesUniform = new osg::Uniform("unif_VertSpanDegrees", 180.0f);
	myHorizSpanDegreesUniform = new osg::Uniform("unif_HorizSpanDegrees", 360.0f);
	myVertStartDegreesUniform = new osg::Uniform("unif_VertStartDegrees", 0.0f);
	myHorizStartDegreesUniform = new osg::Uniform("unif_HorizStartDegrees", 0.0f);
	myStateSet->addUniform(myVertSpanDegreesUniform);
	myStateSet->addUniform(myHorizSpanDegreesUniform);
	myStateSet->addUniform(myVertStartDegreesUniform);
	myStateSet->addUniform(myHorizStartDegreesUniform);

	myAlphaUniform = new osg::Uniform("unif_Alpha", 1.0f);
	myStateSet->addUniform(myAlphaUniform);
	setAlpha(myAlpha);

	update(true);

	myNode = myTransform;

	myScene->getOsgRoot()->addChild(myNode);
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::dispose()
{
	omsg("Pano::dispose");

	if(myNode != NULL && myScene != NULL)
	{
		myScene->getOsgRoot()->removeChild(myNode);
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::update(bool resetGeometry)
{
	if(myGeode != NULL)
	{
		omsg("Updating Pano");

		if(myLTexture != NULL)
		{
			myStateSet->setTextureAttributeAndModes(0, myLTexture, osg::StateAttribute::ON);
		}
		if(myRTexture != NULL)
		{
			myStateSet->setTextureAttributeAndModes(1, myRTexture, osg::StateAttribute::ON);
		}

		//osg::BlendFunc* bf = new osg::BlendFunc();
		//bf->setFunction(GL_SRC_ALPHA, GL_ONE);
		//myStateSet->setAttribute(bf);

		myTransform->pitch = -Math::Pi / 2;

		if(resetGeometry)
		{
			if(myGeometry != NULL)
			{
				myGeode->removeDrawable(myGeometry);
			}
			if(myType == Sphere)
			{
				myGeometry = osgwTools::makeAltAzSphere(myRadius, 24, 24);
			}
			else if(myType == Cylinder)
			{
				myGeometry = osgwTools::makeOpenCylinder(myHeight, myRadius, myRadius, osg::Vec2s(1, 24));
			}
			myGeode->addDrawable(myGeometry);
		}
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::setPanoDegrees(float horizStart, float vertStart, float horizSpan, float vertSpan)
{
	if(myHorizSpanDegreesUniform != NULL) myHorizSpanDegreesUniform->set(horizSpan);
	if(myVertSpanDegreesUniform != NULL) myVertSpanDegreesUniform->set(vertSpan);
	if(myHorizStartDegreesUniform != NULL) myHorizStartDegreesUniform->set(horizStart);
	if(myVertStartDegreesUniform != NULL) myVertStartDegreesUniform->set(vertStart);
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::setCylinderOffsetAndHeight(const Vector3f offset, float height)
{
	myOffset = offset;
	myHeight = height;
	update(true);
	myTransform->offset = osg::Vec3d(myOffset[0], myOffset[1], myOffset[2]);
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void Pano::setAlpha(float value)
{
	myAlpha = value;
	if(myAlphaUniform != NULL)
	{
		myAlphaUniform->set(myAlpha);
		if(myAlpha < 1.0)
		{
			myStateSet->setRenderingHint(osg::StateSet::TRANSPARENT_BIN);
			myStateSet->setMode(GL_BLEND, osg::StateAttribute::ON | osg::StateAttribute::OVERRIDE);
			myStateSet->setMode(GL_DEPTH_TEST, osg::StateAttribute::OFF  | osg::StateAttribute::OVERRIDE); 
		}
		else
		{
			myStateSet->setRenderingHint(osg::StateSet::OPAQUE_BIN);
			myStateSet->setMode(GL_BLEND, osg::StateAttribute::OFF);
			myStateSet->setMode(GL_DEPTH_TEST, osg::StateAttribute::OFF  | osg::StateAttribute::OVERRIDE); 
		}
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////
float Pano::getAlpha()
{
	return myAlpha;
}
