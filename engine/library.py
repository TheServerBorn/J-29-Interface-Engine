DEFAULT_LIBRARY_FOLDER = "PROGRAMS"


def build_library(games):
    """
    Convert the flat game list into a simple filesystem-style
    directory structure.

    Example:

    {
        "WINDOWS": [game, game],
        "DOS": [game],
        "SNES": [game]
    }
    """

    library = {}

    for game in games:
        folder = game.get("folder", DEFAULT_LIBRARY_FOLDER)

        if not folder:
            folder = DEFAULT_LIBRARY_FOLDER

        folder = folder.strip().upper()

        if folder not in library:
            library[folder] = []

        library[folder].append(game)

    # Keep directory and game ordering predictable.
    sorted_library = {}

    for folder in sorted(library):
        sorted_library[folder] = sorted(
            library[folder],
            key=lambda game: game["name"].upper()
        )

    return sorted_library