

class RequestExtension(object):

    def __init__(self, request):
        self.request = request

    def flash_success(self, body, title=''):
        self.request.session.flash({'title': title, 'body': body}, queue='success')

    def flash_error(self, body, title=''):
        self.request.session.flash({'title': title, 'body': body}, queue='error')

    def flash_info(self, body, title=''):
        self.request.session.flash({'title': title, 'body': body}, queue='info')


def get_extensions(request):
    return RequestExtension(request)
