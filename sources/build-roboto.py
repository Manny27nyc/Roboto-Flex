# License: Apache 2.0

from __future__ import print_function

# from glyphNameFormatter.data import name2unicode_AGD
from mutatorMath.ufo.document import DesignSpaceDocumentWriter, DesignSpaceDocumentReader
from designSpaceDocument import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor
#from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor

from fontmake.font_project import FontProject
from fontTools.varLib import build
from fontTools.varLib.mutator import instantiateVariableFont
from defcon import Font
import shutil
from distutils.dir_util import copy_tree
import os

	
def buildDesignSpace(sources, instances, axes):
	# use DesignSpaceDocument because it supports axis labelNames
	doc = DesignSpaceDocument()
	
	for source in sources:
		s = SourceDescriptor()
		s.path = source["path"]
		s.name = source["name"]
		s.copyInfo = source["copyInfo"]
		s.location = source["location"]
		s.familyName = source["familyName"]
		s.styleName = source["styleName"]
		doc.addSource(s)
	
	for instance in instances:
		i = InstanceDescriptor()
		i.location = instance["location"]
		i.familyName = instance["familyName"]
		i.styleName = instance["styleName"]
		doc.addInstance(i)
	
	for axis in axes:
		a = AxisDescriptor()
		a.minimum = axis["minimum"]
		a.maximum = axis["maximum"]
		a.default = axis["default"]
		a.name = axis["name"]
		a.tag = axis["tag"]
		for languageCode, labelName in axis["labelNames"].items():
			a.labelNames[languageCode] = labelName
		a.map = axis["map"]
		doc.addAxis(a)
		
	return doc

def buildGlyphSet(dflt, fonts):
	# fill the glyph set with default glyphs
	for font in fonts:
		for glyph in dflt:
			glyphName = glyph.name
			if glyphName not in font and glyphName not in composites:
				font.insertGlyph(glyph)
				font[glyphName].lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.25] # dark grey

# def buildComposites(composites, fonts):
# 	# build the composites
# 	for font in fonts:
# 		for glyphName in composites.keys():
# 			font.newGlyph(glyphName)
# 			composite = font[glyphName]
# 			composite.unicode = name2unicode_AGD[glyphName]
			
# 			value = composites[glyphName]
# 			items = value.split("+")
# 			base = items[0]
# 			items = items[1:]
	
# 			component = composite.instantiateComponent()
# 			component.baseGlyph = base
# 			baseGlyph = font[base]
# 			composite.width = baseGlyph.width
# 			composite.appendComponent(component)
	
# 			for item in items:
# 				baseName, anchorName = item.split("@")
# 				component = composite.instantiateComponent()
# 				component.baseGlyph = baseName
# 				anchor = _anchor = None
# 				for a in baseGlyph.anchors:
# 					if a["name"] == anchorName:
# 						anchor = a
# 				for a in font[baseName].anchors:
# 					if a["name"] == "_"+anchorName:
# 						_anchor = a
# 				if anchor and _anchor:
# 					x = anchor["x"] - _anchor["x"]
# 					y = anchor["y"] - _anchor["y"]
# 					component.move((x, y))
# 				composite.appendComponent(component)
# 			composite.lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.5] # grey

def setGlyphOrder(glyphOrder, fonts):
	# set the glyph order
	for font in fonts:
		font.glyphOrder = glyphOrder

def clearAnchors(fonts):
	# set the glyph order
	for font in fonts:
		for glyph in font:
		    glyph.clearAnchors()

def saveMasters(fonts, master_dir="master_ufo"):
	# save in master_ufo directory
	for font in fonts:
		path = os.path.join(master_dir, os.path.basename(font.path))

		#added this check because the "master_ufo" folder is getting removed at the beginning of this script
		if not os.path.exists(path):
			os.makedirs(path)
		font.save(path)

with open("sources/RobotoFlex.enc") as enc:
	glyphOrder = enc.read().splitlines()

print ("Cleaning up...")

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)

# Remove temporary 1-drawings
if os.path.exists("sources/1-drawings"):
	shutil.rmtree("sources/1-drawings", ignore_errors=True)


# New
src = {	"sources/1A-drawings/Mains/slnt",
		"sources/1A-drawings/Mains",
		"sources/1A-drawings/Parametric Axes",
		"sources/1A-drawings/Duovars",
		"sources/1A-drawings/Trivars",
		"sources/1A-drawings/Quadravars",
		
		}
	

src_dir = "sources/1-drawings"
master_dir = "master_ufo"
instance_dir = "instances"

# Copy sources to temporary 1-drawings
for source in src:
	copy_tree(source, src_dir)


# use a temporary designspace to build instances with mutator math
familyName = "RobotoFlex"
tmpDesignSpace = "tmp.designspace"
doc = DesignSpaceDocumentWriter(tmpDesignSpace)
# sources
doc.addSource(path="sources/1-drawings/RobotoFlex-Regular.ufo", name="RobotoFlex-Regular.ufo", location=dict(wght=0, wdth=0, opsz=0), styleName="Regular", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-XOPQ27-YOPQ25.ufo", name="RobotoFlex-XOPQ27-YOPQ25.ufo", location=dict(XYOPQ=-1), styleName="XOPQ27-YOPQ25", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-XOPQ175-YOPQ135.ufo", name="RobotoFlex-XOPQ175-YOPQ135.ufo", location=dict(XYOPQ=1), styleName="XOPQ175-YOPQ135", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-XTRA323.ufo", name="RobotoFlex-XTRA323.ufo", location=dict(XTRA=-1), styleName="XTRA323", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-XTRA603.ufo", name="RobotoFlex-XTRA603.ufo", location=dict(XTRA=1), styleName="XTRA603", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTLC416.ufo", name="RobotoFlex-YTLC416.ufo", location=dict(YTLC=-1), styleName="YTLC416", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTLC570.ufo", name="RobotoFlex-YTLC570.ufo", location=dict(YTLC=1), styleName="YTLC570", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTUC528.ufo", name="RobotoFlex-YTUC528.ufo", location=dict(YTUC=-1), styleName="YTUC528", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTUC760.ufo", name="RobotoFlex-YTUC760.ufo", location=dict(YTUC=1), styleName="YTUC760", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTAS649.ufo", name="RobotoFlex-YTAS649.ufo", location=dict(YTAS=-1), styleName="YTAS649", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTAS854.ufo", name="RobotoFlex-YTAS854.ufo", location=dict(YTAS=1), styleName="YTAS854", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTDE-305.ufo", name="RobotoFlex-YTDE-305.ufo", location=dict(YTDE=-1), styleName="YTDE-305", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoFlex-YTDE-98.ufo", name="RobotoFlex-YTDE-98.ufo", location=dict(YTDE=1), styleName="YTDE-98", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)

# axes
doc.addAxis(tag="wght", name="wght", minimum=100, maximum=900, default=400, warpMap=None)
doc.addAxis(tag="wdth", name="wdth", minimum=75, maximum=125, default=100, warpMap=None)
doc.addAxis(tag="opsz", name="opsz", minimum=8, maximum=144, default=14, warpMap=None)






