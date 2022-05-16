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
π = np.pi

def mag(X):
    '''Calculate the length of an array of vectors.'''
    return np.sqrt((np.asarray(X)**2).sum(-1))

def mag1(X):
    '''Calculate the length of an array of vectors, keeping the last dimension
    index.'''
    return np.sqrt((np.asarray(X)**2).sum(-1))[..., np.newaxis]

def dot(X, Y):
    '''Calculate the dot product of two arrays of vectors.'''
    return (np.asarray(X)*Y).sum(-1)

def dot1(X, Y):
    '''Calculate the dot product of two arrays of vectors, keeping the last
    dimension index'''
    return (np.asarray(X)*Y).sum(-1)[..., np.newaxis]

def norm(X):
    '''Computes a normalized version of an array of vectors.'''
    return X / mag1(X)

cross = np.cross

def ensure_3D(x):
    if isinstance(x, (int, float)):
        return np.array([0, 0, x])
    else:
        return np.array(x)
