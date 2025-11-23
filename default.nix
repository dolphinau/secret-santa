{ pkgs ? import <nixpkgs> { }, src ? ./., subdir ? "" }:

let
  theSource = src;
  pythonPackage = pkgs.python313Packages.buildPythonPackage {
    pname = "secret-santa";
    version = "1.0.0";
    src = "${theSource}/${subdir}";
    buildInputs = [
      pkgs.python313Packages.setuptools
      pkgs.python313Packages.wheel
    ];
    propagatedBuildInputs = [
      pkgs.python313Packages.flask
      pkgs.python313Packages.tkinter
    ];

    pyproject = true;
    build-system = [
      pkgs.python313Packages.setuptools
      pkgs.python313Packages.wheel
    ];

    meta = {
      description = "Secret santa flask package";
      license = pkgs.lib.licenses.mit;
    };
  };
  pythonEnv = pkgs.python313.buildEnv.override {
    extraLibs = [
      pkgs.python313Packages.flask
      pkgs.python313Packages.tkinter
      pythonPackage
    ];
    ignoreCollisions = true;
  };
in
pkgs.stdenv.mkDerivation rec {
  name = "secret-santa";
  propagatedBuildInputs = [ pythonEnv ];
  src = "${theSource}/${subdir}/src";

  installPhase = ''
    mkdir -p $out/bin
    cat > $out/bin/${name} <<EOF
#!/bin/sh
exec ${pythonEnv}/bin/python3 ${src}/secret_santa/main.py "\$@"
EOF
    chmod +x $out/bin/${name}
  '';

  meta = {
    description = "Secret santa server application";
    license = pkgs.lib.licenses.mit;
  };
}
