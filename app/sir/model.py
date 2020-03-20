import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pdb
import math

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt
  
def calculate(population=100000, I0=1, R0=0, contact_rate=0.2, recovery_rate=1./10, days=160, run_plot=False):
  t = np.linspace(0, days, days)
  N = population
  beta = contact_rate
  gamma = recovery_rate
  # Everyone else, S0, is susceptible to infection initially. (population - initial infected - initial recovered)
  S0 = N - I0 - R0
  # Initial conditions vector
  y0 = S0, I0, R0
  # Integrate the SIR equations over the time grid, t.
  ret = odeint(deriv, y0, t, args=(N, beta, gamma))
  S, I, R = ret.T
  ventilator_demand = [math.ceil(math.ceil(i) * .17) for i in I]
  response = {'t': t, 'S': S, 'I': I, 'R': R, 'V': ventilator_demand, 'N': N}
  if not run_plot:
    days = [math.floor(day) for day in t.tolist()]
    susceptible = [math.floor(s) for s in S.tolist()]
    infected = [math.floor(i) for i in I.tolist()]
    recovered = [math.floor(r) for r in R.tolist()]
    response = [{'day': d, 'ventilators_needed': v, 'susceptible': s, 'infected': i, 'recovered': r} for d, v, s, i, r in zip(days, ventilator_demand, susceptible, infected, recovered)]
    
  return response
    



def plot(t, S, I, R, V, N):
    # Plot the data on three separate curves for S(t), I(t) and R(t), and Ventilator Demand (V)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.plot(t, V, 'c', alpha=0.5, lw=2, label='Ventilator Demand')
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number')
    ax.set_ylim(0,N)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()