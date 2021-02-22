import numpy as np
import patsy
import statsmodels.api as sm


def polynomial(t, v, deg=3, t_pred=None):
    """ Smooth v-data using polynomial of given degree
    """
    p = np.polyfit(t, v, deg=deg)
    if t_pred is None:
        return np.polyval(p, t)
    else:
        return np.polyval(p, t_pred)


def linear_segments(t, v, num_segments=20, t_pred=None):
    """ Smooth v-data by fitting num_segments equally spaced linear segments
    """
    assert len(t) > num_segments, 'number of segments cannot be more than number of datapoints'
    return spline(t, v, patsy.bs, num_knots=num_segments, params={'deg': 1}, t_pred=t_pred)


def b_spline(t, v, knot_fraction=0.25, num_knots=None, params=None, t_pred=None):
    """ Smooth v-data using B-spline
    """
    return spline(t, v, patsy.bs, knot_fraction, num_knots, params, t_pred=t_pred)


def natural_spline(t, v, knot_fraction=0.25, num_knots=None, params=None, t_pred=None):
    """ Smooth v-data using a natural cubic spline
    """
    return spline(t, v, patsy.cr, knot_fraction, num_knots, params, t_pred=t_pred)


def cubic_spline(t, v, knot_fraction=0.25, num_knots=None, params=None, t_pred=None):
    """ Smooth v-data using a cubic spline
    """
    return spline(t, v, patsy.cc, knot_fraction, num_knots, params, t_pred=t_pred)


def spline(t, v, spline_basis, knot_fraction=0.25, num_knots=None, params=None, t_pred=None):
    """ Smooth using a given spline basis with num_knots
    If 'knots' in params, use those knot locations
    If 'df" in params, set num_knots = params['df']
    If num_knots not given, set num_knots = floor(len(t)*knot_fraction)
    If t_pred given, return predicted values for different time coordinates
    """
    params_ = {} if params is None else {key: params[key] for key in params if key != 'df'}
    # Setup basis function, need to define knots explicitly for prediction to work correctly
    # (I.e. we need to use the same knots for prediction as for fitting!)
    if 'knots' not in params:
        if 'df' in params:
            num_knots_ = params['df']
        else:
            num_knots_ = int(len(t) * knot_fraction) if num_knots is None else num_knots
        knots = tuple(np.linspace(t[0], t[-1], num_knots_))
        params_['knots'] = knots

    base_function = spline_basis(t, **params_)

    model = patsy.dmatrix(base_function)
    fit = sm.GLM(v, model).fit()

    if t_pred is None:
        smoothened = fit.predict(model)
    else:
        pred_base = spline_basis(t_pred, **params_)
        pred_model = patsy.dmatrix(pred_base)
        smoothened = fit.predict(pred_model)
        print('updated')

    return np.array(smoothened)
