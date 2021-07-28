from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User, Group
from teng.models import Business, Subbusiness, Supplier, Keyword, Keyword_en, Keyword_cn


# 取供应商数量最多的前N个分类
def findSupplierTopNCate(num):
    cnt = Supplier.objects.all().count()
    if cnt < num:
        num = cnt
    business = Business.objects.all()
    for bus in business:
        bus.count = 0
        for sub in bus.subbusiness_set.all():
            bus.count = bus.count + sub.supplier_set.count()

    topN = []

    tmp = Business()
    for i in range(num):
        maxc = 0
        for bus in business:
            if bus.count > maxc:
                maxc = bus.count
                tmp = bus
        tmp.count = 0
        print(tmp, maxc)
        topN.append(tmp)
    return topN


# 取供应商被搜索最多的二级分类,#并查找对应的最高访问供应商
def findSupplierSearchTopNSubCate(nums):
    cnt = Subbusiness.objects.all().count()
    print("sub数量：")
    print(cnt)
    if cnt < nums:
        nums = cnt
    print("num数量:")
    print(nums)
    subbusiness = Subbusiness.objects.all()
    for sub in subbusiness:
        sub.count = 0
        for supply in sub.supplier_set.all():
            sub.count = sub.count + supply.visited_times

    topN = []
    num = 1
    tmp = Subbusiness()
    for i in range(nums):
        maxc = 0
        for subbus in subbusiness:
            if subbus.count > maxc:
                maxc = subbus.count
                tmp = subbus
        if tmp.count == 0:
            break
        tmp.count = 0
        print("nowLocal:")
        print(tmp, maxc)
        tmp.num = num
        num = num + 1
        print("num:")
        print(num)
        supply_set = tmp.supplier_set.order_by('-visited_times')
        # 要考虑是否有超过3个
        tmp.top_supply_list = []
        q = supply_set.count()
        if q > 3:
            q = 3
        for j in range(q):
            tmp.top_supply_list.append(supply_set[j])
        topN.append(tmp)
    return topN


# 取访问次数最多的N个分类
def findVisitTopNSupplier(nums):
    cnt = Supplier.objects.all().count()
    if cnt < nums:
        nums = cnt
    supplierList = Supplier.objects.order_by('-visited_times')[0:nums]
    num = 1
    for supplier in supplierList:
        supplier.num = num
        num = num + 1
    return supplierList


# 取信誉最好的N个供应商
def findCreditTopNSupplier(num):
    cnt = Supplier.objects.all().count()
    if cnt < num:
        num = cnt
    supplierList = Supplier.objects.order_by('-credit')[0:num]
    return supplierList


# 取成立时间最久的N个供应商
def findCreateDateTopNSupplier(num):
    cnt = Supplier.objects.all().count()
    num = 1
    if cnt < num:
        num = cnt
    supplierList = Supplier.objects.order_by('created_date')[0:num]
    for sup in supplierList:
        sup.num = num
        num = num + 1
    return supplierList


# 身份认证
def userVisitContro(request):
    pass


# 每页都查分类
def getCommomCate():
    context = {}
    # 获取分类及所有二级分类进行填充
    allSub = []
    allBusiness = Business.objects.all()
    for business in allBusiness:
        business.listSub = business.subbusiness_set
        for sub in business.listSub.all():
            allSub.append(sub)
    context['allBusiness'] = allBusiness
    context['allSub'] = allSub

    return context


# 判断用户的登录状态
def judgeUserLevel(request):
    username = request.session.get('username', '')
    if not username:
        return 0
    user = User.objects.get(username=username)
    group_name = Group.objects.filter(user=user).first().name
    if group_name == 'member':
        return 2
    else:
        return 1


# 提取获取结果列表的公共部分(结果显示)
def getCommomPageData(request, suppliers):
    context = getCommomCate()
    # 分页
    page = request.GET.get('page', 1)
    # 会员非会员能看到的数据不一样 test：会员：全部  非会员：2条
    userLevel = judgeUserLevel(request)
    if userLevel == 2:
        paginator = Paginator(suppliers, 4)
        page_data = paginator.page(page)
    else:
        paginator = Paginator(suppliers[:2], 4)
        page_data = paginator.page(page)
    context['paginator'] = paginator
    context['page_data'] = page_data
    return context


