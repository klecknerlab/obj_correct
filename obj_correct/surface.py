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
from .vector import *
from . import DEFAULT_λ
from . import index

class Surface:
    def __init__(self, n, center, r_clip=None, R=None):
        self.n = n
        self.center = ensure_3D(center)
        self.r_clip = r_clip
        self.R = R if R != 0 else None

    def M(self, n1=1, λ=DEFAULT_λ):
        n2 = index.eval(self.n, λ)
        if self.R is None:
            return np.array([(1, 0), (0, n1/n2)]), n2
        else:
            return np.array([(1, 0), ((n1-n2)/(self.R*n2), n1/n2)]), n2

    def offset(self, offset):
        return Surface(self.n, self.center + ensure_3D(offset), self.r_clip, self.R)

    def trace_rays(self, X, N, n=1, λ=DEFAULT_λ):
        Xf, Nf, n = self._trace_rays(X, N, n, λ)

        if self.r_clip is not None:
            r = mag(Xf[0][..., :2] - self.center[:2])
            print(r)
            print(np.where(r > self.r_clip))
            Nf[np.where(r > self.r_clip)] = -1

            print(Nf)

        return Xf, Nf, n

    def _trace_rays(self, X, N, n, λ):
        nf = index.eval(self.n, λ)
        m = n/nf

        Xf = X.copy()
        Nf = N.copy()

        C = self.center
        if self.R is not None:
            C = C + (0, 0, self.R)
            sgn = np.sign(self.R)

        # Would it be faster to avoid a loop?  Probably, but with the bad
        #  ray detection it's a real pain.  Could be accelerated easily with
        #  numba if required.
        for i, (XX, NN) in enumerate(zip(X, N)):
            if NN[2] <= 0:
                print(i)
                continue

            if self.R is None:
                Ns = np.array([0, 0, -1])
                d = (C[2] - XX[2]) / NN[2]
                Xf[i] += d * NN
            else:
                # https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
                # note: Δ = c - o
                Δ = C - XX
                dp = dot(Δ, NN)
                sqt = dp*dp - (dot(Δ, Δ) - self.R*self.R)

                if sqt < 0:
                    Nf[i] = -1
                    continue

                # sgn > 0: convex surface: first intersection
                # sgn < 0: concave surface: second intersection
                Xf[i] += (dp - sgn * np.sqrt(sqt)) * NN
                Ns = sgn * norm(Xf[i] - C)

            # Compute refraction
            # http://www.starkeffects.com/snells-law-vector.shtml
            cp = cross(NN, Ns)
            sqt = 1 - m*m * dot(cp, cp)

            # Check for total internal reflection, and kill the ray if we get it!
            if sqt < 0:
                Nf[i] = -1
                continue

            Nf[i] = norm(m * cross(Ns, cp) - Ns * np.sqrt(sqt))

        # Output is ray intersection, normal right, index final
        return [Xf], Nf, nf

    # OLD VERSION: vectorized with masks, but doesn't work!
    # def _trace_rays(self, X, N, n, λ):
    #     nf = index.eval(self.n, λ)
    #     m = n/nf
    #     print(n, nf, m)
    #     Xf = X.copy()
    #     Nf = N.copy()
    #
    #
    #     # Planar surface
    #     if self.R is None:
    #         mask = N[..., 2] > 0
    #         good = np.where(mask)
    #
    #         Ns = np.array([0, 0, -1]) * np.ones(N[good].shape)
    #
    #         d = (self.center[2:3] - X[good][..., 2:3]) / N[good][..., 2:3]
    #         Xf[good] += d * N[good]
    #
    #
    #     # Spherical surface
    #     else:
    #         # https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
    #         # note: Δ = c - o
    #         C = self.center + (0, 0, self.R)
    #         Δ = C - Xf
    #         dp = dot(Δ, N)
    #         sqt = dp*dp - (dot(Δ, Δ) - self.R*self.R)
    #
    #         mask = (sqt >= 0) & (N[..., 2] > 0)
    #         good = np.where(mask)
    #
    #         sgn = np.sign(self.R)
    #         # sgn > 0: convex surface: first intersection
    #         # sgn < 0: concave surface: second intersection
    #         sqt = np.sqrt(sqt[good][..., np.newaxis])
    #         Xf[good] += (dp[good][..., np.newaxis] - sgn * sqt) * N[good]
    #         Ns = sgn * norm(Xf[good] - C)
    #
    #         # Set "bad" rays
    #         Nf[np.where(~mask)][..., 2] = -1
    #
    #     print(good)
    #     print(Nf)
    #     print(Ns)
    #     # Compute refraction
    #     # http://www.starkeffects.com/snells-law-vector.shtml
    #     cp = cross(Nf[good], Ns)
    #     sqt = 1 - m*m * dot(cp, cp)
    #
    #     print(sqt)
    #
    #     # Check for total internal reflection, and kill the ray if we get it!
    #     mask2 = sqt > 0
    #     Nf[good][np.where(~mask2)][..., 2] = -1
    #
    #     good2 = np.where(mask2)
    #     sqt = np.sqrt(sqt[good][good2][..., np.newaxis])
    #
    #     print(mask2)
    #
    #     Nf[good][good2] = norm(m * cross(Ns[good2], cp[good2]) - Ns[good2] * sqt)
    #
    #     # Output is ray intersection, normal right, index final
    #     return [Xf], Nf, nf

    def edge(self, r_clip=12.5, force_clip=False, curve_points=100):
        if force_clip:
            rc = min(r_clip, self.r_clip)
        else:
            rc = r_clip if self.r_clip is None else self.r_clip

        x = self.center[0]
        z = self.center[2] + self.R

        ϕm = π/2 if (abs(self.R) < rc) else np.arcsin(rc / self.R)
        ϕ = np.linspace(-ϕm, ϕm, curve_points)

        if (self.R > 0):
            ϕ += π

        r = abs(self.R)
        return np.vstack([z + r*np.cos(ϕ), x + r*np.sin(ϕ)]).T



class PerfectLens(Surface):
    def __init__(self, f, center, r_clip=None, optical_center=None):
        self.center = ensure_3D(center)
        self.f = f
        self.r_clip = r_clip
        self.optical_center = self.center if optical_center is None else ensure_3D(self.optical_center)

    def offset(self, offset):
        return PerfectLens(self.f, self.center + ensure_3D(offset), self.r_clip, self.optical_center)

    def _trace_rays(self, X, N, n=1, λ=DEFAULT_λ):
        # Would it be faster to avoid a loop?  Probably, but with the bad
        #  ray detection it's a real pain.  Could be accelerated easily with
        #  numba if required.
        Xi = X.copy()
        Xf = X.copy()
        Nf = N / N[:, 2:3]

        for i, (XX, NN) in enumerate(zip(X, N)):
            if NN[2] <= 0:
                continue

            # Project to surface
            Xi[i] += (self.center[2] - XX[2]) * Nf[i]

            # Project to virtual lens center
            Xf[i] += (self.optical_center[2] - XX[2]) * Nf[i]

            # Focus
            Nf[i, :2] -= (Xf[i, :2] - self.optical_center[:2]) / self.f

            # Propigate to clip plane
            Xf[i] += (self.center[2] - Xf[i, 2]) * Nf[i]

        return [Xi, Xf], norm(Nf), n

    def M(self, n0=1, λ=DEFAULT_λ):
        d = self.optical_center[2] - self.center[2]
        return np.array([(1+d/self.f, d**2/self.f), (-1/self.f, 1-d/self.f)]), n0


def advance_M(M, d, copy=True):
    if copy:
        M = np.array(M)
    M[0] += d * M[1]
    return M
