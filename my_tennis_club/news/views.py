from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    all_news = News.objects.all().order_by('-published_date')
    return render(request, 'news_list.html', {'news': all_news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news_item': news_item})
