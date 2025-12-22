; CHAMBERS PROTOCOL ENTERPRISE INSTALLER SCRIPT

[Setup]
; Basic Metadata
AppName=Chambers Protocol
AppVersion=1.0.0
AppPublisher=Chambers Capital Ventures
DefaultDirName={autopf}\Chambers Protocol
DefaultGroupName=Chambers Protocol
OutputBaseFilename=ChambersProtocol_Enterprise_Installer
Compression=lzma2
SolidCompression=yes

; Enterprise Settings
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes
DisableWelcomePage=no

[Files]
; 1. The Server (The Brain) - Hidden in background
Source: "dist\chambers_server.exe"; DestDir: "{app}"; Flags: ignoreversion

; 2. The Setup Wizard (The Activator) - Visible to user
Source: "dist\Chambers_Setup.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu Shortcut for the Activator
Name: "{group}\Activate Chambers Protocol"; Filename: "{app}\Chambers_Setup.exe"
; Optional: Desktop Shortcut
Name: "{autodesktop}\Activate Chambers Protocol"; Filename: "{app}\Chambers_Setup.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
; Auto-launch the Activator after installation (Optional, usually good for manual installs)
Filename: "{app}\Chambers_Setup.exe"; Description: "Launch Activation Wizard"; Flags: nowait postinstall skipifsilent
