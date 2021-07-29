from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from teng.models import Keyword, Keyword_en, Subbusiness, Keyword_cn, Business, Supplier


# 0. 工具类
# 0.1 用户身份验证
def UserVisitContr(request):
    # admin中的每个页面都需要审核用户身份
    username = request.session.get('username', '')
    if not username:
        return HttpResponse('请先登录')
    else:
        user = User.objects.filter(username=username).first()
        if Group.objects.filter(user=user) != 'DataEntryClerk':
            return HttpResponse('权限不足')


# 0.2 分页展示（共同）（输入数据获得分页数据）
def get_commom_page(request, object):
    # 分页展示
    context = {}
    page = request.GET.get('page', 1)
    paginator = Paginator(object, 4)
    page_data = paginator.get_page(page)
    context['paginator'] = paginator
    context['page_data'] = page_data
    # 分页优化
    i = page_data.number
    page_range = list(range(max(i - 2, 1), i)) + \
                 list(range(i, min(i + 2, paginator.num_pages) + 1))
    # 加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首尾
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context['page_range'] = page_range
    return context


# 1. 首页
def index(request):
    return render(request, 'myAdmin/index.html')


# 2. 供应商操作
# 2.1 分页展示供应商列表
def show_supply_table(request):
    suppliers = Supplier.objects.all()
    context = get_commom_page(request, suppliers)
    return render(request, 'myAdmin/supply_list.html', {'context': context})


# 2.2 删除指定id供应商
def delete_supplier(request, id):
    Supplier.objects.filter(id=id).delete()
    return redirect('show_supply_table')


# 2.3 去编辑指定id供应商信息页面
def go_edit_supplier(request, id):
    context = {}
    supplier = Supplier.objects.get(id=id)
    context['supplier'] = supplier
    # 切割并展示关键词
    keywordCollection = supplier.keywords_collected
    keyList = keywordCollection.split(",")
    supplier.keyList = keyList
    return render(request, 'myAdmin/go_edit_supply.html', {'context': context})

# 2.4 对供应商进行更新
def update_supplier(request):
    # 分页展示
    suppliers = Supplier.objects.all()
    context = get_commom_page(request, suppliers)

    supplier = Supplier.objects.get(id=request.POST.get('id'))
    keyList = request.POST.getlist('keywordpicker','')
    keyListStr = ''
    for p in keyList:
        keyListStr = keyListStr + p +','
    supplier.keywords_collected = keyListStr[:-1]
    print("")
    supplier.save()
    return render(request, 'myAdmin/supply_list.html', {'context': context})

# 3. 关键词操作（主关键词）
# 3.1 分页展示关键词列表
def show_keyword_table(request):
    keywords = Keyword.objects.all().order_by('-create_time')
    context = get_commom_page(request, keywords)
    return render(request, 'myAdmin/keyword_list.html', {'context': context})


# 3.2 删除指定id关键词
def delete_keyword(request, id):
    Keyword.objects.filter(id=id).delete()
    return redirect('show_keyword_table')


# 3.3 去添加关键词页面
def go_add_keyword(request):
    context = {}
    allCate = []
    for bus in Business.objects.all():
        for subbus in bus.subbusiness_set.all():
            allCate.append(subbus)
    context['allCate'] = allCate
    return render(request, 'myAdmin/go_add_keyword.html', {'context': context})


# 3.4 去编辑关键词页面
def go_edit_keyword(request, id):
    context = {}
    keyword = Keyword.objects.get(id=id)
    context['keyword'] = keyword
    allCate = []
    for bus in Business.objects.all():
        for subbus in bus.subbusiness_set.all():
            allCate.append(subbus)
    context['allCate'] = allCate
    return render(request, 'myAdmin/go_edit_keyword.html', {'context': context})


