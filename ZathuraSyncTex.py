import sublime
import sublime_plugin
import os.path
import subprocess


class ZathuraSyncTexCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if 'LaTeX' not in self.view.settings().get('syntax'):
            return sublime.error_message('Can only use SyncTex on LaTeX files.')

        file_name = self.view.file_name()

        if self.view.is_scratch() or file_name is None:
            return sublime.error_message('Can only use SyncTex on real files.')

        first_line = sublime.Region(0, self.view.text_point(1, 0))
        first_line = self.view.substr(first_line).strip()

        root_file = file_name
        if '!TEX root' in first_line and '=' in first_line:
            root_file = first_line[first_line.index('=') + 1:].strip()
            root_file = os.path.realpath(
                os.path.join(os.path.dirname(file_name), root_file)
            )

        path, file = os.path.split(root_file)
        file_base = os.path.splitext(file)[0]
        pdf_file = os.path.join(path, 'bin', file_base + '.pdf')

        for sel in self.view.sel():
            line, col = self.view.rowcol(sel.begin())
            line += 1
            col += 1

            command = [
                'zathura',
                '--synctex-forward',
                '{line}:{col}:{file}'.format(
                    line=line, col=col, file=file_name
                ),
                pdf_file
            ]

            print('Running:', command)

            subprocess.Popen(command)

            return
