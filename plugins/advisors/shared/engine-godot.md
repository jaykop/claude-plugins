# Godot 프로젝트에서 바꿔 읽기

고문의 SKILL.md 와 reference 파일은 언리얼 기준으로 쓰여 있다. 프로필 `engine.kind` 가 `godot` 이면 고문은 Step 0 에서 이 파일을 먼저 읽고, 언리얼 낱말과 단계를 아래 표대로 바꿔 읽는다.

- 표에 없는 언리얼 전용 단계(예: Build.cs 의존 정리, 런처판 패치 번호 찾기)는 건너뛰고 리포트 "확인 못 한 것"에 "Godot 에 해당 없음 — <단계>"로 적는다. 건너뛴 것을 "문제 없음"으로 읽지 않는다.
- 명령·설정·클래스 이름을 기억으로 쓰지 않는 규칙(perf `categories.md` §2, radar `sources.md` §7)은 그대로다. 이 파일에 "(확인 필요)"가 붙은 이름은 이 파일을 쓸 때도 확실하지 않았던 것이다. 리포트에 넣기 전에 대상 버전의 공식 문서나 엔진 소스로 확인하고, 확인한 위치(URL·조회일 또는 파일:줄)를 적는다.
- design, market, pm 고문은 엔진에 묶인 단계가 없다. 바꿔 읽을 것이 없다.

## 1. engine.kind 정하기

- 프로필을 만들 때(start.md 0-D) `profile_scan.py` 결과의 "엔진 종류 (engine.kind)" 줄을 `[파일]` 출처로 채운다. "둘 다"로 나오면 사용자에게 묻는다. 무인 실행에서 칸이 비어 있으면 스크립트가 엔진을 가린 결과를 따르고, 리포트 머리 "범위"에 그렇게 적는다.
- 스크립트 셋은 엔진을 스스로 가린다. `profile_scan.py` 는 두 엔진을 다 찾는다. `tech_inventory.py` 와 td 의 `module_graph.py` 는 `--project-file` 이 `project.godot` 이면, 또는 `.uproject` 가 없고 `project.godot` 만 있으면 Godot 판(`tech_inventory_godot.py`, `godot_graph.py`)으로 돈다. 그래서 SKILL.md 의 명령을 그대로 쓴다. 엔진을 못 박고 싶으면 `--engine godot` 을 붙인다.
- 나머지 스크립트(`csv_profile_stat.py`, `vcs_churn.py`, `due_check.py`, `pm_calc.py`, design·market 스크립트)는 엔진과 상관없다.

## 2. 낱말 바꿔 읽기 (모든 고문)

