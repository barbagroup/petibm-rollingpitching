name: first
class: center, middle

# Pitching-rolling wing (Replication Study)

**Olivier Mesnard** (mesnardo@gwu.edu)

---

### Replication

.medium[

> *"Replicability is obtaining consistent results across studies aimed at answering the same scientific question, each of which has obtained its own data."*

]

NASEM, "Reproducibility and Replicability in Science" (doi: [10.17226/25303](https://doi.org/10.17226/25303))

<br>
![li_et_al_2016_header](./figures/li_dong_2016_header.png)

---

### Purpose of the replication study

.big[

The original study (Li & Dong, 2016) is not reproducible as the authors do not share their data, code, and computational workflow.

We intend to replicate the study in a reproducible way.

The authors are using a sharp-interface immersed boundary method (with a ghost-cell methodology).
Our software, PetIBM, is based on a diffuse-interface immersed boundary method.
One of our objectives is to understand how the treatment of the immersed boundary affects the numerical solution.

Li & Dong (2016) suggest that the pitching-rolling plates could serve as a better canonical model for investigating the hydrodynamics of bio-inspired flapping propulsion.

]

---

## PetIBM

.bigger[

* Open source, BSD 3-Clause, [GitHub](https://github.com/barbagroup/PetIBM)
* 2D/3D incompressible Navier-Stokes equations
* Projection method *a la* Perot (1993)
* Distributed-memory architectures (PETSc)
* Iterative solvers on distributed GPUs (AmgX, AmgXWrapper)
* Immersed Boundary Methods
  * IBPM (Taira and Colonius, 2007)
  * Decoupled IBPM (Li et al., 2016)

]

---

### Decoupled IBPM

<br>

`
$$
\begin{cases}
    \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} = -\nabla p + \frac{1}{Re} \nabla^2 \mathbf{u} + \int_{s}{\mathbf{f} \left( \mathbf{\xi} \left( \mathit{s}, \mathit{t} \right) \right) \delta_h \left( \mathbf{\xi} - \mathbf{x} \right)} d\mathit{s} \\
    \nabla \cdot \mathbf{u} = 0 \\
    \mathbf{u} \left( \mathbf{\xi} \left( \mathit{s}, t \right) \right) = \int_{\mathbf{x}}{\mathbf{u} \left( \mathbf{x} \right)} \delta_h \left( \mathbf{x} - \mathbf{\xi} \right) d\mathbf{x} = \mathbf{u}_B
\end{cases}
$$
`

<br>
Full discretization (space and time) to form an algebraic system:

`
$$
\begin{bmatrix}
    A & G & -H \\
    D & 0 & 0 \\
    E & 0 & 0
\end{bmatrix}
\begin{pmatrix}
    u^{n+1} \\
    \delta p \\
    \delta f
\end{pmatrix}
=
\begin{pmatrix}
    r^n \\
    0 \\
    u_B^{n+1}
\end{pmatrix}
+
\begin{pmatrix}
    {bc}_1 \\
    {bc}_2 \\
    0
\end{pmatrix}
$$
`

---

### Decoupled IBPM

Set $\gamma \equiv \begin{pmatrix} u^{n+1} \\ \delta f \end{pmatrix}$

and rewrite the system:

`
$$
\begin{bmatrix}
    \bar{A} & \bar{G} \\
    \bar{D} & 0
\end{bmatrix}
\begin{pmatrix}
    \gamma \\
    \delta p
\end{pmatrix}
=
\begin{pmatrix}
    \bar{r}_1 \\
    \bar{r}_2
\end{pmatrix}
$$
`

where

`
$$
\bar{A} \equiv \begin{bmatrix} A & -H \\ E & 0 \end{bmatrix} ;\;
\bar{G} \equiv \begin{bmatrix} G \\ 0 \end{bmatrix} ;\;
\bar{D} \equiv \begin{bmatrix} D & 0 \end{bmatrix}
$$
`

and

`
$$
\bar{r}_1 \equiv \begin{pmatrix} r_n + {bc}_1 \\ u_B^{n+1} \end{pmatrix} ;\;
\bar{r}_2 \equiv {bc}_2
$$
`

---

### Decoupled IBPM

**Idea:** Apply two successive block-LU factorizations to decouple the unknowns.

<br>
First block-LU decomposition:

`
$$
\begin{bmatrix}
    \bar{A} & \bar{G} \\
    \bar{D} & 0
\end{bmatrix}
\begin{pmatrix}
    \gamma \\
    \delta p
\end{pmatrix}
=
\begin{pmatrix}
    \bar{r}_1 \\
    \bar{r}_2
\end{pmatrix}
$$
`

<br>

`
$$
\begin{bmatrix}
    \bar{A} & 0 \\
    \bar{D} & -\bar{D}\bar{A}^{-1}\bar{G}
\end{bmatrix}
\begin{bmatrix}
    I & \bar{A}^{-1}\bar{G} \\
    0 & I
\end{bmatrix}
\begin{pmatrix}
    \gamma \\
    \delta p
\end{pmatrix}
=
\begin{bmatrix}
    \bar{A} & 0 \\
    \bar{D} & -\bar{D}\bar{A}^{-1}\bar{G}
\end{bmatrix}
\begin{pmatrix}
    \gamma^* \\
    \delta p
\end{pmatrix}
=
\begin{pmatrix}
    \bar{r}_1 \\
    \bar{r}_2
\end{pmatrix}
$$
`

<br>
to get the sequence:

`
$$
\begin{aligned}
    & \bar{A} \gamma^* = \bar{r}_1 \\
    & \bar{D}\bar{A}^{-1}\bar{G} \delta p = \bar{D} \gamma^* - \bar{r}_2 \\
    & \gamma = \gamma^* - \bar{A}^{-1}\bar{G} \delta p
\end{aligned}
$$
`

---

### Decoupled IBPM

<br>
Second block-LU decomposition:

`
$$
\bar{A}
\begin{pmatrix}
    u^* \\
    \delta f
\end{pmatrix}
=
\begin{bmatrix}
    A & -H \\
    E & 0
\end{bmatrix}
\begin{pmatrix}
    u^* \\
    \delta f
\end{pmatrix}
=
\begin{pmatrix}
    r^n + {bc}_1 \\
    u_B^{n+1}
\end{pmatrix}
$$
`

<br>

`
$$
\begin{bmatrix}
    A & 0 \\
    E & EA^{-1}H
\end{bmatrix}
\begin{bmatrix}
    I & -A^{-1}H \\
    0 & I
\end{bmatrix}
\begin{pmatrix}
    u^* \\
    \delta f
\end{pmatrix}
=
\begin{bmatrix}
    A & 0 \\
    E & EA^{-1}H
\end{bmatrix}
\begin{pmatrix}
    u^{**} \\
    \delta f
\end{pmatrix}
=
\begin{pmatrix}
    r^n + {bc}_1 \\
    u_B^{n+1}
\end{pmatrix}
$$
`

<br>
to get the sequence:

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^{**} \\
    & u^* = u^{**} + A^{-1}H \delta f
\end{aligned}
$$
`

---

### Decoupled IBPM

**Algo 1:**

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^{**} \\
    & u^* = u^{**} + A^{-1}H \delta f \\
    & DA^{-1}G \delta p = D u^* - {bc}_2 \\
    & u^{n+1} = u^* - A^{-1}G \delta p
\end{aligned}
$$
`

<br>
Sequence of operations:

1. Solve system for intermediate velocity.
2. Enforce the no-slip condition at the immersed boundary.
3. Solve a pressure Poisson system.
4. Project the velocity onto divergence-free space.

$\Rightarrow$ Constraints are satisfied sequentially, not simultaneously.

---

### Variants

**Algo 2** (solve an additional system for the velocity):

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^{**} \\
    & A u^* = A u^{**} + H \delta f \\
    & DA^{-1}G \delta p = D u^* - {bc}_2 \\
    & u^{n+1} = u^* - A^{-1}G \delta p
\end{aligned}
$$
`

<br>
**Algo 3** (group velocity and pressure together):

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & DA^{-1}G \delta p = D u^{**} - {bc}_2 \\
    & u^* = u^{**} - A^{-1}G \delta p \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^* \\
    & u^{n+1} = u^* + A^{-1}H \delta f
\end{aligned}
$$
`

---

### Force prediction scheme

Explicit terms in the RHS of the velocity system:

`
$$
r^n = \frac{1}{\Delta t} u^n - G \tilde{p} + \frac{3}{2} N\left( u^n \right) - \frac{1}{2} N\left( u^{n-1} \right) + \frac{1}{2 Re} L\left( u^n \right) + H \tilde{f}
$$
`

Different schemes to predict the forces $\tilde{f}$:

* set $\tilde{f} = 0$ (scheme 1)
* set $\tilde{f} = f^n$ (scheme 2)
* solve $EA^{-1}H \tilde{f} = u_B^{n+1} - E u^n$ (scheme 3)
* solve $EA^{-1}H \tilde{f} = u_B^{n+1} - E \tilde{u}$ (scheme 4)
  * with $\frac{\tilde{u} - u^n}{\Delta t} + N u^n = -G \tilde{p} + \frac{1}{Re} L u^n + {bc}_1$

---

### Pitching and rolling motion

.big[

* Rolling motion: `$\phi (t) = -A_\phi \cos \left( 2 \pi f t \right)$`
  * $\phi (t)$: instantaneous rolling position at time $t$
  * $A_\phi$: rolling amplitude
  * $f$: flapping frequency
* Pitching motion: `$\theta (t) = -A_\theta \cos \left( 2 \pi f t + \psi \right) + \theta_\text{bias}$`
  * $\theta (t)$: instantaneous pitching position at time $t$
  * $A_\theta$: pitching amplitude
  * $\psi$: phase difference angle between pitching and rolling ($\psi = 90^o$ for baseline case)
  * $\theta_\text{bias}$: static pitching bias (set to $0^o$ to get zero mean lift)

]

---

### Parameters

.medium[

* Reynolds number: $Re = U_\infty c / \nu$
  * $U_\infty$: incoming flow velocity
  * $c$: chord length
* Strouhal number: $St = 2 A_\phi R_\text{avg} f / U_\infty$
  * $R_\text{avg} = S / 2$: average rotational radius in the spanwise direction ($S$ is the span)

| $AR$ | $Re$ | $St$ | $A_\phi$ | $A_\theta$ | $\psi$ | $\theta_\text{bias}$ |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| $1.27$, $1.91$, $2.55$ | $100$, $200$, $400$ | $0.4$, $0.6$, $0.8$, $1.0$, $1.2$ | $45^o$ | $45^o$ | $60^o$, $70^o$, $80^o$, $90^o$, $100^o$, $110^o$, $120^o$ | $0^o$ |

Baseline case used for grid independence study:

$AR = 1.27$, $St = 0.6$, $Re = 200$, and $\psi = 90^o$

]

---

### Hydrodynamic performances

.big[

* Force coefficients

`
$$
C_{T, L, Z} = \frac{\left( T, L, Z \right)}{\frac{1}{2} \rho U_\infty^2 A_\text{plan}}
$$
`

$T$, $L$, $Z$: thrust, lift, and spanwise forces

$A_\text{plan} = \pi c S / 4$: planform area of the plate

* Power coefficient

`
$$
C_{PW} = \frac{P}{\frac{1}{2} \rho U_\infty^3 A_\text{plan}}
$$
`

$P$: hydrodynamic power defined as the surface integration of the inner product between the pressure and the velocity in each discretized element

]

---

### Propulsion efficiency

.medium[

`
$$
\eta = \frac{\bar{T} U_\infty}{\bar{P}}
$$
`

`$\bar{T}$`: cycle-averaged thrust

`$\bar{P}$`: cycle-averaged hydrodynamic power (in which only the positive power is considered)

]
