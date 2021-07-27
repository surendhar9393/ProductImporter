from django.contrib import admin
from .models import ProductUploader, Product


class ProductUploaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_by', 'created_date', 'link', 'started_at', 'completed_at',)
    readonly_fields = ('status',)
    fields = ('link', 'status',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.created_by = request.user

            super().save_model(request, obj, form, change)


admin.site.register(ProductUploader, ProductUploaderAdmin)


class ProductAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name', 'sku', 'is_active', 'description', 'batch', 'created_date',)


admin.site.register(Product, ProductAdmin)
