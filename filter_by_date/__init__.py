from fman import DirectoryPaneCommand, show_alert, show_quicksearch, QuicksearchItem
from fman.url import as_human_readable, as_url, splitscheme
from fman.fs import FileSystem
import fman.fs
import os
from datetime import datetime, date, timedelta
from stat import S_ISDIR
from io import UnsupportedOperation

# No global variables needed anymore - everything is in the URL

class FilterToday(DirectoryPaneCommand):
    def __call__(self):
        import urllib.parse
        scheme, path = splitscheme(self.pane.get_path())

        # If we're already in a filtered view, extract the base path from URL
        if scheme == 'datefilter://':
            # Extract base path from URL like "30/E%3A%2Fdownloads"
            # First part is the days number, second part is the encoded path
            if '/' in path:
                parts = path.split('/', 1)
                if len(parts) > 1 and parts[0] in ['0', '3', '7', '30']:
                    # Decode the base path
                    path = urllib.parse.unquote(parts[1])

        # Encode the path for URL
        encoded_path = urllib.parse.quote(path, safe='')

        # Navigate to the filtered view with encoded path
        self.pane.set_path(f'datefilter://0/{encoded_path}')

class Filter3Days(DirectoryPaneCommand):
    def __call__(self):
        import urllib.parse
        scheme, path = splitscheme(self.pane.get_path())

        # If we're already in a filtered view, extract the base path from URL
        if scheme == 'datefilter://':
            # Extract base path from URL like "30/E%3A%2Fdownloads"
            # First part is the days number, second part is the encoded path
            if '/' in path:
                parts = path.split('/', 1)
                if len(parts) > 1 and parts[0] in ['0', '3', '7', '30']:
                    # Decode the base path
                    path = urllib.parse.unquote(parts[1])

        # Encode the path for URL
        encoded_path = urllib.parse.quote(path, safe='')

        # Navigate to the filtered view with encoded path
        self.pane.set_path(f'datefilter://3/{encoded_path}')

class Filter7Days(DirectoryPaneCommand):
    def __call__(self):
        import urllib.parse
        scheme, path = splitscheme(self.pane.get_path())

        # If we're already in a filtered view, extract the base path from URL
        if scheme == 'datefilter://':
            # Extract base path from URL like "30/E%3A%2Fdownloads"
            # First part is the days number, second part is the encoded path
            if '/' in path:
                parts = path.split('/', 1)
                if len(parts) > 1 and parts[0] in ['0', '3', '7', '30']:
                    # Decode the base path
                    path = urllib.parse.unquote(parts[1])

        # Encode the path for URL
        encoded_path = urllib.parse.quote(path, safe='')

        # Navigate to the filtered view with encoded path
        self.pane.set_path(f'datefilter://7/{encoded_path}')

class Filter30Days(DirectoryPaneCommand):
    def __call__(self):
        import urllib.parse
        scheme, path = splitscheme(self.pane.get_path())

        # If we're already in a filtered view, extract the base path from URL
        if scheme == 'datefilter://':
            # Extract base path from URL like "30/E%3A%2Fdownloads"
            # First part is the days number, second part is the encoded path
            if '/' in path:
                parts = path.split('/', 1)
                if len(parts) > 1 and parts[0] in ['0', '3', '7', '30']:
                    # Decode the base path
                    path = urllib.parse.unquote(parts[1])

        # Encode the path for URL
        encoded_path = urllib.parse.quote(path, safe='')

        # Navigate to the filtered view with encoded path
        self.pane.set_path(f'datefilter://30/{encoded_path}')

class ClearDateFilter(DirectoryPaneCommand):
    def __call__(self):
        import urllib.parse
        scheme, path = splitscheme(self.pane.get_path())

        if scheme == 'datefilter://':
            # Extract base path from URL like "datefilter://30/e:/downloads/"
            parts = path.split('/', 1)
            if len(parts) > 1:
                base_path = urllib.parse.unquote(parts[1])
                # Go back to the original directory
                self.pane.set_path(as_url(base_path))