# 3.5 添加关键词
def add_keyword(request):
    #
    keywords = Keyword.objects.all().order_by('-create_time')
    context = get_commom_page(request, keywords)

    keyword = Keyword()

    keyword_cn = request.POST.get('keyword_cn')
    keyword_en = request.POST.get('keyword_en')
    status = request.POST.get('status')
    similar_set = request.POST.get('similar_set')
    comment = request.POST.get('comment')
    subbus = request.POST.get('subbus')

    keyword.chinese_keyword = keyword_cn
    keyword.english_keyword = keyword_en
    keyword.status = status
    keyword.similar_set = similar_set
    keyword.comment = comment
    keyword.subbusiness_id = subbus

    # 在save之前要考虑什么问题？
    # 看看中文关键词字段有无重复的，如果有重复的加入英文关键词
    cnt_cn = Keyword.objects.filter(chinese_keyword=keyword_cn).count()
    if cnt_cn > 0:
        keyword_tmp = Keyword.objects.get(chinese_keyword=keyword_cn)
        if keyword_tmp.english_keyword != keyword_en:
            keyword_simlar_en = Keyword_en()
            keyword_simlar_en.english_keyword = keyword_en
            keyword_simlar_en.subbusiness_id = subbus
            keyword_simlar_en.keyword = keyword_tmp
            keyword_simlar_en.comment = comment
            keyword_simlar_en.save()
            # return render(request, 'myAdmin/keyword_list.html', {'context': context})
            return redirect('show_keyword_similar_en_table')
        else:
            return render(request, 'myAdmin/keyword_list.html', {'context': context})
    # 看看英文关键词字段有无重复的
    cnt_en = Keyword.objects.filter(english_keyword=keyword_en).count()
    if cnt_en > 0:
        keyword_tmp = Keyword.objects.get(english_keyword=keyword_en)
        if keyword_tmp.chinese_keyword != keyword_cn:
            keyword_simlar_en = Keyword_cn()
            keyword_simlar_en.chinese_keyword = keyword_cn
            keyword_simlar_en.subbusiness_id = subbus
            keyword_simlar_en.keyword = keyword_tmp
            keyword_simlar_en.comment = comment
            keyword_simlar_en.save()
            # return render(request, 'myAdmin/keyword_list.html', {'context': context})
            return redirect('show_keyword_similar_cn_table')
    keyword.save()
    return render(request, 'myAdmin/keyword_list.html', {'context': context})


# 3.6 编辑关键词
def update_keyword(request):
    keywords = Keyword.objects.all().order_by('-create_time')
    context = get_commom_page(request, keywords)

    id = request.POST.get('id')
    keyword_cn = request.POST.get('keyword_cn')
    keyword_en = request.POST.get('keyword_en')
    status = request.POST.get('status')
    similar_set = request.POST.get('similar_set')
    comment = request.POST.get('comment')
    subbus = request.POST.get('subbus')

    # 更新要考虑什么问题
    # 字段还是不可以重复：修改后的与其他重复，因为没修改而与原先重复（数据库中的数据还没改变）
    # 那是否可以先进行一步判断，如果中英关键词都没改，直接保存即可
    keyword = Keyword.objects.get(id=id)
    isChangeCN = 0
    isChangeEN = 0

    if keyword_cn != keyword.chinese_keyword:
        isChangeCN = 1
    if keyword_en != keyword.english_keyword:
        isChangeEN = 1

    if isChangeCN == 1 and isChangeEN == 0:  # 中文关键词改了，有可能被加入英文同义关键词
        cnt_cn = Keyword.objects.filter(chinese_keyword=keyword_cn).count()
        if cnt_cn > 0:
            keyword_tmp = Keyword.objects.get(chinese_keyword=keyword_cn)
            keyword_simlar_en = Keyword_en()
            keyword_simlar_en.english_keyword = keyword_en
            keyword_simlar_en.subbusiness_id = subbus
            keyword_simlar_en.keyword = keyword_tmp
            keyword_simlar_en.comment = comment
            keyword_simlar_en.save()
            keyword.delete()
            # return render(request, 'myAdmin/keyword_list.html', {'context': context})
            return redirect('show_keyword_similar_en_table')
    if isChangeCN == 0 and isChangeEN == 1:  # 英文关键词改了，有可能被加入中文同义关键词
        cnt_en = Keyword.objects.filter(english_keyword=keyword_en).count()
        if cnt_en > 0:
            keyword_tmp = Keyword.objects.get(english_keyword=keyword_en)
            keyword_simlar_en = Keyword_cn()
            keyword_simlar_en.chinese_keyword = keyword_cn
            keyword_simlar_en.subbusiness_id = subbus
            keyword_simlar_en.keyword = keyword_tmp
            keyword_simlar_en.comment = comment
            keyword_simlar_en.save()
            keyword.delete()
            # return render(request, 'myAdmin/keyword_list.html', {'context': context})
            return redirect('show_keyword_similar_cn_table')
    if isChangeCN == 1 and isChangeEN == 1:
        cnt_cn = Keyword.objects.filter(chinese_keyword=keyword_cn).count()
        if cnt_cn > 0:
            keyword_tmp = Keyword.objects.get(chinese_keyword=keyword_cn)
            if keyword_tmp.english_keyword != keyword_en:
                keyword_simlar_en = Keyword_en()
                keyword_simlar_en.english_keyword = keyword_en
                keyword_simlar_en.subbusiness_id = subbus
                keyword_simlar_en.keyword = keyword_tmp
                keyword_simlar_en.comment = comment
                keyword_simlar_en.save()
                keyword.delete()
                # return render(request, 'myAdmin/keyword_list.html', {'context': context})
                return redirect('show_keyword_similar_en_table')
            else:
                keyword.delete()
                return render(request, 'myAdmin/keyword_list.html', {'context': context})
        # 看看英文关键词字段有无重复的
        cnt_en = Keyword.objects.filter(english_keyword=keyword_en).count()
        if cnt_en > 0:
            keyword_tmp = Keyword.objects.get(english_keyword=keyword_en)
            if keyword_tmp.chinese_keyword != keyword_cn:
                keyword_simlar_en = Keyword_cn()
                keyword_simlar_en.chinese_keyword = keyword_cn
                keyword_simlar_en.subbusiness_id = subbus
                keyword_simlar_en.keyword = keyword_tmp
                keyword_simlar_en.comment = comment
                keyword_simlar_en.save()
                keyword.delete()
                # return render(request, 'myAdmin/keyword_list.html', {'context': context})
                return redirect('show_keyword_similar_cn_table')
    keyword.chinese_keyword = keyword_cn
    keyword.english_keyword = keyword_en
    keyword.status = status
    keyword.similar_set = similar_set
    keyword.comment = comment
    keyword.subbus = subbus
    keyword.save()
    return render(request, 'myAdmin/keyword_list.html', {'context': context})


