# o3 discussion for python container plus Claude Caude Sandbox

## changes

We now use the Apify TypeScript SDK, as it has more features and Crawlee is more mature.
Adopt the approach accordingly.

## discussion

Below is the pattern most teams follow when they  

1. ship a slim production image, and  
2. work inside a richer Dev Container that adds editors, test tooling, Claude Code, etc.

──────────────────

1. Production (or “runtime”) image  
──────────────────
File `Dockerfile` in the repository root:

```Dockerfile
# ---- base runtime image ----
FROM python:3.12-slim            # only what the app really needs
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# project deps only (no linters, no test libs)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

• This image is the one your CI pushes to a registry and your
orchestration platform (ECS, K8s, etc.) pulls in production.  
• It stays small and has no build/debug conveniences.

──────────────────
2.  Dev Container image  
──────────────────
Put another Dockerfile inside `.devcontainer/` that *extends the first
stage* and layers on developer-only tools.

```Dockerfile
# .devcontainer/Dockerfile
# ---- dev layer built on top of the runtime stage ----
FROM --platform=$BUILDPLATFORM python:3.12-slim AS runtime      # ①
COPY --from=runtime / /                                         # ← bring in the prod layer

# Add Node and Claude Code
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @anthropic-ai/claude-code

# Dev-only Python tools
RUN pip install --no-cache-dir \
      pytest \
      mypy \
      black

# Nice-to-haves
RUN apt-get install -y git fzf zsh less procps

# Non-root user (required by most devcontainer features)
ARG USERNAME=vscode
RUN useradd -m $USERNAME && chown -R $USERNAME /app
USER $USERNAME
WORKDIR /app
ENV SHELL=/bin/zsh
```

Explanation of the first two lines:

• `FROM --platform=$BUILDPLATFORM python:3.12-slim AS runtime`  
 creates the same base stage as your production image.  
• `COPY --from=runtime / /`  
 pulls that filesystem into the dev layer so everything the app needs is
already present.

──────────────────
3.  devcontainer.json
──────────────────

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "my-app-dev",
  "dockerFile": "Dockerfile",
  "runArgs": [ "--init" ],
  "settings": {
    "terminal.integrated.defaultProfile.linux": "zsh"
  },
  "postCreateCommand": "pip install -r requirements-dev.txt",
  "features": {
    // optional Dev Container Features (GHCR) you’d like:
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  }
}
```

You can also use:

• `"build": { "context": "..", "dockerfile": ".devcontainer/Dockerfile" }`
if you want to keep the dev Dockerfile separate from the runtime one.

──────────────────
Why this layout works well
──────────────────

1. Single source of truth for runtime dependencies.  
&nbsp;&nbsp;‒ Your dev image literally copies the production stage, so it
can’t drift.

2. Fast local iteration.  
&nbsp;&nbsp;‒ The dev layer is cached; rebuilding only re-runs the “tools”
steps.

3. Small prod image.  
&nbsp;&nbsp;‒ The final image that ships contains Python and project libs
only—no Node, Claude CLI, or editors.

4. Easily reproducible CI.  
&nbsp;&nbsp;‒ Your CI pipeline can `docker build --target runtime .`
to guarantee it uses exactly the same layer the Dev Container is built
on.

──────────────────
Alternatives
──────────────────
• Use Dev Container *Features* instead of baking Node yourself:

```jsonc
"features": {
  "ghcr.io/devcontainers/features/python:3": {},
  "ghcr.io/devcontainers/features/node:20": {},
  "ghcr.io/devcontainers/features/common-utils:2": {}
}
```

 This lets you skip a custom Dockerfile entirely, but you lose the
“identical to prod” guarantee.

• Multi-stage single Dockerfile with build-time arg:

```Dockerfile
ARG DEV=false
RUN if [ "$DEV" = "true" ]; then npm install -g @anthropic-ai/claude-code; fi
```

 and in `devcontainer.json` pass `"build": { "args": { "DEV": "true" } }`.

──────────────────
Wrap-up
──────────────────
So yes—maintain a lean production Dockerfile in the project root, then
have a Dev Container Dockerfile that *extends* it and adds Node + Claude
Code and any other editors, linters, or test tools you need. This keeps
production small and stable while giving developers everything they want
inside VS Code.
