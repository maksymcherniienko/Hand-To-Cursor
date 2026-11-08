import math, time

class OneEuroFilter:
    def __init__(self, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = None
        self.dx_prev = 0.0
        self.t_prev = None

    def smoothing_factor(self, t_e, cutoff):
        r = 2 * math.pi * cutoff * t_e
        return r / (r + 1)

    def exponential_smoothing(self, a, x, x_prev):
        return a * x + (1 - a) * x_prev

    def __call__(self, x, t=None):
        if t is None:
            t = time.time()
        
        if self.x_prev is None:
            self.x_prev = x
            self.t_prev = t
            return x

        t_e = t - self.t_prev
        
        # Обчислюємо швидкість (похідну)
        dx = (x - self.x_prev) / t_e
        dx_smoothed = self.exponential_smoothing(self.smoothing_factor(t_e, self.d_cutoff), dx, self.dx_prev)
        
        # Адаптуємо частоту зрізу на основі швидкості
        cutoff = self.min_cutoff + self.beta * abs(dx_smoothed)
        
        # Фільтруємо значення
        x_filtered = self.exponential_smoothing(self.smoothing_factor(t_e, cutoff), x, self.x_prev)
        
        self.x_prev = x_filtered
        self.dx_prev = dx_smoothed
        self.t_prev = t
        
        return x_filtered