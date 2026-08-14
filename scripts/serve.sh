#!/bin/sh
# Local preview for AI Prep Buddy.
#
#   ./scripts/serve.sh           static server  — no Ruby needed  (default)
#   ./scripts/serve.sh jekyll    full Jekyll build — renders .md pages too
#
# A server is required either way. interview.html and simulator.html fetch
# data/*.json, and browsers block fetch() over file://, so opening the HTML
# files directly leaves those pages blank.
#
# localhost counts as a secure context, so the microphone works without HTTPS.

set -e
cd "$(dirname "$0")/.."

PORT="${PORT:-8000}"

serve_static() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found. On macOS: xcode-select --install"
    exit 1
  fi
  cat <<TXT

  Static preview → http://localhost:$PORT

  Works:      index.html · interview.html · simulator.html · roles.html
  Not built:  markdown pages (questions, answers, diagrams, patterns...)
              run './scripts/serve.sh jekyll' for those

  Voice needs Chrome, Edge or Safari. Grant microphone access when prompted.

TXT
  python3 -m http.server "$PORT"
}

serve_jekyll() {
  if ! command -v ruby >/dev/null 2>&1; then
    echo "ruby not found. Install one, then retry:"
    echo "  brew install ruby        # then add it to PATH per brew's instructions"
    echo "Or skip Ruby entirely:  ./scripts/serve.sh"
    exit 1
  fi

  RUBY_V=$(ruby -e 'print RUBY_VERSION')
  RUBY_MAJOR=$(echo "$RUBY_V" | cut -d. -f1)
  RUBY_MINOR=$(echo "$RUBY_V" | cut -d. -f2)
  RUBY_PATH=$(command -v ruby)

  # macOS ships Ruby 2.6.x at /usr/bin/ruby. It is too old for the
  # github-pages gem, and installing gems into it needs sudo. Do not use it.
  if [ "$RUBY_PATH" = "/usr/bin/ruby" ] || [ "$RUBY_MAJOR" -lt 3 ] && [ "$RUBY_MINOR" -lt 7 ]; then
    cat <<TXT
Found system Ruby $RUBY_V at $RUBY_PATH — too old for Jekyll, and it needs
sudo to install gems. Install a user-owned Ruby instead:

  brew install ruby
  echo 'export PATH="/opt/homebrew/opt/ruby/bin:\$PATH"' >> ~/.zshrc
  exec zsh
  ./scripts/serve.sh jekyll

Or skip Ruby entirely — the interview and simulator pages work fine in
static mode:

  ./scripts/serve.sh

TXT
    exit 1
  fi

  if ! command -v bundle >/dev/null 2>&1; then
    echo "Installing bundler..."
    gem install bundler
  fi

  # 'bundle install --path' is deprecated on Bundler 2.1+; configure it instead.
  if [ ! -d vendor/bundle ]; then
    bundle config set --local path vendor/bundle
    bundle install
  fi

  echo
  echo "  Jekyll preview → http://localhost:4000/AI-Prep-Buddy/"
  echo
  bundle exec jekyll serve --livereload --baseurl "/AI-Prep-Buddy"
}

case "$1" in
  jekyll) serve_jekyll ;;
  static|"") serve_static ;;
  *) echo "usage: ./scripts/serve.sh [static|jekyll]"; exit 1 ;;
esac
