Directory to put simple scripts based on the pylcio bindings

Because of the total insanity of some of what the pyLCIO methods return they are wrapped up in utility functions given in pylciohelperfunctions module 

The scripts with names like pylcio-plot-masses.py and pylcio-plot-thetas.py do roughly what you'd expect

Note that when it starts up pylcio prints a message about loading root dictionaries to the stdout (not the stderr!) so anytime you pipe the stdout of a script that imports these modules you should do so through the tail command:

```bash
tail -n +2
```

Using tail like this will simply write it's stdin to its stdout starting from the second line
