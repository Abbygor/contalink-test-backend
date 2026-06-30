from datetime import datetime

from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.invoices.api.cache import (
    build_cache_key,
    get_cached_response,
    set_cached_response,
)
from apps.invoices.api.serializers import InvoiceSerializer
from apps.invoices.services import get_invoices_by_date_range


class InvoiceListView(APIView):
    def get(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            return Response(
                status=400,
                data={
                    "error": "start_date and end_date are required (format YYYY-MM-DD)"
                },
            )

        try:
            start_date = timezone.make_aware(
                datetime.strptime(start_date_str, "%Y-%m-%d")
            )
            end_date = timezone.make_aware(
                datetime.strptime(end_date_str, "%Y-%m-%d").replace(
                    hour=23, minute=59, second=59
                )
            )
        except ValueError:
            return Response(
                status=400,
                data={"error": "Invalid date format. Use YYYY-MM-DD"},
            )

        if start_date > end_date:
            return Response(
                status=400,
                data={"error": "start_date cannot be greater than end_date"},
            )

        cache_key = build_cache_key(query_params=dict(request.query_params))
        cached = get_cached_response(cache_key=cache_key)
        if cached is not None:
            return Response(cached)

        invoices = get_invoices_by_date_range(start_date=start_date, end_date=end_date)

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(invoices, request)
        serializer = InvoiceSerializer(page, many=True)
        respose_data = paginator.get_paginated_response(serializer.data).data

        set_cached_response(cache_key=cache_key, response_data=respose_data)

        return Response(respose_data)
