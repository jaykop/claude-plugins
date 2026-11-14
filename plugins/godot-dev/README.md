# godot-dev — Godot 코드 규칙과 명령줄 점검

Godot 4 GDScript 게임 프로젝트에서 코드와 씬을 작성하거나 리뷰할 때 따르는 규칙과, 에이전트가 Godot를 명령줄로 실행해 점검하는 절차다. 규칙은 jaykop 의 Godot 프로젝트들에 흩어져 있던 코드 지침과 AGENTS.md 에서 모았다. 대부분 두 프로젝트 이상에서 반복된 것이고, 규칙마다 출처 프로젝트를 적었다.

```
/plugin install godot-dev@jaykop
```

| 스킬 | 명령 | 하는 일 |
|---|---|---|
| code | `/godot-dev:code` | GDScript·씬 작성 규칙, 리뷰, 장르별 패턴 부록 |
| cli | `/godot-dev:cli` | 가져오기·부팅 점검·테스트·자동 촬영·내보내기, Windows와 데스크톱 앱 함정 |

명령 이름을 외우지 않아도 된다. Godot 프로젝트에서 "이 기능 구현해 줘", "이 스크립트 리뷰해 줘", "테스트 돌려 줘", "스크린샷 찍어서 확인해 줘" 같은 말로도 불린다.

```
/godot-dev:code 리뷰만 game/scripts/battle/
/godot-dev:cli 점검
/godot-dev:cli 촬영
```

## 이 플러그인에 없는 것

- **Godot 일반 지식.** 상태 머신이나 타일맵 만드는 법처럼 모델이 이미 아는 내용은 넣지 않았다. 필요하면 GodotPrompter 같은 일반 스킬을 따로 설치한다.
- **에디터 조작 MCP.** Godot 파일은 텍스트라 직접 고치고, 확인은 콘솔 실행 파일로 한다. Blender와 Aseprite처럼 바이너리 파일을 다루는 도구만 MCP를 쓴다.
- **작업 절차.** 이슈, 문서 반영, 인계는 `workflow` 플러그인이 맡는다.
- **주석 문체.** 용어와 문체는 `ko-gamedev:style` 이 맡는다.

## 프로젝트 프로필

프로젝트마다 다른 값은 `.claude/godot-dev/profile.md` 에 둔다. 양식은 [shared/profile-template.md](shared/profile-template.md) 다.

| 묶음 | 키 |
|---|---|
| 엔진 | `version`, `godot`, `godot_console`, `project_root`, `renderer`, `language`, `export_templates` |
| 명령 | `import`, `boot_smoke`, `tests`, `validate`, `capture`, `run` |
| 코드 규칙 | `error_policy`(strict·lenient), `comment_language`, `file_header`, `length_review`, `data_format`, `patterns`, `project_code_manual` |

PC마다 다른 경로는 `profile.local.md` 에 두고 버전 관리에서 뺀다. 프로필이 없으면 스킬은 기본값을 쓰고, 실행 파일은 프로젝트 지침에서 찾거나 사용자에게 묻는다.

우선순위는 사용자의 현재 요청, 프로젝트 지침(AGENTS.md, CLAUDE.md)과 프로젝트 코드 문서, 프로필, 이 플러그인 순서다.

## 규칙 구성

| 파일 | 내용 |
|---|---|
| `skills/code/SKILL.md` | 데이터(D), 책임(R), 오류(E), 주석·파일(C) 규칙과 보고 전 체크리스트 |
| `skills/code/reference/gdscript.md` | 타입, 컬렉션 함정, 클래스와 `class_name`, 이름과 멤버 순서, 노드·오토로드, process 함수 |
| `skills/code/reference/scenes.md` | 씬 구조, 스타일, `anchors_preset`·`_ready` 순서 함정 |
| `skills/code/reference/patterns.md` | 선택 부록: data-driven, deterministic-sim, preview, save, editor-tools, dev-args |
| `skills/cli/SKILL.md` | 실행 파일, 점검 순서, 출력 판정, 촬영, 내보내기 |
| `skills/cli/reference/test-runner.md` | 헤드리스 테스트 러너 계약과 입력·글꼴 측정 결과 |
| `skills/cli/reference/windows.md` | BOM, PowerShell 프로세스, AppData 가상화, Python, git 소유자 |

## 출처

규칙 끝의 괄호는 출처 프로젝트다. Wraithbound는 `Action2D` 폴더의 프로젝트다.

| 프로젝트 | 가져온 것 |
|---|---|
| Catena | `docs/development/coding-standards.md`, `scene-structure-standards.md` 의 원칙, GDScript 함정, 주석 규칙 |
| VNTool | `docs/manual/coding-standards.md` 의 짧은 규칙 형식, P-011~P-017, 테마 type variation |
| Wraithbound (Action2D) | `docs/ai/ENGINEERING_RULES.md` 의 `@export` Resource 기본값, Variant cast, process 분해 |
| BeforeTheBell | 코딩 규칙(§15), 데이터 로딩의 CSV Keep File, 저장, 테스트 픽스처 분리 |
| OnceUponATime | 테스트 명령과 러너 계약(§9), 스파이크 결론(§11), 검증기 규칙 |
| Jajang, Jamdok | AGENTS.md 작업 규칙, 편집 도구 호스트, 개발용 실행 인자, Windows 환경 |

데이터 오류 처리는 프로젝트마다 달랐다(VNTool·Wraithbound는 크게 실패, BeforeTheBell은 경고 후 건너뜀). 이 플러그인은 `strict` 를 기본으로 하고 프로필의 `error_policy: lenient` 로 바꿀 수 있게 했다.
