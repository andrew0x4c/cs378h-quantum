# Copyright (c) Andrew Li 2018
# https://github.com/andrew0x4c/cs378h-quantum
# Useful shorthands for various quantum-related math

# ! This file is commented much more than when I was using it
from __future__ import print_function
# ! yes, I wrote this in Python 2

import numpy as np
la = np.linalg
r = np.sqrt
r2 = r(2)
r3 = r(3)
r5 = r(5)
r6 = r(6)
j = 1.0j

# ! "[vec]tor", "[col]umn" (vector), "[row]" (vector),
# ! "[c]omplex [mag]nitude ^ [2]", "[c]omplex [mag]nitude",
# ! "[c]omplex [norm]", "[dag]ger" (conjugate transpose),
# ! "[v]ector [norm]",
# ! "[g]lobal [phase]" (just pick the first nonzero),
# ! "[canon]icalize" (remove global phase),
# ! "[c]omplex [normalize]", "[v]ector [normalize]"
def vec(*args): return np.array(args, dtype=complex)
def col(*args): return vec(*args)[:,np.newaxis]
def row(*args): return vec(*args)[np.newaxis,:]
def cmag2(x): return (x * x.conjugate()).real
def cmag (x): return np.sqrt(cmag2(x))
cnorm = cmag
def dag(x): return x.T.conjugate()
def vnorm(x): return np.sqrt(dag(x).dot(x)).real
def gphase(x, r=True):
    if r: x = rtz(x)
    # added later, to avoid issues like gphase(col(-1.2e-9, 1.0))
    xf = x.flatten()
    ind = xf.nonzero()[0][0]
    return xf[ind] / cnorm(xf[ind])
def canonicalize(x): return x / gphase(x)
canon = canonicalize
def cnormalize(x): return x / cnorm(x)
def vnormalize(x): return x / vnorm(x)

def close(x, y, tol=1e-6):
    if type(x) == np.ndarray or type(y) == np.ndarray:
        return (np.abs(x - y) < tol).all()
    else:
        return abs(x - y) < tol

def vstack(*args): return np.vstack(args)
def hstack(*args): return np.hstack(args)

# ! these are read as "ket zero", "ket one", "ket plus", "ket minus",
# ! "ket i", "ket minus i", and likewise for the bases and bras
ket0  = col(1, 0)
ket1  = col(0, 1)
ketp  = 1/r2 * ket0 + 1/r2 * ket1
ketm  = 1/r2 * ket0 - 1/r2 * ket1
keti  = 1/r2 * ket0 + j/r2 * ket1
ketmi = 1/r2 * ket0 - j/r2 * ket1

basis01  = hstack(ket0, ket1 )
basispm  = hstack(ketp, ketm )
basisimi = hstack(keti, ketmi)
basis10  = hstack(ket1 , ket0)
basismp  = hstack(ketm , ketp)
basismii = hstack(ketmi, keti)

def bra(x):
    if x.shape[1] == 1: return dag(x)
    else: return x

def ket(x):
    if x.shape[0] == 1: return dag(x)
    else: return x

bra0  = bra(ket0)
bra1  = bra(ket1)
brap  = bra(ketp)
bram  = bra(ketm)
brai  = bra(keti)
brami = bra(ketmi)

def dot(*args):
    if len(args) == 1: return args[0]
    return np.linalg.multi_dot(args)
def run(*args):
    return dot(*reversed(args))
def inbasis(B, mat):
    #return dot(B, mat, dag(B))
    return dot(dag(B), mat)

def measure(state, B):
    return cnorm(run(state, dag(B))) ** 2

def mean(*args):
    return np.mean(args, axis=0)
avg = mean

pi = np.pi
cos = np.cos
sin = np.sin

