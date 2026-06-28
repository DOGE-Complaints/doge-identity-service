# Тестовые SMS в identity: как запускать без реального провайдера и где читать OTP-коды

> **Дата:** 2026-06-28 · **Скоуп:** серверное `doge-identity-service` (фронт `spa-app` — вне фокуса).
> **Тип:** операционная документация (how-to), все утверждения подтверждены кодом (`file:line`) по [`analysis.mdc`](../../../.cursor/rules/analysis.mdc).
> **История:** документ вырос из gap-анализа SMS-моков; gap **G-SMS-1** («через mock код негде взять для ручного теста») закрыт стори [STORY-IDS-PV-10](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) — добавлен провайдер `file`. Аудит закрытия: [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](./epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md).

---

## 0. Три режима SMS — что выбрать

| Режим (`SMS_PROVIDER`) | Что делает | Где код | Когда использовать |
|---|---|---|---|
| **`file`** ⭐ | пишет текст SMS в файл на диске, **один файл на номер** | `<cwd>/var/sms-outbox/<номер>.log` → `tail -f` | **Ручной тест через фронт локально.** Бюджет не тратится, сети нет. |
| **`mock`** (default) | складывает SMS в **память процесса** | только in-process `sent_messages` — **снаружи не видно** | Автотесты. Для ручного теста **код взять негде**. |
| **`telnyx`** | реальная отправка через Telnyx | **настоящая SMS** на телефон `+372…` | Финальный e2e на реальном устройстве (тратит бюджет). |

**Вывод для ручного тестирования:** локально — `SMS_PROVIDER=file`. На Railway — см. §6 (есть нюансы).

---

## 1. Быстрый старт локально с `file` (рекомендуется)

1. В `.env`:
   ```bash
   APP_PROFILE=demo                 # file запрещён в pilot — см. §5
   SMS_PROVIDER=file
   FILE_SMS_OUTBOX_DIR=var/sms-outbox   # необязательно; это и есть дефолт
   PHONE_ALLOWED_DIAL_PREFIXES=+372
   ```
   Дефолт `FILE_SMS_OUTBOX_DIR=var/sms-outbox` зашит в коде ([`config.py:9,18`](../../src/core/phone/file/config.py)), переменную можно не задавать.
2. Запустить сервер: `make serve` (поднимает `uvicorn core.api.asgi_app:app`, [`Makefile:3-6`](../../Makefile)).
3. В другом терминале следить за кодами:
   ```bash
   tail -f var/sms-outbox/+37255555555.log
   ```
4. Прогнать флоу с фронта (или curl, §4). Каждый `POST /auth/phone/request` дописывает строку:
   ```
   2026-06-28T10:01:02Z	Your Dogestonia verification code is 482913.
   ```
   Формат: `{UTC-таймстемп до секунды}\t{текст SMS с кодом}` ([`file_sender.py:14-17,34-44`](../../src/core/phone/file/file_sender.py)).

### Где именно лежат файлы
- Путь **относительный** (`Path(settings.outbox_dir)`, [`descriptor.py:16`](../../src/core/phone/file/descriptor.py)) → считается **от текущей рабочей директории процесса (cwd)**, а не от `src/`. Флаг `--app-dir src` в [`Makefile:5`](../../Makefile) влияет только на импорт модулей, не на cwd. При `make serve` из корня сервиса файлы окажутся в `doge-identity-service/var/sms-outbox/`.
- Имя файла = номер, очищенный до `[+0-9]` ([`file_sender.py:11,20-21`](../../src/core/phone/file/file_sender.py)): `+37255555555` → `+37255555555.log`. Каталог создаётся автоматически (`mkdir parents=True, exist_ok=True`, [`file_sender.py:39`](../../src/core/phone/file/file_sender.py)).
- Каталог в [`.gitignore:11`](../../.gitignore) (`var/sms-outbox/`) — в git не попадает.
- Это **plaintext OTP на диске** — осознанно dev-only (поэтому запрещён в pilot, §5).

---

## 2. Быстрый старт с `mock` (для понимания — почему код не видно)

`SMS_PROVIDER=mock` — дефолт ([`schema.py:170`](../../src/core/config/schema.py)). Сервер стартует, флоу работает, но **код для ручного теста взять негде**:
- `MockSmsSender.send` кладёт `(номер, текст)` в in-memory список `_sent` ([`mock_sender.py:23-25`](../../src/core/phone/mock/mock_sender.py)); наружу доступно только свойство `sent_messages` **внутри того же процесса**.
- В HTTP-ответ, логи и БД **plaintext-код не пишется** (см. §3).
- Поэтому `mock` годится для автотестов (они читают `sent_messages` в процессе, [`test_phone_verification_flow.py:51-66`](../../tests/test_phone_verification_flow.py)), но **не для ручного теста через браузер**. Для ручного — используйте `file`.

