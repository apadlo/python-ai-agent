# Branch Protection Settings

This document describes the branch protection rules that should be configured for the `main` branch to ensure code quality and prevent accidental force pushes or deletions.

## Recommended Branch Protection Rules for `main`

To configure these settings, go to your repository on GitHub:
1. Navigate to **Settings** → **Branches**
2. Click **Add rule** or edit the existing rule for `main`
3. Configure the following settings:

### Protection Rules

#### Basic Protections
- ✅ **Require a pull request before merging**
  - Require approvals: 1 (recommended)
  - Dismiss stale pull request approvals when new commits are pushed
  
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Status checks that are required:
    - `lint-and-test` (from the CI workflow)

#### Advanced Protections
- ✅ **Require conversation resolution before merging**
  - All review comments must be resolved before merging

- ✅ **Do not allow bypassing the above settings**
  - Administrators are included in these restrictions

- ✅ **Restrict who can push to matching branches**
  - Only allow specific people, teams, or apps to push

#### Force Push and Deletion Protection
- ✅ **Do not allow force pushes**
  - Nobody should be able to force push to this branch

- ✅ **Do not allow deletions**
  - The main branch should never be deleted

## GitHub Workflows

The repository includes a CI workflow (`.github/workflows/ci.yml`) that runs the following checks:
- **Code linting** with flake8 to catch syntax errors and code quality issues
- **Code formatting** checks with black
- **Python syntax verification** to ensure all Python files compile successfully

These checks run automatically on:
- Every push to the `main` branch
- Every pull request targeting the `main` branch

## Benefits

These protections ensure:
1. **Code Quality**: All code must pass automated checks before being merged
2. **Review Process**: Changes require review and approval
3. **History Preservation**: Force pushes and branch deletions are prevented
4. **Collaboration**: Multiple developers can safely work on the codebase
5. **Traceability**: All changes are documented through pull requests

## Manual Configuration Required

⚠️ **Important**: Branch protection rules must be configured manually in the GitHub repository settings. This cannot be done through code in the repository itself. Follow the steps above to enable these protections.

## Alternative: Automated Configuration

For organizations managing multiple repositories, consider using:
- **GitHub CLI** (`gh api`) to configure branch protection via API
- **Terraform** with the GitHub provider for infrastructure-as-code approach
- **GitHub Apps** with appropriate permissions to manage repository settings

Example using GitHub CLI:
```bash
gh api -X PUT /repos/:owner/:repo/branches/main/protection \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=lint-and-test \
  -f enforce_admins=true \
  -f required_pull_request_reviews[required_approving_review_count]=1 \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

Replace `:owner` and `:repo` with your actual GitHub username/organization and repository name.
