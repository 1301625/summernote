from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import CreateView , ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Post
from .forms import PostForm

from datetime import date

class PostListView(ListView):
    model = Post
    template_name = 'content/content_list.html'



# class PostDetialView(DetailView):
#     model = Post
#     template_name = 'content/content_detail.html'


def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)

    #select = request.POST.get('choice')
    select = request.POST.get('choice')
    try:
        if select:
            count_plus = post
            if count_plus.user_count < count_plus.user_max_count:
                count_plus.user_count+=1
                count_plus.save()
                messages.success(request,"신청되었습니다.")
            else:
                messages.error(request,"인원이 초과되었습니다")
    except :
        return redirect('detail', pk=pk)

    # try:
    #     count = post.objects.get(pk=request.POST.get('choice'))
    #     count.user_count +=1
    #     count.save()
    #     return redirect('list')
    # except :
    #     pass
 #   post.user_count+=1
 #   post.save()

    return render(request, 'content/content_detail.html', {'object': post})

class PostCreateView(CreateView):
    template_name = 'content/content_create.html'
    model = Post
    form_class = PostForm
    #fields = ['title', 'content']
    success_url = reverse_lazy('list')
    success_message = "등록되었습니다."
    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     from datetime import date
    #     if date.today() < post.deadline:
    #         post.save()
    #         return redirect('list')
    #     else:
    #         messages.error(self.request,"날짜를 다시 선택해 주세요")


