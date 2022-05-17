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

import numpy as np
from . import DEFAULT_λ
from .surface import Surface, advance_M
import matplotlib.pyplot as plt
from .vector import ensure_3D, norm
from . import index

class OpticalStack:
    def __init__(self, stack=[], n0=1):
        self.n0 = n0
        self.stack = []
        for layer in stack:
            if isinstance(layer, OpticalStack):
                self.stack += layer.stack
            elif isinstance(layer, Surface):
                self.stack.append(layer)
            else:
                raise ValueError('Layers of the stack must be of type Surface or OpticalStack')

        self.stack.sort(key=lambda layer: layer.center[2])

    def offset(self, offset):
        return OpticalStack([layer.offset(offset) for layer in self.stack], self.n0)


    def trace_rays(self, X, N, z_final, λ=DEFAULT_λ):
        X = np.asarray(X)
        N = norm(N)

        # Quick and dirty way to promote axes -- should probably do something
        # cleaner if performance is an issue!

        X = X * np.ones(N.shape)
        N = N * np.ones(X.shape)

        trace = [X]

        n = self.n0

        for layer in self.stack:
            if layer.center[2] > z_final:
                break

            z = layer.center[2]
            Xt, N, n = layer.trace_rays(trace[-1], N, n, λ)
            trace += Xt

        X = trace[-1].copy()
        good = np.where(N[..., 2] > 0)
        X[good] += (z_final - z) * N[good]/N[good][..., 2:3]

        trace.append(X)

        return np.moveaxis(trace, 0, -2)

    def M(self, λ=DEFAULT_λ, z_final=None):
        n = index.eval(self.n0, λ)
        M = np.eye(2)
        z = 0

        if z_final is None:
            zf = self.stack[-1].center[2]
        else:
            zf = z_final

        for layer in self.stack:
            z1 = layer.center[2]
            if z1 > zf:
                break

            advance_M(M, z1 - z, False)
            z = z1
            M1, n = layer.M(n, λ)

            M = np.matmul(M1, M)

        if z_final is None:
            z_final = z - M[0, 1] / M[1, 1]

        return advance_M(M, z_final - z, False), z_final

    def plot_surfaces(self, r_clip=12.5):
        for layer in stack:
            pass

    def flip(self, offset=0, end=None):
        offset = ensure_3D(offset)

        if end is None:
            end = self._get_end()

        return OpticalStack([layer.flip(end=(offset+end))
            for layer in self.stack], self.n0)

    def _get_end(self):
        if isinstance(self.stack[-1], OpticalStack):
            return self.stack[-1]._get_end()
        elif isinstance(self.stack[-1], Surface):
            return self.stack[-1].center
        else:
            raise ValueError(f'Invalid object in stack ({repr(self.stack[-1])})')


class Element(OpticalStack):
    def __init__(self, n, t, R1=None, R2=None, center=np.zeros(3), n_after=1, r_clip=10, n0=1):
        center = ensure_3D(center)
        self.n0 = n0
        self.stack = [
            Surface(n, center, R=R1, r_clip=r_clip),
            Surface(n_after, center + (0, 0, t), R=R2, r_clip=r_clip)
        ]
