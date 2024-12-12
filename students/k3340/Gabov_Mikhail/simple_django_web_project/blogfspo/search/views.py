from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.shortcuts import render
from app.models import Car, Owner

class ESearchView(View):
    template_name = 'search/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        query = request.GET.get('q')

        if query:
            cars = Car.objects.filter(brand__icontains=query)
            owners = Owner.objects.filter(first_name__icontains=query)


            results = list(cars) + list(owners)

            # Пагинация
            paginator = Paginator(results, 10)
            page = request.GET.get('page')

            try:
                context['results'] = paginator.page(page)
            except PageNotAnInteger:
                context['results'] = paginator.page(1)
            except EmptyPage:
                context['results'] = paginator.page(paginator.num_pages)

            context['query'] = query

        return render(request, self.template_name, context)
