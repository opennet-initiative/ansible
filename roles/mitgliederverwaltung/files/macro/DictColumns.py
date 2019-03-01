# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - macro to collect data from definition lists on pages
    into a data browser widget table

    <<DictColumns(search_term=regex:title:^Examplepage/)>

    @copyright: 2006 by michael cohen <scudette@users.sourceforge.net> (PageDicts)
    @copyright: 2008-2016 by MoinMoin:ReimarBauer (completly rewritten)
    @license: GNU GPL, see COPYING for details.
"""
import re

from collections import defaultdict
from MoinMoin import wikiutil, search
from MoinMoin.Page import Page
from MoinMoin.action.SlideShow import SlidePage
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget
from MoinMoin.datastruct.backends.wiki_dicts import WikiDicts

Dependencies = ["pages"]


def _csv2list(csv):
    """
    converts a string of comma separated values into a list
    @param csv: string of comma separated values
    @returns: list
    """
    csv_list = csv.split(',')
    return [variable.strip() for variable in csv_list if variable.strip()]

def _name2index(all_names, selected_names):
    """
    converts names to the index
    @param all_names: all available names
    @param selected_names: names to lookup index position of all_names
    @return: list of indices
    """
    if selected_names:
        try:
            index = [all_names.index(name) for name in selected_names]
        except ValueError:
            return []
        return index
    return []

class DictColumns(object):
    """
    Collects definition list key and values pairs.
    Each key becomes a column with its values.
    """
    def __init__(self, macro, pagename=u'', title=u'', names=u'',
                 sort=u'', reverse=u'',
                 hide=u'', filter_name=u'NeverExistingDefaultFilter',
                 filter_value=u'', template_page=u'', alias_page=u'',
                 parser=u'text_moin_wiki', markup="definition list",
                 search_term=None, comments=False, enumeration=False):

        self.formatter = macro.formatter
        self.request = macro.request
        self.pagename = pagename
        if not pagename:
            self.pagename = macro.formatter.page.page_name
        self.request.page = Page(self.request, self.pagename)
        self.title = title
        if not title:
            self.title = self.pagename
        self.names = names
        self.sort = sort
        self.reverse = reverse
        self.hide = hide
        self.filter_name = filter_name
        self.filter_value = filter_value
        self.filter_key, self.filter_word = (u"", u"")
        self.comments = comments
        self.enumeration = enumeration
        regex = re.compile(ur'(?P<key>\w*)=(?P<value>.*)', re.UNICODE)
        try:
            self.filter_key, self.filter_word = regex.search(filter_value).groups()
        except AttributeError:
            # Don't filter if syntax was wrong
            self.filter_value = u""
        self.template_page = template_page
        self.alias_page = alias_page
        try:
            self.wiki_parser = wikiutil.importPlugin(
                                    self.request.cfg, "parser",
                                    parser, function="Parser")
        except wikiutil.PluginMissingError:
            self.wiki_parser = None
        self.search_term = search_term
        self.markup = markup
        if search_term is None:
            self.search_term = u'regex:title:^%s/' % self.pagename

    def get_dict(self, dict_source):
        """
        gets the dictionary dependent of the markup
        @param dict_source: pagename to read dict data from
        """
        if self.markup in ("definition list", "dl"):
            return self.request.dicts[dict_source]
        elif self.markup in ("multiline definition list", "mdl"):
            return self.parse_multiline_dict(dict_source)
        elif self.markup in ("title", "t"):
            return self.parse_title(dict_source)

    def parse_multiline_dict(self, dict_source):
        """
        creates a dictionary based on a definition list with multiple entries of the same key. 
        The type of the value is a list
         a:: 1
         b:: 1
         b:: 2
         b:: 3
         c:: 4
        @param dict_source: pagename to read dict data from
        """
        body = Page(self.request, dict_source).get_raw_body()
        ddict = defaultdict(list)

        for match in WikiDicts._dict_page_parse_regex.finditer(body):
            key, value = match.groups()
            ddict[key].append(value)
        return ddict
    
    def parse_title(self, dict_source):
        """
        creates a dictionary based on page titles
        @param dict_source: pagename to read dict data from
        """
        body = Page(self.request, dict_source).get_raw_body()
        parser = SlidePage(self.request, dict_source).createSlideParser()
        ddict = {}
        for title, bodyStart, bodyEnd in parser.parse(body):
            ddict[title] = body[bodyStart:bodyEnd].strip()
        return ddict

    def get_page_list(self):
        """
        selects the pages dependent on a search term,
        without listing of template, dictionary pages and
        the pagename itselfs.
        """
        request = self.request
        search_term = self.search_term
        search_result = search.searchPages(request, search_term)
        pages = [title.page_name for title in search_result.hits]
        if not pages:
            return None
        # exclude some_pages
        filterfn = request.cfg.cache.page_template_regexact.search
        template_pages = request.rootpage.getPageList(filter=filterfn)
        excluded_pages = template_pages + [self.alias_page, self.pagename]
        selected_pages = [page for page in pages if page not in excluded_pages]
        selected_pages.sort()
        return selected_pages

    def get_names(self, selected_pages):
        """
        selects which column names should be used
        @param selected_pages: list of page names
        @return: list of names
        """
        request = self.request
        # use selection and order
        if self.names:
            return self.names
        # use keys from template page, no order
        elif Page(request, self.template_page).exists():
            page_dict = self.get_dict(self.template_page)
            names = page_dict.keys()
        else:
            # fallback use the keys used on selected pages
            names = []
            for page_name in selected_pages:
                page_dict = self.get_dict(page_name)
                keys = page_dict.keys()
                names = names + keys
        return list(set(names))

    def dataset(self, names, selected_pages):
        """
        Sets the data for the data browser widget
        @param names: column names
        @param selected_pages: pages to read key value pairs from
        """
        _ = self.request.getText
        assert isinstance(selected_pages, list)
        request = self.request
        hide_columns = self.hide
        # default alias
        alias_dict = {}
        for name in names:
            alias_dict[name] = name
        if Page(request, self.alias_page).exists():
            alias = self.get_dict(self.alias_page)
            for name in names:
                alias_dict[name] = alias.get(name, name)

        col = Column(self.title, label=self.title)
        if self.title in hide_columns:
            col.hidden = True

        data = TupleDataset()
        data.columns = []
        data.columns.extend([col])

        for page_name in selected_pages:
            page = Page(request, page_name)
            page_dict = self.get_dict(page_name)
            if self.filter_value and page_dict.get(self.filter_key, '') != self.filter_word:
                continue

            row = []
            for name in names:
                if name in page_dict.keys():
                    value = page_dict.get(name, '')
                    if isinstance(value, list) and len(value) > 1:
                        value = ' 1. %s' % '\n 1. '.join(value)
                    elif isinstance(value, list):
                        value = value[0]

                    if self.wiki_parser:
                        row.append((wikiutil.renderText(request, self.wiki_parser, value),
                                    wikiutil.escape(value, 1)))
                else:
                    row.append('')
            if self.comments:
                row.append('')
            try:
                parent, child = page_name.split('/', 1)
            except ValueError:
                child = page_name
            link = page.link_to(request, text="%s" % child)
            data.addRow([link] + row)

        if self.filter_name:
            filtercols = self.filter_name
            for name in names:
                if self.filter_name != u'NeverExistingDefaultFilter' and name in filtercols:
                    col = Column(alias_dict[name], autofilter=(name in filtercols))
                    if name in hide_columns:
                        col.hidden = True
                    data.columns.append(col)
                else:
                    col = Column(alias_dict[name], label=alias_dict[name])
                    if name in hide_columns:
                        col.hidden = True
                    data.columns.extend([col])
            if self.comments:
                col = Column("Comment", label=_("Comment:"))
                data.columns.extend([col])
        return data

    def render(self):
        """
        renders output as widget data browser table
        """
        request = self.request
        _ = request.getText

        selected_pages = self.get_page_list()
        if not selected_pages:
            return _("""\
