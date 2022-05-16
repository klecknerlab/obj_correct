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

# wavelength + NA for rays
λ = 0.5
NA = 0.4

cover = stack.Element('BK7', 2).offset(1) # 2mm "cover glass", 1 mm from focus

# Create the inital rays
X = np.zeros(3)
m = np.linspace(-NA, NA, 101)
N = np.zeros((len(m), 3))
N[:, 0] = m
N[:, 2] = 1



def compute_offset_error(optical_stack, X=X, N=N):
    M, z = optical_stack.M()
    trace = optical_stack.trace_rays(X, N, 15, λ)

    # Get the slope of the final ray
    Nf = trace[:, -1] - trace[:, -2]
    Nf /= Nf[:, 2:3]

    # Project it back to the focus plane for paraxial rays
    Xt = trace[:, -1] + (z - trace[:, -1, 2:3]) * Nf

    return Xt[:, 0]

for offset in (np.linspace(-0.2, 0.2, 11)):
    # The optical stack is the cover + the correction lens
    # Here there are several possible correction lenses listed -- only 1 should be uncommented!
    # We create new optical stacks where we change the lens position
    # Note that each lens has an approximate offset that I added in -- this is where the lens starts
    optics = stack.OpticalStack([
        cover,
        stack.Element('BK7', 2.8, R2=-20.6).offset(3.5+offset) #Thorlabs LA1304, curved surface to the right
        # stack.Element('BK7', 2.6, R2=-25.8).offset(4+offset) #Thorlabs LA1213, curved surface to the right
        # stack.Element('BK7', 2.6, R1=25.8).offset(4.5+offset) #Thorlabs LA1213, curved surface to the left
        # stack.Element('BK7', 2.2, R2=-51.5).offset(6+offset) #Thorlabs LA1207, curved surface to the right
        # stack.Element('BK7', 2.0, R2=-37.21).offset(4.5+offset) #Edmund 67-148, curved surface to the right
        # stack.Element('BK7', 2.0, R1=37.21).offset(5.5+offset) #Edmund 67-148, curved surface to the left
    ])

    plt.plot(m, compute_offset_error(optics) * 1000, label=f'{offset:.2f}')


plt.plot(m, compute_offset_error(cover) * 1000, '-k', label=f'no correction')

plt.title('Offset error when rays projected back to focus plane')
plt.xlabel('NA')
plt.ylabel('Offset (μm)')
plt.ylim(-1, 1)
plt.legend()

plt.show()
