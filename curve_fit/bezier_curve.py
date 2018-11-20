import numpy as np
#from scipy.misc import comb
from scipy.special import comb

def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i



def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    # print('length of points : ', end=''); print(nPoints)
    # print('xPoints : ', end=''); print(xPoints)
    # print('yPoints : ', end=''); print(yPoints)

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    # print('type of polynomial_array :', end=''); print(type(polynomial_array))
    # print('length of polynomial_array :', end=''); print(len(polynomial_array))

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    #print('xvals (np.dot()): ', end=''); print(xvals)

    return xvals, yvals


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    nPoints = 10                                # 設定要產生幾個 random points 
    points = np.random.rand(nPoints, 2)*200     # np.random.rand(5, 2) --> 產生5個 2-D 的隨機(介於0.0~1.0) ndarray
    xpoints = [p[0] for p in points]
    ypoints = [p[1] for p in points]

    xvals, yvals = bezier_curve(points, nTimes=1000)
    
    plt.plot(xvals, yvals)
    plt.plot(xpoints, ypoints, "ro")

    # print 出每個點的順序編號
    for nr in range(len(points)):
        plt.text(points[nr][0], points[nr][1], nr)

    plt.show()
