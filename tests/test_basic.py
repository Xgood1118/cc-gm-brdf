# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brdf.core import brdf_value, build_lut, clamp01, ndf_ggx  # noqa: E402


def test_clamp():
    assert clamp01(-1) == 0
    assert clamp01(2) == 1
    assert clamp01(0.5) == 0.5


def test_ndf_positive():
    assert ndf_ggx(0.5, 0.3) > 0


def test_brdf_range():
    v = brdf_value(0.8, 0.8, 0.7, 0.6, 0.4)
    assert 0 <= v <= 1


def test_lut_shape():
    lut = build_lut(16, 4, 4)
    assert len(lut) == 4
    assert len(lut[0]) == 4
