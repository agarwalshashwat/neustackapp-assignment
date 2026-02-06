# Design Decisions

This document outlines the architectural and design choices made during the development of the Ecommerce Store API.

## Decision: Choice of FastAPI

**Context:** Selecting a web framework for the backend.

**Options Considered:**
- Option A: Flask
- Option B: FastAPI

**Choice:** FastAPI

**Why:** FastAPI provides high performance, out-of-the-box support for asynchronous programming, and automatic OpenAPI documentation. Its use of Pydantic for data validation ensures type safety and reduces boilerplate code compared to Flask.

---

## Decision: In-Memory Storage

**Context:** Determining how to persist cart and order data.

**Options Considered:**
- Option A: Relational Database (SQLite/PostgreSQL)
- Option B: In-memory Python dictionaries/lists

**Choice:** In-memory Storage

**Why:** Per the requirements, "In-memory store is fine." For a technical assignment of this scope, it avoids the overhead of managing database migrations and external dependencies, allowing for a faster setup and demonstration of core logic.

---

## Decision: Thread Safety for Global State

**Context:** Managing concurrent access to the in-memory store.

**Options Considered:**
- Option A: No locking (unsafe)
- Option B: `threading.Lock`

**Choice:** `threading.Lock`

**Why:** Since we are using global in-memory dictionaries and lists to store data, concurrent requests could lead to race conditions (especially during order placement or discount generation). Using a `threading.Lock` ensures that state mutations are atomic and safe.

---

## Decision: Discount Generation Strategy

**Context:** Implementing the "Every nth order gets a coupon code" requirement.

**Options Considered:**
- Option A: Automatically generate code on checkout
- Option B: Explicit Admin API for generation

**Choice:** Explicit Admin API

**Why:** The assignment specifically requested an "Admin API to generate a discount code if the condition is satisfied." This provides administrative control and clearly separates user-facing checkout logic from administrative reward management.

---

## Decision: UUIDs for Cart and Order IDs

**Context:** Generating unique identifiers for resources.

**Options Considered:**
- Option A: Sequential Integers
- Option B: Universally Unique Identifiers (UUID)

**Choice:** UUID

**Why:** UUIDs prevent ID guessing/enumeration attacks (exposure of order volume) and allow for distributed ID generation if the system scales. They are more robust for identifying temporary resources like carts in a stateless API environment.
