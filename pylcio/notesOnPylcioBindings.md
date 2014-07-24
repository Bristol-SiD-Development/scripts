A scratch file for notes on the pylcio bindings:

Flavour tag info all seems to be in the "RefinedJets" collection. BTag and CTag may be accessed as following:


```python
    collection = event.getCollection("RefinedJets")
    pidh = UTIL.PIDHandler(collection)
    algo = pidh.getAlgorithmID( "lcfiplus" )
    ibtag = pidh.getParameterIndex(algo, "BTag")
    ictag = pidh.getParameterIndex(algo, "CTag")
    for particle in collection:
        pid = pidh.getParticleID(particle, algo)
        print "    BTag = " + str(pid.getParameters()[ibtag])   + " CTag = " + str(pid.getParameters()[ictag])
```
