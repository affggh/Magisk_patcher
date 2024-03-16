{ pkgs ? import <nixpkgs> {}, lib ? pkgs.lib }:

let
  python3 = pkgs.python3;

  customtkinter = with python3.pkgs; buildPythonPackage rec {
    pname = "customtkinter";
    version = "5.2.0";
    format = "pyproject";

    src = fetchPypi {
      inherit pname version;
      hash = "sha256-6TRIqNIhIeIOwW6VlgqDBuF89+AHl2b1gEsuhV5hSTc=";
    };

    buildInputs = [ setuptools ];
    propagatedBuildInputs = [ darkdetect typing-extensions ];

    meta = with lib; {
      changelog = "https://github.com/TomSchimansky/CustomTkinter/releases/tag/${version}";
      homepage = "https://github.com/TomSchimansky/CustomTkinter";
      description = "A modern and customizable python UI-library based on Tkinter";
      license = licenses.mit;
      maintainers = with maintainers; [ ataraxiasjel ];
    };
  };

  myPythonEnv = python3.withPackages (ps: with ps; [
    customtkinter
    pillow
    requests
    packaging
  ]);
in

pkgs.mkShell {
  buildInputs = [
    python3
    myPythonEnv
    pkgs.python3Packages.tkinter
    pkgs.android-tools
  ];

  shellHook = ''
    echo "You are now using a NIX environment"
  '';
}

