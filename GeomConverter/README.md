##GeomConverter

###GeomConverter.py
Geometry converter script using the AFS installation of geomConveter found at...
```
	/afs/cern.ch/eng/clic/software/GeomConverter/GeomConverter-2_4/target/GeomConverter-2.4-bin.jar
```
Contains function to convert all files ending in _compact.xml within folder. However, this will require some renaming of files. 

###GeomConverter2.py
Geometry converter again using the AFS installation. Usage...
```
	python GeomConverter2.py compact.xml -o outputDirectory
```
With any combination of the following tags...
- "-l", converts to .lcdd format used with SLIC.
- "-p", converts to .xml format used within slicPandora.
- "-r", converts to .heprep format.