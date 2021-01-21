from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Item

# Create your views here.
def get_dict_item(item):
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "image": item.image.url,
        "weight": item.weight,
        "price": item.price,
    }


def get_item_by_id(req, id):
    item = get_object_or_404(Item, pk=id)
    return JsonResponse(get_dict_item(item))
