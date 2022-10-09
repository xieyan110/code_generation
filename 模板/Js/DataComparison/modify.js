singleApp.controller('fromController', ['$http', '$scope', '$timeout', function ($http, $scope, $timeout) {


    function getUrlParam(key) {
        // 获取参数
        var url = window.location.search;
        // 正则筛选地址栏
        var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)");
        // 匹配目标参数
        var result = url.substr(1).match(reg);
        //返回参数值
        return result ? decodeURIComponent(result[2]) : null;
    }

    let is_add = !Boolean(getUrlParam("id"));

    $scope.model = {
        // guid: "00000000-0000-0000-0000-000000000000",
        // create_time: "1900-01-01",
        {JsInitModifyListTemplate}

    };

    //initData
    $scope.initData = function (func) {
        // 如果是编辑
        if (!is_add) {
            $http.get(`/api/{modelName}/getSingle?id=${getUrlParam("id")}`).then(function (result) {
                $scope.model = result.data.data;
                func();
            }, function () { });
        }
    };
    layui.use(['form', 'layedit', 'laydate'], function () {
        var $ = layui.jquery,
            form = layui.form,
            layer = layui.layer,
            layedit = layui.layedit,
            laydate = layui.laydate;
        //创建一个编辑器
        var editIndex = layedit.build('LAY_demo_editor');

        //自定义验证规则
        form.verify({
            title: function (value) {
                if (value.length < 5) {
                    return '标题至少得5个字符啊';
                }
            }
            , pass: [
                /^[\S]{6,12}$/
                , '密码必须6到12位，且不能出现空格'
            ]
            , content: function (value) {
                layedit.sync(editIndex);
            }
        });
        //日期
        laydate.render({
            elem: '#business_time'
        });
        laydate.render({
            elem: '#date1'
        });



        initData = function () {
            form.val('formMain', {
                // system_name: $scope.model.system_name,
                {JsInitModifyInitDataFuncTemplate}
            });
        }

        //监听提交
        form.on('submit(btnSave)', function (data) {
            // $scope.model.system_name = data.field.system_name;
            {JsModifySaveTemplate}
            //console.log("form details:", $scope.model);
            
            //layer.load(2);
            if (is_add) {
                $.post("/api/{modelName}/add", { post_json: JSON.stringify($scope.model) }, function (result) {
                    if (result.ok == true) {
                        parent.layer.close(parent.layer.getFrameIndex(window.name));
                        layer.msg("保存成功！");
                    } else {
                        layer.msg("保存失败！");
                    }
                }, "json");
            } else {
                $.post("/api/{modelName}/modify", { post_json: JSON.stringify($scope.model) }, function (result) {
                    if (result.ok == true) {
                        parent.layer.close(parent.layer.getFrameIndex(window.name));
                        layer.msg("保存成功！");
                    } else {
                        layer.msg("保存失败！");
                    }
                }, "json");
            }
        });
        $scope.initData(initData);
        
    });

}]);