# instances
instances = [
#	dict(fileName="instances/RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, wdth=125, opsz=1), styleName="opsz144-wght100-wdth151", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoFlex-opsz144-wght100-wdth075.ufo", location=dict(wght=100, wdth=87, opsz=1), styleName="opsz144-wght100-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, wdth=75, opsz=1), styleName="opsz144-wght100-wdth25", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),

# ## Leveling intermediates
#  	dict(fileName="master_ufo/RobotoFlex-opsz14wght1000.ufo", name="RobotoFlex-opsz14wght1000.ufo", location=dict(wght=1000, opsz=0), styleName="opsz14wght1000", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz18wght1000.ufo", name="RobotoFlex-opsz18wght1000.ufo", location=dict(wght=1000, opsz=18), styleName="opsz18wght1000", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz24wght100.ufo", name="RobotoFlex-opsz24wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz24wght1000.ufo", name="RobotoFlex-opsz24wght1000.ufo", location=dict(wght=1000, opsz=24), styleName="opsz24wght1000", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36wght100.ufo", name="RobotoFlex-opsz36wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36wght700.ufo", name="RobotoFlex-opsz36wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36wght1000", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36wght1000.ufo", name="RobotoFlex-opsz36wght1000.ufo", location=dict(wght=1000, opsz=36), styleName="opsz36wght1000", familyName=familyName),
# 
# 
# ## Figures
#  	dict(fileName="master_ufo/RobotoFlex-opsz18-wght100-wdth25.ufo", name="RobotoFlex-opsz18-wght100-wdth25.ufo", location=dict(wght=100, opsz=18, wdth=25), styleName="opsz18-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz24-wght100-wdth25.ufo", name="RobotoFlex-opsz24-wght100-wdth25.ufo", location=dict(wght=100, opsz=24, wdth=25), styleName="opsz24-wght-100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36-wght100-wdth25.ufo", name="RobotoFlex-opsz36-wght100-wdth25.ufo", location=dict(wght=100, opsz=36, wdth=25), styleName="opsz36-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36-wght600-wdth25.ufo", name="RobotoFlex-opsz36-wght600-wdth25.ufo", location=dict(wght=600, opsz=36, wdth=25), styleName="opsz36-wght600-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz18-wght700-wdth25.ufo", name="RobotoFlex-opsz18-wght700-wdth25.ufo", location=dict(wght=700, opsz=18, wdth=25), styleName="opsz18-wght700-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz24-wght700-wdth25.ufo", name="RobotoFlex-opsz24-wght700-wdth25.ufo", location=dict(wght=700, opsz=24, wdth=25), styleName="opsz24-wght700-wdth25", familyName=familyName),
#  	
#  	dict(fileName="master_ufo/RobotoFlex-opsz24-wght100.ufo", name="RobotoFlex-opsz24-wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24-wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36-wght100.ufo", name="RobotoFlex-opsz36-wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36-wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz18-wght700.ufo", name="RobotoFlex-opsz18-wght700.ufo", location=dict(wght=700, opsz=18), styleName="opsz18-wght700", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz24-wght700.ufo", name="RobotoFlex-opsz24-wght700.ufo", location=dict(wght=700, opsz=24), styleName="opsz24-wght700", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36-wght700.ufo", name="RobotoFlex-opsz36-wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36-wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz18-wght1000.ufo", name="RobotoFlex-opsz18-wght1000.ufo", location=dict(wght=1000, opsz=18), styleName="opsz18-wght1000", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz24-wght1000.ufo", name="RobotoFlex-opsz24-wght1000.ufo", location=dict(wght=1000, opsz=24), styleName="opsz24-wght1000", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36-wght1000.ufo", name="RobotoFlex-opsz36-wght1000.ufo", location=dict(wght=1000, opsz=36), styleName="opsz36-wght1000", familyName=familyName),
#  	
#  	
#  	dict(fileName="master_ufo/RobotoFlex-opsz24-wght100-wdth151.ufo", name="RobotoFlex-opsz24-wght100-wdth151.ufo", location=dict(wght=100, opsz=24, wdth=151), styleName="opsz24-wght100-wdth151", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz36-wght700-wdth151.ufo", name="RobotoFlex-opsz36-wght700-wdth151.ufo", location=dict(wght=700, opsz=36, wdth=151), styleName="opsz36-wght700-wdth151", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght500-wdth151.ufo", name="RobotoFlex-opsz144-wght500-wdth151.ufo", location=dict(wght=500, opsz=1, wdth=151), styleName="opsz144-wght500-wdth151", familyName=familyName),
# 	
# ##	NEW Caping
# 	
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth25-GRAD-1.ufo", location=dict(wght=100, opsz=1, wdth=25, GRAD=-200), styleName="opsz144-wght100-wdth25-GRAD-1", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-wdth25-GRAD1.ufo", location=dict(wght=100, opsz=1, wdth=25, GRAD=150), styleName="opsz144-wght100-wdth25-GRAD1", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth151-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth151-GRAD-1.ufo", location=dict(wght=100, opsz=1, wdth=151, GRAD=-200), styleName="opsz144-wght100-wdth151-GRAD-1", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth151-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-wdth151-GRAD1.ufo", location=dict(wght=100, opsz=1, wdth=151, GRAD=150), styleName="opsz144-wght100-wdth151-GRAD1", familyName=familyName),
#  	
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-GRAD1.ufo", location=dict(wght=100, opsz=1, GRAD=150), styleName="opsz144-wght100-GRAD1", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-GRAD-1.ufo", location=dict(wght=100, opsz=1, GRAD=-200), styleName="opsz144-wght100-GRAD-1", familyName=familyName),
#  	
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-GRAD1.ufo", name="RobotoFlex-opsz144-wght1000-GRAD1.ufo", location=dict(wght=1000, opsz=1, GRAD=150), styleName="opsz144-wght1000-GRAD1", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-GRAD-1.ufo", name="RobotoFlex-opsz144-wght1000-GRAD-1.ufo", location=dict(wght=1000, opsz=1, GRAD=-200), styleName="opsz144-wght1000-GRAD-1", familyName=familyName),
#  	
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-GRAD1.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-GRAD1.ufo", location=dict(wght=1000, opsz=1, wdth=25, GRAD=150), styleName="opsz144-wght1000-wdth25-GRAD1", familyName=familyName),
#  	
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-GRAD-1.ufo", name="RobotoFlex-opsz8-wght100-GRAD-1.ufo", location=dict(wght=100, opsz=0, GRAD=-200), styleName="opsz8-wght100-GRAD-1", familyName=familyName),
#  	
#  
# ##	Caping & trimming instances github issue 56
# # 	XOPQ27
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-wdth100-XOPQ27.ufo", name="RobotoFlex-opsz8-wght100-wdth100-XOPQ27.ufo", location=dict(wght=100, opsz=-1, wdth=100, XOPQ=27), styleName="opsz8-wght100-wdth100-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz8-wght100-wdth25-XOPQ27.ufo", location=dict(wght=100, opsz=-1, wdth=25, XOPQ=27), styleName="opsz8-wght100-wdth25-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz8-wght100-wdth151-XOPQ27.ufo", location=dict(wght=100, opsz=-1, wdth=151, XOPQ=27), styleName="opsz8-wght100-wdth151-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght100-wdth100-XOPQ27.ufo", name="RobotoFlex-opsz14-wght100-wdth100-XOPQ27.ufo", location=dict(wght=100, opsz=0, wdth=100, XOPQ=27), styleName="opsz14-wght100-wdth100-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght100-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz14-wght100-wdth25-XOPQ27.ufo", location=dict(wght=100, opsz=0, wdth=25, XOPQ=27), styleName="opsz14-wght100-wdth25-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght100-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz14-wght100-wdth151-XOPQ27.ufo", location=dict(wght=100, opsz=0, wdth=151, XOPQ=27), styleName="RobotoFlex-opsz14-wght100-wdth151-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth100-XOPQ27.ufo", name="RobotoFlex-opsz144-wght400-wdth100-XOPQ27.ufo", location=dict(wght=400, opsz=1, wdth=100, XOPQ=27), styleName="opsz144-wght400-wdth100-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1, wdth=100, XOPQ=27), styleName="opsz144-wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz144-wght400-wdth25-XOPQ27.ufo", location=dict(wght=400, opsz=1, wdth=25, XOPQ=27), styleName="opsz144-wght400-wdth100-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XOPQ=27), styleName="opsz144-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-XOPQ27.ufo", location=dict(wght=1000, opsz=1, wdth=25, XOPQ=27), styleName="opsz144-wght1000-wdth25-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz144-wght400-wdth151-XOPQ27.ufo", location=dict(wght=400, opsz=1, wdth=151, XOPQ=27), styleName="opsz144-wght400-wdth151-XOPQ27", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=1, wdth=151, XOPQ=27), styleName="opsz144-wght100-wdth151", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-XOPQ27.ufo", location=dict(wght=1000, opsz=1, wdth=151, XOPQ=27), styleName="opsz144-wght1000-wdth151-XOPQ27", familyName=familyName),
#   	
# # 	#XOPQ175
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth25-XOPQ175.ufo", name="RobotoFlex-opsz144-wght400-wdth25-XOPQ175.ufo", location=dict(wght=400, opsz=1, wdth=25, XOPQ=175), styleName="opsz144-wght400-wdth25-XOPQ175", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XOPQ=175), styleName="opsz144-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-XOPQ175.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-XOPQ175.ufo", location=dict(wght=1000, opsz=1, wdth=25, XOPQ=175), styleName="opsz144-wght1000-wdth25-XOPQ175", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-XOPQ175.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-XOPQ175.ufo", location=dict(wght=1000, opsz=1, wdth=151, XOPQ=175), styleName="opsz144-wght1000-wdth151-XOPQ175", familyName=familyName),
#   	
# # 	#YOPQ25
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-wdth100-YOPQ25.ufo", name="RobotoFlex-opsz8-wght100-wdth100-YOPQ25.ufo", location=dict(wght=100, opsz=-1, wdth=100, YOPQ=25), styleName="opsz8-wght100-wdth100-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-wdth25-YOPQ25.ufo", name="RobotoFlex-opsz8-wght100-wdth25-YOPQ25.ufo", location=dict(wght=100, opsz=-1, wdth=25, YOPQ=25), styleName="opsz8-wght100-wdth25-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght100-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz8-wght100-wdth151-YOPQ25.ufo", location=dict(wght=100, opsz=-1, wdth=151, YOPQ=25), styleName="opsz8-wght100-wdth151-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght100-wdth100-YOPQ25.ufo", name="RobotoFlex-opsz14-wght100-wdth100-YOPQ25.ufo", location=dict(wght=100, opsz=0, wdth=100, YOPQ=25), styleName="opsz14-wght100-wdth100-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght100-wdth25-YOPQ25.ufo", name="RobotoFlex-opsz14-wght100-wdth25-YOPQ25.ufo", location=dict(wght=100, opsz=0, wdth=25, YOPQ=25), styleName="opsz14-wght100-wdth25-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght100-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz14-wght100-wdth151-YOPQ25.ufo", location=dict(wght=100, opsz=0, wdth=151, YOPQ=25), styleName="opsz14-wght100-wdth151-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth100-YOPQ25.ufo", name="RobotoFlex-opsz144-wght400-wdth100-YOPQ25.ufo", location=dict(wght=400, opsz=1, wdth=100, YOPQ=25), styleName="opsz144-wght400-wdth100-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1, YOPQ=25), styleName="opsz144-wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth25-YOPQ25.ufo", name="RobotoFlex-opsz144-wght400-wdth25-YOPQ25.ufo", location=dict(wght=400, opsz=1, wdth=25, YOPQ=25), styleName="opsz144-wght400-wdth25-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, YOPQ=25), styleName="opsz144-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz144-wght400-wdth151-YOPQ25.ufo", location=dict(wght=400, opsz=1, wdth=151, YOPQ=25), styleName="opsz144-wght400-wdth151-YOPQ25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=1, wdth=151, YOPQ=25), styleName="opsz144-wght100-wdth151", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-YOPQ25.ufo", location=dict(wght=1000, opsz=1, wdth=151, YOPQ=25), styleName="opsz144-wght1000-wdth151-YOPQ25", familyName=familyName),
#   	
# # 	#YOPQ135
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth100-YOPQ135.ufo", name="RobotoFlex-opsz144-wght1000-wdth100-YOPQ135.ufo", location=dict(wght=1000, opsz=1, wdth=100, YOPQ=135), styleName="opsz144-wght1000-wdth100-YOPQ135", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth25-YOPQ135.ufo", name="RobotoFlex-opsz144-wght400-wdth25-YOPQ135.ufo", location=dict(wght=400, opsz=1, wdth=25, YOPQ=135), styleName="opsz144-wght400-wdth25-YOPQ135", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, YOPQ=135), styleName="opsz144-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-YOPQ135.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-YOPQ135.ufo", location=dict(wght=1000, opsz=1, wdth=25, YOPQ=135), styleName="opsz144-wght1000-wdth25-YOPQ135", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-YOPQ135.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-YOPQ135.ufo", location=dict(wght=1000, opsz=1, wdth=151, YOPQ=135), styleName="opsz144-wght1000-wdth151-YOPQ135", familyName=familyName),
#  
# #  	#XTRA323
#  	dict(fileName="master_ufo/RobotoFlex-opsz8-wght1000-wdth25-XTRA323.ufo", name="RobotoFlex-opsz8-wght1000-wdth25-XTRA323.ufo", location=dict(wght=1000, opsz=-1, wdth=25, XTRA=323), styleName="opsz8-wght1000-wdth25-XTRA323", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght1000-wdth100-XTRA323.ufo", name="RobotoFlex-opsz14-wght1000-wdth100-XTRA323.ufo", location=dict(wght=1000, opsz=0, wdth=100, XTRA=323), styleName="opsz14-wght1000-wdth100-XTRA323", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz14-wght1000-wdth25-XTRA323.ufo", name="RobotoFlex-opsz14-wght1000-wdth25-XTRA323.ufo", location=dict(wght=1000, opsz=0, wdth=25, XTRA=323), styleName="opsz14-wght1000-wdth25-XTRA323", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1, wdth=100, XTRA=323), styleName="opsz144-wght100", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth100-XTRA323.ufo", name="RobotoFlex-opsz144-wght1000-wdth100-XTRA323.ufo", location=dict(wght=1000, opsz=1, wdth=100, XTRA=323), styleName="opsz144-wght1000-wdth100-XTRA323", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wdth25.ufo", name="RobotoFlex-opsz144-wdth25.ufo", location=dict(wght=400, opsz=1, wdth=25, XTRA=323), styleName="opsz144-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XTRA=323), styleName="opsz144-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth25.ufo", name="RobotoFlex-opsz144-wght1000-wdth25.ufo", location=dict(wght=1000, opsz=1, wdth=25, XTRA=323), styleName="opsz144-wght1000-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth100-XTRA323.ufo", name="RobotoFlex-opsz144-wght400-wdth100-XTRA323.ufo", location=dict(wght=400, opsz=1, wdth=100, XTRA=323), styleName="opsz144-wght400-wdth100-XTRA323", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=1, wdth=151, XTRA=323), styleName="opsz144-wght1000-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth151-XTRA323.ufo", name="RobotoFlex-opsz144-wght400-wdth151-XTRA323.ufo", location=dict(wght=400, opsz=1, wdth=151, XTRA=323), styleName="opsz144-wght400-wdth151-XTRA323", familyName=familyName),
#  
# #  	#XTRA603
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth100-XTRA603.ufo", name="RobotoFlex-opsz144-wght400-wdth100-XTRA603.ufo", location=dict(wght=400, opsz=1, wdth=100, XTRA=603), styleName="opsz144-wght400-wdth100-XTRA603", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth100-XTRA603.ufo", name="RobotoFlex-opsz144-wght100-wdth100-XTRA603.ufo", location=dict(wght=100, opsz=1, wdth=100, XTRA=603), styleName="opsz144-wght100-wdth100-XTRA603", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght400-wdth25-XTRA603.ufo", name="RobotoFlex-opsz144-wght400-wdth25-XTRA603.ufo", location=dict(wght=400, opsz=1, wdth=25, XTRA=603), styleName="opsz144-wght400-wdth25-XTRA603", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XTRA=603), styleName="opsz144-wght100-wdth25", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-XTRA603.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-XTRA603.ufo", location=dict(wght=1000, opsz=1, wdth=25, XTRA=603), styleName="opsz144-wght1000-wdth25-XTRA603", familyName=familyName),
#  	dict(fileName="master_ufo/RobotoFlex-opsz144-wght100-wdth151-XTRA603.ufo", name="RobotoFlex-opsz144-wght100-wdth151-XTRA603.ufo", location=dict(wght=100, opsz=1, wdth=151, XTRA=603), styleName="opsz144-wght100-wdth151-XTRA603", familyName=familyName),	

]
for instance in instances:
	doc.startInstance(**instance)
	doc.writeInfo()
	doc.writeKerning()
	doc.endInstance()

