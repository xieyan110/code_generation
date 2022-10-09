# encoding:utf-8

import re
from pathlib import Path
import os


def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

# 读取文件获取：命名空间，class名称，class字段名称，类型和中文名称
class project:
    """
    读取文件获取：命名空间，class名称，class字段名称，类型和中文名称
    """
    def __init__(self, file_path):

        self.file_path = file_path
        self.file_content = ""
        # 命名空间名称
        self.project_name = {"projectName":""}
        # 实体类名称
        self.model_name = {"modelName":""}
        # 实体类各个字段的名称 ["名称","类型"，"中文名"]
        self.items = {"ItemName":[["","",""]]}
        # id
        self.class_id = {"ID": ""}

        if(self.project_name["projectName"] == "" and self.model_name["modelName"] == ""):
            self.project_init()

    def get_project_dict(self) -> dict[str:str]:
        return dict(self.project_name, **self.model_name, **self.class_id)

    def project_init(self):
        self.get_file_content()
        # 命名空间名称
        self._get_porject_name()
        # 实体类名称
        self._get_model_name()
        # 实体类各个字段的名称 ["名称","类型"，"中文名"]
        self._get_items()
  
    def get_file_content(self):
        """_summary_:获取实体文件内容
        """
        with open(self.file_path, 'r', encoding='utf-8', errors='igore') as f:
            self.file_content = f.read()

    def _get_porject_name(self) -> str:
        """_summary_
        获取项目名称
        Returns:
            str: _description_
        """
        namespace = re.findall(r"namespace\s+(.+?)\.", self.file_content)[0]
        self.project_name["projectName"] = namespace

    def _get_model_name(self) -> str:
        """_summary_
        获取 实体 class 名称 
        Returns:
            str: _description_
        """
        class_name = re.findall(r'class\s+(.+)\n', self.file_content)[0]
        self.model_name["modelName"] = class_name

    def _get_items(self) -> list[list[str]]:
        # 第一个是中文名，第二个是类型，第三个是名称
        class_items = re.findall(r'\/\/\/.+<summary>\s.+\/\/\/\s(.+)\s.+\s.+public\s+(.+)\s+(.+) { get; set; }', self.file_content)
        self.items["ItemName"] = list(map(lambda item:[item[2],self.type_format(item[1]),item[0]],class_items))
        self.class_id["ID"] = self.items["ItemName"][0][0]
        # print(f"{self.items=}")

    def type_format(self,s:str) -> str:
        if(s == ""):
            return ""
        if("Nullable" in s):
            s = re.findall(r"Nullable<(.+)>", s)[0] + "?"
        if("System." in s):
            s = s.replace("System.", "")
        return s

