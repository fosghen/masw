import math
import numpy as np
from scipy import fftpack


def _ensure_int(x, name='unknown', must_be='an int'):
    """Ensure a variable is an integer."""
    # This is preferred over numbers.Integral, see:L
    # https://github.com/scipy/scipy/pull/7351#issuecomment-299713159L
    try:
        # someone passing True/False is much more likely to be an error than
        # intentional usage
        if isinstance(x, bool):
            raise TypeError()
        x = int(operator.index(x))
    except TypeError:
        raise TypeError('%s must be %s, got %s' % (name, must_be, type(x)))
    return x
    

def _validate_type(item, types=None, item_name=None, type_name=None):
    """Validate that `item` is an instance of `types`.

    Parameters
    ----------
    item : object
        The thing to be checked.
    types : type | str | tuple of types | tuple of str
         The types to be checked against.
         If str, must be one of {'int', 'str', 'numeric', 'info', 'path-like'}.
    """
    if types == "int":
        _ensure_int(item, name=item_name)
        return  # terminate prematurely
    elif types == "info":
        from mne.io import Info as types

    if not isinstance(types, (list, tuple)):
        types = [types]

    check_types = sum(((type(None),) if type_ is None else (type_,)
                       if not isinstance(type_, str) else _multi[type_]
                       for type_ in types), ())
    if not isinstance(item, check_types):
        if type_name is None:
            type_name = ['None' if cls_ is None else cls_.__name__
                         if not isinstance(cls_, str) else cls_
                         for cls_ in types]
            if len(type_name) == 1:
                type_name = type_name[0]
            elif len(type_name) == 2:
                type_name = ' or '.join(type_name)
            else:
                type_name[-1] = 'or ' + type_name[-1]
                type_name = ', '.join(type_name)
        raise TypeError('%s must be an instance of %s, got %s instead'
                        % (item_name, type_name, type(item),))
                        
def _check_input_st(x_in, n_fft):
    """Aux function."""
    # flatten to 2 D and memorize original shape
    n_times = x_in.shape[-1]

    def _is_power_of_two(n):
        return not (n > 0 and ((n & (n - 1))))

    if n_fft is None or (not _is_power_of_two(n_fft) and n_times > n_fft):
        # Compute next power of 2
        n_fft = 2 ** int(math.ceil(math.log(n_times, 2)))
    elif n_fft < n_times:
        raise ValueError("n_fft cannot be smaller than signal size. "
                         "Got %s < %s." % (n_fft, n_times))
    if n_times < n_fft:
        # warn('The input signal is shorter ({}) than "n_fft" ({}). '
             # 'Applying zero padding.'.format(x_in.shape[-1], n_fft))
        zero_pad = n_fft - n_times
        pad_array = np.zeros(x_in.shape[:-1] + (zero_pad,), x_in.dtype)
        x_in = np.concatenate((x_in, pad_array), axis=-1)
    else:
        zero_pad = 0
    return x_in, n_fft, zero_pad


def _precompute_st_windows(n_samp, start_f, stop_f, sfreq, width):
    """Precompute stockwell Gaussian windows (in the freq domain)."""
    tw = fftpack.fftfreq(n_samp, 1. / sfreq) / n_samp
    tw = np.r_[tw[:1], tw[1:][::-1]]

    k = width  # 1 for classical stowckwell transform
    f_range = np.arange(start_f, stop_f, 1)
    windows = np.empty((len(f_range), len(tw)), dtype=np.complex128)
    for i_f, f in enumerate(f_range):
        if f == 0.:
            window = np.ones(len(tw))
        else:
            window = ((f / (np.sqrt(2. * np.pi) * k)) *
                      np.exp(-0.5 * (1. / k ** 2.) * (f ** 2.) * tw ** 2.))
        window /= window.sum()  # normalisation
        windows[i_f] = fftpack.fft(window)
    return windows


    
def _st_power(x, start_f, zero_pad, decim, W):
    """Aux function."""
    n_samp = x.shape[-1]
    n_out = (n_samp - zero_pad)
    n_out = n_out // decim + bool(n_out % decim)
    psd = np.zeros((len(W), n_out), dtype=np.complex64)
    X = fftpack.fft(x)
    XX = np.concatenate([X, X], axis=-1)
    for i_f, window in enumerate(W):
        f = start_f + i_f
        ST = fftpack.ifft(XX[:, f:f + n_samp] * window)
        if zero_pad > 0:
            TFR = ST[:, :-zero_pad:decim]
        else:
            TFR = ST[:, ::decim]       
        psd[i_f] = np.average(TFR, axis=0)
    return psd

def stran(data, sfreq, fmin=None, fmax=None, n_fft=None,
                        width=1.0, decim=1):
    """Compute power and intertrial coherence using Stockwell (S) transform.

    Same computation as `~mne.time_frequency.tfr_stockwell`, but operates on
    :class:`NumPy arrays <numpy.ndarray>` instead of `~mne.Epochs` objects.

    See :footcite:`Stockwell2007,MoukademEtAl2014,WheatEtAl2010,JonesEtAl2006`
    for more information.

    Parameters
    ----------
    data : ndarray, shape (n_epochs, n_channels, n_times)
        The signal to transform.
    sfreq : float
        The sampling frequency.
    fmin : None, float
        The minimum frequency to include. If None defaults to the minimum fft
        frequency greater than zero.
    fmax : None, float
        The maximum frequency to include. If None defaults to the maximum fft.
    n_fft : int | None
        The length of the windows used for FFT. If None, it defaults to the
        next power of 2 larger than the signal length.
    width : float
        The width of the Gaussian window. If < 1, increased temporal
        resolution, if > 1, increased frequency resolution. Defaults to 1.
        (classical S-Transform).
    decim : int
        The decimation factor on the time axis. To reduce memory usage.
    return_itc : bool
        Return intertrial coherence (ITC) as well as averaged power.
    %(n_jobs)s

    Returns
    -------
    st_power : ndarray
        The multitaper power of the Stockwell transformed data.
        The last two dimensions are frequency and time.
    itc : ndarray
        The intertrial coherence. Only returned if return_itc is True.
    freqs : ndarray
        The frequencies.

    See Also
    --------
    mne.time_frequency.tfr_stockwell
    mne.time_frequency.tfr_multitaper
    mne.time_frequency.tfr_array_multitaper
    mne.time_frequency.tfr_morlet
    mne.time_frequency.tfr_array_morlet

    References
    ----------
    .. footbibliography::
    """
    _validate_type(data, np.ndarray, 'data')
    if data.ndim != 3:
        raise ValueError(
            'data must be 3D with shape (n_epochs, n_channels, n_times), '
            f'got {data.shape}')
    n_epochs, n_channels = data.shape[:2]
    n_out = data.shape[2] // decim + bool(data.shape[-1] % decim)
    data, n_fft_, zero_pad = _check_input_st(data, n_fft)

    freqs = fftpack.fftfreq(n_fft_, 1. / sfreq)
    if fmin is None:
        fmin = freqs[freqs > 0][0]
    if fmax is None:
        fmax = freqs.max()

    start_f = np.abs(freqs - fmin).argmin()
    stop_f = np.abs(freqs - fmax).argmin()
    freqs = freqs[start_f:stop_f]

    W = _precompute_st_windows(data.shape[-1], start_f, stop_f, sfreq, width)
    n_freq = stop_f - start_f
    psd = np.zeros((n_channels, n_freq, n_out), dtype=np.complex64)
    for c in range(n_channels):
        psd[c] = _st_power(data[:, c, :], start_f, zero_pad, decim, W)
    
    return np.squeeze(psd)