doc.save()
# read and process the designspace
doc = DesignSpaceDocumentReader(tmpDesignSpace, ufoVersion=2, roundGeometry=False, verbose=False)
print ("Reading DesignSpace...")
doc.process(makeGlyphs=True, makeKerning=True, makeInfo=True)
os.remove(tmpDesignSpace) # clean up

# update the instances with the source fonts
# print str(instances) + ' instances! '
for instance in instances:
	fileName = os.path.basename(instance["fileName"])
	source_path = os.path.join(src_dir, fileName)
	instance_path = os.path.join(instance_dir, fileName)
	source_font = Font(source_path)
	instance_font = Font(instance_path)
	# insert the source glyphs in the instance font
	for glyph in source_font:
		instance_font.insertGlyph(glyph)
	master_path = os.path.join(master_dir, fileName)
	instance_font.save(master_path)

designSpace = "sources/RobotoFlex.designspace"
sources = [
	dict(path="master_ufo/RobotoFlex-Regular.ufo", name="RobotoFlex-Regular.ufo", location=dict( wght=400, wdth=100, opsz=0, GRAD=0, slnt=0), styleName="Regular", familyName=familyName, copyInfo=True),
	
##	Main 
	dict(path="master_ufo/RobotoFlex-GRAD-200.ufo", name="RobotoFlex-GRAD-200.ufo", location=dict(GRAD=-200, opsz=0), styleName="GRAD-200", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-GRAD150.ufo", name="RobotoFlex-GRAD150.ufo", location=dict(GRAD=150, opsz=0), styleName="GRAD150", familyName=familyName, copyInfo=False),
		
	dict(path="master_ufo/RobotoFlex-wght100.ufo", name="RobotoFlex-wght100.ufo", location=dict(wght=100, opsz=0), styleName="wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-wght1000.ufo", name="RobotoFlex-wght1000.ufo", location=dict(wght=1000, opsz=0), styleName="wght1000", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoFlex-opsz8.ufo", name="RobotoFlex-opsz8.ufo", location=dict(opsz=-1), styleName="opsz8", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36.ufo", name="RobotoFlex-opsz36.ufo", location=dict(opsz=36), styleName="opsz36", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144.ufo", name="RobotoFlex-opsz144.ufo", location=dict(opsz=1), styleName="opsz144", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoFlex-wdth25.ufo", name="RobotoFlex-wdth25.ufo", location=dict(wdth=25, opsz=0), styleName="wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-wdth151.ufo", name="RobotoFlex-wdth151.ufo", location=dict(wdth=151, opsz=0), styleName="wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-wdth25.ufo", name="RobotoFlex-wdth25.ufo", location=dict(PWDT=560), styleName="wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-wdth151.ufo", name="RobotoFlex-wdth151.ufo", location=dict(PWDT=867), styleName="wdth151", familyName=familyName, copyInfo=False),

##	Slant
	
	dict(path="master_ufo/RobotoFlex-Slant.ufo", name="RobotoFlex-Slant.ufo", location=dict(slnt=-10, opsz=0), styleName="slnt-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz8-wght400-wdth100-slnt-1.ufo", name="RobotoFlex-opsz8-wght400-wdth100-slnt-1.ufo", location=dict(slnt=-10, opsz=-1, wght=400), styleName="opsz8-wght400-wdth100-slnt-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz14-wght100-slnt-1.ufo", name="RobotoFlex-opsz14-wght100-slnt-1.ufo", location=dict(slnt=-10, opsz=0, wght=100), styleName="opsz14-wght100-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz14-wght400-wdth25-slnt-1.ufo", name="RobotoFlex-opsz14-wght400-wdth25-slnt-1.ufo", location=dict(slnt=-10, opsz=0, wdth=25, wght=400), styleName="opsz14-wght400-wdth25-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz14-wght400-wdth151-slnt-1.ufo", name="RobotoFlex-opsz14-wght400-wdth151-slnt-1.ufo", location=dict(slnt=-10, opsz=0, wdth=151, wght=400), styleName="opsz14-wght400-wdth151-slnt-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25-slnt-1.ufo", name="RobotoFlex-opsz144-wght100-wdth25-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=25, wght=100), styleName="opsz144-wght100-wdth25-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth100-slnt-1.ufo", name="RobotoFlex-opsz144-wght100-wdth100-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=100, wght=100), styleName="opsz144-wght100-wdth100-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151-slnt-1.ufo", name="RobotoFlex-opsz144-wght100-wdth151-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=151, wght=100), styleName="opsz144-wght100-wdth151-slnt-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth25-slnt-1.ufo", name="RobotoFlex-opsz144-wght400-wdth25-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=25, wght=400), styleName="opsz144-wght400-wdth25-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth100-slnt-1.ufo", name="RobotoFlex-opsz144-wght400-wdth100-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wght=400), styleName="opsz144-wght400-wdth100-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth151-slnt-1.ufo", name="RobotoFlex-opsz144-wght400-wdth151-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=151, wght=400), styleName="opsz144-wght400-wdth151-slnt-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-slnt-1.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=25, wght=1000), styleName="opsz144-wght1000-wdth25-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth100-slnt-1.ufo", name="RobotoFlex-opsz144-wght1000-wdth100-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=100, wght=1000), styleName="opsz144-wght1000-wdth100-slnt-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-slnt-1.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-slnt-1.ufo", location=dict(slnt=-10, opsz=1, wdth=151, wght=1000), styleName="opsz144-wght1000-wdth151-slnt-1", familyName=familyName, copyInfo=False),


