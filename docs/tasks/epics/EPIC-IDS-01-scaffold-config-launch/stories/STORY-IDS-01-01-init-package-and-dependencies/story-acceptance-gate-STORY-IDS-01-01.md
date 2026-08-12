# Story Acceptance Gate — STORY-IDS-01-01

- Story: `STORY-IDS-01-01-init-package-and-dependencies`
- Epic: `EPIC-IDS-01`
- Status: PASS

## Checks

- `python3.11 -c "import core"` → PASS
- `python3.11 -m pytest --collect-only -q` → без `ModuleNotFoundError` (количество tests зависит от текущего состояния репозитория)
- `pip show doge-identity-service` → `Version: 0.1.0`
- `find src/core -name '__init__.py' | wc -l` → `11`

## Notes

- Gate привязан к отсутствию `ModuleNotFoundError`, а не к строке `no tests collected`.
