# cdi-api
Common Data Index API to access registry of data catalogs, raw index and search index

## Development

`cdiapi` is implemented in asynchronous, typed Python using the FastAPI framework. We're happy to see any bug fixes, improvements or extensions from the community. For local development without Docker, install the package into a fresh virtual Python environment like this:

```bash
git clone https://github.com/commondataio/cdi-api.git
cd cdi-api
pip install -e .
```

This will install a broad range of dependencies, including `numpy`, `scikit-learn` and `pyicu`, which are binary packages that may require a local build environment. For `pyicu` in particular, refer to the [package documentation](https://pypi.org/project/PyICU/).

### Running the server

You can run the web server like this:

```bash
hypercorn cdiapi.app:app
```

### License and Support

``cdi-api`` is licensed according to the MIT license terms documented in ``LICENSE``. Using the service in a commercial context may require a license from Common Data Index.

### Use prepared scripts

* run_int.sh - Internal version of the cdi-api (hidden behind Kong)
* run_public.sh - Public version of the cdi-api (used by dateno.io search)
