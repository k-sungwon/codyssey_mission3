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

## 테스트

```bash
python3 -m unittest discover -s tests -v
```

테스트는 행렬 검증, MAC 계산, epsilon 기반 판정, JSON 오류 처리, 반복 성능 측정, 생성 패턴 재활용을 검증합니다.
