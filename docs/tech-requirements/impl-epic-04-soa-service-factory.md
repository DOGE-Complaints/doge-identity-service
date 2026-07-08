# NFR: SOA Service Factory

> ⚠️ **Reference-only (2026-06-24):** этот документ скопирован из `doge-complaints-gateway` и описывает ДРУГОЙ сервис (intake/кластеризация историй), не identity. Фактический identity-код — в `src/`; актуальные факты — в `docs/analysis/identity-backend-full-audit-2026-06-24.md` и runtime-docs. Использовать только как шаблон-референс; подлежит переписыванию под identity.

## Назначение

Protocol-based SOA архитектура: каждый репозиторий описан как `Protocol` в `domain/contracts.py`. `DefaultServiceFactory(frozen=True)` принимает Protocol-реализации и создаёт сервисы. `provide_service_factory()` выбирает backend (InMemory/SQLite/Supabase) на основе `DB_BACKEND` env var.

## Источник паттерна

`docs/runtime-docs/bootstrap-infrastructure/03-soa-service-factory.md`

## Бизнес-контекст

`docs/requirements/` — StoryIntakeService, StoryClusterOrchestrator, IssueCreateService и другие сервисы. Они не знают о конкретных репозиториях — только о Protocol-ах.

## Предусловие

- Epic 01 выполнен: `AppConfig`, `provide_app_config()`
- Epic 03 выполнен: `ApiDependencies` с заглушками для сервисов

## Целевые файлы

```
src/core/domain/contracts.py
src/core/application/factory.py
src/core/infrastructure/repositories.py
src/core/infrastructure/service_factory.py
src/core/infrastructure/providers.py
```

---

## Epic Goal

`provide_service_factory()` возвращает `DefaultServiceFactory` с правильными репозиториями для текущего `DB_BACKEND`. `factory.get_story_intake_service()` возвращает рабочий сервис. Смена backend = изменение одной переменной `DB_BACKEND`.

---

## Story 1: Domain Protocols

### Зачем

Protocols в `domain/contracts.py` — единственный источник правды об интерфейсах репозиториев. Domain слой не импортирует httpx, sqlite, fastapi. Сервисы знают только Protocol — им всё равно какой backend используется.

### Tasks

**Task 1.1:** Создать `src/core/domain/contracts.py`.

```python
from __future__ import annotations

from typing import Mapping, Protocol, runtime_checkable


@runtime_checkable
class StoryRepository(Protocol):
    def save_story(self, record: "StoryRecord") -> "StoryRecord": ...
    def get_story(self, story_id: str) -> "StoryRecord | None": ...
    def list_stories(self) -> list["StoryRecord"]: ...
    def list_stories_ready_for_clustering(self) -> list["StoryRecord"]: ...
    def update_lifecycle_status(self, story_id: str, status: "StoryLifecycleStatus") -> None: ...


@runtime_checkable
class IdempotencyRepository(Protocol):
    def get_by_key(self, key: str) -> "IdempotencyRecord | None": ...
    def save(self, record: "IdempotencyRecord") -> "IdempotencyRecord": ...


@runtime_checkable
class StorySignalStore(Protocol):
    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None: ...
    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None: ...


@runtime_checkable
class ClusterMembershipStore(Protocol):
    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None: ...
    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]: ...


@runtime_checkable
class IssueCandidateStore(Protocol):
    def save_candidate(self, candidate: "IssueCandidateRecord") -> None: ...
    def list_candidates(self) -> list["IssueCandidateRecord"]: ...
    def get_candidate(self, cluster_id: str) -> "IssueCandidateRecord | None": ...


@runtime_checkable
class IssueProjectionReadStore(Protocol):
    def list_issues(self, *, status: str | None = None) -> list["DOGEIssue"]: ...
    def get_issue(self, issue_id: str) -> "DOGEIssue | None": ...


@runtime_checkable
class IssueProjectionReadWriteStore(IssueProjectionReadStore, Protocol):
    def save_issue(self, issue: "DOGEIssue") -> None: ...
    def update_issue_status(self, issue_id: str, status: str) -> None: ...


@runtime_checkable
class HealthRepository(Protocol):
    def ping(self) -> bool: ...


@runtime_checkable
class ReviewAuditLogRepository(Protocol):
    def log_decision(self, entry: "ReviewAuditLogEntry") -> None: ...
    def list_entries(self, cluster_id: str) -> list["ReviewAuditLogEntry"]: ...


@runtime_checkable
class EvidencePackRepository(Protocol):
    def save(self, pack: "EvidencePack") -> None: ...
    def get(self, issue_id: str) -> "EvidencePack | None": ...


@runtime_checkable
class StoryEmbeddingStore(Protocol):
    def save_embedding(self, story_id: str, embedding: list[float]) -> None: ...
    def get_embedding(self, story_id: str) -> list[float] | None: ...


@runtime_checkable
class SignalProfileRepository(Protocol):
    def save_profile(self, profile: "SignalProfile") -> None: ...
    def get_profile(self, story_id: str) -> "SignalProfile | None": ...
```

