import pkgutil, importlib, inspect
import app.models

print("MODEL MAP:\n")

for _, module_name, _ in pkgutil.walk_packages(
        app.models.__path__, app.models.__name__ + "."):
    module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_name:
            print(f"{name} -> {module_name}")
