"""
Parameter handling we need in gammacat.

TODO: merge this functionality into `gammapy.utils.modeling`.
"""
import numpy as np
import astropy.units as u

__all__ = [
    'Parameter',
    'Parameters',
]


class Parameter:
    """Parameter from input file.

    TODO: use `gammapy.utils.modeling.Parameter` instead.
    (change formats here so that it works for us.)
    """

    def __init__(self, name=None, val=None,
                 err=None, err_sys=None,
                 scale=1, unit=''):
        self.name = name
        self.val = val
        self.err = err
        self.err_sys = err_sys
        self.scale = scale
        self.unit = u.Unit(unit)

    def __repr__(self):
        return 'Parameter({})'.format(self.__dict__)

    @classmethod
    def from_dict(cls, data):
        # TODO: validate keys and types!!!
        return cls(**data)

    @property
    def real_val(self):
        return self.val * self.scale * self.unit

    @property
    def real_err(self):
        return self.err * self.scale * self.unit

    @property
    def real_err_sys(self):
        return self.err_sys * self.scale * self.unit

    def get_or_default(self, key, unit=None):
        result = getattr(self, key) or np.nan
        result = result * self.scale * self.unit
        result = result.to(unit) if unit else result
        return result


class Parameters:
    """Container with parameter list data member.
    """

    def __init__(self, parlist):
        self.parlist = parlist

    def __repr__(self):
        ss = 'ParameterSet with {} parameters:\n'.format(len(self.parlist))
        for par in self.parlist:
            ss += '- {!r}\n'.format(par)
        return ss

    @classmethod
    def from_dict(cls, data):
        """Make parameter list from data as given in data files."""
        parlist = []
        for name, attrs in data.items():
            pardict = dict(name=name)
            pardict.update(attrs)
            par = Parameter.from_dict(pardict)
            parlist.append(par)
        return cls(parlist=parlist)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.parlist[item]
        elif isinstance(item, str):
            names = [_.name for _ in self.parlist]
            try:
                idx = names.index(item)
            except ValueError:
                raise KeyError('No parameter name: {!r}. Parameters: {!r}'.format(item, names))
            return self.parlist[idx]
        else:
            raise TypeError('Invalid item: {!r}. Must be a number of string.'.format(item))
