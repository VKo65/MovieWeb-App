#TESTING.md – MovieWeb App

This document describes the testing strategy and implemented tests for the MovieWeb Flask application.

---

## What Is Being Tested

### 1. User Management
- `add_user()` – Checks if a new user can be added to the database.
- `get_user_by_id()` – Verifies that the correct user can be retrieved by ID.

### 2. Movie Management
- `add_movie()` – Ensures a new movie can be added to a specific user.
- `get_user_movies()` – Validates that the movie appears in the user’s list.
- `delete_movie()` – Tests that a movie can be deleted and no longer appears in the list.

### 3. API Integration
- `/fetch_movie_data` – Tests the API route for fetching movie details via external source (e.g., OMDb API).

---

## How to Run Tests

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate