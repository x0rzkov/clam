###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Format classes --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#       
#       Licensed under GPLv3
#
###############################################################

from lxml import etree as ElementTree
from clam.common.metadata import CLAMMetaData, RawXMLProvenanceData
from StringIO import StringIO

def getmetadatafromxml(formats, file, node):
    """Read metadata from XML."""
    if not isinstance(node,ElementTree._Element):
        node = ElementTree.parse(StringIO(node)).getroot() 
    if node.tag == 'CLAMMetaData':
        format = node.attrib['format']
        
        formatclass = None
        for cls in dir():
            if isinstance(cls, CLAMMetaData) and cls.__name__ == format:
                formatclass = cls
        if not formatclass:
            raise Exception("Format class " + format + " not found!")
            
        data = {}
        for subnode in node:
            if subnode.tag == 'meta':
                key = subnode.attrib['id']
                value = subnode.text
                data[key] = value
            elif subnode.tag == 'provenance':
                data['provenance'] = RawXMLProvenanceData(subnode)
        return formatclass(file, **data)
    else:    
        raise Exception("Invalid CLAM Metadata!")


class ExampleFormat(CLAMMetaData):

    #A dictionary of attributes that this format can take, the keys correspond
    #to the attributes, the values can be either:
    # True   - Accept any value, this attribute is required
    # False  - Accept any value, but this attribute is not required
    # a list - Accept any of the specified values (if False is a member then this attribute is not required)
    # a specific value - Simply always assign this static value
    attributes = {'encoding':True, 'language':False, 'colour': ['green','red','blue'], 'pi':3.14 }
    
    #Do you want to allow any other custom attributes? Defined by the InputTemplate/OutputTemplate
    allowcustomattributes = True
    
    #Specify a mimetype for your format
    mimetype = "text/plain"
    
    
    #If your format is XML-based, specify a scheme:
    scheme = None
    
    #NOTE: Never override the constructor with different arguments!
    
    def validate(self):
        #Add your validation method here, should return True or False
        return True
        
    def loadinlinemetadata(self):
        #If there is metadata IN the actual file, this method should extract it and assign it to this object. Will be automatically called from constructor. Note that the file (CLAMFile) is accessible through self.file
        pass
        
    def saveinlinemetadata(self):
        #If there is metadata that should be IN the actual file, this method can store it. Note that the file (CLAMFile) is accessible through self.file
        pass
           

class PlainText(CLAMMetaData):
    attributes = {'encoding':True,'language':False }
    mimetype = "text/plain"
                
class TadpoleFormat(CLAMMetaData):    
    attributes = {'encoding':True,'language':False }    
    name = "Tadpole Columned Output Format"
    mimetype = 'text/plain'

class DCOIFormat(CLAMMetaData):    
    name = "DCOI format"
    mimetype = 'text/xml'
    scheme = '' #TODO


class KBXMLFormat(CLAMMetaData):
    name = "Koninklijke Bibliotheek XML-formaat"
    mimetype = 'text/xml'
    scheme = '' #TODO


