# %% md
# # Thevenin's Theorem
# ## Let's draw the circuit first
# For that I will use schemdraw
# ### v1.0

# %% Draw
import schemdraw
schemdraw.use('svg')
elm=schemdraw.elements
d=schemdraw.Drawing(file='thevenin_ckt.svg')
d+=elm.Battery().reverse().up().label(('-','V','+'))
d+=elm.Resistor().right()
d+=elm.Resistor().down().hold()
d+=(R:=elm.Resistor()).right()
d+=elm.Resistor().down().label('$R_L$')
d+=elm.Line().left().tox(0)
d+=elm.Ground()
d.draw()

# %% md
# ## Now the simulation
# For this I will use PySpice

# %% import
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# %% setup
logger = Logging.setup_logging()

# %% circuit
rl=1@u_kOhm
circuit = Circuit("Thevenin's Theorem")
circuit.R('1', 'input', 1, 1@u_kOhm)
circuit.R('3', 1, 'load', 1.5@u_kOhm)
circuit.R('2', 1, circuit.gnd, 2@u_kOhm)
circuit.V('', 'input', circuit.gnd, 72@u_V)

# %% simulate
simulator = circuit.simulator()
analysis = simulator.operating_point()
vth=u_V(float(analysis.load))

# %% rth
circuit.R('L', 'load', circuit.gnd, rl)

# %% simulate
simulator = circuit.simulator()
analysis = simulator.operating_point()
vl=u_V(float(analysis.load))

# %% display
il=vl/rl
rth=vth/il-rl
print('Thevenin equivalent voltage is: {:.2f} V'.format(float(vth)))
print('Current flowing through load is: {:.2f} A'.format(float(il)))
print('Thevenin equivalent resistance is: {:.2f} Ohm'.format(float(rth)))
