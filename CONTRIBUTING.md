Contributing
============

Thank you for contributing! This project is a small sample framework — contributions that clarify usage, add tests, or improve automation are welcome.

How to contribute
- Fork the repository and create a feature branch.
- Make changes with clear, focused commits.

Suggested workflow
1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run tests locally:

```powershell
python run_tests.py
```

3. Add a feature file under `features/` and implement step definitions in `features/steps/`.
4. Add utilities to `utils/` where appropriate.
5. Run the full test suite and ensure reports are generated in `reports/`.

Commit message guidance
- Use conventional commit style where practical, e.g. `feat:`, `fix:`, `docs:`.

Submitting a pull request
- Create a PR against the `main` branch.
- Include a brief description of your change and why it helps.

License and code of conduct
- This sample doesn't include a license — add one if you plan to reuse this code in a public project.
