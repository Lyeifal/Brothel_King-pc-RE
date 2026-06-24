#### GirlFilesDict — File manager for girl packs ####

default preferences.packstate_unrecognized = "Rename"

init -2 python:
    import datetime
    import bisect
    import os
    import shutil


    class GirlFilesDict(NoRollback):

        def __init__(self):
            self.__load_files()

        def __load_files(self): # Goldo: Changed to use get_girl_path() to establish the root folder
            start = datetime.datetime.now()
            self.__pathset = set()
            self.__pathtuple = list() # Start with changeable set
            self.__path_dict = defaultdict(str)
            self.__filetuple_dict = dict()
            self.__pictuple_dict = dict()
            self.__ini_dict = dict()
            self.__packstates = list()
            self.__timestamp = datetime.datetime.now()
            self.__totalcount = 0

            # Move empty/corrupt .avif files to temp/error_images instead of deleting
            all_files = list(renpy.list_files())
            moved_files = []
            moved_file_paths = set()
            error_base = os.path.join(config.gamedir, "temp", "error_images")
            report_path = os.path.join(config.gamedir, "temp", "error_images_report.txt")

            for file in all_files:
                if file.lower().endswith(".avif"):
                    # Skip files already quarantined to avoid moving them deeper
                    if file.startswith("temp/error_images/"):
                        continue
                    try:
                        fpath = renpy.loader.transfn(file)
                        if os.path.getsize(fpath) == 0:
                            # Preserve path relative to the girls folder if possible, else relative to game/
                            if file.startswith("custom/girls/"):
                                rel_path = file[len("custom/girls/"):]
                            elif "/girls/" in file:
                                rel_path = file[file.find("/girls/") + len("/girls/"):]
                            else:
                                rel_path = file

                            dest_path = os.path.join(error_base, rel_path)
                            dest_dir = os.path.dirname(dest_path)
                            if not os.path.exists(dest_dir):
                                os.makedirs(dest_dir)

                            shutil.move(fpath, dest_path)
                            moved_files.append((file, dest_path))
                            moved_file_paths.add(file)
                    except:
                        pass

            if moved_files:
                print("GirlFilesDict: Moved %i empty .avif file(s) to temp/error_images." % len(moved_files))
                try:
                    with open(report_path, "w", encoding="utf-8") as report:
                        report.write("Empty/Corrupt .avif files moved during girl pack loading\n")
                        report.write("Total: %i\n" % len(moved_files))
                        report.write("=" * 60 + "\n\n")
                        for src, dest in moved_files:
                            report.write("SOURCE:  %s\n" % src)
                            report.write("MOVED TO: %s\n\n" % dest)
                except:
                    pass

            for file in all_files:
                if file in moved_file_paths:
                    continue

                if file.startswith(GirlFilesDict.get_packstate_directory()): # Packstate folder
                    self.__packstates.append(file.lower())
                else: # Other folders
                    girlpack_name, girlpack_path, file_name = get_girl_path(file) # get_girl_path only returns values if it is a confirmed girlpack path

                    if girlpack_name: # get_girl_path may return None if the file is not path is hidden
                        if girlpack_name in self.__pathset: # Controls for duplicate girlpack folders
                            if girlpack_path != self.__path_dict[girlpack_name]:
                                raise AssertionError("Two girl packs with the name '%s' were found:\n%s\n%s\nRename one of them to avoid conflicts." % (girlpack_name, self.__path_dict[girlpack_name], girlpack_path))
                                renpy.say("", __("Exiting Ren'Py...{w=1}{nw}"))
                                renpy.quit()

                        else: # __pathset/tuple should be renamed something else since path isn't used anymore
                            self.__pathset.add(girlpack_name)
                            self.__pathtuple.append(girlpack_name)
                            self.__path_dict[girlpack_name] = girlpack_path
                            self.__filetuple_dict[girlpack_name] = list() # Start changeable
                        self.__filetuple_dict[girlpack_name].append(file)
                        if file.endswith("_BK.ini"): self.__ini_dict[girlpack_name] = file
                        self.__totalcount += 1

            # Switch to unchangeable, sorted tuple
            self.__pathtuple.sort()
            self.__pathtuple = tuple(self.__pathtuple)

            for girlpath in self.__pathtuple:
                self.__filetuple_dict[girlpath].sort() # Important! Binary search only works if sorted!
                self.__filetuple_dict[girlpath] = tuple(self.__filetuple_dict[girlpath]) # Switch to unchangeable
                self.__load_pics(girlpath)

            self.__init_duration = datetime.datetime.now() - start

        def __load_pics(self, girlpath): # Where girlpath is the root folder

            # Resetting pictures

            self.__pictuple_dict[girlpath] = list() # Start changeable

            if girlpath not in self.__pathset : return

            # Identifying image files

            imgfiles = [img for img in self.__filetuple_dict[girlpath] if is_imgfile(img)]

            # Creating pictures

            for file in imgfiles:
                pic = Picture(path=file)

                self.__pictuple_dict[girlpath].append(pic)

                # Tracing untagged pics for debugging
                if pic.tags == []:
                    untagged_pics.append(pic.path)

            self.__pictuple_dict[girlpath] = tuple(self.__pictuple_dict[girlpath]) # Switch to unchangeable

        @staticmethod
        # Just to be safe, in case some changes need to be made.
        # The first singleton approach did not work out, since it then got saved by Renpy.
        # (Which made the game use old GirlFilesDicts without updated files & pics)
        def __get():
            #if GirlFilesDict.__singleton is None:
            #    GirlFilesDict.__singleton = GirlFilesDict()
            #return GirlFilesDict.__singleton
            return globalFilesDict

        @staticmethod
        # The directory where the packstates are located in.
        # You only have to change it here.
        # Please make sure it ends with a /
        def get_packstate_directory():
            return "gpackstates/"

        @staticmethod
        # returns the duration of the init.
        # mostly for debugging
        # you can check this in the console with "GirlFilesDict.get_init_duration()"
        def get_init_duration():
            return GirlFilesDict.__get().__init_duration

        @staticmethod
        # returns the total number of files managed by the dictionary
        # mostly for debugging
        # you can check this in the console with "GirlFilesDict.get_totalcount()"
        def get_totalcount():
            return GirlFilesDict.__get().__totalcount

        @staticmethod
        # Returns the _BK.ini for a girlpack, or None if no such file exists
        def get_ini(girlpath):
            try:
                return GirlFilesDict.__get().__ini_dict[girlpath]
            except:
                return None

        @staticmethod
        # Returns the paths of all available girls. Useful for end_of_week stuff.
        def get_paths():
            return GirlFilesDict.__get().__pathtuple

        @staticmethod
        def get_path_dict():
            return GirlFilesDict.__get().__path_dict

        @staticmethod
        # Returns all files for a specific girl.
        # To check if a file exists, use contains_file() instead, it uses a fast binary search.
        def get_files(girlpath):
            return GirlFilesDict.__get().__filetuple_dict[girlpath]

        @staticmethod
        # Looks if a file exists, using fast binary search
        # (Roughly speaking, Binary Search is how you'd look for a name in a phonebook)
        def contains_file(girlpath, file): # Goldo: Changed to use a file's complete path instead.
            instance = GirlFilesDict.__get()
            if girlpath not in instance.__filetuple_dict :
                return False
            else :
                files = instance.__filetuple_dict[girlpath]
                idx = bisect.bisect_left(files, file)
                return idx != len(files) and files[idx] == file

        @staticmethod
        # Gets all pics for a specific girl.
        # Initialized lazy at the first request
        def get_pics(girlpath):
            instance = GirlFilesDict.__get()
            if not girlpath in instance.__pictuple_dict:
                instance.__load_pics(girlpath)
            return instance.__pictuple_dict[girlpath]

        @staticmethod
        # Gets a certain pic for a specific girl. Not using binary search yet.
        # Initialized lazy at the first request
        def get_pic_by_name(girlpath, pic_name):
            pic_name = pic_name.lower()
            instance = GirlFilesDict.__get()
            if not girlpath in instance.__pictuple_dict:
                instance.__load_pics(girlpath)
            for pic in instance.__pictuple_dict[girlpath] :
                if pic.filename == pic_name:
                    return pic
            return None

        @staticmethod # Goldo #
        # The GirlFilesDict timestamp is initialized at Renpy startup
        # Used by AutoRepair to check if there could be new images
        def reload_files():
            GirlFilesDict.__get().__load_files()

        @staticmethod
        # The GirlFilesDict timestamp is initialized at Renpy startup
        # Used by AutoRepair to check if there could be new images
        def get_timestamp():
            instance = GirlFilesDict.__get()
            return instance.__timestamp

        @staticmethod
        # Imports packstates for all girls
        # If simulate = True, only creates a logfile without any renames
        def import_packstates(simulate = False):
            all_results = list()
            total_changes = 0

            for girlpack_name in GirlFilesDict.__get().get_paths():
                result, changes = GirlFilesDict.__import_tags(girlpack_name, simulate)
                renpy.say(__("Checking"), girlpack_name + "{fast}{nw}")
                all_results.append(result)
                total_changes += changes

            with open(config.gamedir + "\\packstate_log.txt", "wt") as log_file :
                log_file.write("\n".join(all_results))

            if (total_changes > 0) :
                if simulate :
                    GirlFilesDict.__get().__load_files() # Revert tags
                    renpy.say("", __("{count} file(s) would be renamed. See {a=call_in_new_context:invoke_packstate_log}{color=[c_magenta]}packstate_log.txt{/color}{/a} in the 'game' directory for details.").format(count=total_changes))
                else :
                    renpy.say("", __("{count} file(s) were renamed. See {a=call_in_new_context:invoke_packstate_log}{color=[c_magenta]}packstate_log.txt{/color}{/a} for details.\nRestarting Renpy. This may take a few seconds.{fast}{nw}").format(count=total_changes))
                    renpy.utter_restart()
            else :
                renpy.say("", __("No files were renamed. See {a=call_in_new_context:invoke_packstate_log}{color=[c_magenta]}packstate_log.txt{/color}{/a} for details."))

        @staticmethod
        # The workhorse of the packstates import
        def __import_tags(girlpack_name, simulate):

            packStateFilePath = GirlFilesDict.get_packstate_directory() + girlpack_name + ".txt" #?

            if packStateFilePath.lower() not in GirlFilesDict.__get().__packstates :
                return (girlpack_name + ": No packstate\n", 0)

            counterChanges = 0
            try :
                with open(config.gamedir + "/" + packStateFilePath, "r") as packStateFile :
                    import_result = ""
                    counterImageStates = 0
                    counterFileChecked = 0
                    counterDuplicates = 0
                    all_renames = list()


                    groupedBySize = dict()
                    # trash needs to come last, or the duplicates would alternate every time
                    for skip_trash in (True, False) :
                        for pic in GirlFilesDict.get_pics(girlpack_name) :
                            if pic.is_trash == skip_trash : continue
                            filesize = pic.get_filesize()
                            if filesize in groupedBySize:
                                groupedBySize[filesize].append(pic)
                            else:
                                groupedBySize[filesize] = [ pic ]
                            pic.is_unrecognized = True

                    filesize = packStateFile.readline()
                    while (len(filesize) != 0) :
                        filesize = int(filesize.strip())
                        hash = packStateFile.readline().strip()
                        tag_filename = packStateFile.readline().strip().lower()
                        tagsSet = set(tag_filename.split())
                        alreadyFound = False
                        counterImageStates += 1
                        if filesize in groupedBySize:
                            for pic in groupedBySize[filesize] :
                                duplicateCheck = (len(groupedBySize[filesize]) > 1)

                                # use set to make the check indifferent to tag order
                                picNeedsRenaming = (set(pic.filename[:pic.filename.find("(")].lower().split()) != tagsSet)
                                if (duplicateCheck or picNeedsRenaming) :
                                    # only get the hash if there are potential duplicates or if the image would need renaming
                                    if (pic.get_hash() == hash) :
                                        pic.is_unrecognized = False
                                        counterFileChecked += 1
                                        if alreadyFound :
                                            counterDuplicates += 1

                                        if picNeedsRenaming or alreadyFound :
                                            pic.is_trash = alreadyFound or tag_filename.startswith("_trash")
                                            pic.oldtags = [] # using oldtags, refresh them later
                                            if alreadyFound : pic.oldtags.append("duplicate")
                                            for tag in tag_filename.split() :
                                                if tag != "_trash" : pic.oldtags.append(tag)

                                            new_name = pic.get_new_name()
                                            if pic.filename[:pic.filename.find("(")] != new_name[:new_name.find("(")]:
                                                counterChanges += 1
                                                if simulate :
                                                    all_renames.append(pic.filename + " -> " + new_name)
                                                else :
                                                    old_filename = pic.filename
                                                    pic.commit_changes()
                                                    all_renames.append(old_filename + " -> " + pic.filename)
                                            pic.make_tags_from_filename() # refresh tags

                                        alreadyFound = True

                                else :
                                    # This part does not rely on the hash for performance reasons
                                    # If both filesize and tags matched, it's reasonably safe to assume that it is the correct image.
                                    # Otherwise, you'd have to calculate the hashes of ALL files EVERY TIME.
                                    pic.is_unrecognized = False

                        filesize = packStateFile.readline()

                counterUnrecognized = 0
                for pic in GirlFilesDict.get_pics(girlpack_name) :
                    if pic.is_unrecognized :
                        if pic.filename.lower().startswith("_untagged") :
                            continue # no need for "_UNRECOGNIZED _UNTAGGED"

                        counterFileChecked += 1
                        new_name = pic.get_new_name()
                        if pic.filename[:pic.filename.find("(")] != new_name[:new_name.find("(")]:
                            counterChanges += 1
                            if simulate :
                                all_renames.append(pic.filename + " -> " + new_name)
                            else :
                                old_filename = pic.filename
                                pic.commit_changes()
                                all_renames.append(old_filename + " -> " + pic.filename)
                            pic.make_tags_from_filename() # refresh tags
                            counterUnrecognized += 1

                import_result = girlpack_name + ": packstate contained " + str(counterImageStates) + " image states.\n"

                if counterFileChecked > 0 :
                    import_result += "  " + str(counterFileChecked) + " file(s) needed to be checked, "
                    if counterChanges > 0:
                        import_result += "and " + str(counterChanges) + " were renamed.\n"
                    else :
                        import_result += "but none had to be changed. Everything's up to date.\n"

                    if counterDuplicates > 0 :
                        import_result += "  Of those, " + str(counterDuplicates) + " were duplicates and marked for deletion (tagged as _TRASH).\n"
                    if counterUnrecognized > 0 :
                        import_result += "  " + str(counterUnrecognized) + " were unrecognized. Those images will be used depending on your game settings.\n"
                    if counterChanges > 0 :
                        import_result += "    " + "\n    ".join(all_renames)
                else :
                    import_result += "  No files were found that had to be changed. Everything's up to date.\n"

            except IOError as e:
                errno, strerror = e.args
                import_result = "I/O error({0}): {1}".format(errno, strerror)
                pass
            except :
                raise
            return (import_result, counterChanges)

    # Global Object Initialized in Python Init -> skips renpy save process
    # So it will always have the newest files when you restart the game
    globalFilesDict = GirlFilesDict()

#</Chris12 PackState>

#### END OF GIRLFILESDICT FILE ####
