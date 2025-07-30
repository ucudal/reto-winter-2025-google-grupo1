# reto-winter-2025-google

## Docs for devs

Use [uv](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)
as the dependency manager. On Windows you may need to restart your PC.

Avoid using `pip`, since that may make you install a dependency globally, and
other contributors won't be able to use it because of that. `uv` ensures your
builds are reproducible.

To add a dependency:

```bash
uv add name-of-dependency
```

To run the project:

```bash
uv run src/main.py # Or whichever file you want.
```

### TODOs

- [ ] Figure out how to make the google frontend thingy work with uv.
