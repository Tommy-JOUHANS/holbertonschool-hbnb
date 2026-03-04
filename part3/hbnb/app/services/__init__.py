"""
Services package initializer.
Provides a singleton facade instance.
"""

from hbnb.app.services.facade import HBnBFacade

# Singleton instance
facade = HBnBFacade()

__all__ = ["facade", "HBnBFacade"]