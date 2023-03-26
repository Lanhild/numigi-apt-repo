# numigi-apt-repo
// Repository used to host custom hooks and packages used in [Numigi](https://numigi.com) laptops.

## Produce a release
1. Place all your packages into the main pool, named accordingly to the conventions of the repository

2. Run the build script in the current directory
```bash
python3 gen-release.py
```

3. Commit your changes

Your package repository should be ready after building.