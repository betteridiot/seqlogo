#!/usr/bin/env python3
import numpy as np
import pandas as pd
import seqLogo
import os
import pytest

def test_pwm():
    np.random.seed(42)
    random_pwm = np.random.dirichlet(np.ones(4), size=6)
    assert seqLogo.Pwm(random_pwm), "PWM could not be generated"

def test_pfm2pwm():
    np.random.seed(42)
    pfm = pd.DataFrame(np.random.randint(0, 36, size=(8, 4)))
    assert seqLogo.pfm2pwm(pfm), "PWM from PFM could not be generated"

def test_seqLogo_plot(tmpdir):
    file = tmpdir.join('test.svg')
    np.random.seed(42)
    pfm = pd.DataFrame(np.random.randint(0, 36, size=(8, 4)))
    pwm = seqLogo.pfm2pwm(pfm)
    seqLogo.seqLogo(pwm, filename = file.strpath)
    assert file.read()