# 模板替换内容
class template_content_builder:
    """
    模板替换内容
    """
    def __init__(self,pro:project) -> None:
        self.pro = pro

        self.is_init = False

        self.css_style_link_template = {"CssStyleLinkTemplateTemplate":''}

        # js 连接模板
        self.js_link_template = {"JsLinkTemplate":'\n\
            <script src="~/JS/{0}/index.js?v=@DateTime.Now.ToString("yyyyMMddHHmmssfff")"></script>'}


        # server 层 页面查询模板
        self.server_switch_page_search_query_list = {"ServerSwitchPageSearchQueryListTemplateTemplate":'\n\
                        case "{0}":\n\
                            queryable.Where(x => x.{0} == v.Trim()); break;'}

        # 实体类 属性名称
        self.model_class_property_list = {"ModelClassPropertyListTemplate":'public {1} {0} {{ get; set; }}'}

        # js columns 模板 
        self.js_columns_property_list = {"JsColumnsPropertyListTemplate":"{{ field: '{0}', width: 120, title: '{2}', sort: true, align: 'center' }},"}

        # js 初始编辑 模板 ["名称","类型"，"中文名"]
        self.js_init_modify_list = {"JsInitModifyListTemplate":"{0}: '',"}

        # js 编辑页面的初始
        self.js_modify_init_data_func = {"JsInitModifyInitDataFuncTemplate":"{0}: $scope.model.{0},"}

        # js 编辑 提交模板
        self.js_modify_save = {"JsModifySaveTemplate":"$scope.model.{0} = data.field.{0};"}



        # html 创建 模板
        self.html_create_box_list = {"HtmlCreateBoxListTemplate":'\n\
                    <div class="layui-inline">\n\
                        <label class="layui-form-label">*{2}</label>\n\
                        <div class="layui-input-inline">\n\
                            <input type="text" name="{0}" ng-model="model.{0}" lay-verify="required" lay-reqtext="{2}是必填项" autocomplete="off" class="layui-input">\n\
                        </div>\n\
                    </div>'}

        # html 编辑 模板
        self.html_modify_list = {"HtmlModifyListTemplate":'\n\
                    <div class="layui-inline">\n\
                        <label class="layui-form-label">*{2}</label>\n\
                        <div class="layui-input-inline">\n\
                            <input type="text" name="{0}" ng-model="model.{0}" placeholder="{2}" lay-verify="required" lay-reqtext="{2}是必填项" autocomplete="off" class="layui-input">\n\
                        </div>\n\
                    </div>'}

        # list 页面搜索
        self.html_search_input_list_template = {"HtmlSearchInputListTemplate":'\n\
                    <div class="layui-inline">\n\
                        <div class="layui-input-inline">\n\
                            <input type="text" name="{0}" placeholder="{2}" autocomplete="off" class="layui-input">\n\
                        </div>\n\
                    </div>'}

        self._template_str()

    def _template_str(self) -> None:
        # 已经初始化
        if(self.is_init == True):
            return
        self.js_link_template["JsLinkTemplate"] = self.js_link_template["JsLinkTemplate"].format(self.pro.model_name["modelName"])
        self._get_server_switch_page_search_query_str()
        self._get_model_class_property_str()
        self._get_js_columns_property_str()
        self._get_js_init_modify_str()
        self._get_html_create_box_str()
        self._get_html_modify_str()
        self._get_search_input_str()
        self._get_js_modify_init_data_func_str()
        self._get_js_modify_save_str()
        self.is_init = True
    
    def get_builder_template_dict(self) -> dict[str:str]:
        return dict(self.css_style_link_template , **self.js_link_template, **self.server_switch_page_search_query_list, **self.model_class_property_list, **self.js_columns_property_list, **self.js_init_modify_list, **self.html_create_box_list, **self.html_modify_list,  **self.js_modify_init_data_func, **self.js_modify_save, **self.html_search_input_list_template, **self.pro.get_project_dict())
        

    def _get_server_switch_page_search_query_str(self) -> None:
        s = self.server_switch_page_search_query_list["ServerSwitchPageSearchQueryListTemplateTemplate"]
        self.server_switch_page_search_query_list["ServerSwitchPageSearchQueryListTemplateTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"][1:]])

    def _get_model_class_property_str(self) -> None:
        s = self.model_class_property_list["ModelClassPropertyListTemplate"]
        self.model_class_property_list["ModelClassPropertyListTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"]])

    def _get_js_columns_property_str(self) -> None:
        s = self.js_columns_property_list["JsColumnsPropertyListTemplate"]
        self.js_columns_property_list["JsColumnsPropertyListTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"]])

    def _get_js_init_modify_str(self) -> None:
        s = self.js_init_modify_list["JsInitModifyListTemplate"]
        self.js_init_modify_list["JsInitModifyListTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"]])

    def _get_html_create_box_str(self) -> None:
        s = self.html_create_box_list["HtmlCreateBoxListTemplate"]
        # 不包括id
        self.html_create_box_list["HtmlCreateBoxListTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"][1:]])
    
    def _get_html_modify_str(self) -> None:
        s = self.html_modify_list["HtmlModifyListTemplate"]
        # 不包括id
        self.html_modify_list["HtmlModifyListTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"][1:]])
    
    def _get_js_modify_init_data_func_str(self) -> None:
        s = self.js_modify_init_data_func["JsInitModifyInitDataFuncTemplate"]
        self.js_modify_init_data_func["JsInitModifyInitDataFuncTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"][1:]])
    
    def _get_js_modify_save_str(self) -> None:
        s = self.js_modify_save["JsModifySaveTemplate"]
        self.js_modify_save["JsModifySaveTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"][1:]])

    def _get_search_input_str(self) -> None:
        s = self.html_search_input_list_template["HtmlSearchInputListTemplate"]
        self.html_search_input_list_template["HtmlSearchInputListTemplate"] = "\n".join([s.format(*i) for i in self.pro.items["ItemName"][1:]])

