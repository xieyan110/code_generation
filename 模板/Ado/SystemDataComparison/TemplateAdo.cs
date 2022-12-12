using {projectName}.Common;
using {projectName}.DB;
using {projectName}.Model.SearchParams;
using {projectName}.Model.ViewModel;
using System.Text;

namespace {projectName}.Ado
{
    public class {modelName}Ado : IQzhealthAdo<{modelName}>
    {
        /// <summary>
        /// 总数 结果
        /// </summary>
        /// <param name="pageParam"></param>
        /// <returns></returns>
        public (int total, List<{modelName}>) PageList(PageParams pageParam)
        {
            DBGenerics db = new();

            var queryable = db.Sugardb.Queryable<{modelName}>();

            foreach(var (k,v) in pageParam.Params)
            {
                if (!string.IsNullOrEmpty(v))
                {
                    switch(k)
                    {
                        {ServerSwitchPageSearchQueryListTemplateTemplate}
                        // case "system_name":
                        //     queryable.Where(x => x.system_name.Contains(v)); break;
                    }
                }
            }
            var lsit = queryable.OrderByDescending(x => x.{ID}).ToPageList(pageParam.PageNumber, pageParam.PageSize, ref pageParam.total);
            return (pageParam.Total, lsit);
        }

    }
}
