"""
Parameter handling we need in gammacat.

TODO: merge this functionality into `gammapy.utils.modeling`.
"""
import numpy as np
import astropy.units as u
from gammapy.spectrum.models import PowerLaw, PowerLaw2, ExponentialCutoffPowerLaw

__all__ = [
    'Parameter',
    'Parameters',
    'make_spec_model',
]

DEFAULT_E_MAX = u.Quantity(1e5, 'TeV')


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
        #     name=data.get('name', None)
        # )

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


def make_spec_model(data):
    """Make a Gammapy spectrum model.

    TODO: how do we want to handle systematic errors?
    (at the moment not taking into account)

    Parameters
    ----------
    data : dict
        Parameter dictionary
    
    Returns
    -------
    model : `~gammapy.spectrum.models.SpectrumModel`
        Spectral model
    """

    spec_type = data['spec_type']
    pars, errs = {}, {}

    if spec_type == 'pl':
        model_class = PowerLaw
        pars['amplitude'] = data['spec_pl_norm']
        errs['amplitude'] = data['spec_pl_norm_err']
        pars['index'] = data['spec_pl_index']
        errs['index'] = data['spec_pl_index_err']
        pars['reference'] = data['spec_pl_e_ref']
    elif spec_type == 'pl2':
        model_class = PowerLaw2
        pars['amplitude'] = data['spec_pl2_flux']
        errs['amplitude'] = data['spec_pl2_flux_err']
        pars['index'] = data['spec_pl2_index']
        errs['index'] = data['spec_pl2_index_err']
        pars['emin'] = data['spec_pl2_e_min']
        e_max = data['spec_pl2_e_max']
        if np.isnan(e_max.value):
            e_max = DEFAULT_E_MAX
        pars['emax'] = e_max
    elif spec_type == 'ecpl':
        model_class = ExponentialCutoffPowerLaw
        from uncertainties import ufloat
        pars['amplitude'] = data['spec_ecpl_norm']
        errs['amplitude'] = data['spec_ecpl_norm_err']
        pars['index'] = data['spec_ecpl_index']
        errs['index'] = data['spec_ecpl_index_err']
        lambda_ = 1. / ufloat(data['spec_ecpl_e_cut'].to('TeV').value, data['spec_ecpl_e_cut_err'].to('TeV').value)
        pars['lambda_'] = u.Quantity(lambda_.nominal_value, 'TeV-1')
        errs['lambda_'] = u.Quantity(lambda_.std_dev, 'TeV-1')
        pars['reference'] = data['spec_ecpl_e_ref']
    else:
        raise ValueError('Invalid spec_type: {}'.format(spec_type))

    model = model_class(**pars)
    model.parameters.set_parameter_errors(errs)

    return model
