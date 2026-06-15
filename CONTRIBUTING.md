# Contributing to TTWars Bot Skills

## How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-skill`)
3. **Commit** your changes
4. **Push** to the branch (`git push origin feature/new-skill`)
5. **Open** a Pull Request

## What to Contribute

- **New skill patterns** for specific automation tasks
- **Example bots** for different use cases
- **Reference data** from other TTWars server instances
- **Bug fixes** in existing examples
- **Documentation** improvements
- **Translations** of game terms

## Skill File Guidelines

When adding to `skills/ttwars-automation/`:

1. Keep the SKILL.md focused and scannable
2. Use tables for reference data
3. Include code examples that are complete and runnable
4. Update the frontmatter description if adding new trigger conditions
5. Test with a real TTWars server instance before submitting

## Code Style

- Python examples should follow PEP 8
- Include docstrings for all classes and functions
- Use type hints where practical
- Keep examples self-contained (no external config files required)

## Reporting Issues

- Include the server URL you're targeting
- Provide the page HTML if parsing fails
- Note the Python version and library versions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