**Важно:** Все `"StoryRecord"`, `"DOGEIssue"` и т.д. — forward references. Реальные dataclass-ы определяются в `domain/models.py`. Protocol слой не импортирует их напрямую — только использует как type hints.

### Acceptance Criteria

- `from core.domain.contracts import StoryRepository` — без ошибок
- Все Protocol-ы имеют `@runtime_checkable` — `isinstance(repo, StoryRepository)` работает
- Domain слой не содержит импортов из `infrastructure.*`, `httpx`, `fastapi`

---

## Story 2: InMemory реализации

### Зачем

Все тесты (unit, service, HTTP, E2E) работают через InMemory репозитории — реализуй их первыми. InMemory не требует никаких внешних зависимостей.

### Tasks

**Task 2.1:** Создать `src/core/infrastructure/repositories.py`.

```python
from __future__ import annotations

from typing import Mapping


class InMemoryHealthRepository:
    def ping(self) -> bool:
        return True


class InMemoryStoryRepository:
    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def save_story(self, record: object) -> object:
        story_id = getattr(record, "story_id")
        self._data[story_id] = record
        return record

    def get_story(self, story_id: str) -> object | None:
        return self._data.get(story_id)

    def list_stories(self) -> list[object]:
        return list(self._data.values())

    def list_stories_ready_for_clustering(self) -> list[object]:
        return [s for s in self._data.values() if getattr(s, "lifecycle_status", None) == "ready_for_clustering"]

    def update_lifecycle_status(self, story_id: str, status: object) -> None:
        record = self._data.get(story_id)
        if record is not None:
            # Dataclass frozen — создаём новый объект с изменённым полем
            import dataclasses
            self._data[story_id] = dataclasses.replace(record, lifecycle_status=status)


class InMemoryIdempotencyRepository:
    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def get_by_key(self, key: str) -> object | None:
        return self._data.get(key)

    def save(self, record: object) -> object:
        key = getattr(record, "key")
        self._data[key] = record
        return record


class InMemoryStorySignalStore:
    def __init__(self) -> None:
        self._data: dict[tuple[str, str], Mapping[str, str]] = {}

    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None:
        self._data[(story_id, policy)] = dict(signals)

    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None:
        return self._data.get((story_id, policy))


class InMemoryClusterMembershipStore:
    def __init__(self) -> None:
        self._memberships: dict[tuple[str, str], str] = {}  # (story_id, lens) -> cluster_id
        self._clusters: dict[tuple[str, str], list[str]] = {}  # (cluster_id, lens) -> [story_ids]

    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None:
        self._memberships[(story_id, lens)] = cluster_id
        key = (cluster_id, lens)
        if key not in self._clusters:
            self._clusters[key] = []
        if story_id not in self._clusters[key]:
            self._clusters[key].append(story_id)

    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]:
        return list(self._clusters.get((cluster_id, lens), []))


class InMemoryIssueCandidateStore:
    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def save_candidate(self, candidate: object) -> None:
        cluster_id = getattr(candidate, "cluster_id")
        self._data[cluster_id] = candidate

    def list_candidates(self) -> list[object]:
        return list(self._data.values())

    def get_candidate(self, cluster_id: str) -> object | None:
        return self._data.get(cluster_id)


class InMemoryIssueProjectionStore:
    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def save_issue(self, issue: object) -> None:
        issue_id = getattr(issue, "issue_id")
        self._data[issue_id] = issue

    def update_issue_status(self, issue_id: str, status: str) -> None:
        issue = self._data.get(issue_id)
        if issue is not None:
            import dataclasses
            self._data[issue_id] = dataclasses.replace(issue, status=status)

    def list_issues(self, *, status: str | None = None) -> list[object]:
        if status is None:
            return list(self._data.values())
        return [i for i in self._data.values() if getattr(i, "status", None) == status]

    def get_issue(self, issue_id: str) -> object | None:
        return self._data.get(issue_id)


class InMemoryReviewAuditLogRepository:
    def __init__(self) -> None:
        self._entries: list[object] = []

    def log_decision(self, entry: object) -> None:
        self._entries.append(entry)

    def list_entries(self, cluster_id: str) -> list[object]:
        return [e for e in self._entries if getattr(e, "cluster_id", None) == cluster_id]


class InMemoryEvidencePackRepository:
    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def save(self, pack: object) -> None:
        issue_id = getattr(pack, "issue_id")
        self._data[issue_id] = pack

    def get(self, issue_id: str) -> object | None:
        return self._data.get(issue_id)


class InMemoryStoryEmbeddingStore:
    def __init__(self) -> None:
        self._data: dict[str, list[float]] = {}

    def save_embedding(self, story_id: str, embedding: list[float]) -> None:
        self._data[story_id] = embedding

    def get_embedding(self, story_id: str) -> list[float] | None:
        return self._data.get(story_id)


class InMemorySignalProfileRepository:
    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def save_profile(self, profile: object) -> None:
        story_id = getattr(profile, "story_id")
        self._data[story_id] = profile

    def get_profile(self, story_id: str) -> object | None:
        return self._data.get(story_id)
```

