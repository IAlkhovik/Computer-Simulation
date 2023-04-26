#from upwind scheme demo (unedited)
class Domain1D:
    def __init__(self, step, min_val=-1, max_val=1):
        from numpy import linspace
        self.step = step
        n = int((max_val - min_val) / step) + 1
        self.vals = linspace(min_val, max_val, n)
        
    def __len__(self): # length in terms of # of grid points
        return len(self.vals)
    
    def __getitem__(self, I): # values by an arbitrary Numpy index-slice `I`
        return self.vals[I]

#from upwind scheme demo (unedited)   
def plot_grid(U, J=[0]
              , figsize=(12, 6.75), markersize=4, linewidth=1
              , title_str=None, axes=True
             ):
    assert isinstance(U, Solution1D)
    
    from matplotlib.pyplot import figure, gca, plot, legend, show
    fig = figure(figsize=figsize)
    ax = gca()

    for c, j in enumerate(J):
        ax.plot(U.X, U[j, 1:-1], 'o-', color=f'C{c}', label=f't={U.T[j]}'
                , markersize=markersize, linewidth=linewidth)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$\approx u(x,t)$', rotation=0, horizontalalignment='right')
    if title_str is not None:
        ax.set_title(title_str, loc='left')
    if axes:
        ax.axhline(0, color='grey', linewidth=0.5, linestyle='dashed')
        ax.axvline(0, color='grey', linewidth=0.5, linestyle='dashed')
    legend()
    show()

#from upwind scheme demo (unedited)
def simulate(U, stepper): # modifies `U` in-place
    for j in range(0, len(U)-1):
        stepper(U, j)
        U.update_ghosts(j)

#from upwind scheme demo (unedited), used as a reference
def step_upwind(U, j, c):
    h, s = U.T.step, U.X.step
    U[j+1, 1:-1] = U[j, 1:-1] + c*h/s*(U[j, 2:] - U[j, 1:-1])

##from upwind scheme demo (unedited), used as a reference
def step_lf(U, j, c):
    h, s = U.T.step, U.X.step
    U[j+1, 1:-1] = 0.5*(U[j, 2:] + U[j, :-2]) + c*h/(2*s)*(U[j, 2:] - U[j, :-2])

#from upwind scheme demo (unedited), used as a reference
def cfl(c, h=None, s=None, U=None):
    if h is None and U is not None:
        h = U.T.step
    if s is None and U is not None:
        s = U.X.step
    assert h is not None and s is not None, \
           f"*** Can't determine time and/or step size (`h`={h}, `s`={s}) ***"
    return c * h / s

#####################################################################    
class Solution1D: # with periodic "ghost boundaries"
    def __init__(self, T, X, u0=None):
        from numpy import zeros
        assert isinstance(T, Domain1D) and isinstance(X, Domain1D)
        self.T = T
        self.X = X
        self.vals = zeros((len(T), len(X) + 2)) # ghost cells
        
        if u0 is not None and len(T) > 0:
            self.vals[0, 1:-1] = u0(X) if callable(u0) else u0
            self.update_ghosts(0)
            
    def __getitem__(self, s): # values by arbitrary Numpy-style slice
        assert isinstance(s, tuple) and len(s) == 2
        J, I = s[0], s[1]
        return self.vals[J, I]
    
    def __setitem__(self, s, x):
        assert isinstance(s, tuple) and len(s) == 2
        J, I = s[0], s[1]
        self.vals[J, I] = x

    def returnMax(self):
        from numpy import amax
        return amax(self.vals)
        
    def __len__(self):
        return len(self.T)
    
    def update_ghosts(self, j): # periodic boundaries
        self.vals[j+1, 0] = self.vals[j, -2]
        self.vals[j+1, -1] = self.vals[j, 1]

    def minMaxFix(self):    ##added a method to remove negative densities and densities over max
        self.vals[self.vals < 0] = 0
        self.vals[self.vals > 160] = 160

def impulse(X, x0=0.0, w=0.25): ##edited width to be .25
    """A rectangular impulse of height 1.0 centered at `x0` with width `2*w`."""
    assert isinstance(X, Domain1D)
    from numpy import zeros
    u0 = zeros(len(X))
    I = (x0-w <= X.vals) & (X.vals <= x0) ##edited ending condition to be x0 instead of x0+w so 160 shock ends at 0
    u0[I] = 160.0
    I2 = (X.vals < x0-w) ##used this to initialize 80 density before 160 shock
    u0[I2] = 80.0
    return u0

##Bungartz upwind
def bungartz_upwind(U, j, c):
    maxSpeed = 120
    maxDensity = 160
    h, s = U.T.step, U.X.step
    U[j+1, 1:-1] = U[j, 1:-1] - c*maxSpeed*h/s*( (1-U[j, 2:]/maxDensity)*U[j, 2:] - (1-U[j, 1:-1]/maxDensity)*U[j, 1:-1])
    U.minMaxFix()

##edited Lax-Friedrichs scheme
def step_lf2(U, j, c):
    h, s = U.T.step, U.X.step
    maxSpeed = 120
    maxDensity = 160
    fNext = maxSpeed*(1-U[j, 2:]/maxDensity)*U[j, 2:]
    fPrevious = maxSpeed*(1-U[j, :-2]/maxDensity)*U[j, :-2]
    U[j+1, 1:-1] = 0.5*(U[j, 2:] + U[j, :-2]) - c*h/(2*s)*(fNext - fPrevious)
    U.minMaxFix()

def experiment(c, h, s
               , u0=impulse
               , stepper=step_upwind
               , x_max=5.0, num_steps=100, t_max=None
              ):
    if t_max is None:
        assert num_steps is not None and num_steps >= 0
        t_max = num_steps * h   ##changed this from s to h because need to evaluate 1200 time steps, not space steps
    T = Domain1D(h, min_val=0.0, max_val=t_max)
    X = Domain1D(s, min_val=-x_max, max_val=x_max)
    U = Solution1D(T, X, u0=u0)
    simulate(U, lambda U, j: stepper(U, j, c))
    plot_grid(U, J=[0, len(U)-1]
              , title_str=f'CFL={cfl(c, U=U)}; u0={u0.__name__}')      

#1.1 Implementation
#c = .001 (to match CFL ratio for original upwind initial time and spatial steps)
#time step(h) = .1, num_steps = 1200 (120.0 logical time)
#spatial step(s) = .01
#u0 = impulse (because given example looks like an impulse)
#stepper = bungartz_upwind
#stepper is an the 7.12 formula from Bungartz et al
experiment(.001, .1, .01, u0=impulse, stepper=bungartz_upwind, x_max=5.0, num_steps=1200)

#1.2 Implementation
#c = .001 (to match CFL ratio for original demo Lax-Friedrichs initial time and spatial steps)
#time step(h) = .1, num_steps = 1200 (120.0 logical time)
#spatial step(s) = .01
#u0 = impulse (because given example looks like an impulse)
#stepper = step_lf2
#stepper is the given Lax-Friedrichs formula in the instructions
experiment(.001, .1, .01, u0=impulse, stepper=step_lf2, x_max=5.0, num_steps=1200)