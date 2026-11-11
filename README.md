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