# 首页
def index(request):
    # test

    context = getCommomCate()
    # 取供应商数量最多前三个大分类
    # business = Business.objects.all()
    # showBusiness = business[0:3]
    showBusiness = findSupplierTopNCate(3)
    showBus0 = showBusiness[0]
    supplier0 = []
    count0 = 0
    for subbus in showBus0.subbusiness_set.all():
        for j in Supplier.objects.filter(categories=subbus):
            supplier0.append(j)
            count0 = count0 + 1
            if count0 == 10:
                break
    context['showBus0'] = showBus0
    context['supplier0'] = supplier0

    showBus1 = showBusiness[1]
    supplier1 = []
    count1 = 0
    for subbus in showBus1.subbusiness_set.all():
        for j in Supplier.objects.filter(categories=subbus):
            supplier1.append(j)
            count1 = count1 + 1
            if count1 == 10:
                break
    context['showBus1'] = showBus1
    context['supplier1'] = supplier1

    showBus2 = showBusiness[2]
    supplier2 = []
    count2 = 0
    for subbus in showBus2.subbusiness_set.all():
        for j in Supplier.objects.filter(categories=subbus):
            supplier2.append(j)
            count2 = count2 + 1
            if count2 == 10:
                break
    context['showBus2'] = showBus2
    context['supplier2'] = supplier2
    # 取访问量最高的5个供应商
    topNVisitSupplier = findVisitTopNSupplier(5)
    context['topNVisitSupplier'] = topNVisitSupplier
    print("topNVisitSupplier.num:")
    print(topNVisitSupplier[1].num)
    # 取信誉最好的4个供应商
    topNCreditSupplier = findCreditTopNSupplier(4)
    context['topNCreditSupplier'] = topNCreditSupplier
    # 取成立时间最久的3个供应商
    topNCreateDateSupplier = findCreateDateTopNSupplier(3)
    context['topNCreateDateSupplier'] = topNCreateDateSupplier
    print("topNCreateDateSupplier:")
    print(topNCreateDateSupplier)
    # 填充热门推荐栏，需要热门（二级）8个，以及对应热门供应商3个
    supplierSearchTopNSubCate = findSupplierSearchTopNSubCate(8)
    context['supplierSearchTopNSubCate'] = supplierSearchTopNSubCate
    return render(request, 'teng/index.html', {'context': context})


# 点击一级分类返回结果
def suppliers_with_business(request, id):
    # 查询出当前business分类下所有的supplier
    nowBusiness = Business.objects.get(id=id)
    suppliers = []
    for subbusiness in nowBusiness.subbusiness_set.all():
        supplier_list = Supplier.objects.filter(categories=subbusiness).order_by('id')
        if supplier_list:
            for list in supplier_list:
                suppliers.append(list)
    context = getCommomPageData(request, suppliers)
    context['nowBusiness'] = nowBusiness
    return render(request, 'teng/cateOneSearchResult.html', {'context': context})


# 点击二级分类返回结果
def suppliers_with_subbusiness(request, id):
    # 查询出当前subbusiness分类下所有的supplier
    nowSubbusiness = Subbusiness.objects.get(id=id)
    nowBusiness = Business.objects.get(id=nowSubbusiness.parent_id)
    suppliers = Supplier.objects.filter(categories=nowSubbusiness)

    context = getCommomPageData(request, suppliers)
    context['nowBusiness'] = nowBusiness
    context['nowSubbusiness'] = nowSubbusiness
    return render(request, 'teng/cateTwoSearchResult.html', {'context': context})


