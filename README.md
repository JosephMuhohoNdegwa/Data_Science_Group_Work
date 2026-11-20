# Numerical Methods: Roots and Interpolation

This repository contains two small Python programs and explains how changing
their inputs changes their outputs.

## 1. `NUM K.py`: circle–parabola intersections

The program finds points that satisfy both equations:

$$
x^2+y^2=4, \qquad y=x^2-1.
$$

SciPy's root solver searches for zeros of the residuals

$$
F_1(x,y)=x^2+y^2-4, \qquad F_2(x,y)=y-x^2+1.
$$

### How the inputs affect the output

The prompts ask for initial values `x_guess` and `y_guess`, which together
form the starting point $(x_0,y_0)$ for the solver. These values guide the
search; they do not constrain the final answer. If the solver converges, the
reported coordinates make both residuals approximately zero.

There are two solutions, mirrored across the y-axis. A starting guess with
positive $x$ will usually converge to the right-hand solution, while a
negative starting guess will usually converge to the left-hand solution. A
poor starting point may fail to converge. The program reports the selected
point, residuals, and convergence status.

### Worked numerical example

Enter the initial guess $(x_0,y_0)=(1.5,1.3)$. At this starting point, the
residuals are

$$
F_1(1.5,1.3)=1.5^2+1.3^2-4=-0.06, \qquad
F_2(1.5,1.3)=1.3-1.5^2+1=0.05.
$$

SciPy's nonlinear root solver iteratively adjusts the coordinates until both
residuals are close to zero. It converges to approximately
$(1.517490,1.302776)$. Starting with a negative $x$ guess, such as
$(-1.5,1.3)$, will typically select the other intersection, approximately
$(-1.517490,1.302776)$.

Substitute $y=x^2-1$ into the circle equation and let $u=x^2$:

$$
u+(u-1)^2=4 \quad\Longrightarrow\quad u^2-u-3=0.
$$

The resulting intersections are

$$
x=\pm\sqrt{\frac{1+\sqrt{13}}{2}}, \qquad
y=\frac{\sqrt{13}-1}{2},
$$

or approximately $(1.51749,1.302776)$ and $(-1.51749,1.302776)$.

## 2. `NUM L.PY`: temperature interpolation

The program takes measurements $(h_i,T_i)$, where $h_i$ is an hour and $T_i$
is a temperature in Celsius, then estimates the temperature at a target hour
$t$.

### How the inputs affect the output

- **Number of measurements (`n`):** must be at least 3. More measurements
  give the cubic spline additional points that shape its curve.
- **Measurement hours (`hours`):** determine the horizontal locations of the
  data. Changing them changes interval widths and interpolation weights. The
  program sorts the hours automatically and requires them to be unique.
- **Temperatures (`temperature`):** determine the measured values. Changing
  one alters the linear estimate on its neighboring interval and can reshape
  the cubic spline across multiple intervals.
- **Target hour (`target_time`):** chooses where both curves are evaluated.
  Moving it changes the estimates along the curves; it must stay between the
  earliest and latest measured hours.
- **Displayed results:** the linear and cubic estimates are rounded to two
  decimal places. The plot shows the measurements and both curves.

### Linear estimate

For $h_i\le t\le h_{i+1}$, linear interpolation uses the two neighboring
measurements:

$$
L(t)=T_i+\frac{T_{i+1}-T_i}{h_{i+1}-h_i}(t-h_i).
$$

Equivalently, let

$$
\alpha=\frac{t-h_i}{h_{i+1}-h_i}; \qquad
L(t)=(1-\alpha)T_i+\alpha T_{i+1}.
$$

As $t$ moves from $h_i$ to $h_{i+1}$, $\alpha$ moves from 0 to 1 and the
estimate moves along a straight line from $T_i$ to $T_{i+1}$.

### Worked numerical example

Suppose the measurements are $(8,20.0)$, $(10,24.4)$, $(12,29.6)$, and
$(14,35.6)$, and the requested hour is $t=11.5$. The target lies between
hours 10 and 12, so the linear estimate uses $(10,24.4)$ and $(12,29.6)$:

$$
\alpha=\frac{11.5-10}{12-10}=0.75,
\qquad
L(11.5)=(1-0.75)(24.4)+0.75(29.6)=28.30\ ^\circ\mathrm{C}.
$$

These four measurements lie on the quadratic curve
$T(h)=0.1(h-8)^2+2(h-8)+20$. A cubic spline with SciPy's default
`not-a-knot` condition reproduces this quadratic for these data, so
$S(11.5)=28.225\ ^\circ\mathrm{C}$, displayed by the program as
**28.23 °C**. The linear estimate is **28.30 °C**.

