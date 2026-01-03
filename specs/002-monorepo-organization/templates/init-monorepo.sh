#!/bin/bash
# Monorepo Initialization Script
# Usage: ./init-monorepo.sh [monorepo-name]

set -e

REPO_NAME="${1:-my-monorepo}"

echo "Initializing monorepo: $REPO_NAME"

# Create root directory
mkdir -p "$REPO_NAME"
cd "$REPO_NAME"

# Initialize git
git init
echo "✓ Git initialized"

# Create directory structure
mkdir -p .spec-kit/{templates,scripts}
mkdir -p apps/{frontend,backend}
mkdir -p specs/{features,api/{endpoints,schemas},database/{entities,migrations},ui/{components,design-tokens}}

echo "✓ Directory structure created"

# Copy .gitignore
if [ -f "../.gitignore.template" ]; then
    cp ../.gitignore.template .gitignore
    echo "✓ .gitignore created"
fi

# Copy Spec-Kit config
if [ -f "../spec-kit-config.yaml.template" ]; then
    cp ../spec-kit-config.yaml.template .spec-kit/config.yaml
    echo "✓ Spec-Kit config created"
fi

# Copy CLAUDE.md files
if [ -f "../CLAUDE.md.root.template" ]; then
    cp ../CLAUDE.md.root.template CLAUDE.md
fi
if [ -f "../CLAUDE.md.frontend.template" ]; then
    cp ../CLAUDE.md.frontend.template apps/frontend/CLAUDE.md
fi
if [ -f "../CLAUDE.md.backend.template" ]; then
    cp ../CLAUDE.md.backend.template apps/backend/CLAUDE.md
fi
echo "✓ CLAUDE.md files created"

# Copy README files
if [ -f "../README.md.template" ]; then
    sed "s/{monorepo-name}/$REPO_NAME/g" ../README.md.template > README.md
fi
if [ -f "../README.frontend.md.template" ]; then
    cp ../README.frontend.md.template apps/frontend/README.md
fi
if [ -f "../README.backend.md.template" ]; then
    cp ../README.backend.md.template apps/backend/README.md
fi
echo "✓ README files created"

# Create placeholder files for specs
touch specs/api/versioning.md
touch specs/database/schema.md
touch specs/ui/interactions.md

echo ""
echo "================================"
echo "Monorepo '$REPO_NAME' initialized successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. cd $REPO_NAME"
echo "2. Review and customize CLAUDE.md files"
echo "3. Initialize frontend: cd apps/frontend && npx create-next-app@latest ."
echo "4. Initialize backend: cd apps/backend && create pyproject.toml"
echo "5. Start creating feature specs in specs/features/"
echo ""
