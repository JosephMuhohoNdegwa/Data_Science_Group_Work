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

## BIT 2118 - Scientific Computing

**Institution:** Mount Kenya University (MKU)

### Task 02: NumPy arrays and numerical computation

`Daily temperature summary.py` stores 24 hourly Celsius readings in a NumPy
array, calculates their mean, minimum, and maximum, and converts every
reading to Fahrenheit using $F=1.8C+32$.

For the supplied readings, the daily mean is **23.12 C**, the minimum is
**17.50 C**, and the maximum is **29.40 C**. Changing the first reading from
18.5 C to 20.5 C increases the mean by $2/24\approx0.08$ C; the minimum and
maximum remain unchanged. The script prints the first six Fahrenheit
readings as well.

Run the program with:

```bash
python "Daily temperature summary.py"
```

#### Task 02.1: Household electricity use

`Household electricity usage.py` analyzes 24 hourly household-consumption
readings in kWh. It uses `numpy.mean`, `numpy.min`, and `numpy.max` to
summarize the data, then multiplies the readings by 1000 to convert them to
Wh.

The verified results are an average of **1.08 kWh** per hour, a minimum of
**0.30 kWh**, and a maximum of **2.50 kWh**. The first six readings convert
to `[500, 400, 300, 300, 400, 600]` Wh. Higher readings may correspond to
periods when multiple appliances are in use.

Run it with:

```bash
python "Household electricity usage.py"
```

Both Task 02 programs require Python 3 and NumPy.

### Task 03: Mathematical functions and vectorization

`Latency vectorization benchmark.py` generates one million simulated
latencies between 5 and 250 ms, converts them to seconds, squares them, and
compares a Python loop with NumPy vectorized operations. On the current
machine, vectorization completed substantially faster; exact timings and
speed-up vary by machine and run. The fixed random seed makes the generated
data reproducible. Reducing the sample count to 100,000 generally reduces
the work and runtime for both methods.

Run the benchmark with:

```bash
python "Latency vectorization benchmark.py"
```

#### Task 03.1: Banking transaction processing

A related application is processing one million simulated transaction
amounts in Kenyan Shillings (KES), converting them to US Dollars using an
exchange rate of 130 KES per USD, and squaring the converted values. A
traditional Python loop and NumPy vectorization can perform the same
operations so their results and execution times can be compared. The
transaction example is described here as an application scenario; a
separate transaction-processing script is not currently included.

The Task 02 and Task 03 programs require NumPy. Install it with
`python -m pip install numpy`.

### Task O: Numerical integration

These programs demonstrate numerical integration to estimate accumulated
quantities from sampled data:

- `code/Task_16_numerical_integration.py` estimates electrical energy from
  smart-meter readings using the trapezoidal and Simpson's rules.
- `code/irrigation_water_volume.py` estimates water delivered by an
  irrigation pump from sampled flow-rate measurements.

The programs require Python 3, NumPy, and SciPy. Install the dependencies with:

```bash
python -m pip install numpy scipy
```

Run the programs with:

```bash
python code/Task_16_numerical_integration.py
python code/irrigation_water_volume.py
```

The examples support learning how numerical integration works, comparing the
trapezoidal and Simpson's rules, and investigating how input data affects
results in related real-world applications. The Task O report documents the
assumptions, input data, outputs, and interpretation; verify numerical
results by running the programs.

This repository is maintained individually for the BIT 2118 Scientific
Computing assignment. The code and documentation should reflect work
completed and verified by the student.

### Task E: Solution of systems of linear equations

Systems of linear equations determine unknown quantities from known
relationships. They can be written in matrix form as

$$
Ax=b,
$$

where $A$ is the coefficient matrix, $x$ contains the unknowns, and $b$
contains the known constants. The example in `Server system equations.py`
uses NumPy's `np.linalg.solve()` to find the Type A and Type B server
quantities from CPU and memory requirements.

In the original case, Type A requires 4 CPU units and 8 GB of memory, while
Type B requires 2 CPU units and 12 GB of memory. For requirements of 20 CPU
units and 72 GB of memory, the solution is 3 Type A and 4 Type B units. The
verification computes $Ax=[20,72]$, matching the specified resource totals.

