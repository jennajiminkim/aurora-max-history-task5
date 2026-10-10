# AI A 고정 검사 실행 기록

- T05-H01~T05-H10의 ID, 입력, 기대값은 최초 `FROZEN-TESTS.json`과 동일합니다.
- 파일 SHA-256: `c03036a50a31473fcb6bce74226b6bda8d0ad8a0e770ed464cfed7ba455b2d23`
- 전체 실행 회차 4회, 각각 PASS 7 / FAIL 3 (H02, H05, H06)
- 오류 회차 4회 (FAIL을 1개 이상 포함한 전체 실행 회차를 1회로 계산)
- 환경 제한으로 검사를 시작하지 못한 초기 네비게이션 오류는 실행 회차로 계산하지 않음.
- Playwright 브라우저는 about:blank 인메모리 DOM 방식으로 합성값만 사용함.
- A 테스트의 기존 결과는 `task5/A-test-results.json`에 고정하며 B 실행은 별도 결과 파일에 보존해야 합니다.
