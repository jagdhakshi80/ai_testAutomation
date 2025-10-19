#!/usr/bin/env python3
import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip()

print("🔍 Verifying Git Push")
print("=" * 30)

# Check current branch
success, branch = run_cmd("git branch --show-current")
print(f"📁 Current branch: {branch}")

# Check if branch exists on remote
success, remote_branches = run_cmd("git ls-remote --heads origin")
if branch in remote_branches:
    print("✅ Branch exists on remote")
else:
    print("❌ Branch not found on remote")
    sys.exit(1)

# Check latest commit
success, latest_commit = run_cmd("git log --oneline -1")
print(f"📝 Latest commit: {latest_commit}")

print("\\n🎉 Git push successful! Ready to create PR.")
print(f"🔗 PR URL: https://github.com/jagdhakshi80/ai_testAutomation/compare/main...{branch}")