##	Parametric
	dict(path="master_ufo/RobotoFlex-XOPQ27.ufo", name="RobotoFlex-XOPQ27.ufo", location=dict(XOPQ=27, opsz=0), styleName="XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-XOPQ175.ufo", name="RobotoFlex-XOPQ175.ufo", location=dict(XOPQ=175, opsz=0), styleName="XOPQ175", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-XTRA323.ufo", name="RobotoFlex-XTRA323.ufo", location=dict(XTRA=323, opsz=0), styleName="XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-XTRA603.ufo", name="RobotoFlex-XTRA603.ufo", location=dict(XTRA=603, opsz=0), styleName="XTRA603", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoFlex-YOPQ25.ufo", name="RobotoFlex-YOPQ25.ufo", location=dict(YOPQ=25, opsz=0), styleName="YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YOPQ135.ufo", name="RobotoFlex-YOPQ135.ufo", location=dict(YOPQ=135, opsz=0), styleName="YOPQ135", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoFlex-YTLC416.ufo", name="RobotoFlex-YTLC416.ufo", location=dict(YTLC=416, opsz=0), styleName="YTLC416", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTLC570.ufo", name="RobotoFlex-YTLC570.ufo", location=dict(YTLC=570, opsz=0), styleName="YTLC570", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTUC528.ufo", name="RobotoFlex-YTUC528.ufo", location=dict(YTUC=528, opsz=0), styleName="YTUC528", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTUC760.ufo", name="RobotoFlex-YTUC760.ufo", location=dict(YTUC=760, opsz=0), styleName="YTUC760", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTAS649.ufo", name="RobotoFlex-YTAS649.ufo", location=dict(YTAS=649, opsz=0), styleName="YTAS649", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTAS854.ufo", name="RobotoFlex-YTAS854.ufo", location=dict(YTAS=854, opsz=0), styleName="YTAS854", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTDE-305.ufo", name="RobotoFlex-YTDE-305.ufo", location=dict(YTDE=-305, opsz=0), styleName="YTDE-305", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTDE-98.ufo", name="RobotoFlex-YTDE-98.ufo", location=dict(YTDE=-98, opsz=0), styleName="YTDE-98", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoFlex-YTFI560.ufo", name="RobotoFlex-YTFI560.ufo", location=dict(YTFI=560, opsz=0), styleName="YTFI560", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-YTFI788.ufo", name="RobotoFlex-YTFI788.ufo", location=dict(YTFI=788, opsz=0), styleName="YTFI788", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-YOLCmin.ufo", name="RobotoFlex-YOLCmin.ufo", location=dict(YOLC=25), styleName="YOLCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YOLCmax.ufo", name="RobotoFlex-YOLCmax.ufo", location=dict(YOLC=130), styleName="YOLCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YOUCmin.ufo", name="RobotoFlex-YOUCmin.ufo", location=dict(YOUC=25), styleName="YOUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YOUCmax.ufo", name="RobotoFlex-YOUCmax.ufo", location=dict(YOUC=135), styleName="YOUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YOFImin.ufo", name="RobotoFlex-YOFImin.ufo", location=dict(YOFI=25), styleName="YOFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YOFImax.ufo", name="RobotoFlex-YOFImax.ufo", location=dict(YOFI=150), styleName="YOFImax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XOLCmin.ufo", name="RobotoFlex-XOLCmin.ufo", location=dict(XOLC=27), styleName="XOLCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XOLCmax.ufo", name="RobotoFlex-XOLCmax.ufo", location=dict(XOLC=170), styleName="XOLCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XOUCmin.ufo", name="RobotoFlex-XOUCmin.ufo", location=dict(XOUC=27), styleName="XOUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XOUCmax.ufo", name="RobotoFlex-XOUCmax.ufo", location=dict(XOUC=170), styleName="XOUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XOFImin.ufo", name="RobotoFlex-XOFImin.ufo", location=dict(XOFI=27), styleName="XOFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XOFImax.ufo", name="RobotoFlex-XOFImax.ufo", location=dict(XOFI=180), styleName="XOFImax", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-XTLCmin.ufo", name="RobotoFlex-XTLCmin.ufo", location=dict(XTLC=129), styleName="XTLCmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoFlex-XTLCmax.ufo", name="RobotoFlex-XTLCmax.ufo", location=dict(XTLC=393), styleName="XTLCmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoFlex-XTUCmin.ufo", name="RobotoFlex-XTUCmin.ufo", location=dict(XTUC=227), styleName="XTUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XTUCmax.ufo", name="RobotoFlex-XTUCmax.ufo", location=dict(XTUC=507), styleName="XTUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XTFImin.ufo", name="RobotoFlex-XTFImin.ufo", location=dict(XTFI=155), styleName="XTFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-XTFImax.ufo", name="RobotoFlex-XTFImax.ufo", location=dict(XTFI=392), styleName="XTFImax", familyName=familyName, copyInfo=False),
 	
