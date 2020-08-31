import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import get_object_or_404

from .models import Item
from .forms import CreateItemForm


logger = logging.getLogger(__name__)

FILTER = 'filter'

class IndexView(View):
    def get(self, request):
        # logger.debug(f'{request}')
        items = Item.objects.all()
        items.order_by('creation_date')
        request.session[FILTER] = 'all'
        if 'active' in request.GET:
            items = items.filter(completed=False)
            request.session[FILTER] = 'active'
        if 'completed' in request.GET:
            items = items.filter(completed=True)
            request.session[FILTER] = 'completed'

        # logger.debug(f'{items}')
        context = {'items': items, 'filter': request.session[FILTER]}
        return render(request, 'TODO/index.html', context)

class CreateView(View):
    def post(self, request):
        logger.debug(f'Post {request.POST}')
        data = request.POST
        title = data['title']
        completed = False
        form = CreateItemForm({'title': title, 'completed': completed})
        if form.is_valid():
            item = Item(title=title, completed=completed)
            item.save()
            logger.debug(f'Item({data}) created')
        else:
            raise Http404
        
        if FILTER in request.session:
            return HttpResponseRedirect(
                '?'.join([
                    reverse('TODO:index'), 
                    request.session[FILTER]
            ]))
        else: 
            return HttpResponseRedirect(reverse('TODO:index'))


class UpdateView(View):
    def post(self, request):
        logger.debug(f'Post {request.POST}')
        data = request.POST
        if 'delete' in data: return self.delete_item(data)
        return self.update_item(data)

    def update_item(self, data):
        id = data['id']
        title = data['title']
        completed = True if 'completed' in data else False
        form = CreateItemForm({'title': title, 'completed': completed})
        if form.is_valid():
            item = get_object_or_404(Item, pk=id)
            item.title = title
            item.completed = completed
            item.save()
            logger.debug(f'Item({data}) created')
        else:
            raise Http404
        return HttpResponseRedirect(reverse('TODO:index'))
        
    def delete_item(self, data):
        id = data['id']
        item = get_object_or_404(Item, pk=id)
        item.delete()
        return HttpResponseRedirect(reverse('TODO:index'))


class ClearDeletedView(View):
    def post(self, request):
        logger.debug(f'Post {request.POST}')
        Item.objects.all().filter(completed=True).delete()
        return HttpResponseRedirect(reverse('TODO:index'))
