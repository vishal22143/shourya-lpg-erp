from app.core.base import Base
import app.models.auth
import app.models.office_aux

print("MODELS LOADED:")
print(list(Base.metadata.tables.keys()))