# 	dict(path="master_ufo/RobotoFlex-YTADmin.ufo", name="RobotoFlex-YTADmin.ufo", location=dict(YTAD=460), styleName="YTADmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YTADmax.ufo", name="RobotoFlex-YTADmax.ufo", location=dict(YTAD=600), styleName="YTADmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YTDDmin.ufo", name="RobotoFlex-YTDDmin.ufo", location=dict(YTDD=-1), styleName="YTDDmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YTDDmax.ufo", name="RobotoFlex-YTDDmax.ufo", location=dict(YTDD=1), styleName="YTDDmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-UDLNmin.ufo", name="RobotoFlex-UDLNmin.ufo", location=dict(UDLN=-195), styleName="UDLNmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-UDLNmax.ufo", name="RobotoFlex-UDLNmax.ufo", location=dict(UDLN=0), styleName="UDLNmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YTRAmin.ufo", name="RobotoFlex-YTRAmin.ufo", location=dict(YTRA=-1), styleName="YTRAmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-YTRAmax.ufo", name="RobotoFlex-YTRAmax.ufo", location=dict(YTRA=1), styleName="YTRAmax", familyName=familyName, copyInfo=False),

	
##	Duovars
	dict(path="master_ufo/RobotoFlex-opsz144-wdth151.ufo", name="RobotoFlex-opsz144-wdth151.ufo", location=dict(wdth=151, opsz=1), styleName="opsz144-wdth151", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoFlex-opsz144-wdth075.ufo", name="RobotoFlex-opsz144-wdth075.ufo", location=dict(wdth=80, opsz=1), styleName="opsz144-wdth25075", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wdth25.ufo", name="RobotoFlex-opsz144-wdth25.ufo", location=dict(wdth=25, opsz=1), styleName="opsz144-wdth25", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz144-wght1000.ufo", name="RobotoFlex-opsz144-wght1000.ufo", location=dict(wght=1000, opsz=1), styleName="opsz144-wght1000", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght700.ufo", name="RobotoFlex-opsz144-wght700.ufo", location=dict(wght=700, opsz=1), styleName="opsz144-wght700", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz8-wdth151.ufo", name="RobotoFlex-opsz8-wdth151.ufo", location=dict(wdth=151, opsz=-1), styleName="opsz8-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz8-wdth25.ufo", name="RobotoFlex-opsz8-wdth25.ufo", location=dict(wdth=25, opsz=-1), styleName="opsz8-wdth25", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz8-wght1000.ufo", name="RobotoFlex-opsz8-wght1000.ufo", location=dict(wght=1000, opsz=-1), styleName="opsz8-wght1000", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz8-wght100.ufo", name="RobotoFlex-opsz8-wght100.ufo", location=dict(wght=100, opsz=-1), styleName="opsz8-wght100", familyName=familyName, copyInfo=False),
	
 	dict(path="master_ufo/RobotoFlex-wght1000-wdth25.ufo", name="RobotoFlex-wght1000-wdth25.ufo", location=dict(wdth=25, wght=1000, opsz=0), styleName="wght1000-wdth25", familyName=familyName, copyInfo=False),
	
	
##	Trivars
	
	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth25.ufo", name="RobotoFlex-opsz8-wght100-wdth25.ufo", location=dict(wght=100, wdth=25, opsz=-1), styleName="opsz8-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth151.ufo", name="RobotoFlex-opsz8-wght100-wdth151.ufo", location=dict(wght=100, wdth=151, opsz=-1), styleName="opsz8-wght100-wdth151", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz8-wght1000-wdth25.ufo", name="RobotoFlex-opsz8-wght1000-wdth25.ufo", location=dict(wdth=25, wght=1000, opsz=-1), styleName="opsz8-wght1000-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz8-wght1000-wdth151.ufo", name="RobotoFlex-opsz8-wght1000-wdth151.ufo", location=dict(wdth=151, wght=1000, opsz=-1), styleName="opsz8-wght1000-wdth151", familyName=familyName, copyInfo=False),
	
	
	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth25.ufo", name="RobotoFlex-opsz14-wght100-wdth25.ufo", location=dict(wght=100, wdth=25, opsz=0), styleName="opsz14-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth151.ufo", name="RobotoFlex-opsz14-wght100-wdth151.ufo", location=dict(wght=100, wdth=151, opsz=0), styleName="opsz14-wght100-wdth151", familyName=familyName, copyInfo=False),
	
#	dict(path="master_ufo/RobotoFlex-opsz14-wght1000-wdth25.ufo", name="RobotoFlex-opsz14-wght1000-wdth25.ufo", location=dict(wght=1000, wdth=25, opsz=0), styleName="opsz14-wght1000-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz14-wght1000-wdth151.ufo", name="RobotoFlex-opsz14-wght1000-wdth151.ufo", location=dict(wght=1000, wdth=151, opsz=0), styleName="opsz14-wght1000-wdth151", familyName=familyName, copyInfo=False),
	
	
	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, wdth=151, opsz=1), styleName="opsz144-wght100-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, wdth=25, opsz=1), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	
 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151.ufo", name="RobotoFlex-opsz144-wght1000-wdth151.ufo", location=dict(wght=1000, opsz=1, wdth=151), styleName="opsz144-wght1000-wdth151", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25.ufo", name="RobotoFlex-opsz144-wght1000-wdth25.ufo", location=dict(wght=1000, opsz=1, wdth=25), styleName="opsz144-wght1000-wdth25", familyName=familyName, copyInfo=False),
	
	

##	Leveling REGENERATE TO CATCH UPDATES
	
 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth100-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth100-GRAD-1.ufo", location=dict(wght=100, opsz=1, GRAD=-200), styleName="opsz144-wght100-wdth100-GRAD-1", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth151-GRAD-1.ufo", location=dict(wght=100, wdth=151, opsz=1, GRAD=-200), styleName="opsz144-wght100-wdth151-GRAD-1", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth25-GRAD-1.ufo", location=dict(wght=100, wdth=25, opsz=1, GRAD=-200), styleName="opsz144-wght100-wdth25-GRAD-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth100-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-wdth100-GRAD1.ufo", location=dict(wght=100, opsz=1, GRAD=150), styleName="opsz144-wght100-wdth100-GRAD1", familyName=familyName, copyInfo=False),
# 	
 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth100-GRAD-1.ufo", name="RobotoFlex-opsz144-wght1000-wdth100-GRAD-1.ufo", location=dict(wght=1000, opsz=1, GRAD=150), styleName="opsz144-wght1000-wdth100-GRAD-1", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-GRAD-1.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-GRAD-1.ufo", location=dict(wght=1000, wdth=151, opsz=1, GRAD=150), styleName="opsz144-wght1000-wdth151-GRAD-1", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-GRAD-1.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-GRAD-1.ufo", location=dict(wght=1000, wdth=25, opsz=1, GRAD=150), styleName="opsz144-wght1000-wdth25-GRAD-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth100-GRAD-1.ufo", name="RobotoFlex-opsz8-wght100-wdth100-GRAD-1.ufo", location=dict(wght=100, opsz=-1, GRAD=-200), styleName="opsz8-wght100-wdth100-GRAD-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth151-GRAD-1.ufo", name="RobotoFlex-opsz8-wght100-wdth151-GRAD-1.ufo", location=dict(wght=100, wdth=151, opsz=-1, GRAD=-200), styleName="opsz8-wght100-wdth151-GRAD-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth25-GRAD-1.ufo", name="RobotoFlex-opsz8-wght100-wdth25-GRAD-1.ufo", location=dict(wght=100, wdth=25, opsz=-1, GRAD=-200), styleName="opsz8-wght100-wdth25-GRAD-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth100-GRAD1.ufo", name="RobotoFlex-opsz8-wght100-wdth100-GRAD1.ufo", location=dict(wght=100, opsz=-1, GRAD=150), styleName="opsz8-wght100-wdth100-GRAD1", familyName=familyName, copyInfo=False),

## Leveling intermediates
# 	dict(path="master_ufo/RobotoFlex-opsz14wght1000.ufo", name="RobotoFlex-opsz14wght1000.ufo", location=dict(wght=1000, opsz=0), styleName="opsz14wght1000", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz18wght1000.ufo", name="RobotoFlex-opsz18wght1000.ufo", location=dict(wght=1000, opsz=18), styleName="opsz18wght1000", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz24wght100.ufo", name="RobotoFlex-opsz24wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz24wght1000.ufo", name="RobotoFlex-opsz24wght1000.ufo", location=dict(wght=1000, opsz=24), styleName="opsz24wght1000", familyName=familyName, copyInfo=False),

# # auto-generate
# # opsz36
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght100.ufo", name="RobotoFlex-opsz36-wght100.ufo", location=dict(wght=100, opsz=0.492), styleName="opsz36-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght700.ufo", name="RobotoFlex-opsz36-wght700.ufo", location=dict(wght=700, opsz=0.492), styleName="opsz36-wght700", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght1000.ufo", name="RobotoFlex-opsz36-wght1000.ufo", location=dict(wght=1000, opsz=0.492), styleName="opsz36-wght1000", familyName=familyName, copyInfo=False),
# # 
# # # auto-generate
# # #opsz144
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght700.ufo", name="RobotoFlex-opsz144-wght700.ufo", location=dict(wght=700, opsz=1), styleName="opsz36wght1000", familyName=familyName, copyInfo=False),