### Acceptance Criteria

- `InMemoryStoryRepository().save_story(record)` сохраняет и `get_story(id)` возвращает тот же объект
- `InMemoryIdempotencyRepository().get_by_key("unknown")` возвращает `None`
- `InMemoryClusterMembershipStore().get_cluster_members("unknown", "lens")` возвращает `[]`
- Все InMemory реализации не имеют внешних зависимостей (только stdlib)

---

## Story 3: ServiceFactory Protocol и DefaultServiceFactory

### Зачем

`ServiceFactory(Protocol)` — контракт фабрики. `DefaultServiceFactory(frozen=True)` — единственная production реализация. Frozen dataclass принимает репозитории как поля и возвращает сервисы через `get_*()` методы.

### Tasks

**Task 3.1:** Создать `src/core/application/factory.py`.

```python
from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from core.config import AppConfig


class ServiceFactory(Protocol):
    @property
    def config(self) -> "AppConfig": ...

    def get_health_service(self) -> object: ...
    def get_story_intake_service(self) -> object: ...
    def get_story_cluster_orchestrator(self) -> object: ...
    def get_issue_create_service(self) -> object: ...
    def get_issue_projection_read_store(self) -> object: ...
    def get_clustering_engine(self) -> object: ...
    def get_issue_promotion_service(self) -> object: ...
    def get_issue_projection_service(self) -> object: ...
    def get_story_projection_policy(self) -> object: ...
    def get_evidence_pack_service(self) -> object: ...
    def get_geo_service(self) -> object: ...
    def get_signal_profile_service(self) -> object: ...
```

**Task 3.2:** Создать `src/core/infrastructure/service_factory.py`.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.config import AppConfig
    from core.domain.contracts import (
        HealthRepository,
        StoryRepository,
        IdempotencyRepository,
        StorySignalStore,
        ClusterMembershipStore,
        IssueCandidateStore,
        IssueProjectionReadWriteStore,
        ReviewAuditLogRepository,
        EvidencePackRepository,
        StoryEmbeddingStore,
        SignalProfileRepository,
    )


