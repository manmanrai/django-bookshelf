from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Book, Review
from .consts import ITEMS_PER_PAGE

class ListBookView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    paginate_by = ITEMS_PER_PAGE

class DetailBookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book/book_detail.html'

class CreateBookView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'book/book_create.html'
    fields = ['title', 'category', 'text', 'thumbnail']
    success_url = reverse_lazy('list-book')

class DeleteBookView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/book_confirm_delete.html'
    # success_url = reverse_lazy('list-book')

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

class UpdateBookView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/book_update.html'
    fields = ['title', 'category', 'text', 'thumbnail']
    # success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.kwargs['pk']})

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'book/review_form.html'
    fields = ['book', 'title', 'text', 'rate']
    # success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['book'] = Book.objects.get(pk=self.kwargs['pk'])
        # print(content)
        return content
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def index_view(request):
    # print('index_view is called')
    object_list = Book.objects.order_by('-id')
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')[:3]

    paginator = Paginator(ranking_list, ITEMS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    # query = request.GET.get('number')
    # print(query)
    return render(request, 'book/index.html', {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj': page_obj})

def get_object(self, queryset=None):
    obj = super().get_object(queryset=queryset)
    if obj.user != self.request.user:
        raise PermissionDenied
    return obj