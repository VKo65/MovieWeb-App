from datamanager.sqlite_data_manager import SQLiteDataManager
from app import app
import time

#Tests running witt App-context
with app.app_context():
    manager = SQLiteDataManager("instance/movies.db")

    # Test 1: add_user()
    print("🔍 Test: add_user()")
    username = f"TestUser_{int(time.time())}"
    user_id = manager.add_user(username)

    assert user_id is not None, "❌ add_user() dont resend ID"
    user = manager.get_user_by_id(user_id)
    assert user is not None, "❌ User not found"
    assert user.username == username, "❌ Username is not correct"
    print("✅ User-Test successful")

    # Test 2: add_movie()
    print("\n🔍 Test: add_movie()")
    movie_title = "The Matrix"
    manager.add_movie(user.id, movie_title, "Lana Wachowski", "1999", "8.7")

    movies = manager.get_user_movies(user.id)
    found = any(movie.title == movie_title for movie in movies)

    assert found, "❌ Movie was not added"
    print("✅ Movie-Test successful")

    # Test 3: update_movie()
    print("\n🔍 Test: update_movie()")
    matrix_movie = next((m for m in movies if m.title == movie_title), None)
    assert matrix_movie is not None, "❌ Movie not found for update"

    success = manager.update_movie(matrix_movie.id, {"rating": 9.9})
    assert success, "❌ update_movie() failed"

    updated_movie = next((m for m in manager.get_user_movies(user.id) if m.id == matrix_movie.id), None)
    assert updated_movie.rating == 9.9, "❌ Movie rating was not updated"
    print("✅ Update-Test successful")

    # Test 4: delete_movie()
    print("\n🔍 Test: delete_movie()")
    latest_movie = next((m for m in reversed(movies) if m.title == movie_title), None)
    assert latest_movie is not None, "❌ Found no movie to delete"
    success = manager.delete_movie(latest_movie.id)
    assert success, "❌ Error while delete_movie()"

    movies_after = manager.get_user_movies(user.id)
    still_exists = any(m.id == latest_movie.id for m in movies_after)
    assert not still_exists, "❌ Movie was not deleted"
    print("✅ Delete-Test successful")


# Test 5: API with Test-Client
print("\n🔍 Test: fetch_movie_data()")
with app.test_client() as client:
    response = client.get("/fetch_movie_data?title=Inception")
    json_data = response.get_json()

    assert response.status_code == 200, "❌ HTTP-Error bei API-Call"
    assert json_data["success"], "❌ API-Response not successful"
    assert "director" in json_data, "❌ No Director in Movie"
    print("✅ API-Test successful")

print("\n🎉 All Tests successful!")
