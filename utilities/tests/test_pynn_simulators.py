from pyNN.utility import get_script_args

simulator = get_script_args(1)[0]
print("Importing pyNN.%s..." % simulator)
exec("import pyNN.%s as simulator" % simulator)

print("Imported!")

