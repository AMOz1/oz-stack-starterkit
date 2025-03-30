# Migration Guide

This document provides information about migrating between different versions of dependencies used in this starter kit, particularly focusing on Tailwind CSS and DaisyUI.

## Migrating to Tailwind CSS 4.x

Tailwind CSS 4.x introduces several significant changes from version 3.x. Here's how to migrate:

### Key Changes in Tailwind CSS 4.x

1. **New Configuration Format**
   - Some configuration options have changed
   - Check the official migration guide for full details

2. **New Default Utilities**
   - Several utilities that were previously in plugins are now built-in
   - Some utilities have been renamed or modified

3. **Performance Improvements**
   - Faster build times and smaller CSS output
   - Better tree-shaking of unused styles

### Migration Steps

1. Update your tailwind.config.js if necessary
2. Check your HTML templates for any class names that need updating
3. Rebuild your CSS file to ensure all changes are applied
4. Test across different screen sizes and browsers

## Migrating to DaisyUI 5.x

DaisyUI 5.x includes several changes from version 3.x that you should be aware of.

### Key Changes in DaisyUI 5.x

1. **Component Updates**
   - Some components have new class names or behavior
   - New components and variants have been added

2. **Theme System**
   - Enhanced theming capabilities
   - Updated default themes

3. **Base Component Changes**
   - Some base components have modified styling
   - Check your custom component extensions

### Migration Steps

1. Review the DaisyUI 5.x changelog
2. Update component class names in your templates
3. Test components with different themes
4. Check custom component styles that might be affected

## Handling Circular Dependencies

If you encounter circular dependency errors during CSS build:

```
CssSyntaxError: tailwindcss: <css input>: You cannot `@apply` the `btn-primary` utility here because it creates a circular dependency.
```

### How to Fix Circular Dependencies

1. **Identify the Problem**
   - Look for component classes used with `@apply` inside component definitions
   - For example, using `@apply btn-primary` inside a custom component

2. **Solution Approaches**
   - Avoid using `@apply` with component classes inside other component definitions
   - Use utility classes instead of component classes when extending components
   - Create more specific utility-based classes instead of nesting components

3. **Example Fix**

   Instead of:
   ```css
   .my-custom-button {
     @apply btn-primary rounded-lg;
   }
   ```

   Use:
   ```css
   .my-custom-button {
     @apply btn rounded-lg bg-primary text-primary-content;
   }
   ```

## Version Compatibility Matrix

| Tailwind CSS | DaisyUI | Status |
|--------------|---------|--------|
| 4.x | 5.x | ✅ Fully supported |
| 3.x | 5.x | ⚠️ May have issues |
| 4.x | 3.x | ⚠️ May have issues |
| 3.x | 3.x | ⚠️ Not recommended |

## Additional Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [DaisyUI Documentation](https://daisyui.com/docs)
- [VERSIONS.md](VERSIONS.md) - Information about version management
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Troubleshooting common issues