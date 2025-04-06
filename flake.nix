{
  description = "project flake";

  inputs = { nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05"; };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        nativeBuildInputs = with pkgs; [
          python312
          python312Packages.tkinter # for matplotlib
          gcc
          stdenv.cc.cc
          pkg-config
          entr
          uv
        ];

        shellHook = ''
          if [ ! -f ".venv" ]; then
            python -m venv .venv
            source .venv/bin/activate
            uv pip install -r requirements.txt
          else
            source .venv/bin/activate
          fi
          export LD_LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]
          }
          echo "Nix environment activated."
        '';
      };
    };
}
