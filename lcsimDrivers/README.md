The driver may be compiled with the following series of commands (assuming you start in the lcsimDrivers directory and have access to AFS):

```bash
export CLASSPATH=$CLASSPATH:/afs/cern.ch/eng/clic/software/lcsim/lcsim-2_5/target/lcsim-2.5-bin.jar #change this if required
cd src
javac -d ../bin/ -classpath $CLASSPATH ./oliversDrivers/TrackSubdetectorHitNumbersDriver.java
cd ../bin
jar -cf ../lcsimDrivers.jar ./
```

You must then point lcsim at the driver in the steering.xml file as explained [here](https://confluence.slac.stanford.edu/display/ilc/lcsim+xml#lcsimxml-ClassPath)
