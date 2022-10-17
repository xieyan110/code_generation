using Microsoft.AspNetCore.Mvc;
using {projectName}.Ado;
using {projectName}.Common;
using {projectName}.DB;
using {projectName}.Model.ViewModel;
using System.Text.RegularExpressions;
using L = {projectName};
using LSearchParams = {projectName}.Model.SearchParams;

namespace QzhealthWeb.Areas.API.Controllers
{
    public class {modelName}Controller : BaseController
    {
        /// <summary>
        /// 列表
        /// </summary>
        public IActionResult list(/*int page, int limit, string searchParams*/)
        {
            //var userInfo = this.getUserInfo();

            var ado = new {modelName}Ado();
            var (count, list) = ado.PageList(new LSearchParams.PageParams(Request.QueryString.Value));
            
            var response = new L.ResponsePage(0, "", count, list.ToList<{modelName}Output>());

            return new ContentResult { Content = response.ToJsonString(), ContentType = "application/json" };
        }
        
        /// <summary>
        /// 获取一个
        /// </summary>
        public IActionResult getSingle(Guid id)
        {
            //var userInfo = this.getUserInfo();

            DBGenerics db = new DBGenerics();
            var response = new L.Response(false, "");
            try
            {
                var model = db.Data<{modelName}>().Where(x => x.{ID} == id).Single();
                if (model is not null)
                {
                    response.ok = true;
                    response.data = model;
                }
            }
            catch/* (Exception ex)*/{ }
            return Json(response);
        }

        /// <summary>
        /// 新增
        /// </summary>
        /// <returns></returns>
        [HttpPost]
        public IActionResult add(string post_json)
        {
            L.Response response = new L.Response(false, "");
            DBGenerics db = new DBGenerics();
            try
            {
                var model = post_json.CastTo<{modelName}>();

                model.create_time = DateTime.Now.ToUniversalTime();
                model.create_user_id = getUserInfo()?.getOrganId() ?? 0;

                response.ok = db.AddTableRow(model);
                response.msg += response.ok ? "成功" : "失败";

            }
            catch (Exception ex)
            {
                response.ok = false;
                response.msg += ex.ToString();
            }

            return Json(response);
        }


        /// <summary>
        /// 编辑
        /// </summary>
        /// <returns></returns>
        [HttpPost]
        public IActionResult modify(string post_json)
        {
            L.Response response = new L.Response(false, "");
            DBGenerics db = new DBGenerics();
            try
            {
                var model = post_json.CastTo<{modelName}>();
                model.create_time = model.create_time.ToUniversalTime();
                response.ok = db.UpTableRow(model);
                response.msg += response.ok ? "成功" : "失败";
            }
            catch (Exception ex)
            {
                response.ok = false;
                response.msg += ex.ToString();
            }

            return Json(response);
        }

        #region 删除
        /// <summary>
        /// 删除
        /// </summary>
        /// <param name="post_json"></param>
        /// <returns></returns>
        [HttpPost]
        public IActionResult delete(string post_json)
        {
            L.Response response = new L.Response(false, "");
            if (string.IsNullOrEmpty(post_json)) return Json(response);

            DBGenerics db = new DBGenerics();
            try
            {
                var model = post_json.CastTo<{modelName}>();

                response.ok = db.DelebleRow(model);
                response.msg += response.ok ? "成功" : "失败";
            }
            catch (Exception ex)
            {
                response.ok = false;
                response.msg += ex.ToString();
            }

            return Json(response);
        }
        /// <summary>
        /// 批量删除
        /// </summary>
        /// <param name="post_json"></param>
        /// <returns></returns>
        [HttpPost]
        public IActionResult batch_delete(string post_json)
        {
            L.Response response = new L.Response(false, "");
            if (string.IsNullOrEmpty(post_json)) return Json(response);

            DBGenerics db = new DBGenerics();
            try
            {
                var model = post_json.CastTo<List<{modelName}>>();

                response.ok = db.DelebleRows(model);
                response.msg += response.ok ? "成功" : "失败";
            }
            catch (Exception ex)
            {
                response.ok = false;
                response.msg += ex.ToString();
            }

            return Json(response);
        }
        #endregion

    }
}
