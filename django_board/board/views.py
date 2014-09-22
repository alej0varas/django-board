from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from vanilla import FormView

from .forms import ThreadForm, ReplyForm
from .models import Thread, Reply


class MainBoardPage(FormView):
    template_name = 'board/main.html'

    form_class = ThreadForm
    success_url = reverse_lazy('board:main')

    def get_context_data(self, **kwargs):
        context = super(MainBoardPage, self).get_context_data(**kwargs)
        context['threads'] = Thread.objects.all().order_by('-pub_date')
        return(context)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(form=form)

        paginator = Paginator(context['threads'], 10)
        page = request.GET.get('page')
        try:
            context['threads'] = paginator.page(page)
        except PageNotAnInteger:
            context['threads'] = paginator.page(1)
        except EmptyPage:
            context['threads'] = paginator.page(paginator.num_pages)

        return(self.render_to_response(context))

    def post(self, request):
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_thread = form.save()
            return(self.form_valid(form))

        return(self.form_invalid(form))


class ThreadView(FormView):
    template_name = 'board/thread.html'

    form_class = ReplyForm
    success_url = None

    def get_context_data(self, pk, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['thread'] = get_object_or_404(Thread, id=pk)
        return(context)

    def get(self, request, pk, **kwargs):
        form = self.get_form()
        context = self.get_context_data(pk=pk, form=form)
        return(self.render_to_response(context))

    def post(self, request, pk, **kwargs):
        form = self.get_form(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_reply = form.save(commit=False)

            # manually setting the foreign key before saving
            thread = Thread.objects.get(id=pk)
            new_reply.thread = thread

            new_reply.save()
            return(self.form_valid(form, pk=pk))

        return(self.form_invalid(form))

    def form_valid(self, form, pk, **kwargs):
        return(HttpResponseRedirect(self.get_success_url(pk=pk)))

    def get_success_url(self, pk, **kwargs):
        if self.success_url is None:
            return(reverse('board:thread', kwargs={'pk': pk}))
