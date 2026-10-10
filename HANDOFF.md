# AURORA MAX HISTORY — AI A → AI B HANDOFF

**AI B는 이 문서와 연결된 작업 저장소의 소스만 읽고 이어받으세요.** AI A와의 대화 전문은 제공하지 않습니다.

## 1. 목표

기존 오로라 정보판 `DAILY RECORDS` 안의 `VIEW HISTORY` 버튼에서 별도 폴더형 `AURORA MAX HISTORY` 모달을 엽니다. 날짜별 실제로 수신한 최고 MAX(OBSERVED), 원천 NOAA UTC 시간, 날짜별 LATEST와 대표 최고 기록을 표시합니다. 실제 사용자의 NOAA 기록은 변경하지 않습니다.

## 2. 현재 상태

- 작업 저장소: https://github.com/jennajiminkim/aurora-max-history-task5
- **작업 브랜치: `t05-ai-a-handoff`**. `main`은 변경하지 않았습니다.
- AI A의 실제 **시작 GitHub 커밋**: `bec15b6033e8cb031257ff69f756787bf41aed10`
- **AI A 종료 소스 코드 버전 ID**: `e13b7d3d87f0d9d7b57a056143e161a83a3b8883` (GitHub에서 실제 존재하는 커밋). 이 커밋에 `app.js`, `index.html`, `styles.css`, `max-history-data.js`의 A 구현이 포함됩니다.
- 그 뒤 추가된 커밋은 인수인계와 고정 검사 실행·증거 게시용이며, 위 **A 종료 소스 파일 4개의 내용은 변경하지 않았습니다**. B는 `t05-ai-a-handoff` 브랜치 최신 코드를 체크아웃하여 시작하고, 체크아웃 당시 **전체 Git HEAD**도 별도로 기록하세요.
- AI A는 읽기 전용 MAX 집계, 날짜 역순, 동점 최고값 우선순위, 구형 레코드 처리, 폴더형 목록·막대 시각화를 구현했습니다.
- AI B가 완성해야 할 기능은 모달 닫기/ESC 및 **날짜 선택 상세 화면**입니다.
- 원본 사이트: https://aurora-observation.vercel.app/ — 변경하지 않음.

## 3. 실행 명령

공개 GitHub 소스만으로 새 폴더에서 재현:

```bash
git clone -b t05-ai-a-handoff https://github.com/jennajiminkim/aurora-max-history-task5.git aurora-t05-b
cd aurora-t05-b
git rev-parse HEAD
python -m pip install playwright
python -m playwright install chromium
node --check app.js
node --check max-history-data.js
python task5/run_frozen.py
```

Python 3 및 Node.js 사용. 기존 Chromium 설치 환경에서는 추가 브라우저 설치가 필요 없을 수 있습니다. 테스트는 메모리 내 합성 데이터만 사용하며 실측 NOAA 요청을 발생시키지 않습니다. 현재 H02/H05/H06 때문에 종료 코드 1, 전체 7/10을 예상합니다.

테스트 계약 무결성:
```bash
shasum -a 256 FROZEN-TESTS.json
```

반드시 `c03036a50a31473fcb6bce74226b6bda8d0ad8a0e770ed464cfed7ba455b2d23`이어야 합니다.

## 4. 통과 검사

AI A의 **고정 10개 중 7 PASS / 3 FAIL**. 증거: `task5/A-test-results.json`, `task5/A-RUNS.md`.

| 검사 | A 결과 | 관찰 내용 |
|---|---|---|
| T05-H01 | PASS | 폴더형 모달, 1440/390px |
| T05-H02 | FAIL | 닫기 × 동작 없음 (Esc는 브라우저에서 지원) |
| T05-H03 | PASS | KST 날짜 최신순 |
| T05-H04 | PASS | LATEST 12 대신 MAX 65 사용 |
| T05-H05 | FAIL | 선택 날짜 MAX UTC 시간이 상세 패널에 없음 |
| T05-H06 | FAIL | 날짜/막대 클릭해도 상세 패널 값이 변경되지 않음 |
| T05-H07 | PASS | 최고 65pt 동점이면 최신 KST 날짜 |
| T05-H08 | PASS | 같은 KST 날짜 병합, 다음 날짜 추가 |
| T05-H09 | PASS | 빈 상태 및 구형 값 fallback |
| T05-H10 | PASS | PREVIEW와 합성 fixture 기록 격리 |

