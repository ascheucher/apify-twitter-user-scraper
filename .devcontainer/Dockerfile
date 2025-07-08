# based on https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile
# but with the same base image as the APIFY Actor Dockerfile
FROM apify/actor-node-playwright-chrome:22-1.53.2

# checks taken over from the production Dockerfile
RUN npm ls crawlee apify puppeteer playwright
RUN node check-playwright-version.mjs
# end of checks

ARG TZ
ENV TZ="$TZ"

# Install basic development tools and iptables/ipset
USER root
RUN apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update && \
  apt-get install -y less \
  git \
  procps \
  sudo \
  fzf \
  zsh \
  man-db \
  unzip \
  gnupg2 \
  gh \
  iptables \
  ipset \
  iproute2 \
  dnsutils \
  aggregate \
  jq \
  curl \
  vim


# Ensure 'node' user exists for devcontainer compatibility across images
RUN id -u node >/dev/null 2>&1 || useradd -ms /bin/zsh node

# Create claude user without sudo privileges
RUN useradd -ms /bin/zsh claude && \
  usermod -a -G node claude

# Ensure default node user has access to /usr/local/share
RUN mkdir -p /usr/local/share/npm-global && \
  chown -R node:node /usr/local/share

# Give both users access to npm global packages
RUN chown -R node:node /usr/local/share/npm-global && \
  chmod -R 775 /usr/local/share/npm-global

ARG USERNAME=node

# Persist bash history.
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
  && mkdir /commandhistory \
  && touch /commandhistory/.bash_history \
  && chown -R $USERNAME /commandhistory

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Create workspace and config directories and set permissions
RUN mkdir -p /workspace/main /home/node/.claude /home/claude/.claude && \
  chown -R node:node /workspace /home/node/.claude && \
  chown -R claude:claude /home/claude/.claude && \
  chmod -R 775 /home/node/.claude

WORKDIR /workspace/main

# Install git-delta as root but ensure both users can access it
RUN ARCH=$(dpkg --print-architecture) && echo "ARCH: $ARCH" && \
  wget "https://github.com/dandavison/delta/releases/download/0.18.2/git-delta_0.18.2_${ARCH}.deb" && \
  dpkg -i "git-delta_0.18.2_${ARCH}.deb" && \
  rm "git-delta_0.18.2_${ARCH}.deb"

# Set up non-root user
USER node

# Install global packages
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin

# Set the default shell to zsh rather than sh
ENV SHELL=/bin/zsh

# Default powerline10k theme
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.0/zsh-in-docker.sh)" -- \
  -p git \
  -p fzf \
  -a "source /usr/share/doc/fzf/examples/key-bindings.zsh" \
  -a "source /usr/share/doc/fzf/examples/completion.zsh" \
  -a "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
  -x

# Install Claude as node user (no sudo needed)
RUN npm config set registry https://verdaccio.hill.eremite.cc && \
  npm config set fetch-retries 2 && \
  npm config set fetch-retry-mintimeout 10000 && \
  npm config set fetch-retry-maxtimeout 10000 && \
  npm install --no-audit --force --loglevel verbose -g @anthropic-ai/claude-code backlog.md

# Copy and set up firewall script (as node user, with sudo access)
COPY init-firewall.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh && \
  echo "node ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/node-firewall && \
  chmod 0440 /etc/sudoers.d/node-firewall
USER node

# Set up claude user environment
USER claude
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin
ENV SHELL=/bin/zsh

# Set up zsh for claude user
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.0/zsh-in-docker.sh)" -- \
  -p git \
  -p fzf \
  -a "source /usr/share/doc/fzf/examples/key-bindings.zsh" \
  -a "source /usr/share/doc/fzf/examples/completion.zsh" \
  -x

USER node