Changing the CPU requirement to 24 while keeping memory at 72 gives 4.5 Type
A and 3 Type B units, with verification $Ax=[24,72]$. This is the exact
solution to the linear system, but it is fractional. The script treats the
unknowns as continuous values; if they represent physical servers that must
be whole, an integer or mixed-integer optimization model is needed.

The model assumes fixed and accurate resource requirements and linear
relationships between server quantities and resource usage. Run the example
with:

```bash
python "Server system equations.py"
```

The program requires NumPy, available through
`python -m pip install numpy`.

### Task 04: Floating-point arithmetic and numerical errors

These Python and NumPy examples demonstrate floating-point comparisons,
absolute and relative error, and numerical stability:

- `code/Task_04_numerical_errors.py` uses the original test values.
- `code/Task_04_numerical_errors_modified.py` uses modified mathematical
  values and test cases to explore their effect on numerical errors and
  calculation accuracy.

Run either program with:

```bash
python code/Task_04_numerical_errors.py
python code/Task_04_numerical_errors_modified.py
```

The examples require Python 3 and NumPy. Install NumPy with
`python -m pip install numpy`.

### Task 05: Matrix algebra and matrix operations

These NumPy examples demonstrate matrix multiplication, rotation, scaling,
combined transformations, determinants, and coordinate transformations:

- `code/Task_05_matrix_algebra.py` rotates a square by 45 degrees and applies
  horizontal and vertical scale factors of 2.0 and 1.5.
- `code/Task_05_matrix_algebra_modified.py` uses a 30-degree rotation and
  scale factors of 1.5 and 2.0 to show how changing matrix values affects
  the transformed coordinates.

Both programs combine the rotation and scaling matrices and apply the
transpose of the combined transformation to row-vector coordinates. They
also print the determinant. Run either example with:

```bash
python code/Task_05_matrix_algebra.py
python code/Task_05_matrix_algebra_modified.py
```

The examples require Python 3 and NumPy. Install NumPy with
`python -m pip install numpy`.

## DATA SCIENCE AND COMPUTING

### Tasks M and M1: Server response-time curve fitting

`Server response curve fitting.py` models the relationship between concurrent
users and server response time with a quadratic curve,
$y=ax^2+bx+c$. The script fits the coefficients to measured data, reports
the root-mean-square error, estimates response time at 500 users, and plots
the measurements with the fitted curve. The example illustrates how
increasing demand can be associated with progressively longer delays. The
fit and prediction depend on the input measurements and should not be
extrapolated beyond their range without caution.

### Tasks N and N1: GPS speed estimation

`GPS speed estimation.py` estimates speed from position samples using finite
differences: a forward difference at the first sample, central differences
at interior samples, and a backward difference at the last sample. The
printed estimates and graph show how the object's speed changes over time.
The same technique can be used with GPS measurements for vehicle monitoring,
including detecting acceleration or slowing; a production speed-limit alert
would additionally need an explicit threshold and suitable handling of
measurement noise.

### Tasks Q and Q1: RC circuit charging

`RC circuit charging.py` uses SciPy's `solve_ivp` to solve the capacitor
charging equation

$$
\frac{dV}{dt}=\frac{V_s-V}{RC}.
$$

It compares the numerical result with the exact RC charging curve, reports
the voltage at the end of the simulation and the maximum difference, and
plots both curves. The example demonstrates numerical integration for a
circuit model used in capacitor energy storage, voltage smoothing, and
timing applications.

### Tasks R and R1: Server allocation optimization

`Server allocation optimization.py` uses constrained optimization to
minimize server planning cost while meeting a minimum total capacity. It
reports a continuous allocation from SciPy's SLSQP solver and separately
searches for the least-cost feasible whole-server combination, since
physical servers cannot be purchased fractionally. This models a data-centre
planning trade-off between infrastructure cost and computing capacity.

### Tasks S and S1: Monte Carlo overload-risk simulation

`Server overload Monte Carlo.py` generates server-demand scenarios from a
normal distribution, estimates the probability that demand exceeds available
capacity, and plots the running probability as more simulations are included.
The fixed random seed makes the example reproducible. Monte Carlo simulation
can help estimate overload risk and inform capacity planning; its estimate
depends on the assumed demand distribution and parameters.
