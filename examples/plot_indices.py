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

from obj_correct import index
import numpy as np
import matplotlib.pyplot as plt

λ = np.linspace(0.3, 0.7, 100)

for name in ['water', '7980', 'N-BK7', 'N-SF11', 'FS']:
    plt.plot(λ*1000, index.eval(name, λ), label=name)

plt.xlabel("Wavelength (nm)")
plt.ylabel('Index of Refraction')
plt.legend()
plt.show()
