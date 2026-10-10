# T05 사전 고정 패키지 — AURORA MAX HISTORY

**상태: 검사/상한 확정, AI A 개발 미시작. 이 패키지는 구현 결과가 아닙니다.**

- 생성 시각: 2026-10-10T23:17:19+09:00 (KST) / 2026-10-10T14:17:19Z (UTC)
- 시작 GitHub 커밋: `b23ff0796fd1dc39e57e4d31ca851791c91d44e4`
- 소스: https://github.com/jennajiminkim/aurora-observation/tree/b23ff0796fd1dc39e57e4d31ca851791c91d44e4
- 원래 배포 사이트: https://aurora-observation.vercel.app/ (본 단계에서 미변경)
- 기준 검사: T05-H01~T05-H10, 정확히 10개; 각 ID별 사전조건·입력·기대 출력은 `FROZEN-TESTS.json`과 `FROZEN-TESTS.md`
- AI A/B 공통: 실제 개발 요청 시점부터 최대 45분, 사용자 메시지 최대 8회
- 요청 수 = 사용자가 해당 AI 세션에 보내는 메시지 수; 최초 구현 지시문도 포함. **도구 호출 수는 따로 실제 기록**.
- AI A와 AI B 모두 `COMMON-FIRST-REQUEST.md`의 본문을 동일한 시작 요청으로 사용. AI B에는 작업 저장소와 **실제 A가 작성한** HANDOFF.md만 전달하고 A와의 대화 내용은 제공하지 않는다.
- A가 작업을 멈췄을 때 `HANDOFF-TEMPLATE.md`를 참고해 실제 `HANDOFF.md`를 생성하고, 버전/검사/재현을 검증한다.
- 이번 준비 패키지를 A 구현 커밋에 해당하는 것으로 오인하지 말 것.

## 이 파일들의 역할

- `FROZEN-TESTS.json`: 자동 시험 구현 및 기계 판독용 규약 (승인 이후 변경 금지).
- `FROZEN-TESTS.md`: 사람이 검토하는 똑같은 10개 검사.
- `COMMON-FIRST-REQUEST.md`: A/B에게 보낼 같은 최초 요청.
- `START-LOG.json`: A/B 시작 종료·실측량 기록 양식. 시작 시각은 아직 비어 있음.
- `HANDOFF-TEMPLATE.md`: AI A 중단 후 7칸 인수인계 작성 참고 양식.
- `SHA256SUMS.txt`: 사전 문서 고정용 체크섬 목록.

## 다음 순서

1. A의 실제 구현 첫 요청을 발송하는 순간 `START-LOG.json`의 `A.actual_started_at_utc`와 `starting_commit_sha`를 기록한다.
2. 원본과 격리된 작업 브랜치/저장소에서 A가 개발을 시작한다. 이전의 다른 A 초안 결과는 이 실험에 혼합하지 않는다.
3. 45분/8요청 내 A 종료 시 소스 버전, 검사 10개 결과, 7칸 HANDOFF.md를 보존한다.
4. AI B를 다른 모델 또는 서비스에서 새로 열어 저장소와 동일한 HANDOFF.md를 제공한다.
5. B 결과를 측정한 뒤 익명 A/B 비교 보고서와 공개 URL을 만든다. A/B 수치는 실제 측정 후 채운다.

## 주의

`FROZEN-TESTS.json`의 SHA를 기준으로 검사 10개 동일성을 검증한다. 원천 파일의 해시를 재계산하려면 `sha256sum FROZEN-TESTS.json`(macOS: `shasum -a 256 FROZEN-TESTS.json`).
