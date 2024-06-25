# Combining the given types of books and removing duplicates to create an ultimate list

book_types_list = [
    [
        "Fiction & Narrative",
        "Guilds & Societies",
        "Histories & Biographies",
        "Manuals & Instructions",
        "People & Places",
        "Politics & Propaganda",
        "Religion & Legends",
        "Research",
        "Jokes, Songs, Riddles, and Plays",
        "Other"
    ],
    [
        "Histories & Biographies",
        "Manuals & Instructions",
        "Religion & Legends",
        "Research",
        "Songs & Riddles",
        "Announcements & Warnings",
        "Inscriptions & Epitaphs",
        "Journals",
        "Letters & Notes",
        "Lists & Records"
    ],
    [
        "Histories & Biographies",
        "Research",
        "Songs & Poems",
        "Other",
        "Announcements & Warnings",
        "Journals & Letters"
    ],
    [
        "Fiction & Narrative",
        "Guilds & Societies",
        "Histories & Biographies",
        "Manuals & Instructions",
        "People & Places",
        "Politics & Propaganda",
        "Religion & Legends",
        "Research",
        "Songs & Poems",
        "Jokes & Riddles",
        "Plays",
        "Other",
        "Advertisements",
        "Announcements & Warnings",
        "Inscriptions & Epitaphs",
        "Journals",
        "Letters & Notes",
        "Lists & Records"
    ],
    [
        "Fiction & Narrative",
        "Guilds & Societies",
        "Histories & Biographies",
        "Manuals & Instructions",
        "People & Places",
        "Politics & Propaganda",
        "Religion & Legends",
        "Research",
        "Songs & Poems",
        "Jokes & Riddles",
        "Plays",
        "Other",
        "Advertisements",
        "Announcements & Warnings",
        "Inscriptions & Epitaphs",
        "Journals",
        "Letters & Notes",
        "Lists & Records"
    ],
    [
        "Fiction & Narrative",
        "Guilds & Societies",
        "Histories & Biographies",
        "Manuals & Instructions",
        "People & Places",
        "Politics & Propaganda",
        "Religion & Legends",
        "Research",
        "Songs & Poems",
        "Jokes & Riddles",
        "Plays",
        "Other",
        "Advertisements",
        "Announcements & Warnings",
        "Inscriptions & Epitaphs",
        "Journals",
        "Letters & Notes",
        "Lists & Records"
    ],
    [
        "Fiction & Narrative",
        "Guilds & Societies",
        "Histories & Biographies",
        "Manuals & Instructions",
        "People & Places",
        "Politics & Propaganda",
        "Religion & Legends",
        "Research",
        "Songs & Poems",
        "Jokes & Riddles",
        "Plays",
        "Other",
        "Advertisements",
        "Announcements & Warnings",
        "Inscriptions & Epitaphs",
        "Lists & Records"
    ]
]

# Combine all types and remove duplicates
ultimate_book_types = set()
for book_types in book_types_list:
    ultimate_book_types.update(book_types)

# Convert to sorted list
ultimate_book_types = sorted(ultimate_book_types)

print(ultimate_book_types)
