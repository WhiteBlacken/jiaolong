from django.contrib import admin

# Register your models here.
from teng.models import Supplier, Keyword, Keyword_cn, Keyword_en, Subbusiness


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_cn', 'name_en']
    search_fields = ['id', 'name_cn', 'name_en']


admin.site.site_header = '椒龙数码数据录入平台'


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['id', 'chinese_keyword', 'english_keyword', 'status']
    search_fields = ['id', 'chinese_keyword', 'english_keyword']
    list_per_page = 20
    actions_on_top = []

    # def get_form(self, request, obj,change):
    #     print("get_form is running")

    # def get_inline_instances(self, request, obj):
    #     print("get inline instance is running")
    # def save_form(self, request, form, change):
    #     print("save_form")
    #     # print(form)
    #     chinese_word = request.POST.get('chinese_keyword', '')
    #     english_word = request.POST.get('english_keyword', '')
    #     status = request.POST.get('status', 0)
    #     similarSet = request.POST.get('similar_set', 0)
    #     comment = request.POST.get('comment', '')
    #     subbuiness = request.POST.get('subbusiness', '')
    #
    #     keyword = Keyword()
    #     keyword.chinese_keyword = chinese_word
    #     keyword.english_keyword = english_word
    #     keyword.status = status
    #     keyword.similar_set = similarSet
    #     keyword.comment = comment
    #     keyword.subbusiness_id = subbuiness
    #
    #     cWord = Keyword.objects.filter(chinese_keyword=chinese_word)
    #     eWord = Keyword.objects.filter(english_keyword=english_word)
    #
    #     if not any(cWord) and not any(eWord):
    #         print("正常保存")
    #         return form.save(commit=False)
    #     if any(cWord) and any(eWord):
    #         print("正常的保存失败")
    #         if cWord.first().english_keyword == eWord.first().english_keyword:
    #             return form.save(commit=False)
    #     if any(cWord):
    #         print("添加到en表")
    #         keyword_en = Keyword_en()
    #         keyword_en.english_keyword = english_word
    #         keyword_en.subbusiness = Subbusiness.objects.get(id=subbuiness)
    #         keyword_en.keyword = cWord.first()
    #         # keyword_en.keyword = keywords.first()
    #         keyword_en.comment = "测试数据"
    #         keyword_en.save()
    #         return form.save(commit=False)
    #     if any(eWord):
    #         print("添加到cn表")
    #         keyword_cn = Keyword_cn()
    #         keyword_cn.chinese_keyword = chinese_word
    #         keyword_cn.subbusiness = Subbusiness.objects.get(id=subbuiness)
    #         keyword_cn.keyword = eWord.first()
    #         # keyword_cn.keyword =keywords.first()
    #         keyword_cn.comment = "测试数据"
    #         keyword_cn.save()
    #         return form.save(commit=False)



    # 参数不可以改
    # def save_model(self, request, obj, form, change):
    #     print("自定义save_model执行ing")
    #     cWord = obj.chinese_keyword
    #     eWord = obj.english_keyword
    #     cWordResult = Keyword.objects.filter(chinese_keyword=cWord)
    #     eWordResult = Keyword.objects.filter(english_keyword=eWord)
    #     # 中英文均不重复,直接插入
    #     if not any(cWordResult) and not any(eWordResult):
    #         # 记录下操作人
    #         print("直接插入")
    #         obj.operator = request.user.username
    #         obj.author = request.user
    #         super().save_model(request, obj, form, change)
    #         return
    #     if any(eWordResult):
    #         print("英文重复，故加入中文同义词")
    #         keyword_cn = Keyword_cn()
    #         keyword_cn.chinese_keyword = cWord
    #         keyword_cn.subbusiness = obj.subbusiness
    #         keyword_cn.keyword = obj
    #         keyword_cn.comment = "重复字段"
    #         keyword_cn.save()
    #
    #         return
    #     if any(cWordResult) :
    #         print("中文重复，故加入英文同义词")
    #         keyword_en = Keyword_en()
    #         keyword_en.english_keyword = eWord
    #         keyword_en.subbusiness = obj.subbusiness
    #         keyword_en.keyword = obj
    #         keyword_en = "重复字段"
    #         keyword_en.save()
    #
    #         return
    #     # 实际上虽然是filter但是最多返回一条数据
    #     # 此分支之前，已经讨论了为空的几种情况，此处先直接插入，系统报错
    #     obj.operator = request.user.username
    #     obj.author = request.user
    #     super().save_model(request, obj, form, change)
    #     print("执行3")
    #     # 下面两句不可以改
    #     # obj.author = request.user
    #     # super().save_model(request, obj, form, change)
    #     print("两者同时重复，还要判断是否是相同对象")


class Keyword_cnAdmin(admin.ModelAdmin):
    list_display = ['id', 'chinese_keyword', 'keyword']
    search_fields = ['id', 'chinese_keyword', 'keyword']
    list_per_page = 20
    # actions_on_top = []


class Keyword_enAdmin(admin.ModelAdmin):
    list_display = ['id', 'english_keyword', 'keyword']
    search_fields = ['id', 'english_keyword', 'keyword']
    list_per_page = 20
    # actions_on_top = []


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Keyword_cn, Keyword_cnAdmin)
admin.site.register(Keyword_en, Keyword_enAdmin)
