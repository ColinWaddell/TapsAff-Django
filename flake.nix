{
  description = "TapsAff Django dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        # Pin to 3.13 - the most recent Django 5.2 LTS officially supports.
        # Switch to pkgs.python314 when you're ready to leapfrog.
        python = pkgs.python313;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv          # venv + dependency management
            pkgs.redis       # production cache backend; used in dev too
            pkgs.ruff        # linter + formatter (replaces pylint/isort/etc)
            pkgs.nodejs      # Gruntfile.js / SCSS pipeline
          ];

          shellHook = ''
            echo "TapsAff dev shell"
            echo "  Python:  $(${python}/bin/python --version 2>&1)"
            echo "  uv:      $(uv --version 2>&1 | head -1)"
            echo "  redis:   $(redis-server --version 2>&1 | head -1 | cut -d'=' -f2 | cut -d' ' -f1)"
            echo "  node:    $(node --version 2>&1)"
            echo
            echo "First-time setup:"
            echo "  uv venv --python ${python}/bin/python"
            echo "  source .venv/bin/activate"
            echo "  uv pip install -r requirements.txt"
            echo "  python manage.py migrate"
            echo
            echo "Optional: start Redis locally for production-like cache:"
            echo "  redis-server --daemonize yes --port 6379"
            echo "  export CACHE=rediscache://localhost:6379/0"
          '';
        };
      });
}