# ! "[t]wo [b]y [t]wo", "[f]our [b]y [f]our", "[sq]uare"
def tbt(*args): return np.array(args, dtype=complex).reshape((2, 2))
def fbf(*args): return np.array(args, dtype=complex).reshape((4, 4))
def sq(*args):
    s = int(np.round(np.sqrt(len(args))))
    assert s ** 2 == len(args)
    return np.array(args, dtype=complex).reshape((s, s))

X = tbt(0, 1, 1, 0)
Y = tbt(0, -1j, 1j, 0)
Z = tbt(1, 0, 0, -1)
H = 1/r2 * tbt(1, 1, 1, -1)
def R(theta):
    return tbt(cos(theta), -sin(theta), sin(theta), cos(theta))
S = tbt(1, 0, 0, j)
T = tbt(1, 0, 0, (1+j)/r2)
I = tbt(1, 0, 0, 1)
NOT = X

# ! "[m]atrix [pow]er"
def mpow(mat, n):
    L, S = la.eig(mat)
    Sinv = la.inv(S)
    assert close(mat, dot(S, np.diag(L), Sinv)), "must be diagonalizable"
    return dot(S, np.diag(L ** n), la.inv(S))

# ! "(square) [r]oot of [NOT]"
rNOT = mpow(NOT, 0.5)

CNOT = fbf(
    1,0,0,0,
    0,1,0,0,
    0,0,0,1,
    0,0,1,0,
)
# ! "[c]ontrolled" (gate)
# later added more general form (was just 2x2 -> 4x4 before)
def C(gate):
    assert gate.shape[0] == gate.shape[1]
    n = gate.shape[0]
    return vstack(
        hstack(np.eye(n, dtype=complex), np.zeros((n, n), dtype=complex)),
        hstack(np.zeros((n, n), dtype=complex), gate),
    )
SWAP = fbf(
    1,0,0,0,
    0,0,1,0,
    0,1,0,0,
    0,0,0,1,
)
# ! "[sw]apped [CNOT]"
swCNOT = run(SWAP, CNOT, SWAP)
# ! "[sw]apped [c]ontrolled" (gate)
def swC(gate): return run(SWAP, C(gate), SWAP)

# ! "[Kron]ecker"
def kron(*args):
    args = list(args)
    x = args.pop(0)
    while args:
        x = np.kron(x, args.pop(0))
    return x

# ! "[t]ensor [prod]uct"
tprod = kron

# example:
# nbasis(tprod(basispm, basispm), C(NOT))

def rtz(x, tol=1e-6):
    x = np.array(x)
    x[np.abs(x) < tol] = 0
    return x
# helpful for when you have col(2e-16, -1) and whatis fails

def whatis(x):
    x = rtz(x)
    was_bra = x.shape[0] == 1
    x = ket(x)
    gp = gphase(x)
    can = canon(x)
    arr = [
        (ket0, "0"), (ket1, "1"),
        (ketp, "+"), (ketm, "-"),
        (keti, "i"), (ketmi, "-i"),
    ]
    for state, name in arr:
        if close(can, state): break
    else:
        return "idk."
    if was_bra: name = "<{}|".format(name)
    else:       name = "|{}>".format(name)
    return "{} * {}".format(gp, name)

class Caller:
    def __init__(self, cb, msg=""): self.cb = cb; self.msg = msg
    def __repr__(self): self.cb(); return self.msg

def lw(n): np.set_printoptions(linewidth=n)
suppon  = Caller(lambda: np.set_printoptions(suppress=True ),
    "Suppressing sci-notation for small values: ON")
suppoff = Caller(lambda: np.set_printoptions(suppress=False),
    "Suppressing sci-notation for small values: OFF")

# note that these were not all added in order
# (for example, I added the (d)measure functions later)

def density(x):
    return ket(x).dot(bra(x))

def densityrun(*args):
    dens = args[0]
    mats = args[1:]
    dotmats = run(*mats)
    # we use inv instead of dag just in case the matrices
    # we want to dot aren't unitary for some reason
    invmats = la.inv(dotmats)
    return dot(dotmats, dens, invmats)

drun = densityrun

