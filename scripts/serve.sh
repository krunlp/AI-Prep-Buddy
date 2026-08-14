#!/bin/sh
# Local preview.
#
#   ./scripts/serve.sh          full Jekyll build (needs Ruby + bundler)
#   ./scripts/serve.sh static   plain HTTP server, no Ruby required
#
# The static mode serves index.html, interview.html, simulator.html and
# roles.html correctly — they are hand-written HTML. Markdown pages
# (questions, answers, diagrams...) only render under Jekyll.
#
# A server is required either way: interview.html and simulator.html fetch
# data/*.json, and browsers block fetch() over file://.

set -e
cd "$(dirname "$0")/.."

if [ "$1" = "static" ]; then
  echo "Static preview on http://localhost:8000"
  echo "  works: index.html, interview.html, simulator.html, roles.html"
  echo "  not rendered: .md pages (use full Jekyll mode for those)"
  python3 -m http.server 8000
else
  if ! command -v bundle >/dev/null 2>&1; then
    echo "bundler not found. Either:"
    echo "  gem install bundler   # then re-run"
    echo "  ./scripts/serve.sh static   # no Ruby needed"
    exit 1
  fi
  [ -d vendor/bundle ] || bundle install --path vendor/bundle
  echo "Jekyll preview on http://localhost:4000/AI-Prep-Buddy/"
  bundle exec jekyll serve --livereload --baseurl "/AI-Prep-Buddy"
fi
