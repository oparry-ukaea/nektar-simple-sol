## Equivalence with Conservation Form of the Euler Equations 

In the below, units are chosen such that the specific ideal gas constant, R, is one and number densities rather than mass densities are used throughout.

$e$ is the specific internal energy and $g=\frac{2\gamma}{\gamma-1}$.

<!-- 
---
### Momentum Equation
$$
\begin{aligned}
    \frac{\partial }{\partial t} (n\boldsymbol{u}) + \nabla\cdot(n\boldsymbol{u}^2) + \nabla (nT) &= S^u, \\
\end{aligned}
$$
-->
---
### Energy Equation

$$
\begin{aligned}
    \frac{\partial }{\partial t} \left( (g-2)nT + n\vert\boldsymbol{u}\vert^2 \right) + \nabla\cdot(gn\boldsymbol{u}T + n\boldsymbol{u}^3) &= S^E\\
    \frac{\partial }{\partial t} \left( \frac{2nT}{\gamma-1} + n\vert\boldsymbol{u}\vert^2 \right) + \nabla\cdot(\frac{2\gamma}{\gamma-1}n\boldsymbol{u}T + n\boldsymbol{u}^3) &= S^E\\
    \frac{\partial }{\partial t} \left( \frac{nT}{\gamma-1} + \frac{n\vert\boldsymbol{u}\vert^2}{2} \right) + \nabla\cdot\left[\boldsymbol{u}\left(\frac{{\gamma}nT}{\gamma-1}+\frac{n\vert\boldsymbol{u}\vert^2}{2}\right)\right] &= \frac{S^E}{2}\\
   \frac{\partial E}{\partial t} + \nabla\cdot\left[\boldsymbol{u}\left(\frac{{\gamma}nT}{\gamma-1}+\frac{n\vert\boldsymbol{u}\vert^2}{2}\right)\right] &= \frac{S^E}{2}\\
   \frac{\partial E}{\partial t} + \nabla\cdot\left[\boldsymbol{u}\left(\frac{{(\gamma-1)}nT + nT}{\gamma-1}+\frac{n\vert\boldsymbol{u}\vert^2}{2}\right)\right] &= \frac{S^E}{2}\\
   \frac{\partial E}{\partial t} + \nabla\cdot\left[\boldsymbol{u}\left(nT+ne+\frac{n\vert\boldsymbol{u}\vert^2}{2}\right)\right] &= \frac{S^E}{2}\\
   \frac{\partial E}{\partial t} + \nabla\cdot\boldsymbol{u}(P+E) &= \frac{S^E}{2}\\
\end{aligned}
$$

(where $e$ is the specific internal energy.)

---
### Nektar solves:

$$
\begin{aligned}
    \frac{\partial \rho}{\partial t} + \frac{\partial {\rho}u}{\partial x} + \frac{\partial {\rho}v}{\partial y} &= S^n, \\
    \frac{\partial }{\partial t} ({\rho}u) + \frac{\partial (p+{\rho}u^2)}{\partial x} + \frac{\partial ({\rho}uv)}{\partial y} &= S^u, \\
    \frac{\partial }{\partial t} ({\rho}v) + \frac{\partial ({\rho}uv)}{\partial x} + \frac{\partial (p+{\rho}v^2)}{\partial y} &= S^v, \\
    \frac{\partial E}{\partial t} + \frac{\partial [u(E+P)]}{\partial x} + \frac{\partial [v(E+P)]}{\partial y}&= S^E .
\end{aligned}
$$

More details on Nektar's approach to solving the compressible Euler equations can be found in the [user guide](https://doc.nektar.info/userguide/latest/user-guidese38.html#x56-2540009.1.1).

---