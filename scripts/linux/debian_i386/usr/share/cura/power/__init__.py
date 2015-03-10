# coding=utf-8
"""
Provides crossplatform checking of current power source, battery warning level and battery time remaining estimate.
Allows you to add observer for power notifications if platform supports it.

Usage:
    from power import PowerManagement, PowerManagementObserver # Automatically imports platform-specific implementation

    class Observer(PowerManagementObserver):
        def on_power_sources_change(self, power_management):
            print "Power sources did change."

        def on_time_remaining_change(self, power_management):
            print "Time remaining did change."

    # class Observer(object):
    #     ...
    # PowerManagementObserver.register(Observer)
"""
__author__ = 'kulakov.ilya@gmail.com'
__version__ = '1.2'

from sys import platform
from power.common import *


try:
    if platform.startswith('darwin'):
        from power.darwin import PowerManagement
    elif platform.startswith('freebsd'):
        from power.freebsd import PowerManagement
    elif platform.startswith('win32'):
        from power.win32 import PowerManagement
    elif platform.startswith('linux'):
        from power.linux import PowerManagement
    else:
        raise RuntimeError("{platform} is not supported.".format(platform=platform))
except RuntimeError as e:
    import warnings
    warnings.warn("Unable to load PowerManagement for {platform}. No-op PowerManagement class is used: {error}".format(error=str(e), platform=platform))
    from power.common import PowerManagementNoop as PowerManagement
