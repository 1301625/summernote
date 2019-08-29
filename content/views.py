from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Post
from .forms import PostForm
from apply.models import Apply

from datetime import date


class PostListView(ListView):
    model = Post
    template_name = 'content/content_list.html'


# class PostDetialView(DetailView):
#     model = Post
#     template_name = 'content/content_detail.html'


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # select = request.POST.get('choice')
    #select = request.POST.get('choice')

        # if post.user_count < post.user_max_count:
        #     apply = Apply.objects.get(post_id=select, user_id=request.user)
        #     apply.post.user_count += 1
        #     # count_plus.user_count+=1
        #     apply.save()

        #messages.success(request, "신청되었습니다.")
        # else:
        #     messages.error(request, "인원이 초과되었습니다")

        #apply = Apply(post_id=select, user_id=request.user)
        #apply.save()

    return render(request,'content/content_detail.html',{'object':post})

    # try:
    #     count = post.objects.get(pk=request.POST.get('choice'))
    #     count.user_count +=1
    #     count.save()
    #     return redirect('list')
    # except :
    #     pass
    #   post.user_count+=1
    #   post.save()

class PostCreateView(CreateView):
    template_name = 'content/content_create.html'
    model = Post
    form_class = PostForm
    # fields = ['title', 'content']
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


@login_required
def apply_post(request, pk):
    post= get_object_or_404(Post,pk=pk)

    try:
        apply = Apply.objects.get(post_id=post.id, user=request.user)
        apply.post.user_count+=1
        apply.save()
    except:
        apply = Apply(post_id=post.id, user=request.user)
        post.user_count+=1
        post.save()
        apply.save()

    return redirect('list')



def apply_list(request, pk):
    post = get_object_or_404(Post,pk=pk)
    list = Apply.objects.filter(post_id=post.id)

    return render(request, 'content/apply_list.html' ,{'apply_list':list})
