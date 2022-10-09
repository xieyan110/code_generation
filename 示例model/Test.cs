using SqlSugar;


namespace QzhealthLibrary.Model.ViewModel
{
    [SugarTable("test")]
    public class Test
    {
        /// <summary>
        /// 测试id
        /// </summary>
        public Guid test_id { get; set; }
        /// <summary>
        /// 名称
        /// </summary>
        public string name { get; set; } = string.Empty;
        /// <summary>
        /// 打招呼信息
        /// </summary>
        public string hello_message { get; set; } = string.Empty;
    }
}
