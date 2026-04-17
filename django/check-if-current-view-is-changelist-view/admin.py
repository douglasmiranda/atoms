# There are many ways to do it, like checking if "change" is in the current url path
# you can adapt to check for _changelist, _change, _delete...


def is_changelist_view(model_admin_instance, request):
    """
    Verify if the current view is changelist.
    Args:
        model_admin_instance (admin.ModelAdmin): ModelAdmin instance.
        request (HttpRequest): Current request.
    Examples:
        @admin.register(Article)
        class ArticleAdmin(admin.ModelAdmin):
            def get_queryset(self, request):
                if is_changelist_view(self, request):
                    return queryset.only("title")
    """
    opts = model_admin_instance.opts
    url_name = request.resolver_match.url_name
    return url_name == f"{opts.app_label}_{opts.model_name}_changelist"
