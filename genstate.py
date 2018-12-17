# Copyright (c) Andrew Li 2018
# https://github.com/andrew0x4c/cs378h-quantum
# Synthesizing a state from |00> using only 1-qubit gates and CNOT

from __future__ import print_function
# ! yes, I wrote this in Python 2
from quantum import *

expi = lambda x: np.exp(j*x)

PHASE = lambda x: np.diag([1, expi(x)])
P = PHASE

# ! checking the math of a particular case
t1 = np.arccos(r(1/10.0))
p1 = 0
p2 = np.arccos(3/5.0)
U = (4+3j)/(20*r2) * dot( sq( r(0.9), r(0.1), r(0.1), r(0.9) ), sq(5, -3-4j, -3-4j, 5) )

run(kets(0,0), tprod(R(t1), R(pi/4)), tprod(P(p1), P(p2)), CNOT, tprod(I, U))

def genstate(psi, can=False):
    cos_t1 = vnorm(psi[0:2])
    psi0 = psi[0:2] / cos_t1
    sin_t1 = vnorm(psi[2:4])
    psi1 = psi[2:4] / sin_t1
    t1 = np.arccos(cos_t1)[0][0].real
    inner = dot(bra(psi0), ket(psi1))
    # inner product is expi(p1) cos(p2)
    cos_p2 = cnorm(inner)
    p2 = np.arccos(cos_p2)[0][0].real
    expi_p1 = inner / cos_p2
    p1 = (sq(0) if close(expi_p1, 0) else np.log(expi_p1) / j)[0][0].real
    gate_t1 = R(t1)
    gate_p1 = P(p1)
    gate_p2 = P(p2)
    psi_mat = np.hstack([psi0, psi1])
    coeff = (1-expi(-2*p2)) / (2*r2*sin(p2)**2)
    other_mat = sq(1, -expi(p2), -expi(p2-p1), expi(-p1))
    gate_U = dot(psi_mat, coeff * other_mat)
    if can: gate_U = canon(gate_U)
    return gate_t1, gate_p1, gate_p2, gate_U

gate_t1, gate_p1, gate_p2, gate_U = genstate(col(0.3, 0.1, 0.3, 0.9))

run(kets(0,0), tprod(gate_t1, R(pi/4)), tprod(gate_p1, gate_p2), CNOT, tprod(I, gate_U))

# tested on complex states, and states with zeros
# compare U above and gate_U

def tgs(*args, **kwargs): # test genstate
    v = col(*args[0:4])
    can = kwargs.get("can", False)
    print("vec:")
    pclstr(v)
    print("norm:", vnorm(v))
    v = vnormalize(v)
    if can: v = canon(v)
    print("vec:")
    pclstr(v)
    gate_t1, gate_p1, gate_p2, gate_U = genstate(v, can=can)
    print("gate_t1:")
    pclstr(gate_t1)
    print("gate_p1:")
    pclstr(gate_p1)
    print("gate_p2:")
    pclstr(gate_p2)
    print("gate_U:")
    pclstr(gate_U)
    result = run(kets(0,0), tprod(gate_t1, R(pi/4)), tprod(gate_p1, gate_p2), CNOT, tprod(I, gate_U))
    if can: result = canon(result)
    print("result")
    pclstr(result)

# this seems to have issues when more than one entry is zero. but that's fine:
# X Y 0 0: apply |0> -> X|0> + Y|1> to qubit 1
# X 0 0 Y: apply |0> -> X|0> + Y|1> to qubit 1, then CNOT
# etc
# also seems like tgs(1, 1, 1, 1) fails due to some degeneracy?
