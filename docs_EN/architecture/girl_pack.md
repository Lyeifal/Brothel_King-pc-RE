# Girl Pack System Architecture

> Last updated: 2026-09-11 (verified against code)
> **Core files**: `game/core/framework/girl_files_dict.rpy` (416 lines), `game/core/framework/girl_factory.rpy` (833 lines), `game/core/framework/girlclass.rpy` (Girl class)
> **Data**: `game/custom/girls/` (currently 102 packs)
> **Editor support**: ✅ Girl pack editor (`tools/bk_editor/girl_pack_editor/` + in-game `game/core/tools/girl_pack_editor/`)

---

## 1. System Responsibilities

The Girl Pack is the unit of content extension; each pack is a folder:

- **`_BK.ini`**: pack metadata (name, author, version, tags, trait overrides, generation options). Parsed by `read_init_file()` (girl_factory.rpy:313) into a dict buffer, tolerant of user typos; throws `AssertionError` when the file is corrupted (:328).
- **Picture assets**: tagged per naming convention (`portrait_*`, `profile_*`, action tags, etc.), mapped by TagRegistry.
- **Custom Traits/Perks and dialogue**: `register_custom_tags_for_pack()` (girl_factory.rpy:515), `register_custom_dialogue_for_pack()` (:535).
- **packstates**: import/export of tagging state (`GirlFilesDict.import_packstates()`, girl_files_dict.rpy:259).

## 2. The Two Pillars

### 2.1 GirlFilesDict (girl_files_dict.rpy:12)

`class GirlFilesDict(NoRollback)` — an index dict of all pack files, instantiated at init -3 as `globalFilesDict` and registered as the service `services.girl_files_dict` (:412).

- `__load_files()` (:17) builds the pack name → file list index via `get_girl_path()`.
- Query API: `get_files()` / `contains_file()` (binary search, :203) / `get_pics()` / `get_tag_index()` / `get_pic_by_name()`.
- Stats API: `get_totalcount()` (:174) / `get_init_duration()` (:167, load duration inspectable in the console).
- `reload_files()` (:246) lets AutoRepair detect newly added pictures.

### 2.2 girl_factory.rpy Factory Functions

- `get_girl_path(file)` (:4): determines which pack a file belongs to; directories starting with an underscore are ignored entirely, directories starting with `#` are treated as container mixes.
- `generate_girls()` (:97) / `create_girl(pack_name, ...)` (:131) / `get_girl()` (:178) / `get_girls()` (:181): girl generation entry points; the v2 hook `girl_generated` fires at :278.
- Generation constraints: `can_generate()` (:613, count/uniqueness checks), `can_spawn()` (:635, location checks), `randomize_girl_level()` (:777, level assignment by chapter).
- Pack scoring: `get_girlpack_rating()` (:691) and `get_plus_rating()` (:741) evaluate pack quality (picture count/tag coverage), affecting generation weights.
- `clone_init_dict()` (:549) supports template cloning.

The Girl class itself is covered in [girl_components.md](girl_components.md) (3,910 lines after componentization).

## 3. Pack Validation

Three layers of validation:

1. **Load time**: `_BK.ini` parse assertions (girl_factory.rpy:328); packs without valid pictures naturally never enter the index.
2. **In-game editor**: `game/core/tools/girl_pack_editor/pack_editor_state.rpy:45` `validate_pack(pack_name)`:
   - No pictures → `"No images found"`;
   - Missing `profile` tag → required (for display); missing `portrait` tag → suggested.
   - Missing/invalid `_BK.ini` reported as a separate issue.
3. **Desktop editor**: `tools/bk_editor/girl_pack_editor/` provides the full toolchain of tagging + INI editing + validation (see [editor_suite.md](editor_suite.md)).

## 4. Inter-System Relationships

```
game/custom/girls/<pack>/ (_BK.ini + pictures)
    └─→ GirlFilesDict (init -3 index, service girl_files_dict)
           ├─→ get_girl_path ownership resolution
           ├─→ tag_dict/TagRegistry tag resolution
           └─→ girl_factory
                  ├─→ create_girl/get_girl → Girl(...).randomize()
                  │        └─→ v2 hook girl_generated (girl_factory.rpy:278)
                  ├─→ can_generate/can_spawn generation constraints
                  └─→ get_girlpack_rating pack quality scoring
```

## 5. Editor Support

| Editor | Support | Notes |
|--------|---------|-------|
| Desktop girl pack editor | ✅ Full | Tagging, INI, Traits/Perks, validation (`tools/bk_editor/girl_pack_editor/`) |
| In-game pack editor | ✅ | `game/core/tools/girl_pack_editor/`, includes `validate_pack` |
| `screen mods` / girlpack_menu | ✅ | Pack management UI (the `girlpack_menu` label in screens.rpy) |

---

## Related Documentation

- [girl_components.md](girl_components.md) — componentization of the Girl class
- [trait_perk.md](trait_perk.md) — pack custom Traits/Perks
- [registry.md](registry.md) — TagRegistry tag mapping
- [editor_suite.md](editor_suite.md) — the editor suite
