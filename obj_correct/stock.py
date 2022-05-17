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

from .stack import Element
import os, json
DATA_DIR = os.path.join(os.path.split(__file__)[0], "data")

class LensLibrary:
    def __init__(self, fn):
        # Do lazy loading!
        self.fn = fn

    def _check_data(self):
        if not hasattr(self, 'data'):
            with open(self.fn, 'r') as f:
                self.data = json.load(f)

            self.fields = set(self.data[next(iter(self.data))].keys())

    def search(self, **keys):
        self._check_data()

        items = set(self.data.keys())

        for k, v in keys.items():
            if k not in self.fields:
                raise ValueError(f'unknown field "{k}"\nvalid options: {self.fields}')
            if isinstance(v, tuple):
                items = set(filter(lambda kk: self.data[kk][k] >= v[0] and self.data[kk][k] <= v[1], items))
            else:
                items = set(filter(lambda kk: self.data[kk][k] == v, items))

        return {k:self.data[k] for k in items}

    def __getitem__(self, k):
        if k not in self.data:
            raise ValueError(f'Unknown item {k}; entries correspond to stock number')

        d = self.data[k]
        return Element(d['glass'], d['t'], d['R1'], r_clip=d['CA']/2)



edmund_plano_convex = LensLibrary(os.path.join(DATA_DIR, 'edmund_plano_convex.json'))
