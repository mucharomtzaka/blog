from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# pagination lib 
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


# Create your views here.
from django.views import generic
from .models import Post


from blog.models import Document
from blog.forms import DocumentForm


class PostList(generic.ListView):
    model = Post
   # queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.filter(status=1).order_by('-created_on')
        return object_list
    
    def get_context_data(self, **kwargs):
        ctx = super(PostList, self).get_context_data(**kwargs)
        
        object_list = self.get_queryset()
        
        #query = self.request.GET.get('q')
        #if query:
        #    object_list = self.model.objects.filter(title__icontains=query)
       # else:
            #object_list = self.model.objects.filter(status=1).order_by('-created_on')
        
        
        #postlist = Post.objects.all()
        paginator = Paginator(object_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        ctx['post_list'] = file_exams
        ctx['documents'] = Document.objects.all()
        return ctx
    

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    

    
#function upload  
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DocumentForm()
    return render(request, 'upload_form.html', {
        'form': form
    })
    
