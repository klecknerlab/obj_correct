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
import os
import json

GLASS_DATA = os.path.join(os.path.split(__file__)[0], "data", "glass.json")

with open(GLASS_DATA, 'r') as f:
    INDEX_MODELS = json.load(f)

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



def eval(n, λ):
    if isinstance(n, str):
        if n in INDEX_MODELS:
            model = INDEX_MODELS[n]
            if isinstance(model, dict):
                model = Sellmeier(**model)
                INDEX_MODELS[n] = model
            return model(λ)
        else:
            raise ValueError(f'Index specified as "{n}", but this is not a known material')
    elif hasattr(n, '__call__'):
        return n(λ)
    elif isinstance(n, (int, float)):
        return n
    else:
        raise ValueError(f'Invalid index specification: "{n}"')
