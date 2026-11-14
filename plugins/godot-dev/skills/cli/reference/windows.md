# Windows and Claude desktop app notes

## File encoding

- Godot text files (`.gd`, `.tscn`, `.tres`, `.json`, `.gdshader`, `.cfg`) are UTF-8 without BOM, with LF line ends.
- Windows PowerShell 5 adds a BOM with `Set-Content -Encoding utf8` and `Out-File -Encoding utf8`. Do not use them for these files. Use the file write tool, or `[IO.File]::WriteAllText($path, $text, (New-Object Text.UTF8Encoding $false))`. (Jamdok, FirstBlade)
- To read Korean text in PowerShell 5: `Get-Content -Raw -Encoding UTF8 <path>`. (VNTool)
- `.gitattributes` baseline used across the projects:

  ```
  * text=auto eol=lf
  *.cmd text eol=crlf
  *.ps1 text eol=crlf
  *.png binary
  *.jpg binary
  *.wav binary
  *.ogg binary
  *.ttf binary
  *.otf binary
  *.aseprite binary
  ```

## Running processes from PowerShell

- `& Godot.exe` (GUI) returns in milliseconds with `$LASTEXITCODE = 0`. `& Godot_console.exe` waits and passes the real exit code. (OnceUponATime)
- With `Start-Process -PassThru`, read `$p.Handle` before the process ends, then `WaitForExit(ms)`. `Wait-Process -Timeout` throws on timeout. (OnceUponATime)
- To end a hung run, kill the tree: `taskkill /T /F /PID <pid>`. Wrap it so an already finished PID does not stop the script. (OnceUponATime)

## AppData in the Claude desktop app

- Writes under AppData from a desktop app session are virtualized. Keep anything other programs must see outside AppData:
  - Godot export templates: a folder next to the Godot executables, for example `Documents\Godot\export_templates\<version>.stable\`. (Jajang, Jamdok)
  - Python environments made with uv: set `UV_PYTHON_INSTALL_DIR` and `UV_CACHE_DIR` to a folder outside AppData, and keep the venv in the project (`tools/.venv`, ignored by git). (Jamdok)
- `user://` resolves under `%APPDATA%` by default. Test scripts can point `APPDATA` and `LOCALAPPDATA` at a temp folder in the project so saves and `godot.log` land where the agent can read them. (OnceUponATime)

## Python tools

- Run project Python with `-I` (isolated mode), so a file in the working folder cannot shadow a standard module. (Jajang)
- Use the project's venv interpreter (`tools/.venv/Scripts/python`), not a global `python`.

## Git

- If git reports "dubious ownership" (a repository created by another Windows account, such as a sandbox account), run git with `-c safe.directory=<repo path>` for that command. Ask the user before you change the global git config. (VNTool)
