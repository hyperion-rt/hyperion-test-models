# A simple model with no dust, just sources, to check that the Doppler Shifting
# is working correctly. This model consists of a disk of sources that is
# rotating in a solid body fashion around the origin. All sources have a
# spectrum that consists of a single spectral line that is narrow enough that we
# can easily see the rotation in a multi-wavelength image. We check that the
# image looks sensible in both binned and peeled images.

import numpy as np
from hyperion.model import Model
from hyperion.util.constants import c

m = Model()

m.set_cartesian_grid([-1., 1], [-1., 1.], [-1., 1])

N = 1000
w = np.random.random(N)**0.5
p = np.random.uniform(0, 2 * np.pi, N)
z = np.random.uniform(-0.1, 0.1, N)

x = w * np.cos(p)
y = w * np.sin(p)

# solid body with 1000 km/s on the outside
v = w * 1e8  # cm / s

vx = - v * np.sin(p)
vy = + v * np.cos(p)
vz = np.repeat(0, N)

# narrow emission line spectrum at 1 micron
wav = np.array([0.9999, 1.0001])
fnu = np.array([1., 1.])
nu = c / (wav * 1.e-4)

for isource in range(N):
    s = m.add_point_source()
    s.position = x[isource], y[isource], z[isource]
    s.velocity = vx[isource], vy[isource], vz[isource]
    s.spectrum = nu[::-1], fnu[::-1]
    s.luminosity = 1

# Set up images

i = m.add_peeled_images(sed=False, image=True)
i.set_wavelength_range(30, 0.995, 1.005)
i.set_image_limits(-1., 1., -1., 1.)
i.set_image_size(100, 100)
i.set_viewing_angles(np.linspace(0., 180, 13), np.linspace(0., 360, 13))

i = m.add_binned_images(sed=False, image=True)
i.set_wavelength_range(30, 0.995, 1.005)
i.set_image_limits(-1., 1., -1., 1.)
i.set_image_size(100, 100)
i.set_viewing_bins(500, 1)

m.set_forced_first_scattering(False)

m.set_n_initial_iterations(0)
m.set_n_photons(imaging=1e6)

m.write('disk_indiv.rtin', overwrite=True)
m.run('disk_indiv.rtout', overwrite=True, mpi=False)