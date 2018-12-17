# Demo of `quantum.py`

There are enough functions and definitions that describing every single one of them would get quite tedious. Since the names of the functions are mostly self-explanatory, or described in the code, we show here some interesting ways you can put them together.

## Using (abusing?) varargs to save keystrokes

```
>>> col(1,2,3,4)
array([[ 1.+0.j],
       [ 2.+0.j],
       [ 3.+0.j],
       [ 4.+0.j]])
>>> row(1,2,3,4)
array([[ 1.+0.j,  2.+0.j,  3.+0.j,  4.+0.j]])
>>> sq(1,2,3,4)
array([[ 1.+0.j,  2.+0.j],
       [ 3.+0.j,  4.+0.j]])
>>> sq(1,0,0,0, 0,0,1,0, 0,1,0,0, 0,0,0,1)
array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j]])
```

## Mixed states

See [Aaronson's lecture notes 6](https://scottaaronson.com/qclec/6.pdf).

Density matrices
```
>>> density(ket0)
array([[ 1.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j]])
>>> density(ketm)
array([[ 0.5+0.j, -0.5+0.j],
       [-0.5+0.j,  0.5+0.j]])
>>> density(keti)
array([[ 0.5+0.j ,  0.0-0.5j],
       [ 0.0+0.5j,  0.5+0.j ]])
```

Equal mixtures of orthogonal states are all maximally mixed
```
>>> (density(ket0) + density(ket1)) / 2
array([[ 0.5+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.5+0.j]])
>>> (density(ketp) + density(ketm)) / 2
array([[ 0.5+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.5+0.j]])
>>> (density(keti) + density(ketmi)) / 2
array([[ 0.5+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.5+0.j]])
```

## Partial trace / tracing out

Tracing out a state
```
>>> psi = col(0.3,0.1,0.3,0.9)
>>> rho = density(psi); rho
array([[ 0.09+0.j,  0.03+0.j,  0.09+0.j,  0.27+0.j],
       [ 0.03+0.j,  0.01+0.j,  0.03+0.j,  0.09+0.j],
       [ 0.09+0.j,  0.03+0.j,  0.09+0.j,  0.27+0.j],
       [ 0.27+0.j,  0.09+0.j,  0.27+0.j,  0.81+0.j]])
>>> traceout(rho, 2, -2)
array([[ 0.10+0.j,  0.18+0.j],
       [ 0.18+0.j,  0.90+0.j]])
>>> traceout(rho, -2, 2)
array([[ 0.18+0.j,  0.30+0.j],
       [ 0.30+0.j,  0.82+0.j]])
```
Note that the traced-out qubit is marked with a negative; one needs to pass in the number of dimensions because the tensor product "forgets" the dimensionality of the original spaces (ex. a 3x3 tensor-product with a 4x4 has the same shape as a 2x2 tensor-product a 6x6).

Tracing out the Bell pair
```
>>> density(bell)
array([[ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j]])
>>> traceout(density(bell), 2, -2)
array([[ 0.5+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.5+0.j]])
```

Tracing out multiple subsystems at once
```
>>> W
array([[ 0.00000000+0.j],
       [ 0.57735027+0.j],
       [ 0.57735027+0.j],
       [ 0.00000000+0.j],
       [ 0.57735027+0.j],
       [ 0.00000000+0.j],
       [ 0.00000000+0.j],
       [ 0.00000000+0.j]])
>>> traceout(density(W), 2, -2, -2)
array([[ 0.66666667+0.j,  0.00000000+0.j],
       [ 0.00000000+0.j,  0.33333333+0.j]])
```

## Running a circuit

With a pure state
```
>>> measure(run(tpow(ket0, 2), tprod(H, I), CNOT, tprod(I, T), CNOT, tprod(H, I)), tpow(basis01, 2))
array([[ 0.85355339],
       [ 0.        ],
       [ 0.14644661],
       [ 0.        ]])
```

With a mixed state
```
>>> init = tprod(density(ket0), (density(ket0) + density(ketp)) / 2)
>>> init
array([[ 0.75+0.j,  0.25+0.j,  0.00+0.j,  0.00+0.j],
       [ 0.25+0.j,  0.25+0.j,  0.00+0.j,  0.00+0.j],
       [ 0.00+0.j,  0.00+0.j,  0.00+0.j,  0.00+0.j],
       [ 0.00+0.j,  0.00+0.j,  0.00+0.j,  0.00+0.j]])
>>> dmeasure(drun(init, tprod(H, I), CNOT, tprod(I, T), CNOT, tprod(H, I)), tpow(basis01, 2))
array([[ 0.64016504],
       [ 0.21338835],
       [ 0.10983496],
       [ 0.03661165]])
```

## Circuit identities

```
>>> run(SWAP, CNOT, SWAP) # or just swCNOT
array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]])
>>> run(tpow(H, 2), CNOT, tpow(H, 2))
array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]])
```
also
```
>>> C(Z)
array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j]])
>>> run(tprod(I, H), CNOT, tprod(I, H))
array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j]])
```

## GHZ state

See [Aaronson's lecture notes 10](https://scottaaronson.com/qclec/10.pdf).

The GHZ state is entangled
```
>>> lw(120)
>>> density(ghz)
array([[ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j]])
```
but tracing over one of the qubits results in only classical correlation
```
>>> ptrace(density(ghz), 2, 2, -2) # trace over last qubit
array([[ 0.5+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.0+0.j],
       [ 0.0+0.j,  0.0+0.j,  0.0+0.j,  0.5+0.j]])
```
Exercise: try this with the W state

## CHSH game

See [Aaronson's lecture notes 14](https://scottaaronson.com/qclec/14.pdf).

Set up Alice and Bob's bases:
```
>>> alice0 = basis01
>>> alice1 = basispm
>>> bob0 = dot(R(pi/8), basis01)
>>> bob1 = dot(R(-pi/8), basis01)
```

Measure their Bell pair
```
>>> measure(bell, tprod(alice0, bob0)) # ok: 00 or 11
array([[ 0.4267767],
       [ 0.0732233],
       [ 0.0732233],
       [ 0.4267767]])
>>> measure(bell, tprod(alice0, bob1)) # ok: 00 or 11
array([[ 0.4267767],
       [ 0.0732233],
       [ 0.0732233],
       [ 0.4267767]])
>>> measure(bell, tprod(alice1, bob0)) # ok: 00 or 11
array([[ 0.4267767],
       [ 0.0732233],
       [ 0.0732233],
       [ 0.4267767]])
>>> measure(bell, tprod(alice1, bob1)) # ok: 01 or 10
array([[ 0.0732233],
       [ 0.4267767],
       [ 0.4267767],
       [ 0.0732233]])
```

For each case, the sum of the "ok" probabilities is 0.85355339, which violates the Bell inequality (which says that the maximum winning probability is 0.75).

## GHZ game

Preshare this state
```
>>> ghzgs
array([[ 0.5+0.j],
       [ 0.0+0.j],
       [ 0.0+0.j],
       [-0.5+0.j],
       [ 0.0+0.j],
       [-0.5+0.j],
       [-0.5+0.j],
       [ 0.0+0.j]])
```

Measure it
```
>>> measure(ghzgs, tprod(basis01, basis01, basis01)) # okay: even parity
array([[ 0.25],
       [ 0.  ],
       [ 0.  ],
       [ 0.25],
       [ 0.  ],
       [ 0.25],
       [ 0.25],
       [ 0.  ]])
>>> measure(ghzgs, tprod(basis01, basispm, basispm)) # okay: odd parity
array([[ 0.  ],
       [ 0.25],
       [ 0.25],
       [ 0.  ],
       [ 0.25],
       [ 0.  ],
       [ 0.  ],
       [ 0.25]])
>>> measure(ghzgs, tprod(basispm, basis01, basispm)) # okay: odd parity
array([[ 0.  ],
       [ 0.25],
       [ 0.25],
       [ 0.  ],
       [ 0.25],
       [ 0.  ],
       [ 0.  ],
       [ 0.25]])
>>> measure(ghzgs, tprod(basispm, basispm, basis01)) # okay: odd parity
array([[ 0.  ],
       [ 0.25],
       [ 0.25],
       [ 0.  ],
       [ 0.25],
       [ 0.  ],
       [ 0.  ],
       [ 0.25]])
```

## Playing with the quantum Fourier transform

```
>>> suppon
Suppressing sci-notation for small values: ON
>>> s = vnormalize(col(1,0,0, 1,0,0, 1,0,0, 1,0,0))
>>> s
array([[ 0.5+0.j],
       [ 0.0+0.j],
       [ 0.0+0.j],
       [ 0.5+0.j],
       [ 0.0+0.j],
       [ 0.0+0.j],
       [ 0.5+0.j],
       [ 0.0+0.j],
       [ 0.0+0.j],
       [ 0.5+0.j],
       [ 0.0+0.j],
       [ 0.0+0.j]])
>>> run(s, QFT(12))
array([[ 0.57735027+0.j],
       [-0.00000000+0.j],
       [ 0.00000000+0.j],
       [ 0.00000000+0.j],
       [ 0.57735027-0.j],
       [ 0.00000000+0.j],
       [ 0.00000000+0.j],
       [-0.00000000+0.j],
       [ 0.57735027-0.j],
       [-0.00000000+0.j],
       [ 0.00000000-0.j],
       [ 0.00000000+0.j]])
```

## Deutsch-Jozsa

```
>>> O = Id(4) # constant function on 4 qubits
>>> measure(run(tpow(ket0, 4), tpow(H, 4), O, tpow(H, 4)), tpow(basis01, 4))
array([[ 1.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.]])
>>> np.random.seed(10)
>>> O = rand_bal(4) # balanced function on 4 qubits
>>> np.diag(O) # just print diagonal
array([-1.+0.j, -1.+0.j,  1.+0.j, -1.+0.j, -1.+0.j,  1.+0.j,  1.+0.j, -1.+0.j,
        1.+0.j,  1.+0.j,  1.+0.j, -1.+0.j, -1.+0.j, -1.+0.j,  1.+0.j,  1.+0.j])
>>> measure(run(tpow(ket0, 4), tpow(H, 4), O, tpow(H, 4)), tpow(basis01, 4))
array([[ 0.    ],
       [ 0.0625],
       [ 0.0625],
       [ 0.25  ],
       [ 0.    ],
       [ 0.0625],
       [ 0.0625],
       [ 0.    ],
       [ 0.0625],
       [ 0.    ],
       [ 0.    ],
       [ 0.0625],
       [ 0.0625],
       [ 0.    ],
       [ 0.25  ],
       [ 0.0625]])
```
Note that the all-zeros state has amplitude 1 for a constant function, and amplitude 0 for a balanced function.

Or just repeatedly run this one line and watch the different results:
```
measure(run(tpow(ket0, 4), tpow(H, 4), rand_bal(4), tpow(H, 4)), tpow(basis01, 4))
```

## Why I wrote `computer.py`

Applying a Hadamard onto qubit 3 (out of 0 to 4)
```
>>> s = tpow(ket0, 5)
>>> s1 = run(s, tprod(I, I, I, H, I))
>>> s2 = run(s, tprod(tpow(I, 3), H, I)) # alternate way
```
Not that bad, but what about...

Applying a CNOT from qubit 0 onto qubit 4 (out of 0 to 4)
```
>>> s = tprod(ketp, tpow(ket0, 4))
>>> s1 = run(s, tprod(I, I, I, SWAP), tprod(I, I, SWAP, I), tprod(I, SWAP, I, I), tprod(CNOT, I, I, I), tprod(I, SWAP, I, I), tprod(I, I, SWAP, I), tprod(I, I, I, SWAP))
```
