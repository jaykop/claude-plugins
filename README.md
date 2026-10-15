# claude-plugins

jaykop 의 [Claude Code](https://code.claude.com) 플러그인 모음이다. 리포 하나가 마켓플레이스(설치할 수 있는 플러그인 목록) 역할을 하고, 플러그인은 `plugins/` 아래에 하나씩 들어 있다. 필요한 플러그인만 골라 설치하면 된다. 일부 플러그인은 Codex 에서도 같은 스킬을 쓴다.

A personal Claude Code plugin marketplace. Some plugins also ship a Codex manifest. Documentation is in Korean.

## 플러그인 목록

| 플러그인 | 설명 | Codex | 설명서 |
|---|---|---|---|
| `advisors` | 게임 프로젝트 고문 6종 — 기획, 신기술, 시장 동향, 최적화, PM, TD(테크니컬 디렉터) | - | [plugins/advisors/README.md](plugins/advisors/README.md) |
| `ko-review` | 한국어 문서·주석 교정, 한 AI 가 쓴 설명을 다른 AI 가 부분 검토하는 설명 변경 목록 | 스킬 | [plugins/ko-review/README.md](plugins/ko-review/README.md) |
| `workflow` | 이슈 기반 작업 흐름 — 다음 작업 고르기, 규모별 구현, 문서 반영, 커밋 전 문서 검토, 인계 메모 | 스킬 | [plugins/workflow/README.md](plugins/workflow/README.md) |

## 설치

Claude Code 세션에서 실행한다.

```
/plugin marketplace add jaykop/claude-plugins
/plugin install advisors@jaykop
```

- 마켓플레이스 이름은 `jaykop` 이다. 설치 명령의 `@` 뒤에 이 이름을 쓴다.
- 한 번 설치하면 모든 프로젝트에서 쓸 수 있다(사용자 범위 설치).
- `owner/repo` 형식이 SSH 로 접속을 시도하다 실패하면 HTTPS 주소를 그대로 쓴다.

  ```
  /plugin marketplace add https://github.com/jaykop/claude-plugins.git
  ```

### 프로젝트에서 플러그인 목록 공유

프로젝트를 clone 한 다른 머신에서도 같은 플러그인을 쓰게 하려면 프로젝트의 `.claude/settings.json` 에 마켓플레이스와 켤 플러그인을 적어 버전 관리에 올린다. 그 프로젝트를 연 Claude Code 가 설치를 안내한다.

```json
{
  "extraKnownMarketplaces": {
    "jaykop": { "source": { "source": "github", "repo": "jaykop/claude-plugins" } }
  },
  "enabledPlugins": {
    "workflow@jaykop": true
  }
}
```

### Codex

Codex 용 마켓플레이스 목록은 `.agents/plugins/marketplace.json` 이다.

```
codex plugin marketplace add jaykop/claude-plugins
```

그다음 Codex 앱의 플러그인 화면에서 설치한다. Codex 는 설치한 플러그인을 `~/.codex/plugins/cache/jaykop/<플러그인>/<version>/` 에 둔다. Codex 플러그인 훅은 쓰지 않고, 필요하면 프로젝트의 `.codex/hooks.json` 으로 연결한다([workflow 설명서](plugins/workflow/README.md#훅-claude-code)).

## 업데이트

Claude Code 플러그인 설정 파일에 `version` 을 적지 않았다. 그래서 커밋마다 버전이 바뀌고, 새 커밋을 push 하면 업데이트로 전달된다.

- 서드파티 마켓플레이스는 자동 업데이트가 기본으로 꺼져 있다. `/plugin` 화면의 Marketplaces 탭에서 `jaykop` 의 자동 업데이트를 켜면 된다.
- 설치된 사본(`~/.claude/plugins/` 아래)은 업데이트 때 덮어써지므로 직접 고치지 않는다. 고칠 곳은 이 리포뿐이다.
- Codex 는 매니페스트(`.codex-plugin/plugin.json`)의 `version` 을 설치 폴더 이름으로 쓴다. 버전이 같으면 새 사본을 받지 않으므로, 플러그인 폴더의 파일을 고치면 이 값을 올린다. 받는 쪽은 `codex plugin marketplace upgrade jaykop` 를 실행하면 설치된 플러그인도 새 버전으로 바뀐다.

## 개발

플러그인을 설치하지 않고 이 리포의 파일을 바로 시험할 수 있다.

```
claude --plugin-dir ./plugins/advisors
```

구조 검사는 다음 명령으로 한다. 구조만 보고 동작은 보지 않는다.

```
claude plugin validate .
claude plugin validate ./plugins/advisors
```

새 플러그인을 추가할 때는 `plugins/<이름>/` 을 만들고 `.claude-plugin/marketplace.json` 의 `plugins` 목록에 항목을 더한다. Codex 에서도 쓰게 하려면 `plugins/<이름>/.codex-plugin/plugin.json` 을 두고 `.agents/plugins/marketplace.json` 에도 더한다.

## 라이선스

[MIT](LICENSE)
