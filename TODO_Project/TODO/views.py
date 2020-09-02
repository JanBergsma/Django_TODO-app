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


class PostView(View):
    def redirect_to_index(self, request):
        if FILTER in request.session:
            return HttpResponseRedirect(
                '?'.join([
                    reverse('TODO:index'),
                    request.session[FILTER]
                ]))
        else:
            return HttpResponseRedirect(reverse('TODO:index'))


class IndexView(View):
    def get(self, request):
        logger.debug(f'IndexView GET {request}')
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


class CreateView(PostView):
    def post(self, request):
        logger.debug(f'CreateView POST {request.POST}')
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

        return self.redirect_to_index(request)


class UpdateView(PostView):
    def post(self, request):
        logger.debug(f'UpdateView POST {request.POST}')
        data = request.POST
        if 'delete' in data:
            return self.delete_item(data, request)
        return self.update_item(data, request)

    def update_item(self, data, request):
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
        return self.redirect_to_index(request)

    def delete_item(self, data, request):
        id = data['id']
        item = get_object_or_404(Item, pk=id)
        item.delete()
        return self.redirect_to_index(request)


class ClearDeletedView(PostView):
    def post(self, request):
        logger.debug(f'ClearDeletedView POST {request.POST}')
        Item.objects.all().filter(completed=True).delete()
        return self.redirect_to_index(request)
