from .utils import conf


def config(request):
    context = {'CONFIG': conf.CONFIG,
               'True': True,
               'False': False,
               }
    return context
