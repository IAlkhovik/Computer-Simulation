import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#yinit = [0.99, 0.01, 0] 
yinit = [0.99, 0.01, 0, 0] 
T = 0.8
K = 8
c = [T , K]
t = [n for n in range(0,100)]

def f(t, y ,c): 
    #dSdt = -c[0]*y[0]*y[1]
    dSdt = -c[0]*y[0]*y[1] - .05*y[0]
    dIdt = c[0]*y[0]*y[1] - y[1]/c[1] 
    dRdt = y[1]/c[1]
    dVdt = .05*y[0]
    #return dSdt, dIdt, dRdt
    return dSdt, dIdt, dRdt, dVdt

def infectLimit(t, y): 
    return y[1]-.0001 
infectLimit.terminate = True 
 
sol = solve_ivp(lambda t, y: f(t,y,c), [t[0], t[-1]], yinit, t_eval=t, events=(infectLimit))

print("The stopping condition occurs at: ")
print(sol.t_events[0])

plt.plot(sol.t, sol.y[0], label='Susceptible')
plt.plot(sol.t, sol.y[1], label='Infected')
plt.plot(sol.t, sol.y[2], label='Recovered')
plt.plot(sol.t, sol.y[3], label='Vaccinated')
plt.legend()
plt.xlabel('Days')
plt.grid(True)
plt.xlim([0, sol.t_events[0]])
plt.show()