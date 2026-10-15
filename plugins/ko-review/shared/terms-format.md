# 프로젝트 전용 낱말 목록 형식

<!-- ko-review: ignore -->

`doc_check.py` 의 기본 목록은 어느 프로젝트에나 맞는 것만 담는다. 프로젝트에서만 쓰는 금지어·표기는 `<프로젝트 루트>/.claude/ko-review/terms.json` 에 둔다(프로필 `terms_file` 로 위치를 바꿀 수 있다). 파일이 있으면 기본 목록에 더해 검사한다.

```json
{
  "banned": { "낱말": "대신 쓸 말과 이유" },
  "banned_soft": { "낱말": "확인할 점" },
  "banned_patterns": { "정규식": "대신 쓸 말과 이유" },
  "soft_patterns": { "정규식": "확인할 점" },
  "lexical_pairs": { "정규식": "주체와 동작이 안 맞는 이유" },
  "variant_sets": [["표기1", "표기2"]]
}
```

| 칸 | 결과 |
|---|---|
| `banned`, `banned_patterns` | 확정 문제. exit code 1 |
| `banned_soft`, `soft_patterns`, `lexical_pairs` | 확인 필요(참고) |
| `variant_sets` | 한 파일 안에서 갈리면 확정 문제, `--tree` 로 볼 때 파일 사이에서 갈리면 참고 |

- 정규식은 Python `re` 문법이다. JSON 안이라 역슬래시는 두 번 쓴다(`"\\s"`).
- 실제 문서에서 확인한 것만 넣는다. 목록은 규칙이 아니라 이미 새어나간 표현의 기록이다.
- 금지어를 예시로 나열하는 문서에는 `<!-- ko-review: ignore -->` 를 넣어 검사에서 뺀다.
