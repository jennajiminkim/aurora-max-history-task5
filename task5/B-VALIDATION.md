# AI B 검사 증거 / 통합 결과

## 보존 버전

- AI A 인수인계 브랜치: `t05-ai-a-handoff`; 인수인계 SHA `9f10f7dac460f315aa6de17833ec9ee485c3bfa1`
- AI B가 업로드한 독립 수정 커밋: `cb5d40cedd11d7767ee9530852262c42ee79e760` (당시 `main`에 업로드)
- 두 작업물의 소스 이력을 부모 커밋으로 보존한 병합 코드 커밋: `261d102c2ca7661c0cb7cf258f4cea19d82c3de5` (브랜치 `t05-ai-b-final`).
- 원본 고정 계약 `FROZEN-TESTS.json` SHA-256: `c03036a50a31473fcb6bce74226b6bda8d0ad8a0e770ed464cfed7ba455b2d23`

## 결과

- AI A 원본 다시 실행: **7 PASS / 3 FAIL** (H02/H05/H06).
- AI B 수정본 재구성 후 실제 원본 CSS/고정 JSON/fixture와 AI A가 보존한 Playwright 브라우저 러너를 사용해 재실행: **10 PASS / 0 FAIL** (실행 종료 코드 0).
- AI B 세션 자체의 최소 환경 10/10은 별도의 잠정 결과로 취급. 위 재검사와 혼동하지 말 것.
- 재구성본의 `app.js`, `index.html`, `t05-b-additions.css` Git 객체 해시는 각각 AI B의 업로드 커밋과 동일함.
- 공개 GitHub `task5/run_frozen.py`는 보존된 AI A 패키지 러너와 구현이 일부 다른 파일이므로 아래 명령으로 **게시된 코드에 대한 추가 독립 재현**을 권장합니다. 아직 그 추가 재실행 결과를 보유하지 않습니다.

```bash
git clone -b t05-ai-b-final https://github.com/jennajiminkim/aurora-max-history-task5.git
cd aurora-max-history-task5
python -m pip install playwright
python -m playwright install chromium
python task5/run_frozen.py > task5/B-test-results.json
```

위 테스트의 종료 코드가 0이고 JSON의 passed가 10인지 확인. `task5/A-test-results.json`은 덮어쓰지 말 것.

## 누락·실측 후 기록할 항목

- AI B 실제 모델/서비스 (공개 비교 구간에서는 익명): 사용자 기록 필요
- AI B 실제 시작/종료 시각, 45분 이내 여부: 사용자 기록 필요
- AI B 사용자 메시지 수 / 8회 이내 여부: 사용자 기록 필요
- AI B 도구 호출 수, 전체 오류 실행 회차: 사용자 기록 필요
- B 시작 때 AI A의 HANDOFF.md와 동일한 원문이었는지, SHA-256 검증 및 누락 여부: 사용자 기록 필요

위 미확인 항목을 추정 수치로 채우지 마세요. 공개 비교 보고서/배포 URL은 아직 완료되지 않았습니다.
