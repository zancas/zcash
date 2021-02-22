let
  config = import ./config.nix;
  inherit (config.nixpkgs) gitrev sha256;

  url = "https://github.com/NixOS/nixpkgs-channels/archive/${gitrev}.tar.gz";
in
  fetchTarball {
    inherit url sha256;
    name = "nixpkgs";
  }