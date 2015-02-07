## ABOUT
This small python package batch processes "Database for Spoken German"-specific xslt
stylesheets to transform the original dgd metadata to cmdi metadata.


## INSTALLATION

 Use ```python setupy.py install ``` to install the package.


## USAGE

**Note Feb 2015** For a more up-to-date How-to refer to the notebook or its html in doc.  


### CONFIGURATION
All important paths are set in the local config.xml. <CONFIG> is root element to the
following subelements:
<GLOBAL>, defining global resources like the XSLT processor.
<CORPUS>, which defines parameters for corpus-metadata
<EVENT>, which defines parameters for event-metadata of a corpus
<SPEAKER>, which defines paramters for speaker-metadata of a corpus

Each element uses the attributes "type" and "corpus"
*	"type" defines the type of resource that is refered to in the element
	each  metadata-specific element uses the type values "stylesheet", "indirectory", "prefix", "outdirectory" to
	define the type of reference denoted via the metadata-element. 
*	"corpus" defines the alias of the corpus refered to. The alias is the official one of the archive of spoken german.
	(e.g. "AD", "BB", "FOLK" etc.) 

### START
Once all parameters are set, just start the python script  