class DateFilterFileSystem(FileSystem):
    scheme = 'datefilter://'

    def get_default_columns(self, path):
        return 'core.Name', 'core.Size', 'core.Modified'

    def resolve(self, path):
        import urllib.parse

        # Parse the path to extract base path and file
        # Format could be:
        # "30/e%3A%2Fdownloads" - root of filter
        # "30/e%3A%2Fdownloads/file.txt" - file in filter

        parts = path.split('/', 2)  # Split into at most 3 parts

        if len(parts) == 1:
            # Just a number like "30"
            return self.scheme + path

        if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
            # Always keep files within our custom scheme so our methods are used
            return self.scheme + path

        return super().resolve(path)

    def iterdir(self, path):
        try:
            import urllib.parse

            # Parse the path to extract days and base path
            # Format: "30/e%3A%2Fdownloads" where 30 is days and rest is encoded path
            parts = path.split('/', 1)

            days = 0
            base_path = None

            if len(parts) >= 1 and parts[0] in ['0', '3', '7', '30']:
                days = int(parts[0])

            if len(parts) > 1:
                base_path = urllib.parse.unquote(parts[1])

            if base_path:
                files = self._get_filtered_files(base_path, days)
                return files
        except Exception:
            # If anything goes wrong, return empty list to prevent crashes
            pass
        return []

    def _get_filtered_files(self, base_path, days_ago):
        from datetime import datetime, date, timedelta
        cutoff_date = datetime.combine(date.today() - timedelta(days=days_ago), datetime.min.time())
        files = []

        try:
            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                try:
                    mtime = os.path.getmtime(item_path)
                    file_mod_date = datetime.fromtimestamp(mtime)
                    if file_mod_date >= cutoff_date:
                        files.append(item)
                except:
                    pass
        except:
            pass

        return files

    def is_dir(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) < 2:
            return False

        if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])

            if len(parts) == 3:
                # A file in the filtered directory
                file_name = parts[2]
                full_path = os.path.join(base_path, file_name)
                return os.path.isdir(full_path)

        return False

    def size_bytes(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) < 2:
            return 0

        if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])

            if len(parts) == 3:
                # A file in the filtered directory
                file_name = parts[2]
                full_path = os.path.join(base_path, file_name)
                try:
                    return os.path.getsize(full_path)
                except:
                    return 0

        return 0

    def modified_datetime(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) < 2:
            return datetime.now()

        if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])

            if len(parts) == 3:
                # A file in the filtered directory
                file_name = parts[2]
                full_path = os.path.join(base_path, file_name)
                try:
                    mtime = os.path.getmtime(full_path)
                    return datetime.fromtimestamp(mtime)
                except:
                    pass

        return datetime.now()

    def copy(self, src_url, dst_url):
        import urllib.parse
        src_scheme, src_path = splitscheme(src_url)

        if src_scheme == self.scheme:
            # Parse path like "30/e%3A%2Fdownloads/file.txt"
            parts = src_path.split('/', 2)

            if len(parts) >= 3 and parts[0] in ['0', '3', '7', '30']:
                base_path = urllib.parse.unquote(parts[1])
                file_name = parts[2]
                real_src = as_url(os.path.join(base_path, file_name))
                fman.fs.copy(real_src, dst_url)
            else:
                raise UnsupportedOperation()
        else:
            raise UnsupportedOperation()

    def move(self, src_url, dst_url):
        import urllib.parse
        src_scheme, src_path = splitscheme(src_url)
        dst_scheme, dst_path = splitscheme(dst_url)

        if src_scheme == self.scheme:
            # Parse source path like "30/e%3A%2Fdownloads/file.txt"
            src_parts = src_path.split('/', 2)

            if len(src_parts) >= 3 and src_parts[0] in ['0', '3', '7', '30']:
                base_path = urllib.parse.unquote(src_parts[1])
                file_name = src_parts[2]
                real_src = os.path.join(base_path, file_name)

                # Check if this is a rename within the same filtered directory
                if dst_scheme == self.scheme:
                    dst_parts = dst_path.split('/', 2)
                    if (len(dst_parts) >= 3 and dst_parts[0] == src_parts[0] and
                        dst_parts[1] == src_parts[1]):
                        # Same directory, just different filename - this is a rename
                        new_file_name = dst_parts[2]
                        real_dst = os.path.join(base_path, new_file_name)

                        # Perform the actual rename
                        try:
                            os.rename(real_src, real_dst)
                            # File renamed successfully
                            # Note: User needs to press F5 to refresh the view
                        except Exception as e:
                            raise UnsupportedOperation(f"Rename failed: {str(e)}")
                    else:
                        # Moving to a different filtered directory - not supported
                        raise UnsupportedOperation("Cannot move between different filtered views")
                else:
                    # Moving to a regular directory
                    real_src_url = as_url(real_src)
                    fman.fs.move(real_src_url, dst_url)
            else:
                raise UnsupportedOperation()
        else:
            raise UnsupportedOperation()

    def stat(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])

            if len(parts) == 3:
                # A file in the filtered directory
                file_name = parts[2]
                full_path = os.path.join(base_path, file_name)
                try:
                    return os.stat(full_path)
                except FileNotFoundError:
                    # File doesn't exist yet (might be checking for a rename target)
                    # Return None to indicate file doesn't exist
                    raise
            elif len(parts) == 2:
                # The filtered directory itself
                return os.stat(base_path)

        # Return a dummy stat for the root
        return os.stat('.')

    def exists(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])

            if len(parts) == 3:
                # A file in the filtered directory
                file_name = parts[2]
                full_path = os.path.join(base_path, file_name)
                return os.path.exists(full_path)
            elif len(parts) == 2:
                # The filtered directory itself
                return os.path.exists(base_path)

        return False

    def touch(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) >= 3 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])
            file_name = parts[2]
            full_path = os.path.join(base_path, file_name)

            # Create the file
            with open(full_path, 'a'):
                os.utime(full_path, None)
        else:
            raise UnsupportedOperation("Cannot create file here")

    def delete(self, path):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = path.split('/', 2)

        if len(parts) >= 3 and parts[0] in ['0', '3', '7', '30']:
            base_path = urllib.parse.unquote(parts[1])
            file_name = parts[2]
            full_path = os.path.join(base_path, file_name)

            if os.path.isdir(full_path):
                import shutil
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
        else:
            raise UnsupportedOperation("Cannot delete this item")

    def rename(self, src_path, new_name):
        import urllib.parse

        # Parse path like "30/e%3A%2Fdownloads/file.txt"
        parts = src_path.split('/', 2)

        if len(parts) >= 3 and parts[0] in ['0', '3', '7', '30']:
            days = parts[0]
            base_path = urllib.parse.unquote(parts[1])
            old_file_name = parts[2]

            # Construct real paths
            old_full_path = os.path.join(base_path, old_file_name)
            new_full_path = os.path.join(base_path, new_name)

            # Check if source file exists
            if not os.path.exists(old_full_path):
                raise UnsupportedOperation(f"Source file does not exist: {old_full_path}")

            # Check if target already exists
            if os.path.exists(new_full_path):
                raise UnsupportedOperation(f"Target file already exists: {new_full_path}")

            # Perform the actual rename
            try:
                os.rename(old_full_path, new_full_path)
                # Return the new path in our scheme format
                encoded_base = urllib.parse.quote(base_path, safe='')
                return f"{days}/{encoded_base}/{new_name}"
            except Exception as e:
                raise UnsupportedOperation(f"Rename failed: {str(e)}")
        else:
            raise UnsupportedOperation("Cannot rename this item")

    def samefile(self, path1, path2):
        import urllib.parse

        # Extract real paths from both URLs
        def get_real_path(path):
            parts = path.split('/', 2)
            if len(parts) >= 2 and parts[0] in ['0', '3', '7', '30']:
                base_path = urllib.parse.unquote(parts[1])
                if len(parts) == 3:
                    return os.path.join(base_path, parts[2])
                return base_path
            return path

        real_path1 = get_real_path(path1)
        real_path2 = get_real_path(path2)

        # If either file doesn't exist, they can't be the same
        if not os.path.exists(real_path1) or not os.path.exists(real_path2):
            return False

        try:
            return os.path.samefile(real_path1, real_path2)
        except (OSError, ValueError):
            return real_path1 == real_path2