# 模板路径，和输出路径
class template_path:
    """
    模板路径，以及输出路径
    """
    def __init__(self,pro:project) -> None:
        self.pro = pro
        self.Ado = Path("模板\Ado\SystemDataComparison\TemplateAdo.cs")
        self.Controller = Path("模板\Controllers\TemplateController.cs")
        self.JsList = Path("模板\Js\DataComparison\list.js")
        self.JsModify = Path("模板\Js\DataComparison\modify.js")
        self.InputModel = Path("模板\ViewModel\SystemDataComparison\Input.cs")
        self.OutputModel = Path("模板\ViewModel\SystemDataComparison\Output.cs")
        self.HtmlList = Path("模板\Views\DataComparison\List.cshtml")
        self.HtmlModify = Path("模板\Views\DataComparison\Modify.cshtml")
        
        # self.generatePathController = GetDesktopPath() / Path("CRM\Controllers\{0}Controller.cs".format(pro.model_name["modelName"]))
        self.generateAdo = GetDesktopPath() / Path("代码生成\Ado\{0}\{0}Ado.cs".format(pro.model_name["modelName"]))
        self.generateController = GetDesktopPath() / Path("代码生成\Controllers\{0}Controller.cs".format(pro.model_name["modelName"]))
        self.generateJsList = GetDesktopPath() / Path("代码生成\Js\{0}\list.js".format(pro.model_name["modelName"]))
        self.generateJsModify = GetDesktopPath() / Path("代码生成\Js\{0}\modify.js".format(pro.model_name["modelName"]))
        self.generateInputModel = GetDesktopPath() / Path("代码生成\ViewModel\{0}\{0}Input.cs".format(pro.model_name["modelName"]))
        self.generateOutputModel = GetDesktopPath() / Path("代码生成\ViewModel\{0}\{0}Output.cs".format(pro.model_name["modelName"]))
        self.generateHtmlList = GetDesktopPath() / Path("代码生成\Views\{0}\List.cshtml".format(pro.model_name["modelName"]))
        self.generateHtmlModify = GetDesktopPath() / Path("代码生成\Views\{0}\Modify.cshtml".format(pro.model_name["modelName"]))



    def get_set(self) -> dict[Path:Path]:
        input_templates = [self.Ado, self.Controller,self.JsList,self.JsModify,self.InputModel,self.OutputModel,self.HtmlList,self.HtmlModify]
        output_templates = [self.generateAdo,self.generateController,self.generateJsList,self.generateJsModify,self.generateInputModel,self.generateOutputModel,self.generateHtmlList,self.generateHtmlModify]
        dic = [(k,v) for (k,v) in zip(input_templates,output_templates)]
        return dic

# 将上面3个class整合在一起
class GenerateTemplate:

    def __init__(self,input_class_file) -> None:
        self.file_path = input_class_file

        self.projects = self._get_projects()
        self.template_contents = self._get_template_content()
        self.template_paths = self._get_template_path()

    def _get_projects(self) -> list[project]:
        return [project(str(i)) for i in Path(self.file_path).iterdir() if i.is_file]
    def _get_template_content(self) -> list[template_content_builder]:
        return [template_content_builder(i) for i in self.projects]
    def _get_template_path(self) -> list[template_path]:
        return [template_path(i) for i in self.projects]

    def builder(self)-> None:
        for template_path,template_content in zip(self.template_paths,self.template_contents):
            for input_template,output_template in template_path.get_set():
                input_template = Path(input_template)
                if(not input_template.exists()):
                    continue
                with input_template.open("r",encoding="utf-8",errors='igore' ) as f:
                    content = f.read()
                for template_key,template_val in template_content.get_builder_template_dict().items():
                    pattern = r"(\{\s?"+template_key+r"\s?\})"
                    content = re.sub(pattern, template_val,content)
                output_template = Path(output_template)
                if(not output_template.parent.exists()):
                    os.makedirs(str(output_template.parent))
                with output_template.open("w",encoding="utf-8",errors='igore' ) as f:
                    f.write(content)
                print(".",end='')


if __name__ == "__main__":
    print("开始生成:",end='')
    # 将该文件夹下面的 model 全部生成代码
    g = GenerateTemplate(r"示例model")
    g.builder()
    print("已生成到桌面文件夹")
