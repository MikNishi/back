from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Post, Tag, Category
from django.shortcuts import get_object_or_404
from django.db.models import Q


class PostSearchView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(content__icontains=query)
            )
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class TagListView(ListView):
    model = Post
    template_name = 'post/post_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'post/post_by_category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class BlogListView(ListView):
    model = Post
    # queryset = Post.objects.order_by('id')
    paginate_by = 2
    template_name = "post/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Передаем категории
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        post_id = self.kwargs.get('id')
        if slug:
            return get_object_or_404(Post, slug=slug)
        else:
            return get_object_or_404(Post, id=post_id)


class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = "post/post_new.html"
    fields = ["name", "content", 'excerpt', "featured_image", 'slug', 'tags', 'category']
    success_message = "%(name)s успешно создан"

    #success_url = reverse_lazy("post_list")
    # def get_success_url(self):
    #     return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     if name == "500":
    #         form.add_error('name', "Сообщение")
    #         messages.error(self.request, "В данный момент у вас не хватает полномочий")
    #         return self.form_invalid(form)
    #
    #     messages.success(self.request, f"{name} успешно создан")
    #     return super().form_valid(form)
    #
    # def form_invalid(self, form):
    #     messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
    #     return super().form_invalid(form)




class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = "post/post_edit.html"
    # success_url = reverse_lazy("post_list")
    fields = ["name", "description", "featured_image"]
    success_message = "%(name)s успешно обновлен"


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    success_url = reverse_lazy("post_list")
