# AI A / AI B 공통 최초 요청 — 양쪽에 **동일한 본문**을 사용

당신은 기존 오로라 관측 정보판의 작은 개선 기능 **AURORA MAX HISTORY**를 수행하는 AI 세션입니다.

시작 소스는 GitHub 저장소 https://github.com/jennajiminkim/aurora-observation 의 커밋 `b23ff0796fd1dc39e57e4d31ca851791c91d44e4`이며, 작업은 별도 작업 브랜치/복사본에서 진행하세요. 기존 `main`과 배포 중인 Vercel 웹사이트는 변경하지 마세요.

`FROZEN-TESTS.json` / `FROZEN-TESTS.md`에 등록된 **T05-H01~T05-H10 정확히 10개 검사**를 기준으로 작업하세요. 검사 ID·입력·기대값을 삭제하거나, 완화하거나, 수정하지 마세요. 모든 시험값은 합성이며, 실제 NOAA 일별 저장소 및 65pt 이벤트 아카이브를 오염시키지 않아야 합니다.

**공통 상한:** 최초 이 구현 요청부터 각 AI의 실제 작업시간은 최대 45분, 사용자 메시지 수는 최대 8회입니다. 요청과 도구 호출 수, 시행한 검사 회차 및 회차별 FAIL 유무를 사실대로 기록하세요.

기존 ASCII 애니메이션, NOAA 데이터 조회, 하루 한 건 LATEST/MAX/MAX TIME, 65pt EVENT ARCHIVE, PREVIEW MODE, VERIFICATION을 보존하면서 **DAILY RECORDS 안의 VIEW HISTORY 버튼으로 폴더형 AURORA MAX HISTORY 화면을 열고 날짜별 MAX 기록을 확인하는 기능**을 완성하도록 협업하세요.

**작업 역할과 중단/재개 지점은 저장소의 현재 작업 상태 및 `HANDOFF.md`가 있으면 그 문서에서 파악하세요. 이전 대화 전문이나 다른 AI의 메모리는 요구하지 마세요.** 없는 사실이나 검사 결과를 추측해 채우지 말고 현재 검사 및 Git 커밋으로 확인하세요.

출력에는 작업 시작/종료 시각, 작업 시작/종료 Git 커밋 SHA, 실제 시간과 사용자 요청·도구 호출 수, 10개 고정 검사의 PASS/FAIL, 오류 회차 수, 남은 문제를 기록하세요.