## Figures
# 	dict(path="master_ufo/RobotoFlex-opsz18-wght100-wdth25.ufo", name="RobotoFlex-opsz18-wght100-wdth25.ufo", location=dict(wght=100, opsz=18, wdth=25), styleName="opsz18-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz24-wght100-wdth25.ufo", name="RobotoFlex-opsz24-wght100-wdth25.ufo", location=dict(wght=100, opsz=24, wdth=25), styleName="opsz24-wght-100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght100-wdth25.ufo", name="RobotoFlex-opsz36-wght100-wdth25.ufo", location=dict(wght=100, opsz=36, wdth=25), styleName="opsz36-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght600-wdth25.ufo", name="RobotoFlex-opsz36-wght600-wdth25.ufo", location=dict(wght=600, opsz=36, wdth=25), styleName="opsz36-wght600-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz18-wght700-wdth25.ufo", name="RobotoFlex-opsz18-wght700-wdth25.ufo", location=dict(wght=700, opsz=18, wdth=25), styleName="opsz18-wght700-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz24-wght700-wdth25.ufo", name="RobotoFlex-opsz24-wght700-wdth25.ufo", location=dict(wght=700, opsz=24, wdth=25), styleName="opsz24-wght700-wdth25", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-opsz24-wght100.ufo", name="RobotoFlex-opsz24-wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght100.ufo", name="RobotoFlex-opsz36-wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz18-wght700.ufo", name="RobotoFlex-opsz18-wght700.ufo", location=dict(wght=700, opsz=18), styleName="opsz18-wght700", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz24-wght700.ufo", name="RobotoFlex-opsz24-wght700.ufo", location=dict(wght=700, opsz=24), styleName="opsz24-wght700", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght700.ufo", name="RobotoFlex-opsz36-wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz18-wght1000.ufo", name="RobotoFlex-opsz18-wght1000.ufo", location=dict(wght=1000, opsz=18), styleName="opsz18-wght1000", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz24-wght1000.ufo", name="RobotoFlex-opsz24-wght1000.ufo", location=dict(wght=1000, opsz=24), styleName="opsz24-wght1000", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght1000.ufo", name="RobotoFlex-opsz36-wght1000.ufo", location=dict(wght=1000, opsz=36), styleName="opsz36-wght1000", familyName=familyName, copyInfo=False),
# 	
# 	
# 	dict(path="master_ufo/RobotoFlex-opsz24-wght100-wdth151.ufo", name="RobotoFlex-opsz24-wght100-wdth151.ufo", location=dict(wght=100, opsz=24, wdth=151), styleName="opsz24-wght100-wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz36-wght700-wdth151.ufo", name="RobotoFlex-opsz36-wght700-wdth151.ufo", location=dict(wght=700, opsz=36, wdth=151), styleName="opsz36-wght700-wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght500-wdth151.ufo", name="RobotoFlex-opsz144-wght500-wdth151.ufo", location=dict(wght=500, opsz=1, wdth=151), styleName="opsz144-wght500-wdth151", familyName=familyName, copyInfo=False),

