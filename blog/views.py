#coding=utf-8
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from models import Article,Tag,Category
from django.http import JsonResponse,HttpResponse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import markdown
from comments.forms import CommentForm
from django.db.models import Q


# Create your views here.
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'article_list': article_list})


'''Web服务器的作用是接受来自用户的http请求，根据请求内容，将处理结果包装成HTTP响应返回给用户
    视图函数首先接受一个名为request的参数，这个参数就是Djang为我们封装好的HTTP请求，
    然后返回响应，这个响应由HttpResponse封装，我们给它传递了一个自定义的字符串
'''

'''01 
   这里的render函数根据我们传入的参数来构成一个HttpResponse。
   其中，第一个参数表示Http请求，第二个参数表示找到blog/index.html这个模板并读取其中的内容，
   第三个参数表示将模板中的变量替换为我们要传递的变量值。即{{title}}替换为‘我的博客首页’，
   {{welcome}}替换为‘欢迎访问我的博客首页’；
   整个的内容被传递给HttpResponse对象，并返回给浏览器，这一过程由render隐式地完成。
'''
# def index(request):
#     latest_article_list = Article.objects.all()  #这是定义的获取文章列表操作是通过视图函数从数据库中获取文章列表
#     # context = {'latest_article_list':latest_article_list}
#     return  render(request,'blog/index.html',context={'title':'我的博客首页',
#                                                       'welcome':'欢迎访问我的博客首页',
#                                                       'latest_article_list':latest_article_list})
#
#     # return HttpResponse('欢迎访问我的博客首页！')


''' 02
    书写获取文章内容函数
    这里的detail()视图函数用到了Python的markdown模块，同时需要在虚拟环境下安装Pygment，
    用于高亮显示，如CSDN中的博客代码显示
'''

# def detail(request,pk):
#     article = get_object_or_404(Article,pk=pk) #从数据库中获取文章
#     '''定义阅读量自增
#         一旦用户点击了文章详细，即detail()视图函数一旦被调用，说明该文章被访问一次
#         调用Article数据模型中increase_views_num方法，实现views_num自增
#     '''
    # article.increase_views_num()
    #
    # article.content = markdown.markdown(article.content,
    #                                     extensions=[
    #                                         'markdown.extensions.extra',
    #                                         'markdown.extensions.codehilite',
    #                                         'markdown.extensions.toc',
    #                                     ])
    #
    # form = CommentForm()
    # comment_list = article.comment_set.all()
    # context = {'article': article,
    #            'form': form,
    #            'comment_list': comment_list
    #            }
    # return render(request, 'blog/detail.html', context=context)



'''03
    显示某个归档日期下的文章列表
'''
# def archives(request,year,month):
#     article_list = Article.objects.filter(pub_date__year = year,
#                                           pub_date__month = month)
#     return render(request,'blog/index.html',context={'article_list':article_list})


'''04
    书写分类页面d的视图函数
'''
# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     article_list = Article.objects.filter(category=cate) #这里传递的pk在base.html模板中定义的是categort.pk，即过滤出该类别下的文章列表
#     return render(request,'blog/index.html',context={'article_list':article_list})

'''05书写指定标签下文章列表视图函数
'''

'''从上面的视图函数可以看出，它们在处理数据对象时的方法非常类似，先从数据库中抽取数据，然后交给渲染模板。
    Django用基于类的通用视图函数来定义取代这些重复的部分
'''


class IndexView(ListView):
    model = Article  #指定要获取数据列表的数据模型
    template_name = 'blog/index.html'     #指定视图函数所渲染的模板
    context_object_name = 'latest_article_list'
    paginate_by = 3 #在类视图ListView中已经帮我们写好了分页逻辑，只需要在类视图中指定属性值就好

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs) #获得父类生成的并传递给模板的字典
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')#如果总的文章数量小于每页要展示的文章数量，那么不需要分页，该布尔值为False

        pagination_data = self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)
        return context

    #定义如何显示分页
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:  #如果没有分页，则不显示分页导航信息
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = list(paginator.page_range)

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data





class ArchivesView(IndexView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'



class ArticleDetailView(DetailView):
    #这里的属性与ListView属性相同
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self,request,*args,**kwargs):
        # 这里只有重写get方法才能调用increase_views_num()方法
        response = super(ArticleDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views_num()
        #视图函数必须有返回值
        return response


    #编写get_object()方法的目的是需要对article的content值进行渲染
    def get_object(self, queryset=None):
        article = super(ArticleDetailView,self).get_object(queryset=None)

        #实例化一个markdown.markdown类，并传入参数
        md = markdown.Markdown(extensions=[
                                'markdown.extensions.extra',      # 转换html结构文本
                                'markdown.extensions.codehilite', #高亮标记代码
                                TocExtension(slugify=slugify),        #自动生成文章目录
                               ])
        article.content = md.convert(article.content)    #利用实例方法convert()将文章内容渲染成HTML文本
        article.toc = md.toc                             #给文章添加目录
        return article


    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context



class CategoryView(IndexView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name =  'article_list'

    '''由于上面的CategoryView类视图获取的是该数据模型下所有的列表，
        但是为了获取指定分类下的文章列表，我们需要重写父类的get_queryset()方法
    '''
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk')) #得到指定分类
        return super(CategoryView,self).get_queryset().filter(category=cate)


class TagView(IndexView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tag=tag)