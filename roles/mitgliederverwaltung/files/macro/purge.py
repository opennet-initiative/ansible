# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Purge Action
    
    Deletes a page completely form disc. You need be superuser
    to call this action. Superuser is assumed to be a trusted
    user which has read, write, delete, revert and admin rights.

    @copyright: 2006 by Oliver Siemoneit
    @license: GNU GPL, see COPYING for details.

    Changes:

    Version 1.1 by Oliver Siemoneit
    * Macro now supports multilang if translations for
      'Purge: "%s"'
      'You cannot purge existing pages. You have to delete them first.'
      'Page has not been removed.'
      'Page successfully removed.'
      'Page does not exist.'
      are provided elsewhere.

"""

import os
from MoinMoin.Page import Page
from MoinMoin import wikiutil


def execute(pagename, request):
    _ = request.getText

    # Check if user is superuser
    if not request.user.isSuperUser():
        result = _('You are not allowed to perform this action.')

    # Check if page exists
    elif Page(request, pagename).exists() == True:
        result = _('You cannot purge existing pages. You have to delete them first.')
        
    else:
        pagedir = Page(request, pagename).getPagePath(use_underlay=0, check_create=0)
        if os.path.exists(pagedir):
            import shutil
            try:
                shutil.rmtree(pagedir)
            except EnvironmentError:
                result = _('Page has not been removed.')
            else:
                result = _('Page successfully removed.')
        else:
            result = _('Page does not exist.')
                
    #Page(request, pagename).send_page(request, result)
    request.theme.add_msg(result, "info")
    Page(request, pagename).send_page()
