import json
from pathlib import Path
import shutil

# Define the categories and their corresponding subcategories
categories = {
    "Culture and Tradition": ["Ancestor Worship", "Claw-Dances", "Cosmetics", "Currency", "Marriage", "Music", "Sex", "Slavery", "Smithing", "Statues", "Way of the Voice"],
    "Law and Politics": ["Alessian Doctrines", "Apex Accord", "Armistice", "Cervant Truce", "Code of Malacath", "Coldharbour Compact", "Concordat of Fraternity", "Elden Accord", "First Charter", "First Treaty of Stros M'Kai", "Green Pact", "Guild Act", "Levitation Act", "Moot", "Pact Primordial", "Rights Charter", "Second Treaty of Stros M'Kai", "Treaty of Khenarthi's Roost", "Treaty of Reich Gradkeep", "Treaty of the Three Clans", "The Stricture", "White-Gold Concordat"],
    "Magical Phenomena": ["Abyssal Geysers", "Amber Plasm", "Astronomy", "Azure Plasm", "Cataclyst", "Chaotic Creatia", "Dark Anchors", "Dark Orbs", "Dreamsleeve", "Harrowstorms", "Memory Stones", "Ooze", "Soulburst", "Sigils", "Souls", "Weather Witch"],
    "Metaphysics": ["Aurbis", "CHIM", "Convention", "Daedrons", "Elements", "Godhead", "Mantling", "Mundus", "Nymics", "Planes of Existence", "Psijic Endeavor", "Reincarnation", "The Towers", "Fate"],
    "Rituals and Prophecies": ["Bloodmoon Prophecy", "Dragonfires", "Dream of Kasorayn", "Great Hunt", "Greymarch", "K'Sharra Prophecy", "Nerevarine Prophecy", "Prophecy of the Dark Heart", "Prophecy of the New Moon", "Prophecy of the Dragonborn", "Purification", "Ritual of the Ancestor Moth", "Tyranny of the Sun", "Wild Hunt"],
    "Empires and Kingdoms": ["Aldmeri Dominion (Kingdom of Alinor)", "Ayleid Empire", "Kingdom of Black Marsh", "Bloodfall Kingdom", "Camoran Dynasty", "Coral Kingdoms of Thras", "Cyrodilic Emperors (Reman", "Akaviri", "Longhouse", "Septim", "Mede)", "Cyrodilic Empire (Alessian", "Second", "Imperial", "Third)", "Direnni Hegemony", "Elsweyr Confederacy (Anequina", "Pellitine)", "Kingdom of Hammerfell", "Kingdoms of High Rock (Camlorn", "Daggerfall", "Evermore", "Farrun", "Jehanna", "Northpoint", "Orsinium", "Shornhelm", "Wayrest)", "Kingdom of Pyandonea", "Kingdoms of Skyrim (Nord Empire", "Eastern", "Western)", "Snow Elf Empire", "Tiger-Dragon's Empire", "Yokudan Empire", "Ysgramor Dynasty"],
    "Notable Events": ["Ayleid Diaspora", "Convention", "Disappearance of the Dwarves", "Duskfall", "Great Collapse", "Interregnum", "Night of Tears", "Planemeld", "Red Year", "Soulburst", "Stormcrown Interregnum", "Sun's Death", "Velothi Exodus", "Void Nights", "Warp in the West"],
    "Wars and Conflicts": ["Merethic Era Wars", "First Era Wars", "Second Era Wars", "Third Era Wars", "Fourth Era Wars"],
    "Symbols": ["Aurbic Eye", "Aurbic Phoenix", "Blessed Life-Tree", "Cross", "Ouroboros", "Red Diamond", "Scarab", "Triquetra", "Triskelion", "Vaia's Golden Ash"],
    "Time": ["Calendar", "Dragon Break", "Holidays", "Kalpa", "Time Wound"],
    "Transportation": ["Air Transportation", "Land Transportation", "Magical Transportation", "Sea Transportation"],
    "Other": ["Disease", "Hygiene", "Weapons"]
}

def create_directories(base_path, categories):
    for category, subcategories in categories.items():
        category_path = base_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        for subcategory in subcategories:
            subcategory_path = category_path / subcategory
            subcategory_path.mkdir(parents=True, exist_ok=True)

def move_files(base_path, categories):
    # Check files in both Appendices and UNCLASSIFIED directories
    for folder in ["Appendices", "UNCLASSIFIED"]:
        appendices_path = base_path / folder
        for json_file in appendices_path.glob('*.json'):
            try:
                for category, subcategories in categories.items():
                    for subcategory in subcategories:
                        if subcategory in json_file.name:
                            new_file_path = base_path / category / json_file.name
                            shutil.move(str(json_file), str(new_file_path))
                            break
            except FileNotFoundError:
                print(f"File not found and skipped: {json_file}")
                continue

# Define base path
base_path = Path('CLEANED_OUTPUT')

# Create directories based on categories and subcategories
create_directories(base_path, categories)

# Move files from Appendices and UNCLASSIFIED to the corresponding new directories
move_files(base_path, categories)

print("File reorganization complete.")
