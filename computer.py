# Copyright (c) Andrew Li 2018
# https://github.com/andrew0x4c/cs378h-quantum
# Simulation of a quantum computer

from __future__ import print_function, division
# ! yes, I wrote this in Python 2

import numpy as np

# shorthand from quantum.py

class Caller:
    def __init__(self, cb, msg=""): self.cb = cb; self.msg = msg
    def __repr__(self): self.cb(); return self.msg

def lw(n): np.set_printoptions(linewidth=n)
suppon  = Caller(lambda: np.set_printoptions(suppress=True ),
    "Suppressing sci-notation for small values: ON")
suppoff = Caller(lambda: np.set_printoptions(suppress=False),
    "Suppressing sci-notation for small values: OFF")

# helper methods

def set_ind(xs, i, x):
    xs = list(xs)
    xs[i] = x
    return xs

def lrange(*args, **kwargs): return list(range(*args, **kwargs))

def verify_gate(gate):
    dims = gate.shape
    ndims = len(dims)
    assert ndims % 2 == 0
    assert dims[:ndims//2] == dims[ndims//2:]

def show_complex(z):
    if not np.get_printoptions()["suppress"]: return str(z)
    return str((0.0 if abs(z.real) < 1e-6 else z.real)
      + 1.0j * (0.0 if abs(z.imag) < 1e-6 else z.imag))

# the actual quantum computer

class QC:
    def __init__(self, dims):
        try: dims = list(dims)
        except TypeError: dims = [2] * dims
        self.dims = dims
        self.ndims = len(self.dims)
        self.data = np.zeros(dims, dtype=complex)
        self.data[(0,) * len(dims)] = 1
    def probs(self):
        return np.abs(self.data) ** 2
    def measure_as(self, n, k, p=None):
        if p is None:
            pdf = np.einsum(self.probs(), lrange(self.ndims), [n])
            #sel = np.random.choice(self.dims[n], p=pdf)
            p = pdf[k]
        if p == 0: raise ValueError("invalid measurement")
        mask = np.zeros(set_ind([1] * self.ndims, n, self.dims[n]))
        mask[tuple(set_ind([0] * self.ndims, n, k))] = 1 / np.sqrt(p)
        self.data = self.data * mask
        return p
    def measure(self, n):
        pdf = np.einsum(self.probs(), lrange(self.ndims), [n])
        sel = np.random.choice(self.dims[n], p=pdf)
        p = pdf[sel]
        self.measure_as(n, sel, p=p)
        return (p, sel)
    def gate(self, gate, on):
        verify_gate(gate)
        inp_inds = lrange(self.ndims)
        out_inds = lrange(self.ndims)
        try: on = list(on)
        except TypeError: on = [on]
        gate_inds = on + lrange(self.ndims, self.ndims + len(gate.shape) // 2)
        for qnum, inum in enumerate(on):
            out_inds[inum] = self.ndims + qnum
        self.data = np.einsum(self.data, inp_inds, gate, gate_inds, out_inds)
    # methods after here are just for convenience
    def multi_measure_as(self, ns, ks):
        return [self.measure_as(n, k) for n, k in zip(ns, ks)]
    def multi_measure(self, ns):
        return [self.measure(n) for n in ns]
    def multi_gate(self, gate, ons):
        for on in ons: self.gate(gate, on)
    def multi_measure_as_2(self, ns, ks):
        mma = self.multi_measure_as(ns, ks)
        all_probs = 1.0
        for prob in mma: all_probs *= prob
        return all_probs
    def multi_measure_2(self, ns):
        mm = self.multi_measure(ns)
        all_probs = 1.0
        all_vals = []
        for prob, val in mm:
            all_probs *= prob
            all_vals.append(val)
        return (all_probs, all_vals)
    def flat_probs(self, thresh=0.0):
        probs = self.probs()
        for inds in alltups(self.dims):
            prob = probs[inds]
            if prob < thresh: continue
            print("".join(str(x) for x in inds), prob)
    def flat_probs_nz(self): self.flat_probs(thresh=1e-8)
    def flat_amps(self, thresh=0.0):
        probs = self.probs()
        for inds in alltups(self.dims):
            prob = probs[inds]
            if prob < thresh: continue
            print("".join(str(x) for x in inds), end=" ")
            print(show_complex(self.data[inds]))
    def flat_amps_nz(self): self.flat_amps(thresh=1e-8)
    def equal_superposition(self, states):
        num = len(states)
        val = 1 / np.sqrt(num)
        self.data[:] = 0
        for state in states: self.data[tuple(state)] = val

# shorthand methods

QC.ma = QC.measure_as
QC.m = QC.measure
QC.g = QC.gate
QC.mma = QC.multi_measure_as
QC.mm = QC.multi_measure
QC.mg = QC.multi_gate
QC.mma2 = QC.multi_measure_as_2
QC.mm2 = QC.multi_measure_2
QC.fp = QC.flat_probs
QC.fpnz = QC.flat_probs_nz
QC.fa = QC.flat_amps
QC.fanz = QC.flat_amps_nz
QC.esp = QC.equal_superposition

# helpers for constructing gates

def logn(x, n):
    val = int(round(np.log(x) / np.log(n)))
    if n ** val != x: raise ValueError("invalid dimensions")
    return val

def qbgate(*args):
    # "qubit gate"
    # as opposed to a qutrit or ququart gate
    qubits = logn(len(args), 4)
    dims = (2,) * (qubits * 2)
    #gate = np.array(args, dtype=complex).reshape(dims)
    # tranpose since we usually see the last dimension as input
    gate = (np.array(args, dtype=complex)
        .reshape((2**qubits,)*2).T.reshape(dims))
    return gate

# more shorthands

r = np.sqrt
r2 = r(2)
r3 = r(3)
r5 = r(5)
r6 = r(6)
j = 1.0j
pi = np.pi
cos = np.cos
sin = np.sin
def expi(x): return np.exp(j * x)
def exp2pii(x): return np.exp(2 * pi * j * x)

X = qbgate(0, 1, 1, 0)
Y = qbgate(0, -1j, 1j, 0)
Z = qbgate(1, 0, 0, -1)
H = 1/r2 * qbgate(1, 1, 1, -1)
def R(theta): return qbgate(cos(theta), -sin(theta), sin(theta), cos(theta))
def P(theta): return qbgate(1, 0, 0, expi(theta))
S = qbgate(1, 0, 0, j)
T = qbgate(1, 0, 0, (1+j)/r2)
I = qbgate(1, 0, 0, 1)
NOT = X

SWAP = qbgate(
    1,0,0,0,
    0,0,1,0,
    0,1,0,0,
    0,0,0,1,
)
CNOT = qbgate(
    1,0,0,0,
    0,1,0,0,
    0,0,0,1,
    0,0,1,0,
)

def alltups(dims):
    all_inds = np.indices(dims).reshape((len(dims), -1)).T
    for inds in all_inds: yield tuple(inds)

def bintups(n):
    for inds in alltups((2,) * n): yield inds

def identity(dims):
    try: dims = tuple(dims)
    except TypeError: dims = (2,) * dims
    arr = np.zeros(dims * 2, dtype=complex)
    for inds in alltups(dims):
        arr[inds * 2] = 1
    return arr

def C(gate):
    verify_gate(gate)
    dims = gate.shape[:len(gate.shape)//2]
    arr = np.zeros(((2,) + dims) * 2, dtype=complex)
    dim_ranges = tuple(slice(dim) for dim in dims)
    arr[((0,) + dim_ranges) * 2] = identity(dims)
    arr[((1,) + dim_ranges) * 2] = gate
    return arr

def phase_oracle(*args):
    qubits = logn(len(args), 2)
    arr = np.zeros((2,) * (qubits * 2), dtype=complex)
    for inds, arg in zip(bintups(qubits), args):
        arr[inds * 2] = 1 - 2 * arg
    return arr

def xor_tups(xs, ys): return tuple(x ^ y for x, y in zip(xs, ys))

def xor_oracle(*args):
    # ex. [0, 0], [0, 1], [0, 0], [1, 0]
    qubits = logn(len(args), 2)
    outs = len(args[0])
    arr = np.zeros((2,) * ((qubits + outs) * 2), dtype=complex)
    for in_inds, arg in zip(bintups(qubits), args):
        for out_inds in bintups(outs):
            arr[in_inds + out_inds + in_inds + xor_tups(out_inds, arg)] = 1
    return arr

def bits(x, n):
    return [(x >> i) & 1 for i in range(n)][::-1]

def unbits(xs):
    accum = 0
    for x in xs: accum = accum * 2 + x
    return accum

def qft(qc, qubits):
    for i, x in enumerate(qubits):
        qc.gate(H, x)
        for j, y in enumerate(qubits[i+1:]):
            qc.gate(C(P(2*pi/2**(j+2))), [y, x])
    for i in range(len(qubits) // 2):
        qc.gate(SWAP, [qubits[i], qubits[~i]])

def cf(x, num=100):
    result = []
    for i in range(num):
        k = int(x)
        result.append(k)
        x -= k
        if x <= 1e-9: # oops, exact rational
            if len(result) >= 2 and result[-1] == 1:
                result.pop(-1)
                result[-1] += 1
            break
        x = 1.0 / x
    return result

def cf_approx(xs, thresh=50):
    for i, x in enumerate(xs):
        if x > thresh: break
    else: i = len(xs)
    a, b = (1, 0)
    for x in xs[i-1::-1]:
        a, b = b + x * a, a
    return a, b

def diffusion(qc, qubits):
    qc.mg(H, qubits)
    qc.mg(X, qubits)
    gate = Z
    for i in range(len(qubits) - 1): gate = C(gate)
    # don't want to mess with ancillas
    qc.g(gate, qubits)
    qc.mg(X, qubits)
    qc.mg(H, qubits)

gd = diffusion # grover diffusion