# auto-generate	
##	NEW Caping
	
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth25-GRAD-1.ufo", location=dict(wght=100, opsz=1, wdth=25, GRAD=-200), styleName="opsz144-wght100-wdth25-GRAD-1", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-wdth25-GRAD1.ufo", location=dict(wght=100, opsz=1, wdth=25, GRAD=150), styleName="opsz144-wght100-wdth25-GRAD1", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-wdth151-GRAD-1.ufo", location=dict(wght=100, opsz=1, wdth=151, GRAD=-200), styleName="opsz144-wght100-wdth151-GRAD-1", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-wdth151-GRAD1.ufo", location=dict(wght=100, opsz=1, wdth=151, GRAD=150), styleName="opsz144-wght100-wdth151-GRAD1", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-GRAD1.ufo", name="RobotoFlex-opsz144-wght100-GRAD1.ufo", location=dict(wght=100, opsz=1, GRAD=150), styleName="opsz144-wght100-GRAD1", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-GRAD-1.ufo", name="RobotoFlex-opsz144-wght100-GRAD-1.ufo", location=dict(wght=100, opsz=1, GRAD=-200), styleName="opsz144-wght100-GRAD-1", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-GRAD1.ufo", name="RobotoFlex-opsz144-wght1000-GRAD1.ufo", location=dict(wght=1000, opsz=1, GRAD=150), styleName="opsz144-wght1000-GRAD1", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-GRAD-1.ufo", name="RobotoFlex-opsz144-wght1000-GRAD-1.ufo", location=dict(wght=1000, opsz=1, GRAD=-200), styleName="opsz144-wght1000-GRAD-1", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-GRAD1.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-GRAD1.ufo", location=dict(wght=1000, opsz=1, wdth=25, GRAD=150), styleName="opsz144-wght1000-wdth25-GRAD1", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-GRAD-1.ufo", name="RobotoFlex-opsz8-wght100-GRAD-1.ufo", location=dict(wght=100, opsz=0, GRAD=-200), styleName="opsz8-wght100-GRAD-1", familyName=familyName, copyInfo=False),
# 	
# auto-generate
# ##	Caping & trimming instances github issue 56
# # 	XOPQ27
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth100-XOPQ27.ufo", name="RobotoFlex-opsz8-wght100-wdth100-XOPQ27.ufo", location=dict(wght=100, opsz=-1, wdth=100, XOPQ=27), styleName="opsz8-wght100-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz8-wght100-wdth25-XOPQ27.ufo", location=dict(wght=100, opsz=-1, wdth=25, XOPQ=27), styleName="opsz8-wght100-wdth25-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz8-wght100-wdth151-XOPQ27.ufo", location=dict(wght=100, opsz=-1, wdth=151, XOPQ=27), styleName="opsz8-wght100-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth100-XOPQ27.ufo", name="RobotoFlex-opsz14-wght100-wdth100-XOPQ27.ufo", location=dict(wght=100, opsz=0, wdth=100, XOPQ=27), styleName="opsz14-wght100-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz14-wght100-wdth25-XOPQ27.ufo", location=dict(wght=100, opsz=0, wdth=25, XOPQ=27), styleName="opsz14-wght100-wdth25-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz14-wght100-wdth151-XOPQ27.ufo", location=dict(wght=100, opsz=0, wdth=151, XOPQ=27), styleName="RobotoFlex-opsz14-wght100-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth100-XOPQ27.ufo", name="RobotoFlex-opsz144-wght400-wdth100-XOPQ27.ufo", location=dict(wght=400, opsz=1, wdth=100, XOPQ=27), styleName="opsz144-wght400-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1, wdth=100, XOPQ=27), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz144-wght400-wdth25-XOPQ27.ufo", location=dict(wght=400, opsz=1, wdth=25, XOPQ=27), styleName="opsz144-wght400-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XOPQ=27), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-XOPQ27.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-XOPQ27.ufo", location=dict(wght=1000, opsz=1, wdth=25, XOPQ=27), styleName="opsz144-wght1000-wdth25-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz144-wght400-wdth151-XOPQ27.ufo", location=dict(wght=400, opsz=1, wdth=151, XOPQ=27), styleName="opsz144-wght400-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=1, wdth=151, XOPQ=27), styleName="opsz144-wght100-wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-XOPQ27.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-XOPQ27.ufo", location=dict(wght=1000, opsz=1, wdth=151, XOPQ=27), styleName="opsz144-wght1000-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
#  	
# # 	#XOPQ175
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth25-XOPQ175.ufo", name="RobotoFlex-opsz144-wght400-wdth25-XOPQ175.ufo", location=dict(wght=400, opsz=1, wdth=25, XOPQ=175), styleName="opsz144-wght400-wdth25-XOPQ175", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XOPQ=175), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-XOPQ175.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-XOPQ175.ufo", location=dict(wght=1000, opsz=1, wdth=25, XOPQ=175), styleName="opsz144-wght1000-wdth25-XOPQ175", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-XOPQ175.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-XOPQ175.ufo", location=dict(wght=1000, opsz=1, wdth=151, XOPQ=175), styleName="opsz144-wght1000-wdth151-XOPQ175", familyName=familyName, copyInfo=False),
#  	
# # 	#YOPQ25
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth100-YOPQ25.ufo", name="RobotoFlex-opsz8-wght100-wdth100-YOPQ25.ufo", location=dict(wght=100, opsz=-1, wdth=100, YOPQ=25), styleName="opsz8-wght100-wdth100-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth25-YOPQ25.ufo", name="RobotoFlex-opsz8-wght100-wdth25-YOPQ25.ufo", location=dict(wght=100, opsz=-1, wdth=25, YOPQ=25), styleName="opsz8-wght100-wdth25-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght100-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz8-wght100-wdth151-YOPQ25.ufo", location=dict(wght=100, opsz=-1, wdth=151, YOPQ=25), styleName="opsz8-wght100-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth100-YOPQ25.ufo", name="RobotoFlex-opsz14-wght100-wdth100-YOPQ25.ufo", location=dict(wght=100, opsz=0, wdth=100, YOPQ=25), styleName="opsz14-wght100-wdth100-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth25-YOPQ25.ufo", name="RobotoFlex-opsz14-wght100-wdth25-YOPQ25.ufo", location=dict(wght=100, opsz=0, wdth=25, YOPQ=25), styleName="opsz14-wght100-wdth25-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght100-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz14-wght100-wdth151-YOPQ25.ufo", location=dict(wght=100, opsz=0, wdth=151, YOPQ=25), styleName="opsz14-wght100-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth100-YOPQ25.ufo", name="RobotoFlex-opsz144-wght400-wdth100-YOPQ25.ufo", location=dict(wght=400, opsz=1, wdth=100, YOPQ=25), styleName="opsz144-wght400-wdth100-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1, YOPQ=25), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth25-YOPQ25.ufo", name="RobotoFlex-opsz144-wght400-wdth25-YOPQ25.ufo", location=dict(wght=400, opsz=1, wdth=25, YOPQ=25), styleName="opsz144-wght400-wdth25-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, YOPQ=25), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz144-wght400-wdth151-YOPQ25.ufo", location=dict(wght=400, opsz=1, wdth=151, YOPQ=25), styleName="opsz144-wght400-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=1, wdth=151, YOPQ=25), styleName="opsz144-wght100-wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-YOPQ25.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-YOPQ25.ufo", location=dict(wght=1000, opsz=1, wdth=151, YOPQ=25), styleName="opsz144-wght1000-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
#  	
# # 	#YOPQ135
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth100-YOPQ135.ufo", name="RobotoFlex-opsz144-wght1000-wdth100-YOPQ135.ufo", location=dict(wght=1000, opsz=1, wdth=100, YOPQ=135), styleName="opsz144-wght1000-wdth100-YOPQ135", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth25-YOPQ135.ufo", name="RobotoFlex-opsz144-wght400-wdth25-YOPQ135.ufo", location=dict(wght=400, opsz=1, wdth=25, YOPQ=135), styleName="opsz144-wght400-wdth25-YOPQ135", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, YOPQ=135), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-YOPQ135.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-YOPQ135.ufo", location=dict(wght=1000, opsz=1, wdth=25, YOPQ=135), styleName="opsz144-wght1000-wdth25-YOPQ135", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth151-YOPQ135.ufo", name="RobotoFlex-opsz144-wght1000-wdth151-YOPQ135.ufo", location=dict(wght=1000, opsz=1, wdth=151, YOPQ=135), styleName="opsz144-wght1000-wdth151-YOPQ135", familyName=familyName, copyInfo=False),
# 
# #  	#XTRA323
# 	dict(path="master_ufo/RobotoFlex-opsz8-wght1000-wdth25-XTRA323.ufo", name="RobotoFlex-opsz8-wght1000-wdth25-XTRA323.ufo", location=dict(wght=1000, opsz=-1, wdth=25, XTRA=323), styleName="opsz8-wght1000-wdth25-XTRA323", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght1000-wdth100-XTRA323.ufo", name="RobotoFlex-opsz14-wght1000-wdth100-XTRA323.ufo", location=dict(wght=1000, opsz=0, wdth=100, XTRA=323), styleName="opsz14-wght1000-wdth100-XTRA323", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz14-wght1000-wdth25-XTRA323.ufo", name="RobotoFlex-opsz14-wght1000-wdth25-XTRA323.ufo", location=dict(wght=1000, opsz=0, wdth=25, XTRA=323), styleName="opsz14-wght1000-wdth25-XTRA323", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100.ufo", name="RobotoFlex-opsz144-wght100.ufo", location=dict(wght=100, opsz=1, wdth=100, XTRA=323), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth100-XTRA323.ufo", name="RobotoFlex-opsz144-wght1000-wdth100-XTRA323.ufo", location=dict(wght=1000, opsz=1, wdth=100, XTRA=323), styleName="opsz144-wght1000-wdth100-XTRA323", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wdth25.ufo", name="RobotoFlex-opsz144-wdth25.ufo", location=dict(wght=400, opsz=1, wdth=25, XTRA=323), styleName="opsz144-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XTRA=323), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25.ufo", name="RobotoFlex-opsz144-wght1000-wdth25.ufo", location=dict(wght=1000, opsz=1, wdth=25, XTRA=323), styleName="opsz144-wght1000-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth100-XTRA323.ufo", name="RobotoFlex-opsz144-wght400-wdth100-XTRA323.ufo", location=dict(wght=400, opsz=1, wdth=100, XTRA=323), styleName="opsz144-wght400-wdth100-XTRA323", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151.ufo", name="RobotoFlex-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=1, wdth=151, XTRA=323), styleName="opsz144-wght1000-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth151-XTRA323.ufo", name="RobotoFlex-opsz144-wght400-wdth151-XTRA323.ufo", location=dict(wght=400, opsz=1, wdth=151, XTRA=323), styleName="opsz144-wght400-wdth151-XTRA323", familyName=familyName, copyInfo=False),
# 
# #  	#XTRA603
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth100-XTRA603.ufo", name="RobotoFlex-opsz144-wght400-wdth100-XTRA603.ufo", location=dict(wght=400, opsz=1, wdth=100, XTRA=603), styleName="opsz144-wght400-wdth100-XTRA603", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth100-XTRA603.ufo", name="RobotoFlex-opsz144-wght100-wdth100-XTRA603.ufo", location=dict(wght=100, opsz=1, wdth=100, XTRA=603), styleName="opsz144-wght100-wdth100-XTRA603", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght400-wdth25-XTRA603.ufo", name="RobotoFlex-opsz144-wght400-wdth25-XTRA603.ufo", location=dict(wght=400, opsz=1, wdth=25, XTRA=603), styleName="opsz144-wght400-wdth25-XTRA603", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth25.ufo", name="RobotoFlex-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=1, wdth=25, XTRA=603), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght1000-wdth25-XTRA603.ufo", name="RobotoFlex-opsz144-wght1000-wdth25-XTRA603.ufo", location=dict(wght=1000, opsz=1, wdth=25, XTRA=603), styleName="opsz144-wght1000-wdth25-XTRA603", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoFlex-opsz144-wght100-wdth151-XTRA603.ufo", name="RobotoFlex-opsz144-wght100-wdth151-XTRA603.ufo", location=dict(wght=100, opsz=1, wdth=151, XTRA=603), styleName="opsz144-wght100-wdth151-XTRA603", familyName=familyName, copyInfo=False),
	
]
instances = [
	#dict(path="master_ufo/RobotoFlex-opsz144-wght700.ufo", filename="RobotoFlex-opsz144-wght700.ufo", location=dict(wght=700, opsz=1), styleName="opsz144-wght700", familyName=familyName, copyInfo=False),
]
axes = [


	dict(minimum=100, maximum=1000, default=400, name="wght", tag="wght", labelNames={"en": "wght"}, map=[], hidden=0),
	dict(minimum=25, maximum=151, default=100, name="wdth", tag="wdth", labelNames={"en": "wdth"}, map=[], hidden=0),
	dict(minimum=8, maximum=144, default=14, name="opsz", tag="opsz", labelNames={"en": "opsz"}, map=[ (8.0, -1), (14.0, 0), (36.0, 0.492), (84.0, 0.946), (144.0, 1.0) ], hidden=0),
# 	dict(minimum=44, maximum=150, default=94, name="PWGT", tag="PWGT", labelNames={"en": "PWGT"}, map=[]),
# 	dict(minimum=560, maximum=867, default=712, name="PWDT", tag="PWDT", labelNames={"en": "PWDT"}, map=[]),
# 	dict(minimum=-1, maximum=1, default=0, name="POPS", tag="POPS", labelNames={"en": "POPS"}, map=[]),
	dict(minimum=-200, maximum=150, default=0, name="GRAD", tag="GRAD", labelNames={"en": "GRAD"}, map=[], hidden=0),
 	dict(minimum=-10, maximum=0, default=0, name="slnt", tag="slnt", labelNames={"en": "slnt"}, map=[], hidden=1),
# 	dict(minimum=-1, maximum=1, default=0, name="YTRA", tag="YTRA", labelNames={"en": "YTRA"}, map=[]),
	dict(minimum=323, maximum=603, default=468, name="XTRA", tag="XTRA", labelNames={"en": "XTRA"}, map=[], hidden=1),
	dict(minimum=27, maximum=175, default=96, name="XOPQ", tag="XOPQ", labelNames={"en": "XOPQ"}, map=[], hidden=1),
	dict(minimum=25, maximum=135, default=79, name="YOPQ", tag="YOPQ", labelNames={"en": "YOPQ"}, map=[], hidden=1),

# 	dict(minimum=25, maximum=130, default=71, name="YOLC", tag="YOLC", labelNames={"en": "YOLC"}, map=[]),
#  	dict(minimum=25, maximum=135, default=79, name="YOUC", tag="YOUC", labelNames={"en": "YOUC"}, map=[]),
#  	dict(minimum=25, maximum=150, default=85, name="YOFI", tag="YOFI", labelNames={"en": "YOFI"}, map=[]),
	dict(minimum=416, maximum=570, default=514, name="YTLC", tag="YTLC", labelNames={"en": "YTLC"}, map=[], hidden=1),
	dict(minimum=528, maximum=760, default=712, name="YTUC", tag="YTUC", labelNames={"en": "YTUC"}, map=[], hidden=1),
	dict(minimum=649, maximum=854, default=750, name="YTAS", tag="YTAS", labelNames={"en": "YTAS"}, map=[], hidden=1),
	dict(minimum=-305, maximum=-98, default=-203, name="YTDE", tag="YTDE", labelNames={"en": "YTDE"}, map=[], hidden=1),
	dict(minimum=560, maximum=788, default=738, name="YTFI", tag="YTFI", labelNames={"en": "YTFI"}, map=[], hidden=1),
# 	
# 	
# 	dict(minimum=27, maximum=170, default=93, name="XOLC", tag="XOLC", labelNames={"en": "XOLC"}, map=[]),
# 	dict(minimum=27, maximum=170, default=93, name="XOUC", tag="XOUC", labelNames={"en": "XOUC"}, map=[]),
# 	dict(minimum=27, maximum=180, default=97, name="XOFI", tag="XOFI", labelNames={"en": "XOFI"}, map=[]),
# 	dict(minimum=129, maximum=393, default=240, name="XTLC", tag="XTLC", labelNames={"en": "XTLC"}, map=[]),
# 	dict(minimum=227, maximum=507, default=367, name="XTUC", tag="XTUC", labelNames={"en": "XTUC"}, map=[]),
# 	dict(minimum=155, maximum=392, default=292, name="XTFI", tag="XTFI", labelNames={"en": "XTFI"}, map=[]),
# 	dict(minimum=155, maximum=392, default=292, name="XTFI", tag="XTFI", labelNames={"en": "XTFI"}, map=[]),

# 	dict(minimum=460, maximum=600, default=563, name="YTAD", tag="YTAD", labelNames={"en": "YTAD"}, map=[]),
# 	dict(minimum=-1, maximum=1, default=0, name="YTDD", tag="YTDD", labelNames={"en": "YTDD"}, map=[]),
# 	dict(minimum=-195, maximum=0, default=-49, name="UDLN", tag="UDLN", labelNames={"en": "UDLN"}, map=[]),

]

