# A simple model to check what happens when a source is moving towards dust and
# we observe both the source and the dust. If we observe the source such that
# the dust is directly behind, and the source is moving towards the dust, we
# should see red-shifted emission from the source and blue-shifted scattered
# light emission.

import numpy as np
from hyperion.model import Model
from hyperion.util.constants import c

m = Model()

m.set_cartesian_grid([-1.,0, 1], [-1., 1.], [-1., 1])

density = np.zeros(m.grid.shape)
density[:,:,0] = 1.

m.add_density_grid(density, 'kmh_lite.hdf5')

# narrow emission line spectrum at 1 micron
wav = np.array([0.9999, 1.0001])
fnu = np.array([1., 1.])
nu = c / (wav * 1.e-4)

s = m.add_spherical_source()
s.position = 0.5, 0., 0.
s.velocity = -1e8, 0., 0.
s.spectrum = nu[::-1], fnu[::-1]
s.luminosity = 1
s.radius = 0.1

# Set up images

i = m.add_peeled_images(sed=False, image=True)
i.set_wavelength_range(30, 0.99, 1.01)
i.set_image_limits(-1., 1., -1., 1.)
i.set_image_size(100, 100)
i.set_viewing_angles(np.linspace(0., 180, 13), np.repeat(0., 13))

m.set_n_initial_iterations(0)
m.set_n_photons(imaging=1e6)

m.write('simple_scat.rtin', overwrite=True)
m.run('simple_scat.rtout', overwrite=True, mpi=True)