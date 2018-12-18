# Demo of `computer.py`

Unlike in `quantum.py`, we can summarize all of the features here.


## Summary of features

Cheat sheet
```
             Long form                     | Short form
Creation:    qc = QC(subsystem_dims)       | qc = QC(num_qubits)
Gates:       qc.gate(g, ns)                | qc.g(g, ns)
             qc.multi_gate(g, ns)          | qc.mg(g, ns)
Measurement: qc.measure(n)                 | qc.m(n)
             qc.measure_as(n, k)           | qc.ma(n, k)
             qc.multi_measure(ns)          | qc.mm(ns)
             qc.multi_measure_as(ns, ks)   | qc.mma(ns, ks)
             qc.multi_measure_2(ns)        | qc.mm2(ns)
             qc.multi_measure_as_2(ns, ks) | qc.mma2(ns, ks)
Dump state:  qc.flat_amps()                | qc.fa()
             qc.flat_amps_nz()             | qc.fanz()
             qc.flat_probs()               | qc.fp()
             qc.flat_probs_nz()            | qc.fpnz()
Misc:        qc.equal_superposition(xs)    | qc.esp(xs)
```

### Create a QC

The constructor for a QC takes in either the number of qubits, or the dimensionality of each subsystem (if you want qutrits or something). All subsystems are initialized to `|0>`.

Examples:
- 8-qubit quantum computer: `qc = QC(8)`
- Qubit-qubit-qutrit system: `qc = QC([2, 2, 3])`

Be warned that the predefined gates only act on qubits; I almost never used non-qubit systems except when testing.

### Apply a gate

#### Single

To apply a gate `g` to subsystems `ns` on a QC object `qc`, run `qc.gate(g, ns)` or `qc.g(g, ns)`. If `ns` has length 1 it can be passed as an integer.

Examples:
- Hadamard qubit 0: `qc.gate(H, [0])` or `qc.g(H, 0)`
- CNOT qubit 0 onto qubit 1: `qc.gate(CNOT, [0, 1])` or `qc.g(CNOT, [0, 1])`
- 3-input controlled phase on qubits 2, 4, 5: `qc.gate(C(C(Z)), [2, 4, 5])` or `qc.g(C(C(Z)), [2, 4, 5])`

#### Multiple

To apply a gate `g` to multiple sets of subsystems `nss` on a QC object `qc`, run `qc.multi_gate(g, nss)` or `qc.mg(g, nss)`. If each set has length 1 they can be passed as a integers.

Examples:
- Hadamard qubits 0, 1, 2: `qc.multi_gate(H, [[0], [1], [2]])` or `qc.mg(H, [0, 1, 2])`
- CNOT qubit 0 onto qubit 1 and qubit 2 onto qubit 3: `qc.multi_gate(CNOT, [[0, 1], [2, 3]])` or `qc.mg(CNOT, [[0, 1], [2, 3]])`

`qc.mg` is very useful if you want to Hadamard all of your qubits; just use `qc.mg(H, range(n))`.

### Perform a measurement

#### Single

To measure subsystem `n` on a QC object `qc` randomly, run `qc.measure(n)` or `qc.m(n)`. The output is a pair containing the probability of the result, and the result itself.

To measure subsystem `n` on a QC object `qc` as a particular value `k`, run `qc.measure_as(n, k)` or `qc.ma(n, k)`. The output is the probability that an actual measurement would have resulted in `k`.

`qc.ma` is very useful if you want to test out cases of a protocol which conditions actions on the results of measurements, like quantum teleportation.

#### Multiple

To measure subsystems `ns` on a QC object `qc` randomly, run `qc.multi_measure(ns)` or `qc.mm(ns)`. This calls `qc.m` sequentially on each element of `ns`, and returns a list of pairs containing probabilities and values.

Alternatively, one can use `qc.multi_measure_2(ns)` or `qc.mm2(ns)`, which returns a pair containing the probability that the entire result occurred, along with the list of results.

To measure subsystems `ns` on a QC object `qc` as particular values `ks`, run `qc.multi_measure_as(ns, ks)` or `qc.mma(ns, ks)`. This calls `qc.ma` sequentially on each element of `ns` and `ks`, and returns a list of probabilities.

