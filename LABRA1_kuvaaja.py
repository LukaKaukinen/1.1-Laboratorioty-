import matplotlib.pyplot as plt
import numpy as np
import scienceplots
import sympy as sp
h0, v0, theta, g, t = sp.symbols("h0 v0 theta g t", real=True, positive=True)


plt.style.use(["science", "notebook", "grid"])

#MUODOSTA FUNKTIO x(THETA) 
y_eq = h0 + v0 * sp.sin(theta) * t - sp.Rational(1, 2) * g * t**2
x_eq = v0 * sp.cos(theta) * t
t_ratkaisut = sp.solve(y_eq, t)

t_oikea = t_ratkaisut[1]
x = v0 * sp.cos(theta) * t_oikea
x_diff = sp.diff(x, theta)
#x_diff = -v0*sp.sin(theta) * ((v0*sp.sin(theta) + sp.sqrt((v0**2)*(sp.sin(theta)+2*g*h0)**2))/g) + v0*sp.cos(theta) * (((v0*sp.cos(theta))/g) + ((2*(v0**2)*sp.sin(theta)*sp.cos(theta)) / (g*sp.sqrt((v0**2)*(sp.sin(theta)**2) + 2*g*h0))))
x_diff_lopullinen = x_diff.subs({
    v0: 2.868,
    g: 9.81,
    h0: 0.862
})
x_lopullinen = x.subs({
    v0: 2.868,
    g: 9.81,
    h0: 0.862
})

x_ratkaistu = sp.solve(x_diff_lopullinen, theta)

#x_diff_lopullinen on se mikä syötetään numpylle eri theta arvoille
x_np = sp.lambdify(theta, x_lopullinen, "numpy")

theta_asteet = np.linspace(0, 60, 200)
theta_radiaanit = np.deg2rad(theta_asteet)
x_arvot = x_np(theta_radiaanit)
plt.plot(theta_asteet, x_arvot, label="Teoreettinen", color="red")
plt.xlabel("Kulma radiaaneina")
plt.ylabel("Teoreettinen kantama")


#MITTAUSTULOSTEN PLOTTI
kulmat = [5, 20, 26, 30, 40]
keskiarvot = [1.55, 1.73, 1.73, 1.75, 1.68]
hajonta = [[1.54, 1.56], [1.72, 1.74], [1.7, 1.76], [1.74, 1.76], [1.66, 1.68]]


h_arr = np.array(hajonta)
keskiarvot_arr = np.array(keskiarvot)

yerr_lower = keskiarvot_arr - h_arr[:, 0]  
yerr_upper = h_arr[:, 1] - keskiarvot_arr  
yerr = [yerr_lower, yerr_upper]


plt.errorbar(
    kulmat, keskiarvot, yerr=yerr, fmt="o", capsize=4, color="black", elinewidth=1, label="Mitattu"
)

plt.xlabel("Kulma (astetta)")
plt.ylabel("Matka (m)")
plt.legend()
plt.title("Kuulan lentoetäisyys")
plt.show()