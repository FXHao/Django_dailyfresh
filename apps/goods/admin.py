from django.contrib import admin
from .models import *
# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    '''修改页面重新生成静态页面'''

    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据调用'''
        super().save_model(request, obj, form, change)

        # 发出任务，让celery work而重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        # cache.delete('index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据时'''
        super().delete_model(request, obj)

        # 发出任务，让celery work而重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        # cache.delete('index_page_data')


# 内容一样，直接继承就好了
class GoodsTypeAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass


class GoodsSKUAdmin(BaseModelAdmin):
    pass


admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(GoodsSKU, GoodsTypeAdmin)
