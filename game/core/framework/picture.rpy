#### Picture classes ####

init -4 python:

    import hashlib
    class Picture(object):

        """This class is for managing pictures and tags."""

        def __init__(self, filename="", path=""): # filename is antiquated, use path

            if filename:
                self.filename = filename
            elif path:
                file_parts = path.split("/")

                self.filename = file_parts[-1]

            if not path:
                raise AssertionError("No path provided for the Picture() object")

            self.path = path

            #<Chris12 PackState>
            self.make_tags_from_filename()
            self.__hashcode = None
            self.__filesize = -1
            #</Chris12 PackState>

            # if self.filename.endswith(".webm"):
            #     self.video = True
            # else:
            #     self.video = False

            lowerExtension = self.filename[-5:].lower()
            self.video = any(lowerExtension.endswith(vid_ext) for vid_ext in VIDEOFORMATS)

        def is_horizontal(self):
            try:
                return (self.y_size <= self.x_size)
            except:
                if len(self.path) < 256 and is_imgfile(self.path, video=False): # 256 characters is the Windows OS limit
                    self.x_size, self.y_size = renpy.image_size(self.path) # image_size() is slow, store the result
                else:
                    return True
                return (self.y_size <= self.x_size)
        
        def is_vertical(self):
            try:
                return (self.y_size > self.x_size)
            except:
                if len(self.path) < 148 and is_imgfile(self.path, video=False): # 148 characters seems to be a limit
                    self.x_size, self.y_size = renpy.image_size(self.path) # image_size() is slow, store the result
                else:
                    return True
                return (self.y_size > self.x_size)


        def get_old(self, x = None, y = None, proportional = True, side = False, profile = False): # Doesn't work with just x or y for now

            if self.video:
                return Movie(play=self.path, channel="video")

            if side:
                return ProportionalScale(self.path, int(config.screen_height*0.2111), int(config.screen_height*0.2111), yalign = 1.0)

            if profile:
                return ProportionalScale(self.path, config.screen_width//2.8, config.screen_height*2//3)

            if x and y:
                if proportional:
                    return ProportionalScale(self.path, x, y)
                else:
                    return im.Scale(self.path, x, y)
            else:
                return self.path

        ## FFUN VIDEO-COMPATIBLE GET METHOD

        def get(self, x = None, y = None, proportional = True, side = False, profile = False): # Doesn't work with just x or y for now
            image_path = self.path

            if side:
                if self.video :
                    return Movie(size=(152,152), play=image_path)
                else :
                    return ProportionalScale(image_path, int(config.screen_height*0.2), int(config.screen_height*0.2), yalign = 1.0)

            if profile:
                if self.video :
                    return Movie(size=(config.screen_width//2.8, config.screen_height*2//3), play=image_path)
                else:
                    return ProportionalScale(image_path, config.screen_width//2.8, config.screen_height*2//3)

            if x and y:
                if self.video :
                    return Movie(size=(x,y), play=image_path)
                if proportional:
                    return ProportionalScale(image_path, x, y)
                else:
                    return im.Scale(image_path, x, y)
            else:
                if self.video :
                    return Movie(play=image_path)
                else:
                    return image_path

        def has_tag(self, tag): # Single tag search
            return self.has_tags([tag])

        def has_tags(self, tags, and_tags = None, not_tags = None, old = False, horizontal=False, vertical=False): # Multiple tag (OR) search. For performance reasons, has_tags should always receive tuples as arguments

            # Censorship (must be handled at the highest level)

            if self.path in persistent.pic_ignore_list:
                return False

            for tag in self.tags:
                if is_censored(tag):
                    return False

            ##! Horizontal/Vertical check: Deactivating for now, the performance hit is too big ##

            # if horizontal and not self.is_horizontal():
            #     return False
            
            # if vertical and not self.is_vertical():
            #     return False

            ##

            if tags:
                for tag in tags:

                    if not tag: # Safety check in case a None value makes it into the tag list
                        continue

                    elif (nsfw == False and tag in nsfw_tags) or (tag in (persistent.forbidden_tags + forbidden_tags)):
                        pass

                    elif tag in self.tags or (old and tag in self.oldtags):
                        if not_tags:
                            for not_tag in not_tags:
                                if not not_tag:  # Safety check in case a None value makes it into the tag list
                                    continue
                                if not_tag in self.tags or (old and not_tag in self.oldtags):
                                    return False

                        if and_tags:
                            for and_tag in and_tags:
                                if not and_tag:  # Safety check in case a None value makes it into the tag list
                                    continue
                                if (nsfw == False and and_tag in nsfw_tags) or (and_tag in (persistent.forbidden_tags + forbidden_tags)):
                                    pass
                                elif not (and_tag in self.tags or (old and and_tag in self.oldtags)):
                                    return False
                            else:
#                                renpy.say("", "Found " + self.filename + " with tags among " + and_text(tags) + " and " + and_text(and_tags) + " but not " + and_text(not_tags))
                                return True
                        else:
#                            renpy.say("", "Found " + self.filename + " with tags among " + and_text(tags))
                            return True

            return False

        def get_weight(self, context=None):

            mod = 1.0

            if context:
                mod = persistent.fix_pic_balance[context]

            try:
                return self.base_weight * mod
            except:
                return self.update_weight() * mod


        def update_weight(self): # Base weight is 100

            for t in frequency_tags.keys():
                if self.has_tag(t):
                    self.base_weight = frequency_tags[t]
                    break
            else:
                self.base_weight = 100

            return self.base_weight


        #<Chris12 PackState>

        def make_tags_from_filename(self):
#             global tag_list_dict
#             global sorted_tag_dict_keys
#             global sorted_tags_with_separator
#             global ending_pattern

            # Initialization has been moved to BKinit_variables.rpy

            self.tags = []
            self.oldtags = []

            # This checks longest tags first. The second parameter allows filtered tag_lists to be used (for tags with spaces)
            def check_all_tags(filename, current_tag_list):

                old_len = len(filename)
                for _tag in current_tag_list:
                    filename = filename.replace(_tag, ' ')
                    new_len = len(filename)
                    if (new_len != old_len):
                        old_len = new_len
                        self.oldtags.append(_tag)
                        self.tags += tag_list_dict[_tag]

                return filename

            filename = self.filename.lower()
            self.is_trash = ("_trash" in filename)
            self.is_unrecognized = ("_unrecognized" in filename)
            filename = ending_pattern.sub(" ", filename) # removes extension and, if found, also (00001) at the end of the filename
            filename = check_all_tags(filename, sorted_tags_with_separator) # First look for tags with separators, e.g. 'cum shower'

            #after excluding all those tags, split the filename and look for exact matches
            parts = filename.split(' ')
            not_found = []
            for part in parts:
                if part.strip() != "":
                    tag_entry = tag_dict.get(part, None)
                    if tag_entry is not None: # tag was found
                        self.oldtags.append(part)
                        self.tags += tag_list_dict[part]
                    else:
                        not_found.append(part)

            if len(not_found) > 0:
                filename = ' '.join(not_found)
                check_all_tags(filename, sorted_tag_dict_keys)

            # Adding tag 'orgy' for bisexual and group pics, by popular demand
            if "group" in self.tags and "bisexual" in self.tags:
                self.tags.append("orgy")

            # Adding 'group' to double only for human partners (by popular demand)
            if "double" in self.tags and "beast" not in self.tags and "monster" not in self.tags and "machine" not in self.tags and "group" not in self.tags:
                self.tags.append("group")

        # calculates a checksum.
        # Has to be the same as the function in the picture namer, so that packstates work
        def get_hash(self):
            if self._m1_BKclasses__hashcode is None :
                BLOCKSIZE = 65536
                hasher = hashlib.sha256()
                with open(config.gamedir + "/" + self.path, 'rb') as afile:
                    buf = afile.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(BLOCKSIZE)
                self._m1_BKclasses__hashcode = hasher.hexdigest()
            return self._m1_BKclasses__hashcode


        # gets the filesize
        # lazily initialized because its only needed by packstate check, not during normal gameplay
        def get_filesize(self):
            if self._m1_BKclasses__filesize < 0:
                self._m1_BKclasses__filesize = os.path.getsize(config.gamedir + "/" + self.path)
            return self._m1_BKclasses__filesize


        # Based on Goldo's Picture Namer
        def get_new_name(self):
            # self.tags.sort(key=sort_tags)

            if self.filename[-5:] in (".jpeg", ".webp"):
                ending = self.filename[-5:]
            else:
                ending = self.filename[-4:]

            if self.is_trash:
                new_file_name = "_TRASH " + " ".join(self.oldtags) + " (%s)" + ending
            elif self.is_unrecognized:
                tag_as_unrecognized = preferences.packstate_unrecognized != "Ignore"
                if self.filename.startswith("_UNRECOGNIZED ") :
                    if tag_as_unrecognized :
                        new_file_name = self.filename # already has the tag
                    else :
                        new_file_name = self.filename[len("_UNRECOGNIZED "):] # remove the tag again
                else :
                    if tag_as_unrecognized :
                        new_file_name = "_UNRECOGNIZED " + self.filename
                    else :
                        new_file_name = self.filename # don't change the name if ignore
            elif self.oldtags:
                new_file_name = " ".join(self.oldtags) + " (%s)" + ending
            else:
                new_file_name = "_UNTAGGED" + " (%s)" + ending

            # When using old filename, put the (%s) into the new_file_name
            if "(" in new_file_name :
                new_file_name = new_file_name[:new_file_name.rfind("(")] + "(%s)" + ending
            else :
                new_file_name = new_file_name[:-len(ending)] + " (%s)" + ending
            return new_file_name

        # Based on Goldo's Picture Namer
        def commit_changes(self):

            i = 0
            new_file_name = self.get_new_name()

            # Compares file names up to the first parenthesis

            if new_file_name[:new_file_name.find("(")] != self.filename[:self.filename.find("(")]:

                while True :
                    if self.rename_file(new_file_name % str(i).zfill(5)):
                        return 1
                    else:
                        i += 1

            return 0

        # Based on Goldo's Picture Namer
        def rename_file(self, name):
            girlpath = self.path[:self.path.rfind("/")]
            os.chdir(config.gamedir + "/" + girlpath)

            try:
                os.rename(self.filename, name)
            except:
                return False

            self.filename = name
            self.path = girlpath + "/" + name

            return True

        #</Chris12 PackState>



## Not mine !       ##


    class ProportionalScale(renpy.Displayable):
        '''Resizes a renpy image to fit into the specified width and height.
        The aspect ratio of the image will be conserved.'''
        def __init__(self, imgname, maxwidth=None, maxheight=None, **properties):
            super(ProportionalScale, self).__init__()
            self.imgname = imgname # Stores the image's relative path for unlocking the gallery
            self.width = maxwidth or config.screen_width
            self.height = maxheight or config.screen_height
            if not renpy.exists(imgname):
                imgname = "resources/backgrounds/not_found.webp"
            self.image = Transform(imgname, size=(self.width, self.height), fit="contain", **properties)

        def render(self, width, height, st, at): # Used for rendering
            return renpy.render(self.image, self.width, self.height, st, at)

        def visit(self): # Used for predicting
            return [ self.image ]

        def per_interact(self): # Used for rollback
            renpy.redraw(self, 0)

    # class ProportionalScale(im.ImageBase):
    #     '''Resizes a renpy image to fit into the specified width and height.
    #     The aspect ratio of the image will be conserved.'''
    #     def __init__(self, imgname, maxwidth=None, maxheight=None, bilinear=True, **properties):
    #         img = im.image(imgname)
    #         super(ProportionalScale, self).__init__(img, maxwidth, maxheight, bilinear, **properties)
    #         self.imgname = imgname # Stores relative path from the 'game/' folder
    #         self.image = img
    #         if maxwidth: # Set maxwidth as None to ignore
    #             self.maxwidth = int(maxwidth)
    #         else:
    #             self.maxwidth = config.screen_width
    #         if maxheight: # Set maxheight as None to ignore
    #             self.maxheight = int(maxheight)
    #         else:
    #             self.maxheight = config.screen_height
    #         self.bilinear = bilinear
    #
    #     def load(self):
    #         #<Chris12 NotFound>
    #         # Loads a neutral image instead of failing, in case an image does not exist
    #         try :
    #             child = im.cache.get(self.image)
    #         except IOError :
    #             # renpy.notify("Missing: " + self.imgname) # Commented out because it causes bugs in the CG gallery. Requires investigation
    #             child = im.cache.get(Image("resources/backgrounds/not_found.webp"))
    #         #</Chris12 NotFound>
    #
    #         width, height = child.get_size()
    #
    #         ratio = min(self.maxwidth/float(width), self.maxheight/float(height))
    #         width = ratio * width
    #         height = ratio * height
    #
    #         if self.bilinear:
    #             try:
    #                 renpy.display.render.blit_lock.acquire()
    #                 rv = renpy.display.scale.smoothscale(child, (width, height))
    #             finally:
    #                 renpy.display.render.blit_lock.release()
    #         else:
    #             try:
    #                 renpy.display.render.blit_lock.acquire()
    #                 rv = renpy.display.pgrender.transform_scale(child, (newwidth, newheight))
    #             finally:
    #                 renpy.display.render.blit_lock.release()
    #         return rv
    #
    #     def predict_files(self):
    #         return self.image.predict_files()

#### END OF BK CLASSES ####