Please use a more selective search term instead of search_term="%s"\
""") % self.search_term

        names = self.get_names(selected_pages)

        data = self.dataset(names, selected_pages)
        table = DataBrowserWidget(request)

        names.insert(0, "__name__")
        sort_columns = _name2index(names, self.sort)
        sort_reverse_columns = _name2index(names, self.reverse) or False

        table.setData(data, sort_columns, reverse=sort_reverse_columns)
        if self.enumeration:
            idx = 0
            for line in data.data:
                line.insert(0, unicode(idx + 1))
                data.data[idx] = line
                idx += 1
            col = Column(" ", label=" ")
            data.columns.insert(0, col)

        html = ''.join(table.format(method='GET'))
        return html

def macro_DictColumns(macro, pagename=unicode, title=u'', names=u'', sort=u'', reverse=u'',
                      hide=u'', filter_name=u'NeverExistingDefaultFilter',
                      filter_value=u'', template_page=u'', alias_page=u'',
                      parser=u'text_moin_wiki',
                      markup=("definition list", "title",
                              "multiline definition list",
                              "dl", "mdl", "t"),
                      comments=False,
                      enumeration=False,
                      search_term=None):
    """
    Creates a table by data browser widget from definition lists key value pairs.
    @param pagename: name of the page
    @param title: entry in upper left corner of the table
    @param name: names of columns, key name of definition list (comma separated)
    @param sort: name of columns to sort by
    @param reverse: name of columns to reverse sort by
    @param hide: name of columns to hide
    @param filter_name: name of columns to filter by autofilter
    @param filter_value: dict definition for value of column to filter by
    @param template_page: pagename of the template for setting column names
    @param alias_page: pagename of the page for setting aliases for column names
    @param parser: name of the parser used to render markup
    @param markup: type of markup for separating key value pairs
    @param search_term: regex used to search for selecting pages
    """
    kw = locals()
    #  wiki input can be a string with comma separated values.
    kw["names"] = _csv2list(kw["names"])
    kw["sort"] = _csv2list(kw["sort"])
    kw["reverse"] = _csv2list(kw["reverse"])
    kw["hide"] = _csv2list(kw["hide"])
    kw["filter_name"] = _csv2list(kw["filter_name"])
    html = DictColumns(**kw).render()
    # works together with
    # http://moinmo.in/FeatureRequests/SortableTables?action=AttachFile&do=view&target=common.js.patch
    # html = html.replace('id="dbw.table', 'class="sortable" id="dbw.table')
    return html

