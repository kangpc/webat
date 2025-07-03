# 文件作用：用于定位元素失败情况处理
# 工作流程：找到最适合的元素，返回 并更新云元素库
import re
import Levenshtein
import requests
def likescore(oldstr,newstr):
    score = Levenshtein.ratio(str(oldstr), str(newstr))
    return score

def getelement(driver,obj_dict):
    # 1.正则提取所有原始taghtml源码中的 关键属性
    print('查找元素失败！开始启动mynium自动维护！')
    old_html = obj_dict['tag']
    try:old_id = re.findall(r'id="(.*?)"',old_html)[0]
    except:old_id = None
    try:old_name = re.findall(r'name="(.*?)"',old_html)[0]
    except:old_name=None
    try:old_class = re.findall(r'class="(.*?)"',old_html)[0]
    except:old_class=None
    try:old_text = re.findall(r'>(.*?)<',old_html)[0]
    except:old_text=''
    try:old_value = re.findall(r'value="(.*?)"',old_html)[0]
    except:old_value=''
    try:old_onclick = re.findall(r'onclick="(.*?)"',old_html)[0]
    except:old_onclick=None
    try:old_style = re.findall(r'style="(.*?)"',old_html)[0]
    except:old_style=''
    try:old_placeholder = re.findall(r'placeholder="(.*?)"', old_html)[0]
    except:old_placeholder=None
    try:old_href = re.findall(r'href="(.*?)"',old_html)[0]
    except:old_href=None
    try:old_type = re.findall(r'type="(.*?)"',old_html)[0]
    except:old_type = None
    try:old_tag_name = re.findall(r'<(.+?) ',old_html)[0]
    except:old_tag_name = re.findall(r'<(.+?)>',old_html)[0]

    # 2. 根据 old_tag_name 筛选出所有相同类型的元素 (升级设想：获取所有iframe，依次进去拿到所有元素)
    new_elements = driver.find_elements_by_tag_name(old_tag_name)

    # 3. 找出其中最像的那个元素
    end_obj = ''
    end_obj_index = ''
    end_obj_score = 0
    for i in range(len(new_elements)):
        tmp_obj_score =0
        # 找出当前元素所有的属性值
        new_id = new_elements[i].get_attribute("id")
        new_name = new_elements[i].get_attribute("name")
        new_class = new_elements[i].get_attribute("class")
        new_text = new_elements[i].text
        new_value = new_elements[i].get_attribute("value")
        new_onclick = new_elements[i].get_attribute("onclick")
        new_style = new_elements[i].get_attribute("style")
        new_placeholder = new_elements[i].get_attribute("placeholder")
        new_href = new_elements[i].get_attribute("href")
        try:
            new_type = re.findall(r'type="(.*?)"', new_elements[i].get_attribute("outerHTML"))[0]
        except:
            new_type = None

        # 计算得分 #后续ai智能计算比率
        tmp_obj_score += likescore(old_id, new_id)
        tmp_obj_score += likescore(old_name, new_name)
        tmp_obj_score += likescore(old_class, new_class)
        tmp_obj_score += likescore(old_text, new_text)
        tmp_obj_score += likescore(old_value, new_value)
        tmp_obj_score += likescore(old_onclick, new_onclick)
        tmp_obj_score += likescore(str(old_style).replace(' ', ''), str(new_style).replace(' ', ''))
        tmp_obj_score += likescore(old_placeholder, new_placeholder)
        tmp_obj_score += likescore(old_href, new_href)
        tmp_obj_score += likescore(old_type, new_type)
        if tmp_obj_score > end_obj_score:
            end_obj = new_elements[i]
            end_obj_index = i
            end_obj_score = tmp_obj_score
    # 目标元素就是 end_obj，目标元素的下标就是 end_obj_index
    # 更新到云元素库
    ## 拼装成元素的字典，进行请求
    obj_dict['tmp_method'] = 'tag name'
    obj_dict['tmp_value'] = old_tag_name
    obj_dict['index'] = end_obj_index
    obj_dict['tag'] = end_obj.get_attribute("outerHTML")
    requests.post('http://127.0.0.1:8000/waibu_update_object/%s/'%int(obj_dict['id']),data=obj_dict)
    print('mynium维护成功！')
    # 返回这个目标元素
    return end_obj

