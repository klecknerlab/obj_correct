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

λ = 0.5
glass = 'BK7'
f = 100
R = f * (index.eval(glass, λ) - 1)
t = 1
r_clip = 8

stack1 = stack.OpticalStack([
    surface.PerfectLens(f, 2*f, r_clip=r_clip)
])
stack2 = stack.Element(glass, t, R1=R, r_clip=r_clip).offset(2*f)

M, z = stack2.M()
# print(stack2.M(z_final = 150))
print(f'f = {f:.2f}, R = {R:.2f}, n = {index.eval(glass, λ):.3f} @ {λ*1E3:.1f} nm')
print(f'focus @ z = {z:.2f}')

X = np.zeros(3)
m = np.linspace(-0.05, 0.05, 21)
N = np.zeros((len(m), 3))
N[:, 0] = m
N[:, 2] = 1

for ray in stack1.trace_rays(X, N, z):
    plt.plot(ray[:, 2], ray[:, 0], '-', linewidth=0.5, color='C0')


for ray in stack2.trace_rays(X, N, z):
    plt.plot(ray[:, 2], ray[:, 0], '-', linewidth=0.5, color='C1')

plt.show()
