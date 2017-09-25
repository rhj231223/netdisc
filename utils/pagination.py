# coding:utf-8

# def pagination(current_page,total_num,single_page_num,show_page):
#     total_page=total_num//single_page_num
#     if total_num%single_page_num:
#         total_page+=1
#
#     start=single_page_num*(current_page-1)
#     end=start+single_page_num
#
#     pre_page=current_page-1
#     if current_page<=1:
#         pre_page=1
#
#     next_page=current_page+1
#     if current_page>=total_page:
#         next_page=total_page
#
#     tmp_page=current_page-1
#     page_list=[]
#
#     while tmp_page>0:
#         if tmp_page%show_page:
#             page_list.append(tmp_page)
#             tmp_page-=1
#         else:
#             break
#
#     tmp_page=current_page
#
#     while tmp_page<=total_page:
#         page_list.append(tmp_page)
#         if tmp_page%show_page:
#             tmp_page+=1
#         else:
#             break
#
#     page_list.sort()
#
#     return (total_page,start,end,page_list,pre_page,next_page)

def pagination(current_page,total_num,sing_page_num,show_page):
    current_page=int(current_page)

    total_page=total_num//sing_page_num
    if total_num%sing_page_num:
        total_page+=1

    start=sing_page_num*(current_page-1)
    end=start+sing_page_num


    pre_page=current_page-1 if current_page>1 else 1
    next_page=current_page+1 if current_page<total_page else total_page


    tmp_page=current_page-1

    page_li=[]

    while tmp_page>=1:
        if tmp_page%show_page:
            page_li.append(tmp_page)
        else:
            break
        tmp_page-=1

    tmp_page=current_page

    while tmp_page<=total_page:
        page_li.append(tmp_page)
        if tmp_page % show_page:
            tmp_page+=1
        else:
            break

    page_li.sort()

    return (total_page,start,end,page_li,pre_page,next_page)

print pagination(1,100,10,5)
