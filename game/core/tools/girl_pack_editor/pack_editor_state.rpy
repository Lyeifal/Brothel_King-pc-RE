#### Girl Pack Editor — State management ####
# Phase 6.2: In-game tool for creating and editing girl packs.
# Manages pack metadata, image tags, and export.

init -1 python:

    class PackEditorState(object):
        """State holder for the in-game Girl Pack Editor.

        Capabilities:
        - Browse installed packs
        - Create new pack scaffold (directory + _BK.ini template)
        - Visual tag editor (click image, assign/modify tags)
        - Preview tag mapping to in-game uses
        - Export to .zip for distribution
        - Validate pack completeness
        """

        def __init__(self):
            self.current_pack = None     # Pack name being edited
            self.current_image = None    # Image being tagged
            self.unsaved_changes = False

        def list_packs(self):
            """Return list of all installed pack names."""
            return list(GirlFilesDict.get_paths())

        def create_pack_scaffold(self, pack_name, author="", version="1.0"):
            """Create directory and default _BK.ini for a new pack."""
            import os
            pack_dir = os.path.join(renpy.config.gamedir, "custom", "girls", pack_name)
            if os.path.exists(pack_dir):
                return False, "Pack '%s' already exists." % pack_name

            os.makedirs(pack_dir)
            ini_path = os.path.join(pack_dir, "_BK.ini")
            with open(ini_path, "w", encoding="utf-8") as f:
                f.write("; Girl Pack: %s\n" % pack_name)
                f.write("; Author: %s\n" % author)
                f.write("; Version: %s\n" % version)
                f.write("\n[identity]\nname = %s\n" % pack_name)
                f.write("\n[base skills]\n")
            return True, "Pack '%s' created at custom/girls/%s/" % (pack_name, pack_name)

        def validate_pack(self, pack_name):
            """Check a pack for missing required tags or invalid INI."""
            issues = []
            pics = GirlFilesDict.get_pics(pack_name)
            if not pics:
                issues.append("No images found")

            has_profile = any("profile" in pic.tags for pic in pics)
            has_portrait = any("portrait" in pic.tags for pic in pics)
            if not has_profile:
                issues.append("Missing 'profile' tag (required for display)")
            if not has_portrait:
                issues.append("Missing 'portrait' tag (recommended)")

            ini = GirlFilesDict.get_ini(pack_name)
            if not ini:
                issues.append("Missing _BK.ini file")

            return issues

    pack_editor = PackEditorState()
