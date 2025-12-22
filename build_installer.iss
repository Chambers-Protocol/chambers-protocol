[Setup]
AppName=Chambers Protocol
AppVersion=1.0.0
DefaultDirName={autopf}\Chambers Protocol
DefaultGroupName=Chambers Protocol
OutputBaseFilename=ChambersProtocol_Enterprise_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
; These pull the files you just built with Python
Source: "dist\chambers_server.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Chambers_Setup.exe"; DestDir: "{app}"; Flags: ignoreversion postinstall nowait skipifsilent; Description: "Launch Activation Wizard"

[Icons]
Name: "{group}\Activate Chambers Protocol"; Filename: "{app}\Chambers_Setup.exe"

[Run]
; Auto-run the setup wizard after installation finishes
Filename: "{app}\Chambers_Setup.exe"; Description: "Activate License"; Flags: nowait postinstall skipifsilent