# Notes for CS378H: Introduction to Quantum Information Science

Some code I wrote while taking the CS378H: Information to Quantum Information Science taught by [Scott Aaronson](https://scottaaronson.com), at UT Austin in Fall 2018.

If you've come here looking for homework solutions, you will not find any! All references to the homework have been removed, although I wrote the code generally enough that there weren't any solutions directly in the code itself.

These files are mostly intended to be run in the REPL like a calculator, using

    python -i quantum.py
    python -i computer.py

However, one could also use `from quantum import *` or `from computer import *` to use the files in a script.

I was also informed by a friend that (paraphrasing) this code looks like it was written by a physicist. Make of that what you will...

## `quantum.py`

For the first half of the course, which covered some of the building blocks of quantum computation (mathematical prerequisites, famous quantum phenomena, etc.), I used `quantum.py`. It contains shorthands for useful functions and values. For example, instead of typing

    1 / np.sqrt(2) * np.array([[1], [1]], dtype=complex)
    # PEP8: 52 chars
    1/np.sqrt(2)*np.array([[1],[1]],dtype=complex)
    # compressed: 46 chars

one can instead type

    1 / r2 * col(1, 1)
    # PEP8: 18 chars
    1/r2*col(1,1)
    # compressed: 13 chars

or in this case

    ketp
    # 4 chars

As another example, we can create a Bell pair using
```
>>> bp = run(tpow(ket0, 2), tprod(H, I), CNOT)
```
which creates the state `|00>`, applies a Hadamard gate to the first qubit, and CNOTs the first qubit onto the second qubit. We can measure it in various bases:
```
>>> measure(bp, tpow(basis01, 2)) # |00>, |01>, |10>, |11> basis
array([[ 0.5],
       [ 0. ],
       [ 0. ],
       [ 0.5]])
>>> measure(bp, tprod(basis01, basispm)) # |0+>, |0->, |1+>, |1-> basis
array([[ 0.25],
       [ 0.25],
       [ 0.25],
       [ 0.25]])
```
Or we can convert it into a density matrix and do a partial trace over the second qubit, or even test out the no-communication theorem by rotating it first:
```
>>> density(bp)
array([[ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j]])
>>> ptrace(density(bp), 2, -2)
array([[ 0.5+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.5+0.j]])
>>> ptrace(drun(density(bp), tprod(I, R(pi/8))), 2, -2)
array([[ 0.5+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.5+0.j]])
```

There are often several aliases, so you won't be embarrassed when you forget if the Bell/EPR pair was `bell`, `EPR`, or `epr`; it's all of them!

For a tour of the available features, see [demo_quantum.md](demo_quantum.md).

## `computer.py`

For the second half of the course, which covered quantum computation and algorithms, I used `computer.py`. It contains a simulation of a quantum computer, along with shorthands for common gates (including oracles) and some algorithms we covered.

For example, here we initialize a quantum computer with 4 qubits, Hadamard the first qubit, CNOT it into the second and third, and measure the third qubit.
```
>>> qc = QC(4)
>>> qc.g(H, 0)
>>> qc.g(CNOT, [0, 1])
>>> qc.g(CNOT, [0, 2])
>>> qc.fanz()
0000 (0.707106781187+0j)
1110 (0.707106781187+0j)
>>> qc.m(2)
(0.49999999999999989, 1)
>>> qc.fanz()
1110 (1+0j)
```

The core of the simulation is surprisingly short; only 40 to 60 lines (depending on how you count helper functions). Most of its power comes from NumPy's `einsum` routine; however, it does inherit some of `einsum`'s bugs ([NumPy issue 11938](https://github.com/numpy/numpy/issues/11938))...
```
>>> qc = QC(26)
>>> qc.g(H, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "computer.py", line 79, in gate
    self.data = np.einsum(self.data, inp_inds, gate, gate_inds, out_inds)
ValueError: invalid subscript '{' in einstein sum subscripts string, subscripts must be letters
```

For a tour of the available features, see [demo_computer.md](demo_computer.md).

## `gen_state.py`

While studying for the midterm, I saw an example problem where we were asked to synthesize a particular two-qubit (entangled) state starting from |00>. However, there was a catch: you can apply any one-qubit gate, but the only two-qubit gate that can be used is CNOT. I realized that if a similar problem came up I might not get a flash of insight quickly enough, so I derived a general form.

Given any two-qubit state `|psi> = a|00> + b|01> + c|10> + d|11>`, my method uses 6 gates with a total of 6 degrees of freedom (the minimum possible). The circuit is as follows:
```
|0> ---[  T1  ]---[ P1 ]---.----------
                           |           |psi>
|0> ---[R_pi/4]---[ P2 ]---@---[ U ]--
```
where T1 is a rotation gate, P1 and P2 are phase gates, and U is a general unitary, for a total of 1 + 1 + 1 + 3 = 6 real degrees of freedom. Of course, the R<sub>pi/4</sub> gate can be replaced by a Hadamard gate.

Roughly, the derivation goes as follows:
- First distribute the amplitudes between the sets `{|00>, |01>}` and `{|10>, |11>}` by the appropriate amount
- Rotate the four amplitudes in complex space such that when the CNOT swaps the amplitudes of `|10>` and `|11>`, it can be corrected by a single unitary on the second qubit
- The key is that unitaries preserve dot products, so we need the CNOT to set the dot product of the vectors [amplitude of `|00>` ; amplitude of `|01>`] and [amplitude of `|10>` ; amplitude of `|11>`] to be the same as that of the target state.

## Other notes

During the course, I found the [Quirk quantum simulator](https://algassert.com/quirk) very useful.

As I write this line, there are 22222 bytes of Python and 35636 bytes of Markdown; i.e. the documentation is more than 50% longer than the code. (Most of that is from demo_computer.md.)

The only differences from the versions I used are
- Added headers, `from quantum import *`, `from __future__ import print_function`
- Added comments of the form `# ! text here`
- Removed some comments about the homeworks
- Removed a few unused lines
- Ported print statements to Python 3 (using `print_function`)

