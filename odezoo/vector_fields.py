"""ODE vector fields."""

from odezoo import backend


def lotka_volterra(y, /, a, b, c, d):
    """Lotka--Volterra dynamics."""
    return backend.numpy.asarray(
        [a * y[0] - b * y[0] * y[1], -c * y[1] + d * y[0] * y[1]]
    )


def van_der_pol(u, du, /, stiffness_constant):
    """Van-der-Pol dynamics."""
    return stiffness_constant * ((1.0 - u**2) * du - u)


def three_body(Y, dY, /, standardised_moon_mass):
    """Restricted three body dynamics."""
    mu, mp = standardised_moon_mass, 1.0 - standardised_moon_mass
    D1 = backend.numpy.linalg.norm(backend.numpy.asarray([Y[0] + mu, Y[1]])) ** 3.0
    D2 = backend.numpy.linalg.norm(backend.numpy.asarray([Y[0] - mp, Y[1]])) ** 3.0
    du0p = Y[0] + 2 * dY[1] - mp * (Y[0] + mu) / D1 - mu * (Y[0] - mp) / D2
    du1p = Y[1] - 2 * dY[0] - mp * Y[1] / D1 - mu * Y[1] / D2
    return backend.numpy.asarray([du0p, du1p])


def pleiades(u, _, /):
    """Following the PLEI definition in Hairer I.

    The vector field maps u -> u'', but to satisfy
    some sort of API for second-order problems,
    we include an unused argument for u'.
    This way, the function can be called like any other second-order ODE,
    which simplifies the testing behaviour.
    """
    x, y = u[:7], u[7:]
    x_diff = x[:, None] - x[None, :]
    y_diff = y[:, None] - y[None, :]
    r = (x_diff**2 + y_diff**2) ** 1.5

    # We divide by r (elementwise) further below, but r contains zeros.
    # Those zeros in r imply zeros in the nominator, so the following
    # manipulation does not alter the result (but avoids warnings)
    r = backend.numpy.where(r == 0, r + 1e-12, r)

    mj = backend.numpy.arange(1, 8)[None, :]
    ddx = backend.numpy.sum(mj * x_diff / r, axis=1)
    ddy = backend.numpy.sum(mj * y_diff / r, axis=1)
    return backend.numpy.concatenate((ddx, ddy))


def lorenz96(y, /, forcing):
    """Lorenz96 dynamics."""
    A = backend.numpy.roll(y, shift=-1)
    B = backend.numpy.roll(y, shift=2)
    C = backend.numpy.roll(y, shift=1)
    D = y
    return (A - B) * C - D + forcing


def rigid_body(y, /, p1, p2, p3):
    r"""Rigid body dynamics without external forces."""
    return backend.numpy.asarray([p1 * y[1] * y[2], p2 * y[0] * y[2], p3 * y[0] * y[1]])
