import re

print("=" * 70)
print("CHECKING WHICH music_db.py METHODS ARE CALLED IN TEST FILES")
print("=" * 70)

methods = [
    "clear_database",
    "load_single_songs",
    "get_most_prolific_individual_artists",
    "get_artists_last_single_in_year",
    "load_albums",
    "get_top_song_genres",
    "get_album_and_single_artists",
    "load_users",
    "load_song_ratings",
    "get_most_rated_songs",
    "get_most_engaged_users"
]

test_files = ["test_music_db.py", "test_assertions.py", "test_quick.py"]

for test_file in test_files:
    print(f"\n{'=' * 70}")
    print(f"FILE: {test_file}")
    print('=' * 70)
    
    with open(test_file, 'r') as f:
        content = f.read()
    
    called_methods = []
    for method in methods:
        # Look for method calls (method followed by opening parenthesis)
        pattern = rf'\b{method}\s*\('
        matches = re.findall(pattern, content)
        if matches:
            count = len(matches)
            called_methods.append((method, count))
    
    if called_methods:
        print(f"\n✓ This file DOES call music_db.py methods:")
        for method, count in called_methods:
            print(f"  - {method}() called {count} time(s)")
    else:
        print(f"\n✗ This file does NOT call any music_db.py methods")

print(f"\n{'=' * 70}")
print("SUMMARY: All Methods Coverage")
print('=' * 70)

for method in methods:
    total_calls = 0
    files_using = []
    for test_file in test_files:
        with open(test_file, 'r') as f:
            content = f.read()
        pattern = rf'\b{method}\s*\('
        matches = re.findall(pattern, content)
        if matches:
            total_calls += len(matches)
            files_using.append(test_file)
    
    if total_calls > 0:
        print(f"✓ {method}(): called {total_calls} times across {len(files_using)} file(s)")
        for f in files_using:
            print(f"    - {f}")
    else:
        print(f"✗ {method}(): NOT CALLED in any test file")

