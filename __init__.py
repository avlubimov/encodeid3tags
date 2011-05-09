# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Sergey Mihailov <sergey.mihailov@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.
#
# INSTALL HOWTO : decomressed files to ~/.gnome2/rhythmbox/plugins/

import rhythmdb, rb
import gtk, glib
import locale

ui_definition = """
<ui>
    <popup name="BrowserSourceViewPopup">
        <menuitem name="EncodeToLibraryPopup" action="EncodeTo" />
    </popup>
     
    <popup name="PlaylistViewPopup">
        <menuitem name="EncodeToPlaylistPopup" action="EncodeTo" />
    </popup>

    <popup name="QueuePlaylistViewPopup">
        <menuitem name="EncodeToQueuePlaylistPopup" action="EncodeTo" />
    </popup>
</ui>"""

class idTagEncode (rb.Plugin):
    def __init__(self):
        rb.Plugin.__init__(self)

    def activate(self, shell):
        self.shell = shell
        self.db = shell.get_property("db")
        self.locale = locale
        if 'ru' in self.locale.getlocale()[0]:
            self.__action = gtk.Action('EncodeTo', _('Перекодировать ID3 подпись'),
                                _('Перекодировать ID3 метаданные в UTF-8.'), '')
        else:
            self.__action = gtk.Action('EncodeTo', _('Encode ID3 tags to UTF-8'),
                                _('Encode id tags by UTF-8.'), '')

        self.__action.connect('activate', self.encode_to_utf8, shell)

        self.__action_group = gtk.ActionGroup('EncodeToActionGroup')
        self.__action_group.add_action(self.__action)
        shell.get_ui_manager().insert_action_group(self.__action_group)

        self.__ui_id = shell.get_ui_manager().add_ui_from_string(ui_definition)

    def deactivate(self, shell):
        shell.get_ui_manager().remove_action_group(self.__action_group)
        shell.get_ui_manager().remove_ui(self.__ui_id)
        shell.get_ui_manager().ensure_update()

        del self.__action_group
        del self.__action

        del self.db
        del self.shell

    def encode_to_utf8(self, action, shell):
	print shell.props
#        entries = shell.props.selected_source.get_entry_view().get_selected_entries()
        entries = shell.props.clipboard.props.source.get_entry_view().get_selected_entries()

        for entry in entries:
            def change_fields(name_fields):
                try:
                    t_var = self.db.entry_get (entry, name_fields)
                    t_var_u8 =  t_var.encode('latin1').decode('cp1251').encode('utf8')
                    self.db.set(entry, name_fields, t_var_u8)
                except:
                    return

            change_fields(rhythmdb.PROP_ARTIST)
            change_fields(rhythmdb.PROP_GENRE)
            change_fields(rhythmdb.PROP_ALBUM)
            change_fields(rhythmdb.PROP_TITLE)
           
            self.db.commit()


