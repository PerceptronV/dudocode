"""
“Commons Clause” License Condition v1.0

The Software is provided to you by the Licensor under the License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or all of the rights granted to you under the License to provide to third parties, for a fee or other consideration (including without limitation fees for hosting or consulting/ support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software. Any license notice or attribution required by the License must also include this Commons Clause License Condition notice.

Software: Dudocode

License: GNU General Public License Version 3

Licensor: SONG YIDING

Dudocode is a pseudocode-to-Python transpiler based on the format specified in CIE IGCSE (Syllabus 0478).
Copyright (C) 2021  SONG YIDING

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import math
import numpy as np


class _AnyType(object):
    def __init__(self, value):
        self.value = str(value)
        self.specialised = False
        self.type = str
        self.specialised_val = self.value

    def __repr__(self):
        return '<dudo._AnyType({}), specialised: {}>'.format(repr(self.value), self.specialised)

    def __str__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        if self.value in ("TRUE", 1):
            return True
        if self.value in ("FALSE", 0):
            return False
        return bool(self.value)

    def infer_type(self, string):
        if string in ('TRUE', 'FALSE'):
            return bool
        if string.replace('-', '').isnumeric():
            return int
        if string.replace('-', '').replace('.', '').isnumeric():
            return float
        return str

    def set_type(self, _type):
        self.type = _type
        self.specialised = True
        self.specialised_val = _type(self.value)

    def camouflage(self, other, strict=False):
        _name = type(other).__name__
        if strict and self.specialised:
            if _name == '_AnyType':
                if not other.specialised:
                    other_type = other.infer_type(other.value)
                    if self.type == float and other_type == int:
                        other.set_type(float)
                    else:
                        other.set_type(other_type)
                return self.specialised_val, other.specialised_val
            return self.specialised_val, other

        classname_mappings = {
            'bool': bool,
            'int': int,
            'float': float,
            'str': str,
        }
        if _name in classname_mappings:
            self.set_type(classname_mappings[_name])
            return self.specialised_val, other

        if _name == '_AnyType':
            self_type = self.infer_type(self.value)
            other_type = other.infer_type(other.value)
            if {self_type, other_type} == {float, int}:
                self.set_type(float)
                other.set_type(float)
            else:
                self.set_type(self_type)
                other.set_type(other_type)
            return self.specialised_val, other.specialised_val

        return self.specialised_val, other

    def __lt__(self, other):
        a, b = self.camouflage(other)
        return a < b

    def __le__(self, other):
        a, b = self.camouflage(other)
        return a <= b

    def __eq__(self, other):
        a, b = self.camouflage(other)
        return a == b

    def __ne__(self, other):
        a, b = self.camouflage(other)
        return a != b

    def __gt__(self, other):
        a, b = self.camouflage(other)
        return a > b

    def __ge__(self, other):
        a, b = self.camouflage(other)
        return a >= b

    def __add__(self, other):
        a, b = self.camouflage(other)
        return a + b

    def __sub__(self, other):
        a, b = self.camouflage(other)
        return a - b

    def __mul__(self, other):
        a, b = self.camouflage(other)
        return a * b

    def __truediv__(self, other):
        a, b = self.camouflage(other)
        return a / b

    def __floordiv__(self, other):
        a, b = self.camouflage(other)
        return a // b

    def __mod__(self, other):
        a, b = self.camouflage(other)
        return a % b

    def __pow__(self, power, modulo=None):
        if self.specialised:
            return pow(self.specialised_val, power, modulo)
        return pow(self.infer_type(self.value)(self.value), power, modulo)

    def __radd__(self, other):
        a, b = self.camouflage(other)
        return b + a

    def __rsub__(self, other):
        a, b = self.camouflage(other)
        return b - a

    def __rmul__(self, other):
        a, b = self.camouflage(other)
        return b * a

    def __rtruediv__(self, other):
        a, b = self.camouflage(other)
        return b / a

    def __rfloordiv__(self, other):
        a, b = self.camouflage(other)
        return b // a

    def __rmod__(self, other):
        a, b = self.camouflage(other)
        return b % a

    def __rpow__(self, power, modulo=None):
        if self.specialised:
            return pow(power, self.specialised_val, modulo)
        return pow(power, self.infer_type(self.value)(self.value), modulo)

    def __neg__(self):
        if self.specialised:
            return -self.specialised_val
        return -(self.infer_type(self.value)(self.value))

    def __len__(self):
        if self.specialised:
            return len(self.specialised_val)
        return len(self.infer_type(self.value)(self.value))

    def __abs__(self):
        if self.specialised:
            return abs(self.specialised_val)
        return abs(self.infer_type(self.value)(self.value))

    def __round__(self, n=None):
        if self.specialised:
            return round(self.specialised_val, n)
        return round(self.infer_type(self.value)(self.value), n)

    def __trunc__(self, n=None):
        if self.specialised:
            return math.trunc(self.specialised_val)
        return math.trunc(self.infer_type(self.value)(self.value))

    def __floor__(self, n=None):
        if self.specialised:
            return math.floor(self.specialised_val)
        return math.floor(self.infer_type(self.value)(self.value))

    def __ceil__(self, n=None):
        if self.specialised:
            return math.ceil(self.specialised_val)
        return math.ceil(self.infer_type(self.value)(self.value))


class _ArrayTemplateDummy(object):
    def __init__(self):
        pass

    def __getitem__(self, item):
        pass


class _Array(object):
    def __init__(self, slices=None, type=None, arr=None, starts=None):
        if slices is not None:
            dimensions = [i.stop - i.start + 1 if i.start is not None else i.stop for i in slices]
            self.starts = np.array([i.start if i.start is not None else 1 for i in slices])
            self.values = np.full(dimensions, self.infer_value_from_type(type))
        elif arr is not None:
            self.starts = starts
            self.values = arr.copy()
        else:
            raise ValueError("No argument provided to intialise array")
        self.shape = self.values.shape
        self.num_dims = len(self.shape)

    def infer_value_from_type(self, _type):
        if _type is None:
            return None
        if _type == str:
            return ''
        if _type == int:
            return 0
        if _type == float:
            return 0.0
        if _type == bool:
            return False
        return None

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return '<dudo.Array({}), start_indices: {}, shape: {}>'.format(repr(self.values), self.starts, self.shape)

    def __len__(self):
        return len(self.values)

    def get_index(self, idx, dim):
        if idx >= 0:
            if idx < self.starts[dim]:
                raise IndexError("Index {} out of range".format(idx))
            return idx - self.starts[dim]
        if idx < 0:
            return idx

    def __getitem__(self, item):
        if type(item).__name__ == 'int':
            if self.num_dims == 1:
                return self.values[self.get_index(item, 0)]
            return _Array(arr=self.values[self.get_index(item, 0)], starts=self.starts[1:].copy())

        ret = self.values.__getitem__(self.get_index(item[0], 0))
        item_dims = len(item)
        for dim in range(1, item_dims):
            ret = ret.__getitem__(self.get_index(item[dim], dim))

        if self.num_dims == item_dims:
            return ret
        return _Array(arr=ret, starts=self.starts[item_dims:].copy())

    def __setitem__(self, key, value):
        if type(key).__name__ == 'int':
            self.values[self.get_index(key, 0)] = value
            return value

        arr = self.values
        final_dim = len(key) - 1
        for dim in range(0, final_dim):
            arr = arr.__getitem__(self.get_index(key[dim], dim))
        arr.__setitem__(self.get_index(key[final_dim], final_dim), value)
        return value
