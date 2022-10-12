singleApp.controller('listCtrl', ['$http', '$scope', '$timeout', function ($http, $scope, $timeout) {

    $scope.list = [];
    $scope.model;

    /**
     * 加载打印模板列表
     * */


    layui.use(['form', 'table'], function () {
        
        var api_prefix = "/api/{modelName}";

        var $ = layui.jquery,
            form = layui.form,
            table = layui.table;

        function reloadTable() {
            table.reload('table1', {
                url: api_prefix + '/list'
                , where: {} //设定异步数据接口的额外参数
                //,height: 300
            });
        };



        function renderTable() {
            table.render({
                elem: '#table1',
                url: api_prefix + '/list',
                //toolbar: '#toolbarDemo',
                defaultToolbar: [],
                cols: [[
                    { type: "checkbox", width: 50 },
                    // { field: 'system_name', width: 120, title: '系统名称', sort: true, align: "center" },
                    {JsColumnsPropertyListTemplate}
                    { title: '操作', width: 135, toolbar: '#table1Bar', align: "center" }
                ]],
                limits: [10, 15, 20, 25, 50, 100],
                limit: 15,
                page: true,
                //skin: 'line'
            });
        };

        renderTable();

        // 监听搜索操作
        form.on('submit(data-search-btn)', function (data) {
            //执行搜索重载
            table.reload('table1', {
                page: {
                    curr: 1
                }
                , where: data.field,
            }, 'data');

            return false;
        });

        // 新增
        $("#btnAdd").click(function () {
             layer.open({
                type: 2,
                title: '添加',
                content: "{modelName}Modify",
                area: ['700px', '470px'],
                success: function (layero, index) {
                },
                cancel: function (index) {
                },
                end: function () {
                    renderTable();
                }
            });
        });

        $("#btnDelete").click(function () {
            var checkStatus = table.checkStatus('table1');
            console.log('check status: ', checkStatus);

            if (checkStatus.data.length == 0) {
                window.parent.layer.msg("未选中行！", { offset: '15px' });
                return;
            }

            layer.confirm("确定删除选中的行吗？", { btn: ['确认', '取消'], title: "提示" }, function () {
                layer.load(2);
                $.post(api_prefix + "/batch_delete", { post_json: JSON.stringify(checkStatus.data) }, function (result) {
                    layer.closeAll();
                    reloadTable();
                }, "json");
            });
        });




        //监听工具条
        table.on('tool(table1Filter)', function (obj) {
            var data = obj.data;
            var layEvent = obj.event;

            switch (layEvent) {
                case "disactive":
                case "active":
                    //layer.load(2);
                    //var post_data = { id: data.id, status: layEvent == 'disactive' ? 0 : 1 };
                    //$.post(api_prefix + "/toggleStatus", post_data, function (result) {
                    //    layer.closeAll();
                    //    renderTable();
                    //}, "json");
                    //break;

                case "delete":
                    layer.confirm("确定删除吗？", { btn: ['确认', '取消'], title: "提示" }, function () {
                        layer.load(2);

                        $.post(api_prefix + "/delete", { post_json: JSON.stringify(data) }, function (result) {
                            layer.closeAll();
                            reloadTable();
                        }, "json");
                    });
                    break;

                case "edit":
                    layer.open({
                        type: 2,
                        title: '编辑',
                        content: `{modelName}Modify?id=${data.{ID}}`,
                        area: ['700px', '470px'],
                        success: function (layero, index) {
                        },
                        cancel: function (index) {
                        },
                        end: function () {
                            $('#search_btn').click();
                        }
                    });
                    break;
                default:
                    break;
            }
        });


    });
}]);