# 搜索关键词返回结果
def search_by_keyword(request):
    context = getCommomCate()
    # 拿到post中提交的分类值和关键词
    businessId = request.POST.get('search_category', 1)
    searchText = request.POST.get('search_text', '')
    page = request.GET.get('page', 1)
    print('option value is ' + businessId + ' searchText is ' + searchText)
    # 通过关键词去查找内容（通过分类值进行限制） 要修改，仅作为test
    # get返回值的数量只能为1，为空或者>=2都会报错
    keyword = Keyword.objects.filter(chinese_keyword=searchText)
    # pro:怎么判断keyword（集合）是否为空
    paginator = []
    page_data = []
    # 这边要再改掉，能和前面进行复合
    if keyword:
        suppliers = Supplier.objects.filter(categories=keyword[0].subbusiness).order_by('id')
        # 分页
        # 会员非会员能看到的数据不一样 test：会员：全部  非会员：2条

        userLevel = judgeUserLevel(request)
        if userLevel == 0:
            return HttpResponse('请先登录')
        if userLevel == 2:
            paginator = Paginator(suppliers, 4)
            page_data = paginator.page(page)
        else:
            paginator = Paginator(suppliers[:2], 4)
            page_data = paginator.page(page)
    # 前三条测试后看是否要删掉
    # context['keyword'] = keyword
    # context['searchText'] = searchText
    # context['businessId'] = businessId
    context['paginator'] = paginator
    context['page_data'] = page_data
    return render(request, 'teng/keywordSearchResult.html',
                  {'context': context})


def quick_view(request, id):
    supply = Supplier.objects.get(id=id)

    return render(request, "teng/example.html", {'supply': supply})


def start(request):
    return HttpResponse("this is start")


def test(request):
    allBuniess = Business.objects.all()
    allSubbuniess = []
    for bus in allBuniess:
        for subbus in bus.subbusiness_set.all():
            allSubbuniess.append(subbus)
    return render(request, "testForm.html", {'allSubbuniess': allSubbuniess})


def testFinished(request):
    chinese_word = request.POST.get('chinese_keyword', '')
    english_word = request.POST.get('english_keyword', '')
    status = request.POST.get('status', 0)
    similarSet = request.POST.get('similar set', 0)
    comment = request.POST.get('comment', '')
    subbuiness = request.POST.get('subbusiness', '')
    keyword = Keyword()
    keyword.chinese_keyword = chinese_word
    keyword.english_keyword = english_word
    keyword.status = status
    keyword.similar_set = similarSet
    keyword.comment = comment
    keyword.subbusiness_id = subbuiness

    cWord = Keyword.objects.filter(chinese_keyword=chinese_word)
    eWord = Keyword.objects.filter(english_keyword=english_word)

    if not any(cWord) and not any(eWord):
        keyword.save()
        return HttpResponse("chinese_word:" + chinese_word + " status:" + status + " subbuiness:" + subbuiness)
    if any(cWord) and any(eWord):
        if cWord.first().english_keyword == eWord.first().english_keyword:
            return HttpResponse("chinese_word:" + chinese_word + " status:" + status + " subbuiness:" + subbuiness)
    if any(cWord):
        keyword_en = Keyword_en()
        keyword_en.english_keyword = english_word
        keyword_en.subbusiness = Subbusiness.objects.get(id=subbuiness)
        keyword_en.keyword = cWord.first()
        # keyword_en.keyword = keywords.first()
        keyword_en.comment = "测试数据"
        keyword_en.save()
        return HttpResponse("chinese_word:" + chinese_word + " status:" + status + " subbuiness:" + subbuiness)
    if any(eWord):
        keyword_cn = Keyword_cn()
        keyword_cn.chinese_keyword = chinese_word
        keyword_cn.subbusiness = Subbusiness.objects.get(id=subbuiness)
        keyword_cn.keyword = eWord.first()
        # keyword_cn.keyword =keywords.first()
        keyword_cn.comment = "测试数据"
        keyword_cn.save()
        return HttpResponse("chinese_word:" + chinese_word + " status:" + status + " subbuiness:" + subbuiness)

    # return HttpResponse("chinese_word:"+chinese_word+" status:"+status+" subbuiness:"+subbuiness)
