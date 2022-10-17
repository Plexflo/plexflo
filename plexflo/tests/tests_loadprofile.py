import unittest

from plexflo.loadprofiles.profiles import show, use, impact_of_policy_every_year_on_peak_kW

def test_load():

    df = use()
    if 'kW_multiplier' in df.columns and df.shape[0] == 24:
        return True