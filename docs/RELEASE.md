# Release

The release process is run with github actions. To release a new version:

1. Update the version number in `wagtail_jotform/__init__.py`

2. Update the changelog in `docs/CHANGELOG.md`

3. Commit and push the changes

4. Create a new release in github, with the tag name `X.X.X` and the release title `X.X.X`

5. The release will be built and published to pypi automatically