### Cubic spline estimate

The cubic spline is a smooth piecewise-cubic function $S(t)$ that passes
through every measurement:

$$
S(h_i)=T_i \quad\text{for each measurement }i.
$$

Because its pieces are joined smoothly, changing a measurement can affect the
curve over several intervals. This program uses SciPy's default
`CubicSpline` boundary condition, `not-a-knot`.

## Input limits and running the programs

- Enter numeric values for all prompts.
- `NUM L.PY` needs at least three measurements with distinct hours, and its
  target hour must be inside the measured range.
- Hours are treated as ordinary numbers. For example, 23 and 1 are sorted
  numerically; the program does not interpret them as consecutive times
  across midnight.
- Install the dependencies with `python -m pip install numpy scipy matplotlib`.
- Run either program with `python "NUM K.py"` or `python "NUM L.PY"` and
  follow its prompts.

## Iterative methods for linear systems

`Iterative temperature methods.py` demonstrates Jacobi and Gauss-Seidel
iteration for the linear system

$$
AX=b,
$$

where $A$ is the coefficient matrix, $X$ is the vector of unknowns, and $b$
is the right-hand-side vector. Both methods start from an initial estimate
and stop when the largest change between successive estimates is less than
the selected tolerance:

$$
\left\lVert X^{(k+1)}-X^{(k)}\right\rVert_\infty < \varepsilon.
$$

The program also solves the selected system directly with
`numpy.linalg.solve` as a reference and plots the iteration changes on a
logarithmic vertical scale.

### Select a model

The program offers three systems:

1. **Original 5-point temperature model:** a five-variable tridiagonal
   system with 2 on the diagonal, -1 on adjacent diagonals, and
   $b=[100,0,0,0,20]$. It represents five interior temperatures influenced
   by boundary temperatures of 100 C and 20 C.
2. **Modified 3-point temperature model:** a three-variable tridiagonal
   system with 4 on the diagonal, -1 on adjacent diagonals, and
   $b=[100,50,20]$. The changed equations produce different temperature
   estimates and convergence behavior.
3. **General 3-variable linear system:**
   $$
   A=\begin{bmatrix}10&-2&1\\-1&8&-2\\2&-1&7\end{bmatrix},
   \qquad b=[30,20,10].
   $$
   This demonstrates that the methods also apply to systems unrelated to
   the temperature example.

Changing the model changes the equations, solution, and iteration behavior.

### Initial guesses and stopping controls

- **Initial guesses:** enter one comma-separated value for each unknown, or
  press Enter to start from zeros. The starting vector changes the sequence
  of estimates and may change how many iterations are needed.
- **Tolerance:** a smaller positive tolerance requires smaller changes
  between successive estimates and generally takes more iterations. The
  successive-change criterion is a stopping test; by itself it is not a
  guarantee of the same-sized error from the exact solution for every system.
- **Maximum iterations:** a positive limit on the number of steps. If neither
  method reaches the tolerance in time, the program reports that it did not
  converge within the limit. Increasing the limit allows more steps but does
  not ensure convergence.

The program rejects invalid model choices, guesses with the wrong number of
entries, nonnumeric guesses or controls, nonpositive tolerance or iteration
limits, and systems with a zero diagonal entry.

### How the methods update the estimates

Jacobi computes every component of the next estimate using only the previous
iteration:

$$
x_i^{(k+1)}=\frac{1}{a_{ii}}
\left(b_i-\sum_{j\ne i}a_{ij}x_j^{(k)}\right).
$$

Gauss-Seidel uses already-updated components from the current iteration and
the remaining components from the previous one:

$$
x_i^{(k+1)}=\frac{1}{a_{ii}}
\left(b_i-\sum_{j<i}a_{ij}x_j^{(k+1)}
-\sum_{j>i}a_{ij}x_j^{(k)}\right).
$$

For these models, Gauss-Seidel typically reaches the chosen tolerance in
fewer iterations. The graph shows the maximum component change at each step;
decreasing curves indicate that the estimates are stabilizing.

### Example results

With zero initial guesses, tolerance `1e-8`, and a maximum of 500 iterations,
the program produced these results:

| Model | Jacobi iterations | Gauss-Seidel iterations | Solution (approximately) |
| --- | ---: | ---: | --- |
| Original 5-point temperature | 150 | 75 | `[86.6667, 73.3333, 60.0000, 46.6667, 33.3333]` |
| Modified 3-point temperature | 22 | 12 | `[30.7143, 22.8571, 10.7143]` |
| General 3-variable system | 20 | 11 | `[3.54528, 3.15992, 0.86705]` |

