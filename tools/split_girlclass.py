"""Extract GirlFilesDict from girlclass.rpy into its own file."""

from pathlib import Path

SRC = Path("game/core/framework/girlclass.rpy")
OUT = Path("game/core/framework/girl_files_dict.rpy")

with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()

# GirlFilesDict starts at line 5907 (0-indexed: 5906)
# It ends at line 6244 (0-indexed: 6243)
# We also want the default statement before it (line 5905, 0-indexed: 5904)

# Extract GirlFilesDict block (including the default statement and closing comment)
gfd_lines = lines[5904:6244]  # from default statement to end of file before final comment

# Write new file
with open(OUT, "w", encoding="utf-8") as f:
    f.write("#### GirlFilesDict — File manager for girl packs ####\n\n")
    f.writelines(gfd_lines)
    f.write("\n#### END OF GIRLFILESDICT FILE ####\n")

print(f"Written {OUT} ({len(gfd_lines)} lines)")

# Trim original file
with open(SRC, "w", encoding="utf-8") as f:
    f.writelines(lines[:5904])
    f.write("\n#### END OF BK GIRLCLASS FILE ####\n")

print(f"Trimmed {SRC} to {5904} lines")
