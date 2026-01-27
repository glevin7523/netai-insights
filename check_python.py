import sys

print("=" * 50)
print("PYTHON ENVIRONMENT CHECK")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Virtual environment: {'venv' in sys.executable}")
print()

# Check basic packages
packages_to_check = [
    ("pip", None),
    ("setuptools", None),
]

for package, version in packages_to_check:
    try:
        if package == "pip":
            import pip
            print(f"✓ pip version: {pip.__version__}")
        elif package == "setuptools":
            import setuptools
            print(f"✓ setuptools installed")
    except ImportError:
        print(f"✗ {package} not installed")

print("\n" + "=" * 50)
print("Run the following command to update pip:")
print("python -m pip install --upgrade pip setuptools wheel")
print("=" * 50)