These counts apply to the program's maximum-change stopping criterion and
the stated settings.

Run the program with:

```bash
python "Iterative temperature methods.py"
```

Install its dependencies with `python -m pip install numpy matplotlib`.

## Task P: Ordinary Differential Equations - Euler's Method

This example uses Euler's Method to approximate a fish population's growth
over 10 years. It models the population with the ordinary differential
equation

$$
\frac{dP}{dt}=rP,
$$

where $P$ is the population, $t$ is time in years, and $r$ is the growth
rate. The program starts with 100 fish, uses a constant growth rate of
0.2 per year, and takes one-year steps.

Euler's Method advances the current estimate using

$$
P_{n+1}=P_n+h f(t_n,P_n).
$$

For this model, $f(t,P)=rP$, so the update is

$$
P_{n+1}=P_n+h rP_n.
$$

With $P_0=100$, $r=0.2$, and $h=1$, the first step gives
$P_1=100+1(0.2\cdot100)=120$ fish.

### Program and expected output

The implementation is `fish_population_euler.py`. It prints the estimated
population for each year and plots population against time. The first
estimates are:

| Year | Estimated population |
| ---: | -------------------: |
| 0 | 100.00 |
| 1 | 120.00 |
| 2 | 144.00 |
| 3 | 172.80 |
| 4 | 207.36 |

Run it with:

```bash
python fish_population_euler.py
```

The program requires Python 3, NumPy, and Matplotlib. Install the project
dependencies with `python -m pip install numpy scipy matplotlib`.

### Changing the step size

In the program, change `h = 1.0` to `h = 0.5` to use half-year steps. A
smaller step generally improves Euler's approximation for this smooth growth
model, at the cost of more calculations. Compare the output using each step
size.

### Graph interpretation and assumptions

The graph places time on the horizontal axis and estimated population on the
vertical axis. The population rises, with larger yearly increases as the
estimated population grows, because the model makes the growth rate
proportional to the current population.

This simplified model assumes an initial population of 100, a constant
growth rate of 0.2 per year, unlimited food and space, and no effects from
disease, predators, or environmental changes. Population values are
mathematical estimates and may be fractional; real fish populations may
behave differently.

## Task 09: Eigenvalues and eigenvectors

`Student performance PCA.py` uses a covariance-matrix eigenanalysis to
identify the main pattern of variation in eight students' marks across four
subjects: Mathematics, Programming, Physics, and Statistics. Each row of the
input matrix is a student, and each column is a subject.

The program calculates each subject's mean, centers the marks by subtracting
those means, and computes the covariance matrix. It then finds and sorts the
covariance matrix's eigenvalues and eigenvectors. The eigenvector associated
with the largest eigenvalue gives the dominant direction of variation; the
eigenvalue indicates the amount of variation along that direction. The
program reports the dominant direction's percentage of total variance and
checks the eigenvalue equation

$$
Av=\lambda v,
$$

where $A$ is the covariance matrix, $v$ is the dominant eigenvector, and
$\lambda$ is its eigenvalue.

### Assumptions and input data

The example assumes the eight demonstration records are accurate numerical
marks on the same 0-to-100 scale, and that each subject is a separate
variable. The data are illustrative and are not actual university exam
records.

| Student | Mathematics | Programming | Physics | Statistics |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 80 | 85 | 75 | 82 |
| 2 | 70 | 75 | 65 | 72 |
| 3 | 90 | 95 | 85 | 92 |
| 4 | 60 | 65 | 55 | 62 |
| 5 | 85 | 88 | 80 | 86 |
| 6 | 75 | 78 | 70 | 76 |
| 7 | 95 | 98 | 90 | 96 |
| 8 | 65 | 68 | 60 | 66 |

### Results and interpretation

For these data, the mean marks are 77.50 in Mathematics, 81.50 in
Programming, 72.50 in Physics, and 79.00 in Statistics. The leading
eigenvalue is approximately 592.0989, and the leading component explains
about 99.87% of the total variation.

The dominant eigenvector has components with nearly equal magnitudes for all
four subjects. This indicates that they contribute similarly to the primary
pattern of variation in this particular dataset. Eigenvector signs are
arbitrary: reversing all signs describes the same principal direction.
The near-zero verification error confirms that the computed eigenpair
satisfies $Av=\lambda v$ to numerical precision.

Run the analysis with:

```bash
python "Student performance PCA.py"
```

The program requires NumPy, available through
`python -m pip install numpy`.
