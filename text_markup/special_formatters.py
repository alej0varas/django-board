import re


from django.core.exceptions import ObjectDoesNotExist


import board.models


def format_references(text):
    referenced_text = text[:]

    for match in re.findall('&gt;&gt;\d+', text):
        ref = match[8:]  # saving referenced post's id

        try:
            thread = board.models.Thread.objects.get(id=int(ref))
            thread_url = thread.get_absolute_url()
            ref_url = thread_url + '#' + ref  # final reference url

            repl = '<a href="{}">{}</a>'.format(ref_url, match)
            referenced_text = referenced_text.replace(match, repl)

        except ObjectDoesNotExist:
            try:
                reply = board.models.Reply.objects.get(id=int(ref))
                thread_url = reply.thread.get_absolute_url()
                ref_url = thread_url + '#' + ref

                repl = '<a href="{}">{}</a>'.format(ref_url, match)
                referenced_text = referenced_text.replace(match, repl)

            except ObjectDoesNotExist:
                pass

    return(referenced_text)