def densitymeasure(state, B):
    return col(*np.diag(densityrun(state, dag(B)))).real

dmeasure = densitymeasure

def densityinbasis(B, mat):
    return dot(dag(B), mat, B)

dinbasis = densityinbasis

def color(p, tol=1e-6):
    angle = np.angle(p)
    mag = np.abs(p)
    if mag <= tol:
        x, y = (3, 3)
    elif mag < 0.5 + tol:
        num = int(np.round(angle / (2 * np.pi) * 8) % 8)
        x, y = [
            (4, 4), (4, 3),
            (4, 2), (3, 2),
            (2, 2), (2, 3),
            (2, 4), (3, 4),
        ][num]
    else: #elif mag < 1.0 + tol:
        num = int(np.round(angle / (2 * np.pi) * 16) % 16)
        x, y = [
            (5, 5), (5, 4), (5, 3), (5, 2),
            (5, 1), (4, 1), (3, 1), (2, 1),
            (1, 1), (1, 2), (1, 3), (1, 4),
            (1, 5), (2, 5), (3, 5), (4, 5),
        ][num]
    return 36 * y + 6 * x + 1 * y + 16

def colormat(mat, sc=2):
    return "".join(
        ("".join("\x1b[48;5;{}m".format(color(val)) + "  "  * sc
            for val in row)
        + "\x1b[0m\n") * sc
        for row in mat)

# TODO: this does make colors, but is hard to understand
# consider having brightness be magnitude

def product(xs):
    acc = 1
    for x in xs: acc *= x
    return acc

def traceout(mat, *args):
    is_traced = [x < 0 for x in args]
    old_dims = [abs(x) for x in args]
    axes = [abs(x) if x < 0 else 1 for x in args]
    new_dims = [1 if x < 0 else x for x in args]
    eyes = [np.eye(x, dtype=complex) for x in old_dims]
    inds = np.indices(axes).reshape((len(args), -1))
    new_size = product(new_dims)
    accum = np.zeros((new_size, new_size), dtype=complex)
    for p in inds.T:
        bookend = tprod(*[eye[:,ind:ind+1] if traced else eye
            for traced, ind, eye in zip(is_traced, p, eyes)])
        accum += dot(dag(bookend), mat, bookend)
    return accum

trace_out = traceout
partialtrace = traceout
partial_trace = traceout
ptrace = traceout

# useful for testing partial trace computations
bell = 1/r2 * col(1,0,0,1)
EPR = bell
epr = EPR

def kets(*args):
    return tprod(*[[ket0, ket1][int(arg)] for arg in args])
def bras(*args):
    return bra(kets(*args))
GHZ = 1/r2 * (kets(0,0,0) + kets(1,1,1))
ghz = GHZ
W = 1/r3 * (kets(0,0,1) + kets(0,1,0) + kets(1,0,0))
w = W

class Qutrit: pass

qt = Qutrit
qt.ket0 = col(1,0,0)
qt.ket1 = col(0,1,0)
qt.ket2 = col(0,0,1)
qt.bra0 = bra(qt.ket0)
qt.bra1 = bra(qt.ket1)
qt.bra2 = bra(qt.ket2)
qt.epr = 1/r3 * (tprod(qt.ket0, qt.ket0)
               + tprod(qt.ket1, qt.ket1)
               + tprod(qt.ket2, qt.ket2))
qt.EPR = qt.epr
qt.bell = qt.epr
def kets3(*args):
    return tprod(*[[qt.ket0, qt.ket1, qt.ket2][int(arg)] for arg in args])
def bras3(*args):
    return bra(kets3(*args))