---

## 3. Почему код не «утекает» сам по себе

| Этап | Что с кодом | Видно снаружи? |
|------|-------------|----------------|
| Генерация | `plaintext_code = _generate_otp_code(...)` ([`otp_engine.py:48`](../../src/core/phone/otp_engine.py)) | нет |
| Сессия/БД | хранится только `code_hash = hash_secret(...)` ([`otp_engine.py:55`](../../src/core/phone/otp_engine.py)) | нет (только хеш) |
| Текст SMS | `"Your Dogestonia verification code is {code}."` ([`sms_text.py:4-5`](../../src/core/phone/sms_text.py)) | — |
| HTTP-ответ | `{sent, expires_at}` ([`handlers.py:531-532`](../../src/core/api/handlers.py)) | **кода нет** |
| Логи/аудит | пишется `event_type`, номер **хешируется** | **кода нет** |
| **Отправка** | `mock` → память; `file` → файл; `telnyx` → реальная SMS | зависит от провайдера |

Единственная «легитимная утечка» кода в открытом виде — **то, что делает активный провайдер**: память (`mock`), файл (`file`) или SMS (`telnyx`). Это намеренный анти-leak дизайн ([spa STORY-SPA-ID-04:51](../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-04-phone-verification-flow.md)) — поэтому `file` строго demo-only.

---

## 4. Полный ручной флоу (endpoints)

Все вызовы — `Authorization: Bearer <supabase_access_token>`, `Content-Type: application/json`.

```bash
# 1) запросить код (сервер отправит «SMS» активным провайдером)
curl -X POST http://localhost:8100/auth/phone/request \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"phone":"+37255555555"}'
# ← {"data":{"sent":true,"expires_at":"…"}}   (кода в ответе НЕТ)

# 2) подсмотреть код (режим file):
tail -n1 var/sms-outbox/+37255555555.log     # → …\tYour Dogestonia verification code is 482913.

# 3) подтвердить
curl -X POST http://localhost:8100/auth/phone/confirm \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"phone":"+37255555555","code":"482913"}'
# ← {"data":{"status":"verified"}}

# 4) проверить флаг
curl http://localhost:8100/me -H "Authorization: Bearer $TOKEN"   # → phone_verified:true
```
Оркестрация запроса: [`handlers.py:494-510`](../../src/core/api/handlers.py) (`registry.get_active` → `create_phone_verification_session` → `sender.send`). Правила кода (6 цифр, TTL 5 мин, 5 попыток, cooldown 60с) — серверные `PHONE_*` ([`.env.example:62-69`](../../.env.example)), через API не отдаются.

---

## 5. demo vs pilot: что разрешено

| `SMS_PROVIDER` | `APP_PROFILE=demo` | `APP_PROFILE=pilot` |
|---|---|---|
| `mock` | ✅ работает | ✅ работает (но верификация «бутафорская») |
| `file` | ✅ работает | ❌ **`ConfigError` на старте** ([`schema.py:180-182`](../../src/core/config/schema.py)) — plaintext OTP на диск в pilot запрещён |
| `telnyx` | ✅ (если заданы creds) | ✅ (creds обязательны при отправке) |

- Валидация значения провайдера: [`schema.py:173-176`](../../src/core/config/schema.py) (неизвестный → `ConfigError`).
- Pilot **не требует** Telnyx (SMS-полей нет в pilot-required списке, [`schema.py:185+`](../../src/core/config/schema.py)) — pilot можно запустить с `mock`.
- **Важно:** `file` нельзя использовать под `pilot`. Если ваш Railway-сервис запущен с `APP_PROFILE=pilot`, провайдер `file` не стартует вообще (см. §6).

---

## 6. Будет ли это работать на Railway? ⚠️ (важные нюансы)

Короткий ответ: **`file`-режим технически запишет файлы и на Railway, но прочитать их там — неудобно, а `mock` — невозможно.** Разбор по фактам:

### 6.1 Что известно про деплой из репозитория
- [`railway.json`](../../railway.json) содержит **только** healthcheck `/health` (эндпоинт есть: [`asgi_app.py:285-286`](../../src/core/api/asgi_app.py)) и timeout. **Нет** `startCommand` и **нет** конфигурации **Volume** (persistent disk).
- Значит файловая система контейнера на Railway — **эфемерная**: persistent-том не примонтирован.

### 6.2 `mock` на Railway → код прочитать НЕЛЬЗЯ
Код лежит в памяти процесса ([`mock_sender.py:24`](../../src/core/phone/mock/mock_sender.py)), наружу не выставлен, в логи не пишется. Удалённо достать его нечем. ❌

