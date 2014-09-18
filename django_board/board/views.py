from django.core.urlresolvers import reverse_lazy

from vanilla import FormView

from .forms import ThreadForm
from .models import Thread, Reply


class MainBoardPage(FormView):
    template_name = 'board/main.html'

    form_class = ThreadForm
    success_url = reverse_lazy('b:main')

    def get_context_data(self, **kwargs):
        context = super(MainBoardPage, self).get_context_data(**kwargs)
        context['threads'] = Thread.objects.all().order_by('-pub_date')
        return(context)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(form=form)
        return(self.render_to_response(context))

    def post(self, request):
        form = self.get_form(data=request.POST)
        if form.is_valid():
            new_thread = form.save()
            return(self.form_valid(form))
        return(self.form_invalid(form))
