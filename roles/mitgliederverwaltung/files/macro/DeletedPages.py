# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - DeletedPages Macro

    This macro shows a list of pages that have been deleted by
    ?action=delete but still exist silently on disc.
    You need to be superuser to call this macro.

    Syntax:
    
    [[DeletedPages]]
    
    @copyright: 2006 by Oliver Siemoneit
    @license: GNU GPL, see COPYING for details.

    DeletedPages partly based on _macro_TitleSearch from
    wikimarco.py by Jürgen Hermann
    @copyright: 2000-2004 by Jürgen Hermann <jh@web.de>
    @license: GNU GPL, see COPYING for details.

    Changes:

    Version 1.1 by Oliver Siemoneit
    * Macro supports multilang if translations for
      '[Unerase] ' and '[Purge completely] ' are provided elsewhere.

    
"""


import os
from MoinMoin import wikiutil
from MoinMoin import user
from MoinMoin.Page import Page


Dependencies = ["pages"]

def execute(macro, args):
    request = macro.request
    _ = request.getText
    formatter = macro.formatter
        
    # Check if user is superuser. If not: return with error msg
    if not request.user.isSuperUser():
        err = _('You are not allowed to perform this action.')
        return "%s%s%s" % (formatter.sysmsg(1), formatter.text(err), formatter.sysmsg(0))

    pages = []
    visible_pages = request.rootpage.getPageList(exists=1)
    existing_pages = request.rootpage.getPageList(exists=0)
    for page in existing_pages:
        if visible_pages.count(page) == 0:
            pages.append(page)
    html = []
    index_letters = []
    
    # Sort ignoring case
    tmp = [(name.upper(), name) for name in pages]
    tmp.sort()
    pages = [item[1] for item in tmp]
                
    current_letter = None
    for wikipagename in pages:
        letter = wikiutil.getUnicodeIndexGroup(wikipagename)
        if letter not in index_letters:
            index_letters.append(letter)
        if letter != current_letter:
            html.append(u'<a name="%s"><h3>%s</h3></a>' % (
                wikiutil.quoteWikinameURL(letter), letter.replace('~', 'Others')))
            current_letter = letter
        else:
            html.append(u'<br>')
        html += macro.formatter.div(1, css_class='searchresults')       
        html += macro.formatter.definition_list(1)
        
        html += macro.formatter.definition_term(1)
        html.append(u'%s\n' % Page(request, wikipagename).link_to(request, attachment_indicator=1))
        html += macro.formatter.definition_term(0)
    
        html += macro.formatter.definition_desc(1)
        acl = Page(request, wikipagename).getACL(request)
        aclstring = acl.getString()
        if aclstring == '':
            aclstring = '-'
        html.append(u'%s ' % aclstring)
        html += macro.formatter.linebreak(0)
        rev = Page(request, wikipagename).get_real_rev()
        if rev > 1:
            rev = rev-1
        html.append(u'%s ' % Page(request, wikipagename).link_to(request, _('[Unerase] '), "action=revert&rev=%d" %rev))
        html.append(u'%s ' % Page(request, wikipagename).link_to(request, _('[Purge completely] '), "action=purge"))
        html += macro.formatter.definition_desc(0)
        
        html += macro.formatter.definition_list(0)
        html += macro.formatter.div(0, css_class='searchresults') 
       
    index = _make_index_key(index_letters)
    return u'%s%s' % (index, u''.join(html))


def _make_index_key(index_letters, additional_html=""):
    index_letters.sort()
    links = map(lambda ch:
                    '<a href="#%s">%s</a>' %
                    (wikiutil.quoteWikinameURL(ch), ch.replace('~', 'Others')),
                index_letters)
    return "<p>%s%s</p>" % (' | '.join(links), additional_html)