qt.kets = staticmethod(kets3)
qt.bras = staticmethod(bras3)
qt.I = np.eye(3, dtype=complex)
qt.CSUM = hstack(
    qt.kets(0,0), qt.kets(0,1), qt.kets(0,2),
    qt.kets(1,1), qt.kets(1,2), qt.kets(1,0),
    qt.kets(2,2), qt.kets(2,0), qt.kets(2,1),
)
qt.SWAP = hstack(
    qt.kets(0,0), qt.kets(1,0), qt.kets(2,0),
    qt.kets(0,1), qt.kets(1,1), qt.kets(2,1),
    qt.kets(0,2), qt.kets(1,2), qt.kets(2,2),
)
qt.ROTR = hstack(qt.ket1, qt.ket2, qt.ket0)
qt.ROTL = hstack(qt.ket2, qt.ket0, qt.ket1)
qt.SWAP01 = hstack(qt.ket1, qt.ket0, qt.ket2)
qt.SWAP02 = hstack(qt.ket2, qt.ket1, qt.ket0)
qt.SWAP12 = hstack(qt.ket0, qt.ket2, qt.ket1)
qt.omega = np.exp(2 * j * pi/3)
qt.omega2 = qt.omega ** 2
qt.F = 1/r3 * sq(
    1, 1        , 1        ,
    1, qt.omega , qt.omega2,
    1, qt.omega2, qt.omega ,
)
qt.X = qt.ROTR
qt.Z = hstack(qt.ket0, qt.omega * qt.ket1, qt.omega2 * qt.ket2)

class MidStates: pass

ms = MidStates
ms.s0p = cos(pi/8) * ket0 + sin(pi/8) * ket1
ms.s1p = sin(pi/8) * ket0 + cos(pi/8) * ket1
ms.s0m = cos(pi/8) * ket0 - sin(pi/8) * ket1
ms.s1m = sin(pi/8) * ket0 - cos(pi/8) * ket1
# ! labelled by which two states it is between
# ! for example, "[s]tate between ket[0] and ket[p]"

log2 = np.log2

def entropy(*args):
    assert close(sum(args), 1.0)
    return -sum(x * log2(x) if x else 0.0 for x in args)

def gghz(n):
    # generalized GHZ
    return (kets(*([0] * n)) + kets(*([1] * n))) / r2

def fgghz(n):
    # fake generalized GHZ
    return (density(kets(*([0] * n))) + density(kets(*([1] * n)))) / 2

# ! "[t]ensor [pow]er"
def tpow(mat, n):
    assert n >= 1
    curr = mat
    for x in range(n-1): curr = tprod(curr, mat)
    return curr

ghzgs = (kets(0,0,0) - kets(0,1,1) - kets(1,0,1) - kets(1,1,0)) / 2
# GHZ game state/strategy

# ! "[n]oisy [B]ell [p]air"
def nbp(e):
    dens_epr = density(epr)
    dens_mix = (density(kets(0,0)) + density(kets(1,1))) / 2
    return (1 - e) * dens_epr + e * dens_mix

def clstr(arr):
    # clean string
    import re
    arr = repr(arr)
    regex = r"([-+ ]?0\.0*(j|(?![0-9])))"
    return re.sub(regex, lambda m: " " * len(m.group(0)), arr)

def pclstr(arr): print(clstr(arr))

def QFT(d):
    arr = np.zeros((d, d), dtype=complex)
    for p in range(d):
        for q in range(d):
            arr[p][q] = 1/r(d) * np.exp(2*pi*j*p*q/d)
    return arr

# we need some bigger matrices
def diag(*arr): return np.array(np.diag(arr), dtype=complex)
def I_(n): return np.eye(n, dtype=complex)
# ! "[rand]om [bal]anced (phase oracle)"
def rand_bal(n):
    # there's actually no reason for this not to work for
    # any even n, but we usually look at functions from
    # {0, 1}^n -> {0, 1}
    s = 2 ** n
    nums = [-1] * (s/2) + [1] * (s/2)
    return diag(*np.random.permutation(nums))
# also, yes, the notation is a bit inconsistent.
# but I_n usually refers to the nxn matrix, while
# we also use n to count the qubits in a circuit.
def Id(n): return I_(2 ** n) # "(Id)entity" gate. happy?

