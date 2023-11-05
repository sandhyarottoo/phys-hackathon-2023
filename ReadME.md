# <strong>Pong-Inertial</strong>
## A simple yet unintuitive game
#### Ben Coull-Neveu, Franco Del-Balso, Piotre Jakuc, Sandhya Rottoo

It's just pong... but rotating. We know, pretty mind boggling.
What's different about this pong, you may ask. It turns out that on a (non-inertial) rotating body, there exist so-called fictitious forces at play.
These forces are fully describe, rather succinctly, by just a few straight-forward (okay, *maybe* not) equations. For our purposes, we don't need to consider the translational force in the non-inertial frame (unfortunately, since it indubitably the most intuitive one of the bunch). Centrifugal, coriolis and azimuthal can be described as follows: 

```math
\begin{align} \vec{F}_{fictitious} &= \vec{F}_{centrifugal} + \vec{F}_{coriolis} + \vec{F}_{azimuthal} \nonumber \\ &= -m\vec{\omega} \times (\vec{\omega} \times \vec{r}) - 2m\vec{\omega} \times \vec{v} - m\frac{d\vec{\omega}}{dt}\times \vec{r}. \nonumber  \end{align}
 ```
