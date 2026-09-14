# Bank API

A small banking API that processes account events — **deposit**, **withdraw** and **transfer** — through a single `POST /event` endpoint, exposes account balances via `GET /balance`, and can wipe its own state via `POST /reset`.

The project is built with Django and Django REST Framework, and is organised following **Clean Architecture**: business rules live in plain Python objects with no framework dependencies, and the database and the web layer are plug-in details around them.

---

## Tech stack

| Tool | Purpose |
|------|---------|
| Python 3.12+ | Language (developed on 3.13) |
| Django 6.1 | Application framework, ORM, migrations |
| Django REST Framework 3.18 | HTTP layer, serialization, validation, exception handling |
| drf-spectacular 0.30 | OpenAPI 3 schema generation + Swagger UI |
| SQLite | Default persistence (swappable — see *Configuration*) |
| pytest + pytest-django | Test runner |

---

## Architecture

The codebase is split into four layers. The **Dependency Rule** is enforced: dependencies only point inwards, and no inner layer knows anything about an outer one.

| Layer | Contains | Depends on |
|-------|----------|------------|
| `domain/` | Entities (`Account`, `Transaction`), business invariants, domain exceptions, and the repository **interfaces** | Nothing but the Python standard library |
| `application/` | Use cases (`TransactionService`, `BalanceService`, `ResetService`) and the DTOs they consume | `domain/` only |
| `infrastructure/` | Django ORM models, repository **implementations**, migrations | `domain/` + Django |
| `api/` | DRF views, serializers, OpenAPI schema, exception handler | `application/` + `domain/` + DRF |

Two consequences worth pointing out:

- **The domain has zero framework imports.** `app/domain/` imports only `abc`, `dataclasses` and `enum`. Business rules such as *"you cannot withdraw more than your balance"* live in `Account`, not in a view or a model, and are unit-tested without a database, an HTTP client or Django itself.
- **Persistence is a swappable adapter.** `AccountRepository` and `TransactionRepository` are abstract interfaces declared in the domain. `infrastructure/` provides two implementations of each — one backed by the Django ORM, one in memory — and `app/wiring.py` acts as the composition root that picks which pair to inject. The use cases never learn which one they got.

### Project structure

```
app/
├── domain/                  # Entities, invariants, exceptions, ports (no framework)
│   ├── entities/            #   Account, Transaction, TransactionType
│   ├── repositories/        #   AccountRepository, TransactionRepository (ABCs)
│   └── exceptions.py
├── application/             # Use cases + DTOs
│   ├── services.py
│   └── dtos.py
├── infrastructure/          # Adapters: Django ORM models, repositories, migrations
│   ├── models.py
│   └── repositories/        #   orm.py | in_memory.py
├── api/                     # DRF views, serializers, OpenAPI schema, exception handler
└── wiring.py                # Composition root: builds the services and injects adapters

config/                      # Django settings, WSGI/ASGI entrypoints
tests/                       # Domain, service and API tests
```

---

## Getting started

### 1. Clone and enter the project

```bash
git clone <repository-url>
cd bank-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
```

macOS / Linux:

```bash
source venv/bin/activate
```

Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000`.

---

## API reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/event` | Processes a `deposit`, `withdraw` or `transfer` |
| `GET` | `/balance?account_id=<id>` | Returns the balance of an account |
| `POST` | `/reset` | Clears all accounts and transactions |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/schema` | OpenAPI 3 schema (YAML) |

---

## API documentation

Interactive documentation is generated from the code by drf-spectacular. With the server running, open:

- **Swagger UI** — <http://127.0.0.1:8000/docs>
- **OpenAPI schema** — <http://127.0.0.1:8000/schema>

---

## Running the tests

```bash
DJANGO_SETTINGS_MODULE=config.settings pytest
```

The suite is layered the same way the code is:

- `tests/test_domain.py` — entity invariants, no framework involved.
- `tests/test_services.py` — use cases driven through the in-memory adapters, no database.
- `tests/test_api.py` — the full HTTP contract, end to end.

---

## Configuration

`config/settings.py` exposes a single switch that selects the persistence adapter:

```python
USE_IN_MEMORY_REPOSITORIES = True   # in-memory dictionaries, no database
USE_IN_MEMORY_REPOSITORIES = False  # Django ORM + SQLite
```

Nothing outside `app/wiring.py` reacts to this flag — which is the practical demonstration that the persistence choice really is an outer-layer detail.

---

## idempotency

`POST /event` is not idempotent. The endpoint moves money, so any client retry — a request that timed out, a proxy that resends, a user pressing the button twice — is processed as a second, distinct event and the account is debited or credited again. Nothing in the current design prevents that, and for a banking API it is the gap that matters most.

A future version would close it with an optional `Idempotency-Key` header:

- a store that **atomically** claims the key before the event runs — a table with a unique constraint on the key, or Redis — so that two simultaneous retries cannot both win the claim;
- the response of the first request stored against the key and replayed to every retry that carries it, leaving the accounts untouched;
- a fingerprint of the payload alongside the key, so that reusing one key for a different operation is rejected rather than silently answered with the wrong stored response;
- `409` while the first request is still in flight, instead of racing it.

The seam is already there: the use cases receive their collaborators through the constructor and `app/wiring.py` is the only place that knows which implementations they get, so the store would enter as one more injected port without the domain layer learning about it.
