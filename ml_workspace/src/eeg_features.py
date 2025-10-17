import numpy as np
from scipy.signal import welch, find_peaks
from scipy.integrate import simpson  # <-- THIS LINE IS CHANGED

def calculate_band_power(data, sf, band, window_sec=None, relative=False):
    """
    Calculate the power in a specific frequency band.
    """
    low, high = band
    if window_sec is not None:
        nperseg = window_sec * sf
    else:
        nperseg = len(data)

    freqs, psd = welch(data, sf, nperseg=nperseg)
    idx_band = np.logical_and(freqs >= low, freqs <= high)
    freq_res = freqs[1] - freqs[0]

    # Compute absolute power using Simpson's rule
    band_power = simpson(psd[idx_band], dx=freq_res)  # <-- THIS LINE IS CHANGED

    if relative:
        total_power = simpson(psd, dx=freq_res)  # <-- THIS LINE IS CHANGED
        if total_power == 0:
            return 0.0
        return band_power / total_power
    else:
        return band_power

def detect_spikes(data, sf, prominence=0.5, width=1):
    """
    Detects spikes in an EEG signal.
    """
    normalized_data = data / np.std(data)
    height_threshold = 3 * np.std(normalized_data)
    peaks, _ = find_peaks(
        normalized_data, 
        prominence=prominence, 
        width=width,
        height=height_threshold
    )
    return len(peaks)