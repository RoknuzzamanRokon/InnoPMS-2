# InnoPMS Starter Backend

Simple starter PMS backend built with FastAPI, SQLAlchemy ORM, Pydantic, Alembic, MySQL, Pipenv, and `.env` configuration.

## Stack

- FastAPI
- SQLAlchemy ORM
- Pydantic
- Alembic
- MySQL
- Pipenv
- `.env` config

## Setup

1. Install dependencies:

```powershell
pipenv install
```

2. Create `.env`:

```powershell
Copy-Item .env.example .env
```

3. Update database values in `.env`.

4. Run the migration:

```powershell
pipenv run alembic upgrade head
```

5. Start the API:

```powershell
pipenv run uvicorn app.main:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

## Business Rules

- `room_type_id` is a manual `BIGINT` field.
- No `ROOM_TYPE` table exists in this starter.
- No foreign key is added on `room_type_id`.
- Inventory is maintained by `property_id + room_type_id + inventory_date`.
- Booking uses check-in inclusive and check-out exclusive dates.
- Formula: `available_rooms = total_rooms - booked_rooms - blocked_rooms`

## Test Order

1. Run migration
2. Create property
3. Create rooms
4. Initialize inventory
5. Check inventory before booking
6. Book 2 rooms
7. Check inventory after booking

## Sample Requests

Create property:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/properties" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Demo Hotel\",\"property_type\":\"hotel\",\"star_rating\":4}"
```

Create 10 rooms:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/rooms/bulk" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"floor\":\"1\",\"room_status\":\"vacant\",\"room_numbers\":[\"101\",\"102\",\"103\",\"104\",\"105\",\"106\",\"107\",\"108\",\"109\",\"110\"],\"inventory_start_date\":\"2026-03-10\",\"inventory_end_date\":\"2026-03-17\"}"
```

Initialize inventory:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/inventory/initialize" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"start_date\":\"2026-03-10\",\"end_date\":\"2026-03-17\"}"
```

Inventory before booking:

```bash
curl "http://127.0.0.1:8000/api/v1/inventory?property_id=1&room_type_id=1&start_date=2026-03-10&end_date=2026-03-17"
```

Book 2 rooms for 3 nights:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/bookings/book" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"start_date\":\"2026-03-10\",\"end_date\":\"2026-03-13\",\"rooms_to_book\":2}"
```

Block rooms:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/bookings/block" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"start_date\":\"2026-03-13\",\"end_date\":\"2026-03-15\",\"qty\":1}"
```

Release blocked rooms:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/bookings/release-block" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"start_date\":\"2026-03-13\",\"end_date\":\"2026-03-15\",\"qty\":1}"
```

Demo endpoints:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/rooms/demo/create-10" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"start_room_number\":101,\"inventory_start_date\":\"2026-03-10\",\"inventory_end_date\":\"2026-03-17\"}"
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/inventory/demo/initialize" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"days\":7}"
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/bookings/demo/book-2" ^
  -H "Content-Type: application/json" ^
  -d "{\"property_id\":1,\"room_type_id\":1,\"start_date\":\"2026-03-10\"}"
```