| 언리얼 | Godot | 메모 |
|---|---|---|
| 프로젝트 파일 `.uproject` | `project.godot` | 프로필 `project_file` 에 그 경로를 적는다 |
| 엔진 버전 파일 `Engine/Build/Build.version` | 커스텀 빌드면 엔진 소스의 `version.py`. 아니면 C# 프로젝트 파일(`*.csproj`)의 `Godot.NET.Sdk/<버전>`, 그것도 없으면 `project.godot` 의 `config/features` 버전 | `config/features` 에는 마이너 버전까지만 있다(패치 번호 모름). 스크립트가 이 순서로 읽는다 |
| 소스 빌드 여부(`EngineAssociation`) | 프로젝트 파일에 적히지 않는다 | `engine.source_build` 는 추측하지 않고 사용자에게 묻는다 |
| `engine.root`(엔진 소스·설치 폴더) | 커스텀 빌드일 때만 Godot 엔진 소스 폴더(`version.py` 가 있는 곳). 공식 배포판이면 비워 둔다 | 비어 있으면 엔진 클래스·설정·명령줄 이름은 대상 버전의 공식 문서와 공개 소스 저장소의 그 버전 태그로 확인한다 |
| 게임 코드 폴더 `Source`, `Plugins/*/Source` | `project.godot` 가 있는 폴더(res://) 전체 | 외부 애드온(`addons/<이름>`)은 판정에서 뺄 때 `--exclude` 로 준다 |
| 플러그인 `.uplugin` | `addons/<이름>/plugin.cfg`(에디터 플러그인), `*.gdextension`(GDExtension), 둘 다 없는 `addons/<이름>`(스크립트 애드온) | 엔진에 들어 있는 기능(렌더러, 물리 엔진 등)은 플러그인이 아니라 설정이다 |
| 프로젝트 파일의 플러그인 켜짐·꺼짐 | `project.godot` 의 `[editor_plugins] enabled` | 에디터 플러그인을 꺼도 그 애드온의 런타임 스크립트는 쓸 수 있다. GDExtension 과 스크립트 애드온은 켜고 끄는 칸이 없다 |
| 플러그인 성숙도 표시(`IsExperimentalVersion`, `IsBetaVersion`) | 애드온 파일에는 없다 | 엔진 기능의 실험 표시는 대상 버전 공식 문서의 클래스 설명 원문으로 확인한다(엔진 소스면 `doc/classes/*.xml` 의 실험 표시 — 확인 필요) |
| 모듈과 `*.Build.cs` 의존 선언 | 없다 | td 의 모듈 지도는 폴더를 모듈로, 파일 안의 참조를 간선으로 센다(§4) |
| 설정 파일 `Config/Default*.ini` | `project.godot` | 기능 태그별 값(`키.mobile` 처럼 점 뒤에 태그)도 같은 설정으로 본다. 적히지 않은 설정은 엔진 기본값이다 |
| 콘솔 변수(CVar), 콘솔 명령 | 프로젝트 설정(ProjectSettings) 키, 엔진 싱글턴(`Engine`, `Performance`, `RenderingServer` 등)의 속성·메서드, 명령줄 인자 | 실행 중 조작 경로는 게임이 직접 만든 디버그 명령·디버그 콘솔 애드온이다 |
| 블루프린트 에셋(`.uasset`, 이진이라 못 읽음) | `.tscn`·`.tres` 는 텍스트라 읽는다. `.res`·`.scn`(이진)과 에디터에서만 보이는 것은 못 읽는다 | 언리얼 문서의 "블루프린트 확인 못 함"은 이진 리소스에만 쓴다. 씬 안의 시그널 연결(`[connection]`)과 스크립트 연결도 텍스트로 센다 |
| 틱, 틱 그룹 | `_process`, `_physics_process`, 노드의 처리 우선순위(`process_priority`, `process_physics_priority` — 확인 필요), 씬 트리 순서 | 같은 프레임의 실행 순서를 정하는 장치다 |
| 네트워크 복제, 원격 호출 | 고수준 멀티플레이어(`MultiplayerAPI`, `@rpc`, `MultiplayerSynchronizer`, `MultiplayerSpawner` — 확인 필요) | 권한 검사는 `is_multiplayer_authority()` 같은 호출을 찾는다(확인 필요) |
| 쿡·패키징 | 내보내기(`export_presets.cfg`) | 대상 플랫폼은 `export_presets.cfg` 의 `platform` |
| 측정 파일 폴더 `Saved/Profiling` | 정해진 곳이 없다 | `perf.profiling_dir` 은 사용자에게 묻는다 |
| 자동화 테스트(Automation Spec 등) | GUT, gdUnit4(GDScript·C#) | `profile_scan.py` 가 `extends GutTest`, `extends GdUnitTestSuite`, `[TestSuite]` 로 찾는다 |

## 3. 기술 동향 고문(radar)

- **기술 목록**(SKILL.md Step 1): 명령은 그대로다. 상태 다섯 가지의 Godot 뜻은 결과 끝 설명에 있다. "엔진에 있으나 꺼짐"은 `addons` 에 있지만 `[editor_plugins]` 에 켜짐으로 적히지 않은 에디터 플러그인이다.
  - "엔진 폴더를 못 찾아" 단계는 없다. Godot 은 엔진 폴더 없이도 목록이 다 나온다. 공식 배포판이면 `engine.root` 를 묻지 않는다.
  - "변경 없음"의 입력 지문은 `version.py`(엔진 폴더를 줬을 때), `project.godot`, `export_presets.cfg`, `*.csproj`, `plugin.cfg`, `*.gdextension` 이다. 게임 코드는 지문에 들지 않으므로 사용 흔적만 바뀐 것은 `stale_after_days` 가 지나야 반영된다.
  - "켜짐·사용 흔적 없음"은 에디터 도구만 더하는 플러그인이거나 GDExtension 이 등록한 클래스 이름으로만 쓰는 경우일 수 있다. "안 쓴다"고 단정하지 않는다.
- **우리 트리의 1차 근거**(SKILL.md D2): `.uplugin` 대신 `plugin.cfg`(이름, 버전, 스크립트)와 `.gdextension`(`compatibility_minimum`, 라이브러리 경로)을 읽는다. 커스텀 빌드면 엔진 소스의 그 모듈 폴더를 읽는다.
- **1차 출처**(sources.md §1): 아래는 찾기 시작할 곳이다. 접근 가능 여부와 주소는 실행할 때 열어 보고 `source-checks.md` 에 적는다.
  - 공식 블로그와 릴리스 공지(godotengine.org 의 글 목록과 릴리스 페이지)
  - 버전별 공식 문서(docs.godotengine.org 의 버전 판). 이전 안내 문서(마이너 버전 사이 업그레이드 안내)가 있으면 버전 점검의 1차 근거다
  - 공개 소스 저장소 godotengine/godot 의 릴리스 태그, 변경 기록, 이슈 트래커(공식 이슈 트래커로 본다)
  - 제안 저장소 godotengine/godot-proposals 는 계획이다. 출시 근거로 쓰지 않는다(발표 단계 ②까지)
  - 애셋 라이브러리와 애드온 저장소는 그 애드온 공급사의 자료로 본다(sources.md §1 의 공급사 규칙)
- **커뮤니티 채널**(sources.md §10): 채널 목록은 그대로 쓴다. qiita 태그는 공개 기술 이름(예: `Godot` — 확인 필요)으로 쓴다.
- **엔진 버전 점검표**(upgrade-checklist.md): 항목 번호는 그대로 두고 아래처럼 바꿔 읽는다.
  - 2: 대조 대상은 기술 목록의 애드온·GDExtension 과 설정 표, 그리고 게임 코드가 쓰는 엔진 클래스·메서드다. 바뀐 API 를 쓰는 파일 수는 analyst 에 `.gd`·`.cs`·`.tscn`·`.tres` 검색식으로 센다.
  - 3: 언리얼 성숙도 표시 대신, 우리가 쓰는 엔진 기능 가운데 공식 문서에 실험 기능으로 적힌 것이 대상 버전에서 어떻게 바뀌는지 본다.
  - 4: 커스텀 빌드일 때만. 애드온을 고쳐 쓰면("엔진을 고쳐서 씀") 그 애드온도 여기서 센다.
  - 5: `project.godot` 의 `config_version` 이 바뀌는 버전(3 → 4 처럼 큰 이전)은 따로 "막힘 후보"로 적고 이전 안내 문서를 1차 근거로 둔다.
  - 7: 애드온마다 대상 버전 지원을 그 애드온 저장소·애셋 라이브러리에서 본다. `plugin.cfg` 에는 지원 버전 칸이 없다. GDExtension 은 `compatibility_minimum`·`compatibility_maximum`(확인 필요)과 공급사 자료를 함께 본다.
  - C# 프로젝트면 `Godot.NET.Sdk` 버전과 그 버전이 요구하는 .NET 버전도 항목 2 에 넣는다.

## 4. TD 고문(td)

- **모듈 지도**(SKILL.md, audit-scopes.md §1): 명령은 그대로다. 결과 머리가 "— Godot"이면 Godot 판이다.
  - 모듈은 폴더다. `addons/<이름>` 은 애드온 하나, 그 밖은 프로젝트 폴더 바로 아래 폴더 하나다. 더 잘게 보려면 `--unit-depth 2` 를 준다.
  - 코드가 `scripts/` 같은 폴더 하나에 몰린 프로젝트(Godot 에서 흔하다)는 모듈이 하나로 뭉친다. 결과 머리에 "--unit-depth N 로 다시 돌릴 것" 주의가 있으면 그 값으로 다시 돌리고, 리포트에는 다시 돌린 결과를 쓴다. 쓴 `--unit-depth` 값은 TD 기록 판정 기준 표에 적어 다음 점검도 같은 값으로 돌린다.
  - 간선은 참조 종류(preload, extends, class_name 사용, autoload 사용, 씬·리소스 참조, 셰이더 include, C# using, 동적 로드, 경로 문자열)마다 묶어 센다. 순환 의존과 층 판정에서는 동적 로드와 경로 문자열을 뺀다.
  - `--engine-root`, `--includes` 는 쓰지 않는다. 주면 무시하고 "주의"로 적는다.
  - 판정 표 바꿔 읽기:

    | 언리얼 분류 | Godot |
    |---|---|
    | 층 규칙 위반 | 그대로 |
    | 런타임 → 에디터 의존 | 결과의 "에디터 전용 코드에 기대는 곳". 조건 칸(`Engine.is_editor_hint()`, `#if TOOLS`)이 없으면 등급은 확인함, 있으면 참고로만 적는다. 내보낸 빌드에서 그 조건이 안전한지는 문서·내보내기 시험으로 확인할 일로 적는다 |
    | 순환 의존 | 그대로(동적 로드와 경로 문자열을 뺀 참조 기준) |
    | 지울 후보 의존, 선언 없는 include | 해당 없음. 의존 선언이 없어서다 |

  - 산출물의 "include 가 많은 헤더"는 "다른 모듈이 많이 참조하는 파일"로 바꾼다. "autoload" 표(전역 싱글턴과 그것을 이름으로 부르는 모듈 수)와 "가리키는 파일이 없는 res:// 경로"를 산출물에 더한다.
- **지금 구조 조사**(SKILL.md): 진입점·상태를 쓰는 지점에 더해 아래를 찾는다. 시그널 연결(코드의 `connect` 와 `.tscn` 의 `[connection]`), 그룹(`add_to_group`, `get_nodes_in_group`, `call_group`), 노드 경로 문자열(`$`, `get_node`, `%고유 이름`) — 씬 구조에 묶인 참조다, 씬 상속과 인스턴스, 여러 곳이 같은 `.tres` 를 고치는 공유 리소스.
- **엔진 수정**(audit-scopes.md §2): 커스텀 빌드이고 `engine.root` 가 Godot 엔진 소스일 때만 한다. 순정 엔진(`td.vanilla_engine_root`)은 같은 버전의 공식 소스다. 버전은 `Build/Build.version` 대신 `version.py` 로 읽는다. 공식 배포판이면 엔진 수정은 "해당 없음"이고, 고쳐 쓰는 애드온이 있으면 그 애드온 폴더를 셀 폴더로 주고 순정은 애드온 원본 저장소의 같은 버전으로 본다.
- **에이전트 검증 가능성**(audit-scopes.md 의 축 1~6): 아래 검색식을 언리얼 검색식 대신 쓴다. 여기 적힌 검색식은 대화 실행에서 따로 확인받지 않아도 되고 무인 실행에서도 쓴다. 더 찾을 것이 있으면 대화 실행에서 확인받는다.
  1. 난수 경로
     - GDScript 전역 난수: `(?<![\w.])(randi|randf|randi_range|randf_range|randfn|randomize|rand_from_seed|seed)\s*\(`
     - C# 전역 난수: `GD\.(Randi|Randf|RandRange|Randfn|Randomize|Seed)\b`, `new\s+Random\(`
     - 시드를 가진 스트림: `RandomNumberGenerator`
     - 프레임 간격(참고 사실로만): `project.godot` 의 `physics/common/physics_ticks_per_second`, 명령줄 `--fixed-fps`(확인 필요)
  2. 상태 재현
     - GDScript: `ResourceSaver\.save`, `FileAccess\.open`, `ConfigFile`, `JSON\.(stringify|parse)`, `(var_to_str|str_to_var|var_to_bytes|bytes_to_var)\s*\(`
     - C#: `ResourceSaver\.Save`, `FileAccess\.Open`, `ConfigFile`, `Json\.(Stringify|Parse)`
     - 입력 기록·재생: `Input\.parse_input_event` 를 쓰는 곳
  3. 텍스트 출력
     - GDScript: `(?<![\w.])(print|print_debug|print_rich|printerr|prints|printt|push_warning|push_error)\s*\(`
     - C#: `GD\.(Print|PrintRich|PrintErr|PrintS|PrintT|PushWarning|PushError)\b`
     - 파일 로그 설정: `project.godot` 의 파일 로그 항목(확인 필요)
     - 화면만: 디버그용 `Label`·`draw_` 호출, 디버그 그리기 애드온
  4. 재컴파일 없는 조작
     - 게임이 만든 디버그 명령·치트(명령 이름 표를 가진 autoload, 디버그 콘솔 애드온)
     - GDScript: `OS\.get_cmdline_(user_)?args`, `OS\.is_debug_build`. C#: `OS\.GetCmdline(User)?Args`, `OS\.IsDebugBuild`
     - GDScript 는 스크립트를 고쳐도 다시 빌드하지 않지만, 이것은 조작 경로로 세지 않는다
     - 에디터 원격 조작: `.mcp.json` 과 켜진 원격 조작 애드온(기술 목록)
  5. 수치의 데이터 분리
     - GDScript 상수: `^\s*const\s+\w+\s*(:\s*(int|float))?\s*:?=\s*-?[0-9.]`. C# 상수: `const\s+(float|double|int)\s+\w+\s*=\s*-?[0-9.]`
     - 이미 뺀 방식(선례): `@export`, `\[Export\]`, `Resource` 를 상속한 데이터 클래스와 `.tres`, `ProjectSettings\.get_setting`, `.json`·`.csv` 데이터 파일
  6. 자동 시험
     - 테스트 수: `extends\s+(GutTest|GdUnitTestSuite)` 파일의 `func\s+test_`, `\[TestSuite\]` 파일의 `\[TestCase\]`
     - 자체 테스트 러너: 알려진 틀을 쓰지 않고 `extends Node` 스크립트와 씬으로 직접 만든 러너가 흔하다. `profile_scan.py` 결과의 "자체 러너 후보"(테스트 폴더나 `test_*.gd`·`run_all.gd` 같은 이름)와 "--headless 실행"(실행 스크립트·CI 설정의 줄)을 analyst 에 넘겨, 러너마다 확인 함수 호출 수와 실패를 종료 코드로 내는지(`get_tree\(\)\.quit\(` 에 넘기는 값)를 받는다. 결과는 "알려진 틀 기준 N 개, 자체 러너 M 개(확인 N 곳)"처럼 나눠 적는다. 알려진 틀이 0 이어도 자체 러너가 있으면 "없음"으로 분류하지 않는다
     - 화면 없이 돌리는 명령이 적힌 곳(프로젝트 스크립트와 CI 설정): `--headless`, `--script`·`-s`, `--quit`, `--quit-after`, GUT·gdUnit4 명령줄 실행 스크립트(확인 필요), `extends\s+(SceneTree|MainLoop)` 스크립트. 명령은 실행하지 않는다

## 5. 최적화 고문(perf)

- **측정 파일**(SKILL.md Step 0, measure.md §5):
  - 에디터 디버거의 프로파일러·비주얼 프로파일러·모니터는 화면 도구다. 화면에 뜬 숫자는 근거로 쓰지 않는다(measure.md §5). 파일로 남긴 값만 쓴다.
  - 프레임별 CSV: 게임 안에서 `Performance.get_monitor()` 값을 프레임마다 CSV 한 행으로 쓰는 측정용 스크립트(보통 autoload)가 있으면, 머리 행 하나와 프레임 행들인 CSV 라서 `csv_profile_stat.py` 로 그대로 집계한다. 측정 시간 모니터 값의 단위(초인지 ms 인지)는 대상 버전 문서로 확인하고(확인 필요), `--budget-ms`·`--hitch-ms` 와 비교하려면 ms 로 쓴 열을 고른다. 그런 스크립트가 없으면 측정 계획에 "측정용 스크립트 명세"(남길 모니터 이름, 열 이름, 단위, 파일 위치)를 넣고 `code_change_entry` 나 사용자에게 넘긴다. 고문이 스크립트를 쓰지 않는다(rules.md §7).
  - 렌더링 CPU·GPU 시간은 `RenderingServer` 의 뷰포트 렌더 시간 측정 기능(확인 필요)으로 같은 CSV 에 넣는다.
  - 측정용 스크립트 명세의 기본형은 아래다. 측정 계획에 그대로 옮기고, 프로젝트에 맞게 열을 빼거나 더한다. 모니터·메서드 이름과 단위는 모두 확인 필요라서, 명세를 넘길 때 "대상 버전 문서로 이름과 단위를 확인할 것"을 함께 적는다.

    | 열 이름 | 값 | 단위 |
    |---|---|---|
    | `Frame` | 기록 시작 뒤 프레임 번호 | 개 |
    | `FrameTime` | `_process` 의 `delta` × 1000 | ms |
    | `ProcessTime` | `Performance.TIME_PROCESS` × 1000 | ms |
    | `PhysicsTime` | `Performance.TIME_PHYSICS_PROCESS` × 1000 | ms |
    | `RenderCpuTime` | 뷰포트의 측정 렌더 CPU 시간 | ms |
    | `RenderGpuTime` | 뷰포트의 측정 렌더 GPU 시간 | ms |
    | `DrawCalls` | `Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME` | 개 |
    | `Objects` | `Performance.OBJECT_COUNT` | 개 |
    | `Nodes` | `Performance.OBJECT_NODE_COUNT` | 개 |
    | `StaticMemMB` | `Performance.MEMORY_STATIC` ÷ 1048576 | MB |

    - 머리 행 한 줄 뒤에 프레임마다 한 행을 쓴다. `csv_profile_stat.py` 가 그대로 읽는다(`--stats "FrameTime,ProcessTime,PhysicsTime,RenderCpuTime,RenderGpuTime"`).
    - 파일 이름에 시나리오 ID 와 반복 번호를 넣는다(예: `S01_r1.csv`). 점검 기록의 "측정 파일 이름 규칙"이 이것을 읽는다.
    - 저장 위치는 `perf.profiling_dir` 이다. 게임은 실행 중에 `user://` 에 쓰는 것이 보통이므로, 측정이 끝나면 그 폴더로 옮기는 방법도 명세에 적는다.
    - 측정 조건(수직 동기화, 프레임 상한, 해상도, 렌더러, 빌드 종류)은 파일 끝에 남기지 말고 측정 조건 표에 사람이 적는다. `csv_profile_stat.py` 의 메타데이터 행 형식을 따로 맞추지 않아도 된다.
    - 워밍업 프레임은 기록 뒤 `--skip-frames` 로 뺀다.
  - 명령줄 측정 조건: 수직 동기화 끄기, 고정 프레임(`--fixed-fps`), FPS 출력(`--print-fps`), 시작 시간 측정(`--benchmark`, `--benchmark-file`) — 모두 확인 필요.
  - GPU 캡처는 외부 그래픽 디버거로 한다. C# 의 GC 와 할당은 .NET 진단 도구로 잰다.
  - `profile_scan.py` 의 측정 파일 폴더 줄은 "정해진 폴더가 없다"로 나온다. 그때만 `perf.profiling_dir` 을 묻는다.
- **부문 분류표**(categories.md): 항목 ID 는 바꾸지 않는다. 아래만 바꿔 읽는다.
  - 게임 스레드 CPU 는 메인 스레드다. 게임스레드-02 "블루프린트에서 매 프레임 도는 로직"은 "GDScript 에서 매 프레임 도는 로직"으로 읽는다. 측정은 측정 파일의 처리 시간 열로, 코드 검색은 `_process`·`_physics_process` 본문으로 한다.
  - 렌더 스레드는 렌더링 스레드 모델 설정(`project.godot`, 확인 필요)에 따라 메인 스레드에서 돌 수 있다. 판정은 측정한 렌더링 CPU 시간으로 한다.
  - GC: GDScript 는 참조 세기라 GC 멈춤이 없고, 해제가 한 프레임에 몰리는지를 본다. C# 이면 .NET GC 를 본다.
  - 빌드·쿡 시간은 내보내기 시간과 C# 빌드 시간이다.
  - 표의 언리얼 명령(`stat`, `dumpticks`, Insights 채널)은 쓰지 않는다. 대신 쓸 Godot 이름은 대상 버전 문서·엔진 소스에서 확인한 것만 쓴다.
- **명령 이름 확인**(categories.md §2): `engine.root` 가 있으면 엔진 소스에서 이름을 찾는다(명령줄 인자는 엔진 시작 코드, 모니터 이름은 `Performance` 클래스 문서 파일 — 확인 필요). 없으면 대상 버전 공식 문서의 클래스 레퍼런스와 명령줄 안내 페이지에서 찾고 URL·조회일을 적는다.
- **테스트**(tests.md): 형식은 GUT·gdUnit4 다. 씬·리소스에 묶인 로직은 씬을 불러 돌리는 테스트(테스트 틀의 씬 실행 도구 — 확인 필요)로 명세한다. "팀 공유 필요"는 `project.godot` 변경(autoload 추가, 애드온 켜기, 입력 맵), `*.csproj` 패키지 추가, 테스트 애드온 설치다.

## 6. 프로필 칸

| 칸 | Godot 값 |
|---|---|
| `engine.kind` | `godot` |
| `engine.name` | Godot Engine (C# 을 쓰면 .NET 판이라고 적는다) |
| `engine.version` | 스크립트가 읽은 버전. 패치 번호를 모르면 사용자에게 확인 |
| `engine.source_build` | 사용자에게 묻는다 |
| `engine.root` | 커스텀 빌드일 때만 엔진 소스 폴더 |
| `project_file` | `project.godot` 의 경로 |
| `source_roots` | 비우면 `project.godot` 가 있는 폴더 전체. 게임 코드 폴더만 보려면 그 폴더들을 적는다. `project.godot` 가 하위 폴더(예: `game/`)에 있으면 그 바깥 코드(도구 스크립트 등)는 범위 밖이다. 같이 보려면 `source_roots` 에 바깥 폴더까지 모두 적는다(이때 프로젝트 폴더도 함께 적는다) |
| `radar.engine_mod_dirs` | 커스텀 빌드면 엔진 소스 아래 폴더(상대 경로는 `engine.root` 기준), 고쳐 쓰는 애드온이면 `addons/<이름>`(프로젝트 루트 기준) |
| `perf.profiling_dir` | 측정용 스크립트가 CSV 를 남기는 폴더 |
| `perf.test_command` | GUT·gdUnit4 의 명령줄 실행 명령 |
