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
            base_path = urllib.parse.unquote(parts[1])

            if len(parts) == 2:
                # Root of filtered directory
                return self.scheme + path

            if len(parts) == 3:
                # A file in the filtered directory
                file_name = parts[2]
                return as_url(os.path.join(base_path, file_name))

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

        if src_scheme == self.scheme:
            # Parse path like "30/e%3A%2Fdownloads/file.txt"
            parts = src_path.split('/', 2)

            if len(parts) >= 3 and parts[0] in ['0', '3', '7', '30']:
                base_path = urllib.parse.unquote(parts[1])
                file_name = parts[2]
                real_src = as_url(os.path.join(base_path, file_name))
                fman.fs.move(real_src, dst_url)
            else:
                raise UnsupportedOperation()
        else:
            raise UnsupportedOperation()