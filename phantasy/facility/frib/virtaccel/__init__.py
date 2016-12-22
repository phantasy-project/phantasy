# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from .flame import build_virtaccel as build_flame_virtaccel
from .flame import VirtualAccelerator as FlameVirtualAccelerator

from .impact import build_virtaccel as build_impact_virtaccel
from .impact import VirtualAccelerator as ImpactVirtualAccelerator
