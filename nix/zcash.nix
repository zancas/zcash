let
  inherit (builtins) attrValues;
  inherit (import ./util) nixpkgs config srcDir;
  inherit (nixpkgs) stdenv;
  inherit (config.zcash) pname;

  version = import ./version.nix;
  packages = import ./packages;
  vendoredCrates = import ./vendoredCrates;
in
  stdenv.mkDerivation {
    inherit pname version;
    src = srcDir;

    nativeBuildInputs = attrValues packages ++ [
      nixpkgs.autoreconfHook
      nixpkgs.file
      nixpkgs.git
      nixpkgs.hexdump
      nixpkgs.pkg-config
      vendoredCrates # FIXME: Is this needed here vs CONFIG_SITE?
    ];

    CONFIG_SITE = nixpkgs.writeText "config.site" ''
      RUST_TARGET='${nixpkgs.buildPlatform.config}'
      RUST_VENDORED_SOURCES='${vendoredCrates}'
    '';

    configureFlags = [
      "--with-boost=${packages.boost}"
    ];

    # Patch absolute paths from libtool to use nix file:
    # See https://github.com/NixOS/nixpkgs/issues/98440
    preConfigure = ''sed -i 's,/usr/bin/file,${nixpkgs.file}/bin/file,g' ./configure'';
  }