@dataclass(frozen=True)
class DefaultServiceFactory:
    # Required
    health_repository: "HealthRepository"
    story_repository: "StoryRepository"
    idempotency_repository: "IdempotencyRepository"
    issue_candidate_store: "IssueCandidateStore"
    review_audit_log_repository: "ReviewAuditLogRepository"
    evidence_pack_repository: "EvidencePackRepository"
    config: "AppConfig"

    # Optional (None = InMemory default not provided)
    story_signal_store: "StorySignalStore | None" = None
    cluster_membership_store: "ClusterMembershipStore | None" = None
    issue_projection_store: "IssueProjectionReadWriteStore | None" = None
    story_embedding_store: "StoryEmbeddingStore | None" = None
    signal_profile_repository: "SignalProfileRepository | None" = None

    def get_health_service(self) -> object:
        # Import здесь, чтобы избежать circular imports на уровне модуля
        # from core.application.services import HealthService
        # return HealthService(repository=self.health_repository)
        return object()  # заглушка — заменить после создания HealthService

    def get_story_intake_service(self) -> object:
        # from core.application.services import StoryIntakeService
        # return StoryIntakeService(
        #     repository=self.story_repository,
        #     idempotency_repository=self.idempotency_repository,
        #     story_signal_store=self.story_signal_store,
        #     log_debug_dir=self.config.log_debug_dir,
        # )
        return object()  # заглушка

    def get_story_cluster_orchestrator(self) -> object:
        return object()  # заглушка

    def get_issue_create_service(self) -> object:
        return object()  # заглушка

    def get_issue_projection_read_store(self) -> object:
        return self.issue_projection_store  # type: ignore

    def get_clustering_engine(self) -> object:
        return object()  # заглушка

    def get_issue_promotion_service(self) -> object:
        return object()  # заглушка

    def get_issue_projection_service(self) -> object:
        return object()  # заглушка

    def get_story_projection_policy(self) -> object:
        return object()  # заглушка

    def get_evidence_pack_service(self) -> object:
        return object()  # заглушка

    def get_geo_service(self) -> object:
        return object()  # заглушка

    def get_signal_profile_service(self) -> object:
        return object()  # заглушка
