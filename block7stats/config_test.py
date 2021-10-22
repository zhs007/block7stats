# -*- coding:utf-8 -*-
import pytest
from block7stats.config import loadConfig


def test_loadConfig():
    cfg = loadConfig('./tests/config.yaml')

    assert cfg['urlroot'] == 'https://block7serv.heyalgo.io/v1/games'
    assert cfg['token'] == '123abc'
    assert cfg['startUID'] == 579
