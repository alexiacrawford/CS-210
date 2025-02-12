'''
Alexia Crawford
10/09/2023
Estimating Pi
Credit: worked with Sam 
'''
import random
import doctest
import points_plot

def in_unit_circle(x: float, y: float) -> bool: #write body here
    '''
    Returns True if and only if (x,y) lies within the circle
    with origin (0,0) and radius 1.0.
    
    >>> in_unit_circle(0.0, 0.0)
    True
    >>> in_unit_circle(1.0,1.0)
    False
    
    # You were wondering, weren't you? 
    >>> in_unit_circle(0.5, -0.5)
    True
    >>> in_unit_circle(-0.9, -0.5)
    False
    '''
    # circle equation: x^2+y^2=1
    squared_distance = x**2 + y**2
    return squared_distance <= 1.0
        
def rand_point_unit_sq() -> tuple[float, float]:
    '''Returns random x,y both in range 0..1.0, 0..1.0.'''
    x = random.random()
    y = random.random()
    return x, y

a,b = rand_point_unit_sq()

def plot_random_points(n_points: int = 500):
    '''Generate and plot n_points points
    in interval (0,0) to (1,1).
    Creates a window and prompts the user before
    closing it.
    '''
    points_plot.init()
    for i in range(n_points):
        x, y = rand_point_unit_sq()
        points_plot.plot(x, y, color_rgb=(50, 50, 50))
    points_plot.wait_to_close()

GOOD_PI = 3.141592653589793  # A very good estimate, from math.pi

SAMPLES = 1_000   # More =>  more precise, but slower

def relative_error(est: float, expected: float) -> float:
    '''Relative error of estimate (est) as non-negative fraction of expected value.

    >>> round(relative_error(3.0, 5.0), 2)
    0.4
    >>> round(relative_error(5.0, 3.0), 2)
    0.67
    >>> relative_error(pi_approx(), GOOD_PI) <= 0.01  # within 1%
    True
    '''
    abs_error = est - expected
    rel_error = abs(abs_error / expected)
    return rel_error

def pi_approx() -> float: #write this code
    '''Return an estimate of pi by sampling random points.
    >>> relative_error(pi_approx(), GOOD_PI) <= 0.01  # Within 1%
    True
    >>> relative_error(pi_approx(), GOOD_PI) <= 0.01  # Within 1%
    True
    >>> relative_error(pi_approx(), GOOD_PI) <= 0.01  # Within 1%
    True
    '''
    
'''total tried is initially 0
total within circle is initially 0
loop some number of times:
     generate a point p
     add one to total tried
     if p is within the unit circle:
         add one to total within circle
     else
         do nothing
         '''
def pi_approx() -> float:
    total_tried = 0
    total_within_circle = 0
    num_iterations = 10000

    for _ in range(num_iterations):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        
        distance = x**2 + y**2
        
        total_tried += 1
        
        if distance <= 1:
            total_within_circle += 1

    estimated_pi = 4 * (total_within_circle / total_tried)
    return estimated_pi

estimated_pi = pi_approx()
print(f"Estimated pi: {estimated_pi}")


#points_plot.plot(x, y, color_rgb=(255, 10, 10)) ## Red
#points_plot.plot(x, y, color_rgb=(240, 240, 240)) ## Light grey

def main():
    doctest.testmod()
    plot_random_points() # Eyeball test
    points_plot.init() # Enables plotting
    estimate = pi_approx()
    print(f"Pi is approximately {estimate}")
    points_plot.wait_to_close()

if __name__ == "__main__":
    main()

