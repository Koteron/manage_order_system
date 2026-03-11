"""
Rate Limiting Configuration.

This module centralizes the SlowAPI Limiter instance to prevent 
circular imports. It enforces global request thresholds to protect 
the service from brute-force attacks and resource exhaustion.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["500/hour", "10/minute"],
)