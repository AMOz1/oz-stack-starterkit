# Version Management Guide

This document provides information about the specific versions of key dependencies used in this starter kit and how to maintain them.

## Required Versions

This starter kit is designed to work with specific versions of key dependencies:

| Dependency | Required Version | Description |
|------------|------------------|-------------|
| Tailwind CSS | 4.x | Utility-first CSS framework |
| DaisyUI | 5.x | Component library for Tailwind CSS |
| Node.js | ≥14.0.0 | JavaScript runtime |
| npm | ≥6.0.0 | Package manager for Node.js |
| Python | ≥3.8 | Programming language |

## Version Verification

We've included tools to help you verify and fix version mismatches:

### Check Current Versions

```bash
# For Node.js dependencies
npm list tailwindcss daisyui

# For Python version
python --version

# For npm version
npm --version
```

### Automated Verification

Run the provided verification script:

```bash
npm run verify-versions
```

This script checks for the correct versions of Tailwind CSS and DaisyUI and reports any issues.

### Fixing Version Mismatches

If you need to fix version issues:

```bash
npm run fix-versions
```

This will install the correct versions of Tailwind CSS and DaisyUI.

## Manual Installation

If you need to manually install the correct versions:

```bash
# Install Tailwind CSS 4.x and DaisyUI 5.x
npm install tailwindcss@^4.0.0 daisyui@^5.0.9 --save
```

## Breaking Changes and Compatibility

### Tailwind CSS 4.x Changes

Tailwind CSS 4.x introduces several changes from version 3.x:

- New utilities and variants
- Some utilities have been renamed or modified
- Configuration changes in tailwind.config.js
- Performance improvements

### DaisyUI 5.x Changes

DaisyUI 5.x includes these changes from version 3.x:

- New and updated components
- Modified class names for some components
- Theme system enhancements
- Bug fixes and performance improvements

## Troubleshooting Version Issues

If you encounter issues with versions:

1. Clear npm cache: `npm cache clean --force`
2. Delete node_modules: `rm -rf node_modules`
3. Reinstall dependencies: `npm install`
4. Run version verification: `npm run verify-versions`
5. Fix versions if needed: `npm run fix-versions`

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Version Update Policy

When new versions of Tailwind CSS or DaisyUI are released:

1. Test compatibility with the new version in a development environment
2. Update version requirements in package.json
3. Update the version verification script (verify-versions.js)
4. Document any breaking changes in this file
5. Update the fix-versions script in package.json