from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView ,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages


from django.contrib.auth.decorators import login_required  # 로그인 필요
from django.views.decorators.http import require_POST  # post 요청만 허용

import json
from django.http import HttpResponse


from .models import Post, Apply, Chatroom
from .forms import PostForm , CommentForm






class PostListView(ListView):
    model = Post
    template_name = 'content/content_list.html'
    queryset = Post.objects.prefetch_related('users', 'author').order_by('-id')  # 쿼리 최적화

#제네릭 디테일 뷰
# class PostDetialView(DetailView):
#     model = Post
#     template_name = 'content/content_detail.html'


#댓글 폼 테스트
def comment_form(request):
    form = CommentForm()
    return render(request, 'content/comment_form.html', {'form':form})

def post_detail(request, pk):
    post = Post.objects.prefetch_related('users','author','comment_set').get(pk=pk)  # 해당 Post디비를 가져옴
    apply = post.apply_set.filter(user_id=request.user.id)  # 유저가 디비에 있는지 확인

    form = CommentForm()

    content = {
        'comment_form ': form,
        'object': post,
        'apply': apply,
    }
    return render(request, 'content/content_detail.html', content)


    # apply = Apply.objects.prefetch_related('user').filter(post_id=pk,user_id=request.user.id) #접속한유저가 신청 유무확인
    # apply = post.users.filter(post__apply__user_id=request.user.id, apply__post_id=pk)
    # content = { 'object': get_object_or_404(Post,pk=pk),
    #           'apply': Apply.objects.filter(post_id=pk)}
    # print(Apply.objects.filter(post_id=pk))

    # select = request.POST.get('choice')
    # select = request.POST.get('choice')

    # if post.user_count < post.user_max_count:
    #     apply = Apply.objects.get(post_id=select, user_id=request.user)
    #     apply.post.user_count += 1
    #     # count_plus.user_count+=1
    #     apply.save()

    # messages.success(request, "신청되었습니다.")
    # else:
    #     messages.error(request, "인원이 초과되었습니다")

    # apply = Apply(post_id=select, user_id=request.user)
    # apply.save()



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

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect('list')
    #     from datetime import date
    #     if date.today() < post.deadline:
    #         post.save()
    #         return redirect('list')
    #     else:
    #         messages.error(self.request,"날짜를 다시 선택해 주세요")

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'content/content_create.html'

    #해당 사용자 검증
    def get_queryset(self):
        qs= self.request.user
        return self.model.objects.filter(author=qs)

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    success_messages = "삭제되었습니다"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_queryset(self):
        qs = self.request.user
        return self.model.objects.filter(author=qs)




@login_required
@require_POST
def apply_post(request,pk):
    #pk = request.POST.get('pk', None)
    #print("pk:", pk)
    post = get_object_or_404(Post, pk=pk)
    if post.users.filter(id=request.user.id).exists():
        messages="이미 신청 되었습니다"
        #return redirect('detail', pk=pk)
    else:
        post.apply_set.create(user_id=request.user.id, post_id=pk)
        # apply = Apply(user=request.user, post_id=pk)
        messages="신청 되었습니다"

    data = {
        'total_user': post.total_user(),
        'message' : messages,
    }
    return HttpResponse(json.dumps(data) ,content_type='application/json')
        # ap = Apply.objects.filter(post_id=pk).count()
    # post = get_object_or_404(Post,pk=pk)
    # post.user_count = ap
    # print(post.user_count)
    # print(ap)
    # post.save()

    # try:
    #     apply = Apply.objects.get(post_id=pk, user=request.user)
    #     apply.post.user_count += 1
    #     apply.save()
    # except:
    #     apply = Apply.objects.create(post_id=pk, user=request.user)
    #     # post.user_count+=1
    #     apply.objects.model.post.user_count += 1
    #     print(apply)
    #     # post.save()
    #     apply.save()

    # if request.user != apply.post.author:
    #   print("다릅니다")

    # apply.post.user_count = apply.user.count()

    # else:
    #    print("같습ㄴ디ㅏ")


@login_required
def apply_cancel(request, pk):
    apply = Apply.objects.filter(post_id=pk)

    if apply.filter(user_id=request.user).exists():
        apply.get(user_id=request.user).delete()
        message = "취소 되었습니다"
    else:
        message= "신청 하지 않았습니다"

    data = {
        'total_user' : apply.count(),
        'message' : message
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


    #return redirect('detail', pk=pk)
    # 불가능
    # post = Post.objects.get(pk=pk)
    #
    # if post.users.filter(id=request.user.id).exists():
    #     post.apply_set.clear(user_id=request.user.id, post_id=pk)
    #     post.save()
    # post.apply_set.remove(id=request.user.id ,)
    # post.users.filter(post__apply__user_id=request.user).delete() 유저 자체를 지움
    # post.save()
    # 나중에 방법
    # apply = Apply.objects.filter(post_id=pk, user_id=request.user.id)
    # if apply:
    #
    #     apply.delete()
    # else:

    # print(post)

    # if apply.objects.filter(user_id=request.user.id).exists():
    #    print("존재")
    # if post.users.filter(id=request.user.id):
    #    post.user_count_minus()

    #    print(post)

    # try:
    #     apply = Apply.objects.filter(post_id=pk, user=request.user)
    #     print(apply.post_set.all())
    #     if apply:
    #         apply.delete()
    #         apply.post.user_count -= 1
    #         messages.success(request, "신청이 취소 되었습니다.")
    #     else:
    #         messages.error(request, "신청자가 존재 하지 않습니다")
    # except:
    #     pass


def apply_list(request, pk):
    list = Apply.objects.select_related().filter(post_id=pk)
    # post = Post.objects.prefetch_related().filter(id=pk)

    if list:
        return render(request, 'content/apply_list.html', {'apply_list': list})
    # list = Apply.objects.get(post_id=pk) #get은 하나만 가져올떄 , 하나 이상 가져오면 오류
    else:
        messages.error(request, "존재하지 않습니다")
        return redirect('detail', pk=pk)


def room(request, pk):

    #TODO 채팅방 메시지 사용자 분류 재작성
    chat_message = Chatroom.objects.select_related().filter(post_id=pk)
    author  = Post.objects.get(pk=pk).author_id

    apply = Apply.objects.select_related('user').filter(post_id=pk).values('user_id')

    #apply의 user_id : dict_values 값을 꺼내기위해 리스트 생성
    dic_convert = []
    for i in apply:
        dic_convert.append(list(i.values()))
    # 2차원 리스트 1차원 리스트로 변경
    users =sum(dic_convert, [])

    content = {
        'chat_message' : chat_message,
        'users' : users,
        'author' : author,
        'pk' : pk
    }
    return render(request, 'content/room.html', content)



