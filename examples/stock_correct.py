#!/usr/bin/python3
#
# Copyright 2022 Dustin Kleckner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from obj_correct import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import time

# wavelength + NA for rays
λ = 0.5
plot_NA = 0.5


cover = stack.Element('N-BK7', 2).offset(1) # 2mm "cover glass", 1 mm from focus


# Optimization parameters
opt_λ = 0.5
opt_NA = 0.4
min_z = cover.get_end()[2] + 0.5
max_z = 10

# Create the inital rays
X = np.zeros(3)
m = np.linspace(-opt_NA, opt_NA, 21)
N = np.zeros((len(m), 3))
N[:, 0] = m
N[:, 2] = 1


m2 = np.linspace(-plot_NA, plot_NA, 101)
N2 = np.zeros((len(m2), 3))
N2[:, 0] = m2
N2[:, 2] = 1


def compute_offset_error(optical_stack, X=X, N=N, λ=opt_λ):
    M, z = optical_stack.M()
    trace = optical_stack.trace_rays(X, N, 15, λ)

    # Get the slope of the final ray
    Nf = trace[:, -1] - trace[:, -2]
    Nf /= Nf[:, 2:3]

    # Project it back to the focus plane for paraxial rays
    Xt = trace[:, -1] + (z - trace[:, -1, 2:3]) * Nf

    return Xt[:, 0]


lens_stock = stock.edmund_plano_convex

lenses = lens_stock.search(diameter=12)

stock_id = next(iter(lenses))
info = lenses[stock_id]


def err_func(offset, lens):
    if isinstance(offset, np.ndarray):
        offset = offset[0]
    err = compute_offset_error(stack.OpticalStack([cover, lens.offset(offset)]))
    return (err**2).mean() * 1000

# for z in np.linspace(min_z, max_z - info['t'], 11):
#     start = time.time()
#     optics = stack.OpticalStack([cover, lens.offset(z)])
#     err = compute_offset_error(optics)
#     el = time.time() - start
#     print(f'z = {z:.2f}, RMS error: {np.std(err)*1000}')
#     plt.plot(m, err * 1000, label=f'{z:.2f}')

results = {}

for flipped in (False, True):
    for stock_id, info in lens_stock.search(diameter=12).items():
        lens = lens_stock[stock_id]
        if flipped:
            lens = lens.flip()

        mz = max_z - info['t']

        res = optimize.minimize(err_func, (0.5*(min_z + mz),), args=(lens,), bounds=((min_z, mz),))
        z = res['x'][0]

        results[(stock_id, flipped)] = (z, res['fun'], lens)

        print(f"{stock_id} (dia={info['diameter']}, f={info['f']}{' flipped' if flipped else ''}, {info['glass']}) RMS error: {res['fun']} @ z={z:.2f}")


best = list(results.keys())
best.sort(key=lambda k: results[k][1])
# print(best[:10])

best_err = results[best[0]][1]

for id in best:
    z, err, lens = results[id]
    if err > best_err * 5:
        break
    stock_id, flipped = id
    info = lens_stock.data[stock_id]
    optics = stack.OpticalStack([cover, lens.offset(z)])
    err = compute_offset_error(optics, N=N2)
    plt.plot(m2, err * 1000, label=f"{stock_id} (dia={info['diameter']}, f={info['f']}{' flipped' if flipped else ''}, {info['glass']}) @ z={z:.2f}")

plt.legend()
plt.ylim(-1, 1)
plt.show()






# for offset in (np.linspace(-0.2, 0.2, 11)):
#     # The optical stack is the cover + the correction lens
#     # Here there are several possible correction lenses listed -- only 1 should be uncommented!
#     # We create new optical stacks where we change the lens position
#     # Note that each lens has an approximate offset that I added in -- this is where the lens starts
#     optics = stack.OpticalStack([
#         cover,
#         stack.Element('N-BK7', 2.8, R2=-20.6).offset(3.5+offset) #Thorlabs LA1304, curved surface to the right
#         # stack.Element('N-BK7', 2.6, R2=-25.8).offset(4+offset) #Thorlabs LA1213, curved surface to the right
#         # stack.Element('N-BK7', 2.6, R1=25.8).offset(4.5+offset) #Thorlabs LA1213, curved surface to the left
#         # stack.Element('N-BK7', 2.2, R2=-51.5).offset(6+offset) #Thorlabs LA1207, curved surface to the right
#         # stack.Element('N-BK7', 2.0, R2=-37.21).offset(4.5+offset) #Edmund 67-148, curved surface to the right
#         # stack.Element('N-BK7', 2.0, R1=37.21).offset(5.5+offset) #Edmund 67-148, curved surface to the left
#     ])
#
#     plt.plot(m, compute_offset_error(optics) * 1000, label=f'{offset:.2f}')
#
#
# plt.plot(m, compute_offset_error(cover) * 1000, '-k', label=f'no correction')
#
# plt.title('Offset error when rays projected back to focus plane')
# plt.xlabel('NA')
# plt.ylabel('Offset (μm)')
# plt.ylim(-1, 1)
# plt.legend()
#
# plt.show()
