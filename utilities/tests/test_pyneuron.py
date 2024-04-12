import neuron

print("PyNEURON Engine running...")

neuron.h("create soma")
neuron.h("access soma")
neuron.h("insert Kv2like")
neuron.h("forall psection()")

print("NEURON version is: %s" % neuron.sys.version)
