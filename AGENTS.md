# AGENTS.md

- Always use uv instead of pip
- Add dependencies by running `uv add`, not by editing pyproject.toml directly.
- Format the code with `ruff format` and check it with `ruff check` and `uv run pyright`.

## Coding style

- No hacky things. Think carefully and implement things in a neat, ordered way. Solve problems with thinking, not with trying a lot of things until one works.
- Type-checker and linters are a central, core part of the coding style, not afterthoughts. Do not try to circumvent them, actually fix the problems they point out. `cast` and type ignores are forbidden.
- Do not write slop. No defensive code, no entire new functions for a single line of code, no try/catch, isinstance or type conversions "just in case". Things in this category that you should avoid include, among other things:
  - Using `.get` or `getattr` instead of indexing a dictionary or accessing an attribute.
  - Trying to normalize malformed data instead of failing fast.
  - Calling list()/set()/tuple()/etc. on something that is already a list/set/tuple.
  - Handling exceptions we are not raising ourselves. When calling a function of our codebase, examine it and only put it in a try/except if it actually raises. This does not mean "just cleanup in a finally" or "trace and raise again"; it really means assume it won't happen. 
  - <=3 statements or few helper functions that are only called once.
  - `del` keyword. If a function needs to have unused parameters to satisfy a
    signature, use `_`.
  - "alias" functions that just call another function.
- Always make the minimal changes to achieve the desired result.
- Keep type-safety as a primary concern. No `cast`, `type: ignore` or `Any`; avoid untyped dicts. All data moving within our app should be fully typed. All external data coming in (i.e. from disk or the network) should be validated with pydantic. asserts are generally acceptable to get around pytorch's bad stubs. 

### Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## Theory of mind
We are doing a report to be delivered as a final result and writing code that will only be seen by my teammates. I need you to really think twice about things and have theory of mind here. If I tell you not to do X, then just don't do X, don't say in the report "we don't do X" in the same way that we don't say that we had lunch while we trained the models. If I tell you to keep things aligned with the class content, don't say in the report "class-aligned", because of course it should be. You need to understand the difference between private process and public results. This is a report, not a diary. You also need to keep a mental model of the reader in your mind. Not because you know what "forensic" means or you found a paper about it, it means that the reader should have the slightest idea of what that word means. The knowledge of the reader is exactly the class content in ./md. 