# 3.7 放弃添加或编辑关键词
# 放弃按钮（edit和add共用一个）
def unsave_keyword(request):
    return redirect('show_keyword_table')

# 3.8 查看主关键词
def go_view_keyword(request,id):
    context = {}
    keyword = Keyword.objects.get(id=id)
    context['keyword'] = keyword
    allCate = []
    for bus in Business.objects.all():
        for subbus in bus.subbusiness_set.all():
            allCate.append(subbus)
    context['allCate'] = allCate
    return render(request,'myAdmin/go_view_keyword.html',{'context':context})

# 4. 中文/英文关键词同义词
# 4.1 展示列表
# 中
def show_keyword_similar_cn_table(request):
    keyword_cn = Keyword_cn.objects.all().order_by('-id')
    context = get_commom_page(request, keyword_cn)
    return render(request, 'myAdmin/keyword_cn_list.html', {'context': context})


# 英
def show_keyword_similar_en_table(request):
    keyword_en = Keyword_en.objects.all().order_by('-id')
    context = get_commom_page(request, keyword_en)
    return render(request, 'myAdmin/keyword_en_list.html', {'context': context})


# 4.2 删除
# 中
def delete_keyword_cn(request, id):
    Keyword_cn.objects.filter(id=id).delete()
    return redirect('show_keyword_similar_cn_table')


# 英
def delete_keyword_en(request, id):
    Keyword_en.objects.filter(id=id).delete()
    return redirect('show_keyword_similar_en_table')


# 4.3 去编辑页面
# 中
def go_edit_keyword_cn(request, id):
    context = {}
    keyword = Keyword_cn.objects.get(id=id)
    context['keyword'] = keyword
    allCate = []
    for bus in Business.objects.all():
        for subbus in bus.subbusiness_set.all():
            allCate.append(subbus)
    context['allCate'] = allCate
    return render(request, 'myAdmin/go_edit_keyword_cn.html', {'context': context})


# 英
def go_edit_keyword_en(request, id):
    context = {}
    keyword = Keyword_en.objects.get(id=id)
    context['keyword'] = keyword
    allCate = []
    for bus in Business.objects.all():
        for subbus in bus.subbusiness_set.all():
            allCate.append(subbus)
    context['allCate'] = allCate
    return render(request, 'myAdmin/go_edit_keyword_en.html', {'context': context})


# 4.4 放弃 编辑或新增 按钮
# 中
def unsave_keyword_cn(request):
    return redirect('show_keyword_similar_cn_table')


# 英
def unsave_keyword_en(request):
    return redirect('show_keyword_similar_en_table')


