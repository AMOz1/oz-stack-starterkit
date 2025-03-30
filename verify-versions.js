#!/usr/bin/env node

const chalk = require('chalk');
const semver = require('semver');
const packageJson = require('./package.json');

// Define required versions
const REQUIRED_VERSIONS = {
  'tailwindcss': {
    required: '^4.0.0',
    name: 'Tailwind CSS',
  },
  'daisyui': {
    required: '^5.0.9',
    name: 'DaisyUI',
  }
};

// Check installed versions
async function checkVersions() {
  let hasErrors = false;
  
  for (const [pkg, info] of Object.entries(REQUIRED_VERSIONS)) {
    try {
      const installedPkg = require(`${pkg}/package.json`);
      const installedVersion = installedPkg.version;
      
      if (!semver.satisfies(installedVersion, info.required)) {
        console.error(chalk.red(`❌ ${info.name} version mismatch!`));
        console.error(chalk.red(`   Required: ${info.required}`));
        console.error(chalk.red(`   Installed: ${installedVersion}`));
        console.error(chalk.yellow(`   Run: npm install ${pkg}@${info.required} --save`));
        hasErrors = true;
      } else {
        console.log(chalk.green(`✅ ${info.name} version: ${installedVersion}`));
      }
    } catch (e) {
      console.error(chalk.red(`❌ ${info.name} is not installed!`));
      console.error(chalk.yellow(`   Run: npm install ${pkg}@${info.required} --save`));
      hasErrors = true;
    }
  }
  
  if (hasErrors) {
    console.error(chalk.red('\n⚠️ Some dependencies have version mismatches. Please fix them before continuing.\n'));
    console.error(chalk.yellow('Run: npm run fix-versions'));
    process.exit(1);
  } else {
    console.log(chalk.green('\n✅ All dependencies have correct versions.\n'));
  }
}

checkVersions();