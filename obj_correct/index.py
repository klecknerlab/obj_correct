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

class Sellmeier:
    def __init__(self, A=1, B=None, C=None):
        self.A = A
        self.B = B
        self.C = C

    def __call__(self, λ):
        n2 = self.A
        λ2 = λ**2
        for B, C in zip(self.B, self.C):
            n2 += B * λ2 / (λ2 - C)

        return np.sqrt(n2)

INDEX_MODELS = {
    # https://en.wikipedia.org/wiki/Sellmeier_equation
    "BK7": Sellmeier(B=(1.03961212, 0.231792344, 1.01046945),
                     C=(6.00069867E-3, 2.00179144E-2, 103.560653)),
    "FS":  Sellmeier(B=(0.696166300, 0.407942600, 0.897479400),
                     C=(4.67914826E-3, 1.35120631E-2, 97.9340025)),

    # https://opg.optica.org/ao/viewmedia.cfm?uri=ao-46-18-3811&seq=0&html=true
    # used values for 20C
    "water": Sellmeier(B=(5.684027565E-1, 1.726177391E-1, 2.086189578E-2, 1.130748688E-1),
                       C=(5.101829712E-3, 1.821153936E-2, 2.620722293E-2, 1.069792721E1)),
}

def eval(n, λ):
    if isinstance(n, str):
        if n in INDEX_MODELS:
            return INDEX_MODELS[n](λ)
        elif n.upper() in INDEX_MODELS:
            return INDEX_MODELS[n.upper()](λ)
        else:
            raise ValueError(f'Index specified as "{n}", but this is not a known material')
    elif hasattr(n, '__call__'):
        return n(λ)
    elif isinstance(n, (int, float)):
        return n
    else:
        raise ValueError(f'Invalid index specification: "{n}"')
