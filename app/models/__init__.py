# AUTO-EXPORT ALL SQLALCHEMY MODELS + SAFE LEGACY ALIASES (FINAL)

import pkgutil
import importlib
import inspect
from sqlalchemy.orm import DeclarativeMeta

__all__ = []
package_name = __name__

# --- Auto-export all real SQLAlchemy models ---
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{package_name}.{module_name}")
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, DeclarativeMeta):
            globals()[name] = obj
            __all__.append(name)

# --- Legacy / business aliases (SAFE, ORDERED) ---

# Users
if 'User' in globals():
    AppUser = User
    __all__.append('AppUser')

# BDA
if 'BDA' in globals():
    BDASale = BDA
    __all__.append('BDASale')

# Office / Cash
if 'CashHandover' in globals():
    OfficeCashDay = CashHandover
    OfficeCash = CashHandover
    OfficeExpense = CashHandover
    __all__.extend(['OfficeCashDay', 'OfficeCash', 'OfficeExpense'])

# Trips
if 'DeliveryTrip' in globals():
    Trip = DeliveryTrip
    __all__.append('Trip')

# Stock
if 'StockMovement' in globals():
    Stock = StockMovement
    __all__.append('Stock')