### 6.3 `file` на Railway → файлы пишутся, но есть три подвоха
1. **Не видно в `railway logs`.** `FileSmsSender` пишет в **файл** ([`file_sender.py:40`](../../src/core/phone/file/file_sender.py)), а не в stdout. Поток логов Railway показывает stdout/stderr — кодов там не будет.
2. **Нужен доступ в шелл контейнера.** Чтобы сделать `cat/tail` файла `<cwd>/var/sms-outbox/<номер>.log` на работающем сервисе, нужен интерактивный доступ внутрь контейнера (зависит от возможностей/плана платформы). Без него файл недостижим.
3. **Эфемерность.** Persistent-том не сконфигурирован (§6.1) → файлы живут только до перезапуска/редеплоя контейнера и не переживают их.
4. **Профиль.** Если сервис запущен с `APP_PROFILE=pilot`, `file` вообще не стартует (§5, [`schema.py:180-182`](../../src/core/config/schema.py)) — для `file` нужен `APP_PROFILE=demo`.

### 6.4 Что делать для ручного теста «в облаке» (по убыванию практичности)
- **Telnyx + реальный `+372`** — единственный режим, где код приходит на устройство без доступа в контейнер. Подходит для облака напрямую. Тратит бюджет.
- **Railway Volume + `file`.** Примонтировать Railway Volume (напр. в `/data`) и задать `FILE_SMS_OUTBOX_DIR=/data/sms-outbox` — файлы станут persistent. Но **чтение всё равно требует доступа в контейнер** (п.6.3.2). *(Том в репозитории сейчас не настроен — это инфраструктурная правка вне кода.)*
- **Локальный прогон против облачной БД.** Запустить identity локально (`SMS_PROVIDER=file`, `tail -f`), указав в `.env` те же Supabase-креды, что и в облаке — фронт-тест гоняем на локальный identity, коды читаем из локальных файлов.
- **(Не построено)** demo-only dev-эндпоинт `GET /dev/last-otp`, читающий outbox/`sent_messages` — это был вариант 2 закрытия G-SMS-1; в коде его нет. Был бы самым удобным для облака, но потребовал бы отдельной стори с жёстким `demo`-gate.

### 6.5 Резюме по Railway
| Сценарий | Результат |
|---|---|
| Railway + `mock` | ❌ код недоступен |
| Railway + `file` (без Volume) | ⚠️ пишется в эфемерный диск, не в логах, нужен шелл; теряется при редеплое |
| Railway + `file` + Volume | ⚠️ persistent, но читать всё равно через шелл контейнера; `APP_PROFILE=demo` обязателен |
| Railway + `telnyx` | ✅ реальная SMS на телефон |
| **Локально + `file`** | ✅ **проще всего: `tail -f var/sms-outbox/<номер>.log`** |

---

## 7. Сводка проверенных фактов (file:line)

- Провайдер `file`: [`file_sender.py`](../../src/core/phone/file/file_sender.py) (append, санитайз, таймстемп), [`config.py`](../../src/core/phone/file/config.py) (`FILE_SMS_OUTBOX_DIR`, default `var/sms-outbox`), [`descriptor.py`](../../src/core/phone/file/descriptor.py).
- Провайдер `mock`: [`mock_sender.py:9-25`](../../src/core/phone/mock/mock_sender.py) (in-memory).
- Реестр/выбор активного: [`registry_builder.py`](../../src/core/phone/registry_builder.py), `get_active` [`registry.py:24-25`](../../src/core/phone/registry.py).
- `SMS_PROVIDER` default `mock` + валидация + file-fail-fast в pilot: [`schema.py:170-182`](../../src/core/config/schema.py); pilot-required без SMS: [`schema.py:185+`](../../src/core/config/schema.py).
- `file`/`mock` не поднимают HTTP-клиент: [`runtime_factory.py:14-15`](../../src/core/phone/runtime_factory.py).
- Реестр строится 1 раз при старте: [`providers.py:130-132`](../../src/core/infrastructure/providers.py), [`service_factory.py:75-76`](../../src/core/infrastructure/service_factory.py).
- Код только хешируется в сессию: [`otp_engine.py:48-64`](../../src/core/phone/otp_engine.py); текст SMS: [`sms_text.py:4-5`](../../src/core/phone/sms_text.py); в ответе кода нет: [`handlers.py:531-532`](../../src/core/api/handlers.py); отправка: [`handlers.py:494-510`](../../src/core/api/handlers.py).
- Деплой: [`railway.json`](../../railway.json) (healthcheck `/health`, без startCommand/Volume), `/health` [`asgi_app.py:285-286`](../../src/core/api/asgi_app.py), запуск [`Makefile:3-11`](../../Makefile).
- Тестовый шов (чтение кода в автотестах): [`test_phone_verification_flow.py:51-66`](../../tests/test_phone_verification_flow.py); тесты `file`: [`test_phone_file_sms_sender.py`](../../tests/test_phone_file_sms_sender.py).
- Анти-leak на фронте: [spa STORY-SPA-ID-04:51](../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-04-phone-verification-flow.md).