```

**Важно:** Заглушки (`return object()`) заменяются реальными конструкторами по мере реализации конкретных сервисов. Структура фабрики и dependency injection остаётся неизменной.

### Acceptance Criteria

- `DefaultServiceFactory` является `frozen=True` — мутация полей бросает `FrozenInstanceError`
- `DefaultServiceFactory(...).config` возвращает переданный `AppConfig`
- `ServiceFactory(Protocol)` не является базовым классом — нет наследования

---

## Story 4: provide_service_factory() — выбор backend

### Зачем

Единственная точка в коде, где `DB_BACKEND` определяет конкретные реализации репозиториев. Снаружи этой функции никто не знает, используется ли InMemory или Supabase.

### Tasks

**Task 4.1:** Создать `src/core/infrastructure/providers.py`.

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from core.config import provide_app_config, AppConfig
from core.infrastructure.repositories import (
    InMemoryHealthRepository,
    InMemoryStoryRepository,
    InMemoryIdempotencyRepository,
    InMemoryStorySignalStore,
    InMemoryClusterMembershipStore,
    InMemoryIssueCandidateStore,
    InMemoryIssueProjectionStore,
    InMemoryReviewAuditLogRepository,
    InMemoryEvidencePackRepository,
    InMemoryStoryEmbeddingStore,
    InMemorySignalProfileRepository,
)
from core.infrastructure.service_factory import DefaultServiceFactory

if TYPE_CHECKING:
    from core.application.factory import ServiceFactory


def provide_service_factory(config: AppConfig | None = None) -> "ServiceFactory":
    """
    Build ServiceFactory with the correct backend repositories.
    Backend selection: DB_BACKEND env var.
    - in_memory: all InMemory* repositories
    - supabase: all Supabase* repositories (requires Epic 05)
    - sqlite: all Sqlite* repositories (future)
    """
    resolved_config = config or provide_app_config()

    # Default: InMemory for all repositories
    health_repository = InMemoryHealthRepository()
    story_repository = InMemoryStoryRepository()
    idempotency_repository = InMemoryIdempotencyRepository()
    story_signal_store = InMemoryStorySignalStore()
    cluster_membership_store = InMemoryClusterMembershipStore()
    issue_candidate_store = InMemoryIssueCandidateStore()
    issue_projection_store = InMemoryIssueProjectionStore()
    review_audit_log_repository = InMemoryReviewAuditLogRepository()
    evidence_pack_repository = InMemoryEvidencePackRepository()
    story_embedding_store = InMemoryStoryEmbeddingStore()
    signal_profile_repository = InMemorySignalProfileRepository()

    if resolved_config.db_backend == "supabase" and resolved_config.supabase_url:
        # Supabase реализации добавляются в Epic 05
        # from core.infrastructure.db_supabase import (
        #     SupabaseDatabase,
        #     SupabaseStoryRepository,
        #     SupabaseIdempotencyRepository,
        #     ...
        # )
        # supabase_db = SupabaseDatabase.from_http(
        #     supabase_url=resolved_config.supabase_url,
        #     service_role_key=resolved_config.supabase_service_role,
        #     timeout_s=float(resolved_config.request_timeout_s),
        # )
        # story_repository = SupabaseStoryRepository(supabase_db)
        # ...
        pass  # заглушка до Epic 05

    return DefaultServiceFactory(
        health_repository=health_repository,
        story_repository=story_repository,
        idempotency_repository=idempotency_repository,
        story_signal_store=story_signal_store,
        cluster_membership_store=cluster_membership_store,
        issue_candidate_store=issue_candidate_store,
        issue_projection_store=issue_projection_store,
        review_audit_log_repository=review_audit_log_repository,
        evidence_pack_repository=evidence_pack_repository,
        story_embedding_store=story_embedding_store,
        signal_profile_repository=signal_profile_repository,
        config=resolved_config,
    )
```

### Acceptance Criteria

- `provide_service_factory()` при `DB_BACKEND=in_memory` возвращает `DefaultServiceFactory` с InMemory репозиториями
- `provide_service_factory(config)` — принимает явный config (для тестов)
- Смена `DB_BACKEND` через env — единственное изменение, нужное для смены backend

---

## Critical Pitfalls

- Protocol не является базовым классом — `isinstance(obj, StoryRepository)` требует `@runtime_checkable`; для type-checking используй mypy/pyright
- `DefaultServiceFactory` создаёт новые сервисы при каждом `get_*()` вызове — если сервис имеет heavy init, рассмотри кеширование (осторожно с shared state)
- Optional поля в `DefaultServiceFactory` должны проверяться внутри `get_*()` — иначе `AttributeError` при обращении к `None`
- Domain слой (`contracts.py`) не должен импортировать из `infrastructure.*` — нарушение этого правила создаёт circular imports

## Верификация эпика

```bash
# 1. Импорты работают
python3.11 -c "
from core.domain.contracts import StoryRepository, IdempotencyRepository
from core.infrastructure.repositories import InMemoryStoryRepository, InMemoryIdempotencyRepository
from core.infrastructure.service_factory import DefaultServiceFactory
from core.infrastructure.providers import provide_service_factory
print('Imports OK')
"

# 2. Protocol runtime check
python3.11 -c "
from core.domain.contracts import StoryRepository
from core.infrastructure.repositories import InMemoryStoryRepository
repo = InMemoryStoryRepository()
assert isinstance(repo, StoryRepository), 'Protocol check failed'
print('Protocol isinstance OK')
"

# 3. Factory создаётся
python3.11 -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://test', 'DB_BACKEND': 'in_memory'})
from core.infrastructure.providers import provide_service_factory
factory = provide_service_factory()
print('db_backend:', factory.config.db_backend)
print('Factory OK')
"

# 4. Tests
python3.11 -m pytest tests/test_di_service_factory.py -v
```
