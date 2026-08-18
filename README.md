# Mini NPU 시뮬레이터

Python 표준 라이브러리만으로 만든 콘솔 기반 MAC(Multiply-Accumulate) 패턴 판별 시뮬레이터입니다. 입력 패턴과 Cross/X 필터를 비교해 점수, 판정, 성능을 출력합니다.

## 주요 기능

- 3x3 사용자 입력 기반 필터/패턴 판정
- `data.json` 기반 다중 크기 배치 분석
- `Cross`, `X`, `UNDECIDED` 판정과 PASS/FAIL 요약
- 2D 배열과 Flat 1D 배열 MAC 성능 비교
- 임의 N 크기의 Cross/X 자동 생성 및 성능 분석

## 실행 방법

```bash
git clone git@github.com:k-sungwon/codyssey_mission3.git
cd codyssey_mission3
python3 main.py
```

## 실행 모드

| 모드 | 설명 |
| --- | --- |
| `1` | 3x3 필터 A/B와 패턴을 직접 입력해 판정합니다. |
| `2` | `data.json`의 필터와 패턴을 일괄 분석합니다. |
| `3` | 크기 N의 Cross/X를 생성해 MAC 및 성능을 분석합니다. |
| `0` | 프로그램을 종료합니다. |

## 프로젝트 구조

```text
tiny_mac_cal/
|
|- main.py                    # 프로그램 시작점
|- data.json                  # JSON 분석 입력 데이터
|- mini_npu/
|  |- application.py          # 실행 흐름과 모드 조율
|  |- models.py               # Filter, Pattern, MatchResult 데이터 객체
|  |- calculators.py          # 2D / Flat MAC 계산 전략
|  |- performance.py          # 반복 시간 측정
|  |- loader.py               # JSON 로드와 검증
|  |- input.py                # 콘솔 행렬 입력
|  |- reporter.py             # 콘솔 출력 형식
|  |- helpers.py              # 검증, 라벨, 판정, 생성 함수
|
|- tests/                     # 자동화된 unittest 모음
|- docs/project-structure.md  # 상세 다이어그램과 파일별 책임
```

## 실행 구조

```text
main.py
  -> Application (흐름 조율)
       -> Input / DataLoader / Generator
       -> MAC 계산기 (2D, Flat)
       -> PerformanceAnalyzer
       -> ConsoleReporter
```

`Application`은 실행 흐름만 조율합니다. 데이터 객체는 상태를 보관하고, 계산기는 계산만 하며, 로더는 로드만 하고, 출력기는 형식화만 담당합니다.

전체 실행 다이어그램과 파일별 책임은 [프로젝트 구조 문서](docs/project-structure.md)에서 확인할 수 있습니다.
모드별 코드 호출 순서와 인자 흐름은 [코드 실행 흐름 가이드](docs/code-flow-guide.html)에서 확인할 수 있습니다.

## 모드별 코드 플로우

| 모드 | 시작 코드 | 주요 이동 경로 |
| --- | --- | --- |
| Mode 1 | [run_manual_mode](mini_npu/application.py#L48-L56) | [입력 파싱](mini_npu/input.py#L4-L28) -> [MAC 분석](mini_npu/application.py#L89-L104) -> [2D/Flat 측정](mini_npu/application.py#L121-L130) -> [출력](mini_npu/reporter.py#L10-L56) |
| Mode 2 | [run_json_mode](mini_npu/application.py#L67-L87) | [JSON 로드](mini_npu/loader.py#L22-L85) -> [키/라벨 정규화](mini_npu/helpers.py#L24-L37) -> [MAC 분석](mini_npu/application.py#L89-L104) -> [요약 출력](mini_npu/reporter.py#L39-L56) |
| Mode 3 | [run_generated_mode](mini_npu/application.py#L58-L65) | [크기/라벨 입력](mini_npu/application.py#L137-L154) -> [패턴 생성](mini_npu/application.py#L106-L119) -> [Cross/X 생성 함수](mini_npu/helpers.py#L44-L66) -> [성능 출력](mini_npu/reporter.py#L26-L37) |

## 테스트

```bash
python3 -m unittest discover -s tests -v
```

테스트는 행렬 검증, MAC 계산, epsilon 기반 판정, JSON 오류 처리, 반복 성능 측정, 생성 패턴 재활용을 검증합니다.

## 결과 리포트

- 모드 1은 3x3 필터 A/B와 3x3 패턴을 입력받아 각 필터의 MAC 점수, 최종 판정, 2D/Flat 계산별 평균 시간을 출력합니다.
- 모드 1의 판정 결과는 A 점수가 더 크면 `A`, B 점수가 더 크면 `B`, 두 점수 차이가 허용오차보다 작으면 `UNDECIDED`입니다.
- 수동 입력에서 한 행의 값 개수가 부족하거나 많으면 해당 행만 다시 입력받습니다.
- 수동 입력에서 숫자로 변환할 수 없는 값이 들어오면 오류 메시지를 출력하고 해당 행을 다시 입력받습니다.
- 모드 2는 `data.json`의 `filters`와 `patterns`를 읽고, `size_{N}` 또는 `size_{N}_{idx}` 키에서 크기 N을 추출합니다.
- 모드 2는 패턴 크기에 맞는 필터 묶음을 선택해 Cross/X 점수를 계산합니다.
- JSON 라벨은 `cross`, `+`, `Cross`를 `Cross`로, `x`, `X`를 `X`로 정규화해 문자열 표기 차이로 인한 오판정을 막습니다.
- 모드 2에서 예측값이 `UNDECIDED`이고 expected가 `Cross` 또는 `X`이면 정답과 다르므로 `FAIL`로 집계됩니다.
- 실패 원인은 크게 입력 스키마 오류, 행렬 크기 불일치, 숫자가 아닌 행렬 값, 알 수 없는 라벨, 기대값과 예측값 불일치로 나뉩니다.
- 성능 측정은 계산기별로 같은 MAC 계산을 10회 반복한 뒤 평균 ms를 출력합니다.
- 연산 횟수는 행렬 크기가 N x N일 때 한 번의 필터 비교에 필요한 MAC 수인 N²으로 출력합니다.
- 시간 복잡도는 필터 하나와 패턴 하나를 비교할 때 O(N²), 패턴 P개와 필터 F개를 비교할 때 O(P x F x N²)입니다.
- Flat 1D 방식은 반복문 모양이 1차원이지만 펼쳐진 리스트 길이가 N²이므로 이론적 시간 복잡도는 2D 방식과 같은 O(N²)입니다.
- 공간 복잡도는 행렬 데이터를 저장하는 데 O(N²)이 필요하고, Flat 방식은 펼친 리스트를 만들기 때문에 추가 O(N²) 공간을 사용할 수 있습니다.
- 콘솔 요약은 전체 케이스 수, 통과 수, 실패 수를 `SUMMARY | total=... | pass=... | fail=...` 형식으로 출력합니다.
- 실패 케이스가 있으면 요약 뒤에 `FAILED_CASE | case=... | predicted=... | expected=...` 또는 `FAILED_CASE | case=... | reason=...` 형식으로 실패 목록을 출력합니다.
