from pyNN.utility import get_script_args
import sys

if len(sys.argv) > 1 and sys.argv[1].lower() in ["nest", "neuron", "brian2"]:
    simulator = get_script_args(1)[0]  
else:
    simulator = "neuroml"

print("Importing pyNN.%s..." % simulator)
exec("import pyNN.%s as simulator" % simulator)

print("Imported!")