고정 10개 전체를 실행한 회차 중 하나 이상 FAIL이 있는 **오류 회차 4회**. 사용자 요청 수 1, 작업시간 12분 44초. 도구 호출 수는 자동 집계되지 않아 임의 숫자를 만들지 않았습니다. AI B는 자기 작업시간과 요청/호출 수를 별도로 기록하세요.

## 5. 남은 문제

- **첫 실패 H02:** `#maxHistoryClose` 클릭 후 `#maxHistoryDialog.open`이 여전히 참입니다. 클릭 및 Escape로 닫혀야 하며 LIVE/EVENT 저장 내용을 그대로 유지해야 합니다.
- **H05:** 2026-08-25 날짜 선택 시 `#maxHistoryDetail`에 `2026-08-25 11:20 UTC` 표시 필요.
- **H06:** 2026-10-09 선택 시 `#maxHistoryDetail`에 `2026-10-09`, `9 pt` (MAX), `5 pt` (LATEST), `2026-10-09 12:04 UTC` 표시 필요.
- 새 작업 폴더/환경에서 검사 명령을 재현하고 누락이 있다면 문서 수정 전/후를 명시하세요.

## 6. 다음 행동

1. 저장소 `t05-ai-a-handoff` 브랜치를 새 폴더에 clone, `git rev-parse HEAD`를 B 시작 전체 SHA로 기록.
2. `FROZEN-TESTS.json` SHA 확인, `python task5/run_frozen.py`로 7 PASS / 3 FAIL 확인. 시험에 필요한 의존성을 설치.
3. `app.js`의 이벤트 등록 위치에서 닫기 × 연결, ESC 처리 검토. 기록 변경 없이 닫고 초점 복귀.
4. `renderMaxHistory()`와 `MaxHistoryData.model(...).rows`를 이용해 날짜 행 클릭 및 상세 MAX/LATEST/MAX TIME 표시 구현.
5. **동일한 T05-H01~H10 총 10개**를 그대로 재실행하여 PASS 10개 달성. 결과를 별도 `task5/B-test-results.json` 등에 남기고 A 증거는 보존.
6. B 시작→B 종료시간, 요청 수(최초 1회 포함), 도구 호출 수(가능하면), 실패 회차, 시작/종료 소스 SHA를 기록하고 이름을 가린 공개 비교 보고서를 완성.

## 7. 건드리지 말 것

- `FROZEN-TESTS.json` / `FROZEN-TESTS.md`의 검사 ID·입력·기대값과 동일한 45분·8요청 사용 상한.
- 기존 오로라 ASCII 애니메이션/프레임 속도, NOAA 15분 간격, DAILY RECORDS, 65pt EVENT ARCHIVE, PREVIEW, T04 VERIFICATION.
- 실측 LIVE 로컬 기록과 실제 NOAA 응답. 합성 테스트만 분리된 `sessionStorage` 키 `aot_t05_history_fixtures_only`에 저장.
- 기존 공개 서비스와 원본 저장소 main을 변경하지 않음.
- AI A와의 대화, 개인정보, 비밀값을 B에게 제공하거나 공개 보고서에 포함하지 않음.
- 모델/서비스 이름은 평가용 공개 보고서 비교 구간에서는 익명 A/B로 표시.

**인계 동일성:** B는 이 GitHub 브랜치의 `HANDOFF.md` 원본 파일을 그대로 읽고 복제 시 SHA-256으로 동일성을 검증하세요.
