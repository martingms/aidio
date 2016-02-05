# Not working.
# https://ccrma.stanford.edu/~jos/filters/Definition_Simplest_Low_Pass.html
def simplestlowpass(it, init=0.0):
    for sa in it:
        yield sa + init
        init = sa

# Not working.
# https://stkrs.googlecode.com/svn/trunk/fodder/VCF/MoogVCF.c
# https://ccrma.stanford.edu/~jos/fp/
def moogvcf1(it, cutoff, res, rate=44100):
    assert cutoff >= 0.0 and cutoff <= (rate / 2), 'Cutoff out of range'
    assert res >= 0.0 and res <= 1.0, 'Resonance out of range'

    freq = cutoff / (rate / 2) # ? # Nyquist
    q = 1.0 - freq
    p = freq + 0.8 * freq * q
    f = p + p - 1.0
    q = res * (1.0 + 0.5 * q * (1.0 - q + 5.6 * q * q))

    (b0, b1, b2, b3, b4) = (0, 0, 0, 0, 0)
    for sa in it:
        # Feedback
        sa -= q * b4
        t1 = b1;  b1 = (sa + b0) * p - b1 * f
        t2 = b2;  b2 = (b1 + t1) * p - b2 * f
        t1 = b3;  b3 = (b2 + t2) * p - b3 * f
        b4 = (b3 + t1) * p - b4 * f
        # Clipping
        b4 = b4 - b4 * b4 * b4 * 0.166667
        b0 = sa

        yield b4
