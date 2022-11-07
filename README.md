## A Simple Scrape-off Layer Solver
### Background
This solver models plasma transport in the scrape-off layer (SOL).
It can run with either a 1D or 2D mesh, but in both cases, the SOL is effectively treated as a 1D flux tube, with mass being added continously near the centre of the domain and flowing out to a divertor at either end. Neutral species are ignored and the plasma is assumed to have an ideal-gas equation of state. For 2D meshes, the tube has a finite width but all of the dynamics of interest remain (by design) along the length of the tube, with periodic boundary conditions  applied along its sides.

The code in this repo extends a [1D-only implementation](https://github.com/ExCALIBUR-NEPTUNE/nektar-1d-sol) written by Dave Moxey.

---
### Equations

The starting point is a set of non-dimensionalised equations describing the evolution of SOL density, momentum and energy, which were derived for a 1D system in [1]:

$$
\begin{aligned}
    U_r \frac{\partial n}{\partial t} &= 
        - \frac{\partial }{\partial s}(nu)
        + S^n, \\
    U_r \frac{\partial }{\partial t} (nu)&= 
        - \frac{\partial }{\partial s} (nu^2)
        - \frac{\partial }{\partial s} (nT)
        + S^u, \\
    U_r \frac{\partial }{\partial t} \left( (g-2)nT + nu^2  \right) &= 
        - \frac{\partial }{\partial s}(gnuT + nu^3)
        + \kappa_d \frac{\partial^2  T}{\partial s^2}
        + S^E.
\end{aligned}
$$
$U_r$ controls the relative weight of the time-dependent terms, $\kappa_d$ is the heat diffusion/conductivity coefficient and $g$ is related to the ratio of specific heats, $\gamma$, by $g=\frac{2\gamma}{\gamma-1}$. Generalising to multiple spatial dimensions, then choosing $U_r=1$, ignoring conduction ($\kappa_d=0$) and moving all terms except sources to the LHS, we have:
$$
\begin{aligned}
    \frac{\partial n}{\partial t} + \nabla\cdot(n\boldsymbol{u}) &= S^n, \\
    \frac{\partial }{\partial t} (n\boldsymbol{u}) + \nabla\cdot(n\boldsymbol{u}^2) + \nabla (nT) &= S^u, \\
    \frac{\partial }{\partial t} \left( (g-2)nT + n\vert\boldsymbol{u}\vert^2 \right) + \nabla\cdot(gn\boldsymbol{u}T + n\boldsymbol{u}^3) &= S^E.
\end{aligned}
$$
Using the ideal gas law, [it can be shown](docs/eqns) that this system is exactly equivalent (modulo a factor of 2 in the energy equation) to the conservation form of the compressible Euler equations solved by Nektar++.

---

### References

[1] W. Arter. Study of source terms in the SOLF1D edge code. Tech. rep. CCFE-DETACHMENT-RP2-Draft. CCFE, 2015.

[2] W. Saunders and E. Threlfall. Finite Element Models: Performance. Tech. rep. CD/EXCALIBUR-FMS/0047-M2.2.2. https://github.com/ExCALIBUR-NEPTUNE/Documents/blob/main/reports/ukaea_reports/CD-EXCALIBUR-FMS0047-M2.2.2.pdf. UKAEA, 2021.