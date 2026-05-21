This document collects best practices for writing high-quality packages in Macaulay2. It is intended as a practical guide for package authors at any experience level, covering documentation, testing, external program interfaces, and general code quality. Following these guidelines will help ensure your package is readable, maintainable, and useful to the broader Macaulay2 community.

## 1. Documentation

- For medium and large packages, include a list of featured functions in the description block, organized into thematic groups if needed, with links to examples.
- The description block should give a high-level overview of the package's purpose and capabilities — it should not contain tutorials or detailed examples, but may link to them.
- Avoid putting examples directly in the description block unless there is a compelling reason.

## 2. Testing

- Keep all tests in a dedicated file or directory, separate from the main source code.
- Write tests for every exported function at minimum; aim for full coverage of internal functions as well.
- Name every test with a descriptive comment immediately before it, indicating what behavior is being tested (not just which function).
- Tests should cover edge cases and expected failure modes, not only the happy path.

## 3. Interfacing with external programs

- If your package calls external programs (e.g., `gfan`, `Normaliz`, `Bertini`), do so through a dedicated interface package with the word "interface" in the name, rather than calling them directly. More precisely, run commands should only exist in interface packages.
- Cite all external programs your package depends on in the package documentation and cite them appropriately.

## 4. Code quality and style

- Follow the Macaulay2 package [style guide](https://github.com/Macaulay2/M2/wiki/Package-Writing-Style-Guide).
- Be consistent in how you organize methods, documentation, and files across the whole package.
- Comment your code appropriately.
- Only export symbols (methods, types, constants) that are intended for end users; keep implementation details unexported.
- Before implementing new functionality, check whether existing packages already provide it — avoid reinventing the wheel.
- Avoid unnecessary dependencies; only rely on other packages when they provide clear value.