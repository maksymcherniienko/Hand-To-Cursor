# Instructions for Coding Agents

Before changing code, read:

1. `docs/project-overview.md`
2. `docs/architecture.md`
3. `docs/decisions.md`
4. The root `README.md` and the specific source/configuration files involved in
   the task

Use the documentation as context, not as a substitute for inspecting current
code. If documentation and implementation disagree, verify the behavior in
code and update the documentation when the change makes it stale.

## Before implementation

- Briefly explain the planned realization to the user before making changes.
- List the files expected to change and why. Refine the list if inspection
  reveals additional necessary files.
- State any important assumptions or unresolved behavior choices; ask the user
  when a choice materially changes expected behavior.
- For a small, local feature, make a small, local change. Do not change the
  entire project globally or refactor unrelated components just to implement
  it.

## During implementation

- Explain the meaningful implementation steps and decisions as work proceeds;
  avoid narrating routine tool use.
- Follow existing module boundaries and preserve current behavior outside the
  requested scope.
- After implementing a feature, update the directly related documentation
  before writing the final response. Document the final behavior, configuration,
  usage, or architecture changes as applicable; do not leave the docs update as
  a follow-up item.
- Run the smallest relevant validation and report what it does and does not
  verify.

## After implementation

- Verify that the relevant documentation reflects the implemented feature.
- Summarize the changes and list the affected files.
- Report validation results.
- Identify known risks, limitations, or unverified runtime behavior that
  future developers should be aware of. Do not imply that hardware-dependent
  behavior was tested unless it was actually exercised.
