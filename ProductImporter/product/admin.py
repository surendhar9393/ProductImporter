from .models import ProductUploader, Product
from django.contrib import messages, admin


class ProductUploaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_by', 'created_date', 'link', 'started_at', 'completed_at',)
    readonly_fields = ('status',)
    fields = ('link', 'status',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.created_by = request.user

            super().save_model(request, obj, form, change)


admin.site.register(ProductUploader, ProductUploaderAdmin)


def delete_all_product(modeladmin, request, queryset):
    Product.objects.all().delete()
    messages.error(request, 'Products deleted Successfully')
    return True


class ProductAdmin(admin.ModelAdmin):
    fields = ('name',)
    search_fields = ("sku",)
    list_filter = ('is_active',)
    list_display = ('id', 'name', 'sku', 'is_active', 'description', 'batch', 'created_date',)

    actions = [delete_all_product]

    def my_action(modeladmin, request, queryset):
        pass

    my_action.short_description = "Act on all %(verbose_name_plural)s"
    my_action.acts_on_all = True

    def changelist_view(self, request, extra_context=None):
        actions = self.get_actions(request)
        if actions:
            data = request.POST.copy()
            print("opd---")
            data['select_across'] = '1'
            request.POST = data
            response = self.response_action(request, queryset=self.get_queryset(request))
            if response:
                return response
        return super(ProductAdmin, self).changelist_view(request, extra_context)


admin.site.register(Product, ProductAdmin)