doc = buildDesignSpace(sources, instances, axes)


#add rule for dollar. Needs to be after doc = buildDesignSpace() because this doc is a DesignSpaceDocument(), rather than the doc above which is a DesignSpaceDocumentReader() object
r1 = RuleDescriptor()
r1.name = "dollar-stroke-wght"
r1.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r1.subs.append(("dollar", "dollar.rvrn"))
doc.addRule(r1)
	
r2 = RuleDescriptor()
r2.name = "dollar-stroke-wdth"
r2.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r2.subs.append(("dollar", "dollar.rvrn"))
doc.addRule(r2)

r3 = RuleDescriptor()
r3.name = "coloncurrency-stroke-wght"
r3.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r3.subs.append(("coloncurrency", "coloncurrency.rvrn"))
doc.addRule(r3)
	
r4 = RuleDescriptor()
r4.name = "coloncurrency-stroke-wdth"
r4.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r4.subs.append(("coloncurrency", "coloncurrency.rvrn"))
doc.addRule(r4)

r5 = RuleDescriptor()
r5.name = "won-stroke-wght"
r5.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r5.subs.append(("won", "won.rvrn"))
doc.addRule(r5)
	
r6 = RuleDescriptor()
r6.name = "won-stroke-wdth"
r6.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r6.subs.append(("won", "won.rvrn"))
doc.addRule(r6)

r7 = RuleDescriptor()
r7.name = "cent-stroke-wght"
r7.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r7.subs.append(("cent", "cent.rvrn"))
doc.addRule(r7)
	
r8 = RuleDescriptor()
r8.name = "cent-stroke-wdth"
r8.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r8.subs.append(("cent", "cent.rvrn"))
doc.addRule(r8)

r9 = RuleDescriptor()
r9.name = "uni20B2-stroke-wght"
r9.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r9.subs.append(("uni20B2", "uni20B2.rvrn"))
doc.addRule(r9)
	
r10 = RuleDescriptor()
r10.name = "uni20B2-stroke-wdth"
r10.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r10.subs.append(("uni20B2", "uni20B2.rvrn"))
doc.addRule(r10)

r11 = RuleDescriptor()
r11.name = "uni20B2-stroke-wght"
r11.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r11.subs.append(("uni20B2", "uni20B2.rvrn"))
doc.addRule(r11)
	
r12 = RuleDescriptor()
r12.name = "uni20B1-stroke-wdth"
r12.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r12.subs.append(("uni20B1", "uni20B1.rvrn"))
doc.addRule(r12)

r13 = RuleDescriptor()
r13.name = "uni20B1-stroke-wght"
r13.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r13.subs.append(("uni20B1", "uni20B1.rvrn"))
doc.addRule(r13)

r14 = RuleDescriptor()
r14.name = "naira-stroke-wdth"
r14.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r14.subs.append(("naira", "naira.rvrn"))
doc.addRule(r14)

r15 = RuleDescriptor()
r15.name = "naira-stroke-wght"
r15.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r15.subs.append(("naira", "naira.rvrn"))
doc.addRule(r15)

r16 = RuleDescriptor()
r16.name = "uni20B5-stroke-wdth"
r16.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r16.subs.append(("uni20B5", "uni20B5.rvrn"))
doc.addRule(r16)

r17 = RuleDescriptor()
r17.name = "uni20B5-stroke-wght"
r17.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r17.subs.append(("uni20B5", "uni20B5.rvrn"))
doc.addRule(r17)

r18 = RuleDescriptor()
r18.name = "diagonalbarO-stroke-wdth"
r18.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r18.subs.append(("diagonalbarO", "diagonalbarO.rvrn"))
doc.addRule(r18)

r19 = RuleDescriptor()
r19.name = "diagonalbarO-stroke-wght"
r19.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r19.subs.append(("diagonalbarO", "diagonalbarO.rvrn"))
doc.addRule(r19)

r20 = RuleDescriptor()
r20.name = "diagonalbaro-stroke-wdth"
r20.conditions.append(dict(name="wdth", minimum=25, maximum=85))
r20.subs.append(("diagonalbaro", "diagonalbaro.rvrn"))
doc.addRule(r20)

r21 = RuleDescriptor()
r21.name = "diagonalbaro-stroke-wght"
r21.conditions.append(dict(name="wght", minimum=600, maximum=1000))
r21.subs.append(("diagonalbaro", "diagonalbaro.rvrn"))
doc.addRule(r21)


doc.write(designSpace)

default = "RobotoFlex-Regular.ufo"
# load the default font
default_path = os.path.join(src_dir, default)
dflt = Font(default_path)

sources = [source.name for source in doc.sources]
# take the default out of the source list
sources.remove(default)

print ("Building masters...")

# load font objects
fonts = []
accentFonts = []
for fileName in sources:
	source_path = os.path.join(src_dir, fileName)
	master_path = os.path.join(master_dir, fileName)
	if os.path.exists(master_path):
		# use this updated instance
		font = Font(master_path)
	else:
		font = Font(source_path)
	if fileName not in ['RobotoFlex-opsz144.ufo', 'RobotoFlex-wght100.ufo', 'RobotoFlex-wght1000.ufo', 'RobotoFlex-wdth151.ufo', 'RobotoFlex-wdth25.ufo']:
	    accentFonts.append(font)
	fonts.append(font)
	
#buildGlyphSet(dflt, fonts)
allfonts = [dflt]+fonts
#buildComposites(composites, accentFonts)
setGlyphOrder(glyphOrder, allfonts)
clearAnchors(allfonts)
saveMasters(allfonts)

# build Variable Font

ufos = [font.path for font in allfonts]
project = FontProject()
project.run_from_ufos(
	ufos, 
	output=("ttf-interpolatable"), # FIXME this also build master_ttf and should not.
	remove_overlaps=False, 
	reverse_direction=False, 
	use_production_names=False)

#temp changed rel path to work in same dir, was:  ../fonts/RobotoFlex-VF.ttf
outfile = "RobotoFlex[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght].ttf"

#make folder if it doesn't exist
destFolder = "fonts"
if not os.path.exists(destFolder):
    os.makedirs(destFolder)
outfile = os.path.join(destFolder, outfile)



finder = lambda s: s.replace("master_ufo", "master_ttf").replace(".ufo", ".ttf")



varfont, _, _ = build(designSpace, finder)
print ("Saving Variable Font...")
varfont.save(outfile)

print ("Cleaning up...")

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)

# Remove temporary 1-drawings
if os.path.exists("sources/1-drawings"):
	shutil.rmtree("sources/1-drawings", ignore_errors=True)

print ("DONE!")

# SUBSET COMMAND
# pyftsubset RobotoFlex-VF.ttf --text-file=ascii-subset.txt --output-file=RobotoFlex-subset-VF.ttf
