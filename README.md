# secret-santa

## Add command to nixos

```nix
{ pkgs ? import <nixpkgs> { } }:

let
  secret-santa =
    let
      defaultNix = builtins.fetchurl {
        url = "https://raw.githubusercontent.com/dolphinau/secret-santa/refs/heads/main/default.nix";
        sha256 = "1sihdgsg84kprycsg102rj9qnwd97zwx17x2wn42q4rmn918wvvx";
      };
    in pkgs.callPackage defaultNix {
      src = pkgs.fetchFromGitHub {
        owner = "dolphinau";
        repo = "secret-santa";
        rev = "a9b1f880d2fa50dbdff03a51b582deacb0972d90";
        sha256 = "sha256-v/fvJAlnMxMjlP6Z1cgHyKfno79yRSpKwY7pF0irISA=";
      };
    };
  in [
    secret-santa
  ]
```
