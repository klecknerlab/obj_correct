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

lenses = stock.edmund_plano_convex.search(diameter=12)
for lens in sorted(lenses, key=lambda l: lenses[l]['f']):
    info = lenses[lens]
    print(f"#{lens}: diameter={info['diameter']:.1f}, f={info['f']} R1={info['R1']}, t={info['t']}, glass={info['glass']}")

lens = '18-057'
optics = stock.edmund_plano_convex[lens]

print(f'\nOptics stack of item #{lens}:')

for layer in optics.stack:
    print('   ' + repr(layer))


print(f'\nOptics stack of item #{lens}, flipped and offset:')

for layer in optics.flip(offset=1).stack:
    print('   ' + repr(layer))
