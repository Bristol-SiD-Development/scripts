A scratch file for notes on the pylcio bindings:

Flavour tag info all seems to be in the "RefinedJets" collection. BTag and CTag may be accessed as following:


```python
collection = event.getCollection("RefinedJets")
idh = UTIL.PIDHandler(collection)
algo = pidh.getAlgorithmID( "lcfiplus" )
ibtag = pidh.getParameterIndex(algo, "BTag")
ictag = pidh.getParameterIndex(algo, "CTag")
for particle in collection:
    pid = pidh.getParticleID(particle, algo)
    print "    BTag = " + str(pid.getParameters()[ibtag])   + " CTag = " + str(pid.getParameters()[ictag])
```

For some reason it appears that the getMomentum() method of a reconstructed particle object returns around 160 floats rather than the three that are advertised. For this reason and others the "pylciohelperfunctions.py" module has been created to hide away some of the crazy.