Alternatively, one can use `qc.multi_measure_as_2(ns, ks)` or `qc.mma2(ns, ks)`, which returns the probability that the entire result occurred.

### Viewing the internal state

#### Amplitudes

To print the amplitudes of the states of a QC object `qc`, run `qc.flat_amps()` or `qc.fa()`. To only show the nonzero amplitudes, run `qc.flat_amps_nz()` or `qc.fanz()`.

#### Probabilities

To print the probabilities of measuring the states of a QC object `qc` (if the entire state were measured now), run `qc.flat_probs()` or `qc.fp()`. To only show the nonzero probabilities, run `qc.flat_probs_nz()` or `qc.fpnz()`.

### Miscellaneous

#### Equal superposition

To set a QC object `qc` to an equal superposition of states `xs` (represented as lists), run `qc.equal_superposition(xs)` or `qc.esp(xs)`.

Examples:
- Create the state `1/sqrt(3) (|00> + |01> + |10>)`: `qc.esp([[0,0], [0,1], [1,0]])`


## Minus-Sign Test

See [Minus-Sign Test](https://www.scottaaronson.com/blog/?p=613).

Seems like the Hadamard gate just flips a coin:
```
>>> qc = QC(1); qc.g(H, 0)
>>> qc.fpnz()
0 0.5
1 0.5
>>> qc = QC(1); qc.g(NOT, 0); qc.g(H, 0)
>>> qc.fpnz()
0 0.5
1 0.5
```
The amplitudes tell the real story:
```
>>> qc = QC(1); qc.g(H, 0)
>>> qc.fanz()
0 (0.707106781187+0j)
1 (0.707106781187+0j)
>>> qc.g(H, 0)
>>> qc.fpnz()
0 1.0
>>> qc = QC(1); qc.g(NOT, 0); qc.g(H, 0)
>>> qc.fanz()
0 (0.707106781187+0j)
1 (-0.707106781187+0j)
>>> qc.g(H, 0)
>>> qc.fpnz()
1 1.0
```


## Quantum Zeno effect

See [Aaronson's lecture notes 4](https://scottaaronson.com/qclec/4.pdf).

We emulate measuring in different bases by rotating before and after measuring in the `{|0>, |1>}` basis.
```
>>> qc = QC(1)
>>> qc.fanz()
0 (1+0j)
>>> for x in range(1, 101):
...     qc.g(R(-pi/2 * x/100), 0)
...     qc.m(0)
...     qc.g(R(pi/2 * x/100), 0)
... 
(0.9997532801828658, 0)
(0.9997532801828658, 0)
(0.99975328018286558, 0)
(0.99975328018286602, 0)
(96 more lines)
>>> qc.fanz()
1 (1+0j)
```
The starting state is `|0>`, and with 100 measurements we "dragged" it to `|1>`.

Note that here the probability of every step succeeding is ~0.9997532801828658<sup>100</sup>, which is ~0.9756269141438807. In other words, we have a ~97% probability of success.

Exercises:
- Try different numbers of iterations.


## Watched pot effect

See [Aaronson's lecture notes 4](https://scottaaronson.com/qclec/4.pdf).

First, we look at the case without measurement.
```
>>> qc = QC(1)
>>> qc.fanz()
0 (1+0j)
>>> for x in range(1, 101):
...     qc.g(R(pi/2 * 1/100), 0)
... 
>>> qc.fanz()
1 (1+0j)
```
Now we measure at every step:
```
>>> qc = QC(1)
>>> qc.fanz()
0 (1+0j)
>>> for x in range(1, 101):
...     qc.g(R(pi/2 * 1/100), 0)
...     qc.m(0)
... 
(0.9997532801828658, 0)
(0.99975328018286558, 0)
(0.9997532801828658, 0)
(0.99975328018286558, 0)
(96 more lines)
>>> qc.fanz()
0 (1+0j)
```
A closer look at each step shows how measuring collapses the superposition into a basis state:
```
>>> qc.fanz()
0 (1+0j)
>>> qc.g(R(pi/2 * 1/100), 0)
>>> qc.fanz()
0 (0.999876632482+0j)
1 (0.0157073173118+0j)
>>> qc.m(0)
(0.9997532801828658, 0)
>>> qc.fanz()
0 (1+0j)
```

Exercises:
- Try different numbers of iterations.


## Elitzur-Vaidman bomb

See [Aaronson's lecture notes 4](https://scottaaronson.com/qclec/4.pdf).

Suitcase doesn't have bomb
```
>>> def suitcase(qc):
...     pass
... 
>>> qc = QC(1)
>>> for x in range(1, 101):
...     qc.g(R(pi/2 * 1/100), 0)
...     suitcase(qc)
... 
>>> qc.m(0)
(1.0000000000000009, 1)
```
We measured `|1>`, so there was no bomb.

Suitcase has bomb
```
>>> def suitcase(qc):
...     prob, val = qc.m(0)
...     if val == 1: assert False, "BOOM!"
... 
>>> qc = QC(1)
>>> for x in range(1, 101):
...     qc.g(R(pi/2 * 1/100), 0)
...     suitcase(qc)
... 
>>> qc.m(0)
(1.0, 0)
```
We measured `|0>`, so there was a bomb, but we didn't set it off!

Exercises:
- Try different numbers of iterations.


## Quantum teleportation

See [Aaronson's lecture notes 10](https://scottaaronson.com/qclec/10.pdf).

We will analyze each case separately, using the following setup for each case:
```
>>> qc = QC(3)
>>> qc.g(qbgate(0.6, -0.8, 0.8, 0.6), 0) # give Alice her state 0.6|0> + 0.8|1>
>>> qc.fanz()
000 (0.6+0j)
100 (0.8+0j)
>>> qc.g(H, 1) # create the Bell pair
>>> qc.g(CNOT, [1, 2])
>>> qc.fanz()
000 (0.424264068712+0j)
011 (0.424264068712+0j)
100 (0.565685424949+0j)
111 (0.565685424949+0j)
>>> qc.g(CNOT, [0, 1]) # perform quantum teleportation
>>> qc.g(H, 0)
>>> qc.fanz()
000 (0.3+0j)
001 (0.4+0j)
010 (0.4+0j)
011 (0.3+0j)
100 (0.3+0j)
101 (-0.4+0j)
110 (-0.4+0j)
111 (0.3+0j)
```
Now Alice has to measure her qubits.

Alice measures `|0>`, `|0>`:
```
>>> qc.mma2(range(2), [0, 0])
0.24999999999999992
>>> qc.fanz() # no correction is needed
000 (0.6+0j)
001 (0.8+0j)
>>> qc.fanz() # same as Alice's qubit
000 (0.6+0j)
001 (0.8+0j)
```
Alice measures `|0>`, `|1>`:
```
>>> qc.mma2(range(2), [0, 1])
0.24999999999999992
>>> qc.fanz() # need to apply X
010 (0.8+0j)
011 (0.6+0j)
>>> qc.g(X, 2)
>>> qc.fanz() # same as Alice's qubit
010 (0.6+0j)
011 (0.8+0j)
```
Alice measures `|1>`, `|0>`:
```
>>> qc.mma2(range(2), [1, 0])
0.24999999999999992
>>> qc.fanz() # need to apply Z
100 (0.6+0j)
101 (-0.8+0j)
>>> qc.g(Z, 2)
>>> qc.fanz() # same as Alice's qubit
100 (0.6+0j)
101 (0.8+0j)
```
Alice measures `|1>`, `|1>`:
```
>>> qc.mma2(range(2), [1, 1])
0.24999999999999992
>>> qc.fanz() # need to apply X and Z
110 (-0.8+0j)
111 (0.6+0j)
>>> qc.g(X, 2)
>>> qc.g(Z, 2)
>>> qc.fanz() # same as Alice's qubit
110 (0.6+0j)
111 (0.8+0j)
```

Exercises:
- Generalize this to arbitrary k-level quantum system (qutrits, ququarts, etc.), not just qubits
- Teleport an n-qubit entangled state (using n ebits of entanglement)


## Uncomputing

See [Aaronson's lecture notes 17](https://scottaaronson.com/qclec/17.pdf).

We wish to compute `(x0 xor x1) and x2` and store it in `x3`. Easy! Use CNOT to compute the XOR, and use Toffoli to compute the AND. We'll use some ancilla qubits for this.
```
>>> qc = QC(6)
>>> qc.mg(H, [0, 1, 2]) # example input
>>> qc.g(CNOT, [0, 4]) # CNOT x0 into x4
>>> qc.g(CNOT, [1, 4]) # CNOT x1 into x4, x4 has x0 xor x1
>>> qc.g(C(CNOT), [4, 2, 5]) # Toffoli x2 and x4 into x5, x5 has (x0 xor x1) and x2
>>> qc.g(CNOT, [5, 3]) # CNOT it into our answer register
>>> qc.fanz()
000000 (0.353553390593+0j)
001000 (0.353553390593+0j)
010010 (0.353553390593+0j)
011111 (0.353553390593+0j)
100010 (0.353553390593+0j)
101111 (0.353553390593+0j)
110000 (0.353553390593+0j)
111000 (0.353553390593+0j)
```
But wait! We have garbage in `x4` and `x5` that is entangled with our input and output, so we need to uncompute.
```
>>> qc = QC(6)
>>> qc.mg(H, [0, 1, 2]) # example input
>>> qc.g(CNOT, [0, 4]) # CNOT x0 into x4
>>> qc.g(CNOT, [1, 4]) # CNOT x1 into x4, x4 has x0 xor x1
>>> qc.g(C(CNOT), [4, 2, 5]) # Toffoli x2 and x4 into x5, x5 has (x0 xor x1) and x2
>>> qc.g(CNOT, [5, 3]) # CNOT it into our answer register
>>> qc.g(C(CNOT), [4, 2, 5]) # uncompute Toffoli
>>> qc.g(CNOT, [1, 4]) # uncompute CNOT
>>> qc.g(CNOT, [0, 4]) # uncompute CNOT
>>> qc.fanz()
000000 (0.353553390593+0j)
001000 (0.353553390593+0j)
010000 (0.353553390593+0j)
011100 (0.353553390593+0j)
100000 (0.353553390593+0j)
101100 (0.353553390593+0j)
110000 (0.353553390593+0j)
111000 (0.353553390593+0j)
```


## Deutsch's

See [Aaronson's lecture notes 17](https://scottaaronson.com/qclec/17.pdf).

For `00`:
```
>>> O = phase_oracle(0, 0)
>>> qc = QC(1)
>>> qc.g(H, 0)
>>> qc.g(O, 0)
>>> qc.g(H, 0)
>>> qc.m(0)
(0.99999999999999956, 0)
```
With probability 1 we measure 0, which is the parity of `00`.

For `01`:
```
>>> O = phase_oracle(0, 1)
>>> qc = QC(1)
>>> qc.g(H, 0)
>>> qc.g(O, 0)
>>> qc.g(H, 0)
>>> qc.m(0)
(0.99999999999999956, 1)
```
With probability 1 we measure 1, which is the parity of `01`.

For `10`:
```
>>> O = phase_oracle(1, 0)
>>> qc = QC(1)
>>> qc.g(H, 0)
>>> qc.g(O, 0)
>>> qc.g(H, 0)
>>> qc.m(0)
(0.99999999999999956, 1)
```
With probability 1 we measure 1, which is the parity of `10`.

For `11`:
```
>>> O = phase_oracle(1, 1)
>>> qc = QC(1)
>>> qc.g(H, 0)
>>> qc.g(O, 0)
>>> qc.g(H, 0)
>>> qc.m(0)
(0.99999999999999956, 0)
```
With probability 1 we measure 0, which is the parity of `11`.

It is useful to look at the amplitudes before and after the oracle, to actually see its effects:
```
>>> O = phase_oracle(0, 1)
>>> qc = QC(1)
>>> qc.g(H, 0)
>>> qc.fanz()
0 (0.707106781187+0j)
1 (0.707106781187+0j)
>>> qc.g(O, 0)
>>> qc.fanz()
0 (0.707106781187+0j)
1 (-0.707106781187+0j)
>>> qc.g(H, 0)
>>> qc.m(0)
(0.99999999999999956, 1)
```


## Deutsch-Josza

See [Aaronson's lecture notes 17](https://scottaaronson.com/qclec/17.pdf).

Constant function
```
>>> O = phase_oracle(0, 0, 0, 0, 0, 0, 0, 0)
>>> qc = QC(3)
>>> qc.mg(H, range(3))
>>> qc.g(O, range(3))
>>> qc.mg(H, range(3))
>>> qc.fanz()
000 (1+0j)
>>> qc.mm2(range(3))
(0.99999999999999911, [0, 0, 0])
```
We measured `|000>`, which means our function was constant.

Balanced function
```
>>> O = phase_oracle(0, 1, 1, 0, 0, 1, 0, 1)
>>> qc = QC(3)
>>> qc.mg(H, range(3))
>>> qc.g(O, range(3))
>>> qc.mg(H, range(3))
>>> qc.fanz()
001 (0.5+0j)
011 (0.5+0j)
101 (-0.5+0j)
111 (0.5+0j)
>>> qc.mm2(range(3))
(0.24999999999999972, [1, 0, 1])
```
We measured something other than `|000>` (specifically `|101>`), which means our function was balanced.


## Bernstein-Vazirani

See [Aaronson's lecture notes 18](https://scottaaronson.com/qclec/18.pdf).

Here we use `s = 001`.
```
>>> O = phase_oracle(0, 1, 0, 1, 0, 1, 0, 1)
>>> qc = QC(3)
>>> qc.mg(H, range(3))
>>> qc.g(O, range(3))
>>> qc.mg(H, range(3))
>>> qc.mm2(range(3))
(0.99999999999999911, [0, 0, 1])
```
With probability 1 we measured `|001>`, which is the value of the secret string s.

Here we use `s = 110`.
```
>>> O = phase_oracle(0, 0, 1, 1, 1, 1, 0, 0)
>>> qc = QC(3)
>>> qc.mg(H, range(3))
>>> qc.g(O, range(3))
>>> qc.mg(H, range(3))
>>> qc.mm2(range(3))
(0.99999999999999911, [1, 1, 0])
```
With probability 1 we measured `|110>`, which is the value of the secret string s.


## Simon's

See [Aaronson's lecture notes 18](https://scottaaronson.com/qclec/18.pdf).

Here we use "hidden XOR mask" `s = 101`.
```
>>> O = xor_oracle([0,1,0], [1,0,0], [0,0,1], [1,1,0],
...                [1,0,0], [0,1,0], [1,1,0], [0,0,1])
>>> qc = QC(6)
>>> qc.mg(H, range(3))
>>> qc.g(O, range(6)) # CNOT answer onto ancillas x3, x4, x5
>>> qc.mm2(range(3, 6)) # measure output (optional)
(0.24999999999999983, [1, 0, 0])
>>> qc.fanz() # if only we could measure twice...
001100 (0.707106781187+0j)
100100 (0.707106781187+0j)
>>> qc.mg(H, range(3))
>>> qc.fanz()
000100 (0.5+0j)
010100 (0.5+0j)
101100 (-0.5+0j)
111100 (-0.5+0j)
>>> qc.mm2(range(3))
(0.24999999999999994, [1, 1, 1])
```
We measured `|z_1> = |111>`, and indeed `s @ z_1 = 101 @ 111 = 0 (mod 2)`.

Note that at the last `fanz`, the only possible measurements `z` were those with `s @ z = 0 (mod 2)`. This is despite potentially measuring different results at the first `mm2`; the differing `|x>` and `|y>` only cause differing phases in the final state.

Another run of the same oracle might go like this:
```
>>> O = xor_oracle([0,1,0], [1,0,0], [0,0,1], [1,1,0],
...                [1,0,0], [0,1,0], [1,1,0], [0,0,1])
>>> qc = QC(6)
>>> qc.mg(H, range(3))
>>> qc.g(O, range(6)) # CNOT answer onto ancillas x3, x4, x5
>>> qc.mm2(range(3, 6)) # measure output (optional)
(0.24999999999999983, [0, 1, 0])
>>> qc.fanz() # if only we could measure twice...
000010 (0.707106781187+0j)
101010 (0.707106781187+0j)
>>> qc.mg(H, range(3))
>>> qc.fanz()
000010 (0.5+0j)
010010 (0.5+0j)
101010 (0.5+0j)
111010 (0.5+0j)
>>> qc.mm2(range(3))
(0.24999999999999994, [1, 0, 1])
```
We measured `|z_2> = |101>`, and indeed `s @ z_2 = 101 @ 101 = 0 (mod 2)`.

Now we actually have enough information to recover `s`. The unique nonzero vector `s` where `s @ z_1 = s @ z_2 = 0 (mod 2)` is `101`. In other words, we can find using row-reduction that the dimension of the null-space of the matrix [1, 1, 1; 1, 0, 1] over F<sub>2</sub> is 1, which has a unique nonzero element.

Exercises:
- Try not measuring the output register; by the no-communication theorem, this should produce the same result. What are the intermediate states?


## Shor's (period finding part)

See [Aaronson's lecture notes 19](https://scottaaronson.com/qclec/19.pdf), [Aaronson's lecture notes 20](https://scottaaronson.com/qclec/20.pdf), [Aaronson's lecture notes 21](https://scottaaronson.com/qclec/21.pdf).

Actually implementing the oracle for modular exponentiation would be quite tedious, so we just show how Shor's algorithm can be used to find the period of a function.

Note that the candidates for examples of factoring are given by [A046388](http://oeis.org/A046388). N = 15 is not interesting since all periods are powers of 2 (so the result of the QFT is exact). N = 21 is a homework question. N >= 33 requires Q >= 2048, which means there are >= 11 inputs and >= 6 outputs for the xor oracle, which requires storing an array with >= 2<sup>(11 + 6) * 2</sup> = 2<sup>34</suP> entries (since the code doesn't use a sparse representation of gates), which definitely does not fit into memory.

Take the period-10 function which returns the last digit of a number (i.e. x mod 10). We take Q = 128 which is the smallest power of 2 that is at least 10<sup>2</sup>. Thus our xor-oracle has 7 bits input and 4 bits output.

```
>>> Q = 128
>>> O = xor_oracle(*[bits(x % 10, 4) for x in range(Q)])
>>> qc = QC(11) # 7 input + 4 output
>>> qc.mg(H, range(7))
>>> qc.g(O, range(11))
>>> qc.fanz()
00000000000 (0.0883883476483+0j)
00000010001 (0.0883883476483+0j)
00000100010 (0.0883883476483+0j)
00000110011 (0.0883883476483+0j)
(120 more lines)
11111000100 (0.0883883476483+0j)
11111010101 (0.0883883476483+0j)
11111100110 (0.0883883476483+0j)
11111110111 (0.0883883476483+0j)
>>> qc.mm2(range(7, 11)) # optional
(0.093749999999999931, [1, 0, 0, 0])
>>> qc.fanz()
00010001000 (0.288675134595+0j)
00100101000 (0.288675134595+0j)
00111001000 (0.288675134595+0j)
01001101000 (0.288675134595+0j)
01100001000 (0.288675134595+0j)
01110101000 (0.288675134595+0j)
10001001000 (0.288675134595+0j)
10011101000 (0.288675134595+0j)
10110001000 (0.288675134595+0j)
11000101000 (0.288675134595+0j)
11011001000 (0.288675134595+0j)
11101101000 (0.288675134595+0j)
>>> qft(qc, range(7))
>>> qc.fpnz()
00000001000 0.09375
00000011000 0.000419699582214
00000101000 0.0004290569703
00000111000 0.000445572554672
00001001000 0.000470853740941
00001011000 0.000507715295514
00001101000 0.00056108940984
00001111000 0.000640042884518
00010001000 0.000762742757327
00010011000 0.00097073596191
00010101000 0.00138077311579
00010111000 0.00246216627673
00011001000 0.0085527807191
00011011000 0.0834633425134
00011101000 0.00113146176151
00011111000 9.37519676359e-05
00100011000 3.36806483126e-05
00100101000 0.000104116217955
00100111000 0.000201434384336
00101001000 0.000338400432909
00101011000 0.000550775957661
00101101000 0.000929969579309
00101111000 0.00176482837156
00110001000 0.00444559057601
00110011000 0.0290881445225
00110101000 0.0578409504445
00110111000 0.00396575322351
00111001000 0.00105463177371
(90 more lines)
11111001000 0.000470853740941
11111011000 0.000445572554672
11111101000 0.0004290569703
11111111000 0.000419699582214
>>> prob, val = qc.mm2(range(7)); prob; val
0.083463342513380681
[1, 0, 0, 1, 1, 0, 1]
>>> l = unbits(val); l
77
```
We leave quite a lot of the last `fpnz` to show the behavior of the peaks of the QFT.

Now that we have `l = kQ/s +/- epsilon`, we use the continued fraction approximation to recover `s`:
```
>>> l_over_Q = float(l) / Q; l_over_Q
0.6015625
>>> cf(l_over_Q)
[0, 1, 1, 1, 1, 25]
>>> cf_approx(cf(l_over_Q), 15)
(3, 5)
```
We choose the threshold of 15 as an example here; formally one would use the value of Q to determine when the approximation is good enough.

Thus we now know that the period `s` is a multiple of 5 (the denominator). After running the algorithm a few more times, we would have enough samples such that the LCM of the denominators is 10 with high probability.

Exercises:
- Run the example enough times to recover `s`.
- Define an modular exponentiation oracle for N = 15 or N = 21, and actually compute the factorization.
- Plot the probabilities of measuring states after the QFT.
- Try not measuring the output register; by the no-communication theorem, this should produce the same result. What are the intermediate states?


## Grover's

See [Aaronson's lecture notes 22](https://scottaaronson.com/qclec/22.pdf).

We'll do Grovers on an 8-item list with 1 marked item. If you wish to use `fanz`, note that the implementation of the Grover diffusion operator introduces a global phase of -1. The marked item will be `|101>`.
```
>>> O = phase_oracle(0,0,0,0, 0,1,0,0)
>>> qc = QC(3)
>>> qc.mg(H, range(3))
>>> qc.fpnz() # after 0 iterations
000 0.125
001 0.125
010 0.125
011 0.125
100 0.125
101 0.125
110 0.125
111 0.125
>>> qc.g(O, range(3))
>>> gd(qc, range(3))
>>> qc.fpnz() # after 1 iteration
000 0.03125
001 0.03125
010 0.03125
011 0.03125
100 0.03125
101 0.78125
110 0.03125
111 0.03125
>>> qc.g(O, range(3))
>>> gd(qc, range(3))
>>> qc.fpnz() # after 2 iterations
000 0.0078125
001 0.0078125
010 0.0078125
011 0.0078125
100 0.0078125
101 0.9453125
110 0.0078125
111 0.0078125
>>> qc.mm2(range(3))
(0.94531249999999722, [1, 0, 1])
```
We have found the marked item after 2 iterations of Grover's algorithm.

We can also demonstrate the souffle-like behavior where running Grover's for too long results in the success probability going down again.
```
>>> O = phase_oracle(0,0,0,0, 0,1,0,0)
>>> qc = QC(3)
>>> qc.mg(H, range(3)) # after 0 iterations
>>> qc.g(O, range(3)); gd(qc, range(3)) # after 1 iteration
>>> qc.g(O, range(3)); gd(qc, range(3)) # after 2 iterations
>>> qc.g(O, range(3)); gd(qc, range(3)) # after 3 iterations
>>> qc.fpnz()
000 0.095703125
001 0.095703125
010 0.095703125
011 0.095703125
100 0.095703125
101 0.330078125
110 0.095703125
111 0.095703125
>>> qc.g(O, range(3)); gd(qc, range(3)) # after 4 iterations
>>> qc.fpnz()
000 0.14111328125
001 0.14111328125
010 0.14111328125
011 0.14111328125
100 0.14111328125
101 0.01220703125
110 0.14111328125
111 0.14111328125
>>> qc.mm2(range(3))
(0.14111328124999936, [0, 1, 1])
```
We measured `|011>`, which is definitely not the marked item.

Exercises:
- Vary the length of the list, to get a feel for the O(sqrt(N)) runtime.
- Vary the number of marked items.
- Implement one of the applications of Grover's algorithm such as OR of ANDs.
