using SqlSugar;


namespace QzhealthLibrary.Model.ViewModel
{
    /// <summary>
    /// 检擦项目配置
    /// </summary>
    [SugarTable("project_configuration")]
    public class ProjectConfiguration
    {
        /// <summary>
        /// 检擦项目配置id
        /// </summary>
        public Guid project_configuration_id { get; set; }
        /// <summary>
        /// 项目编码
        /// </summary>
        public string project_code { get; set; } = string.Empty;
        /// <summary>
        /// 项目名称
        /// </summary>
        public string project_name { get; set; } = string.Empty;
        /// <summary>
        /// 英文名称
        /// </summary>
        public string en_name { get; set; } = string.Empty;
        /// <summary>
        /// 助记码
        /// </summary>
        public string memory_code { get; set; } = string.Empty;
        /// <summary>
        /// 缩写
        /// </summary>
        public string acronym { get; set; } = string.Empty;
        /// <summary>
        /// 单位
        /// </summary>
        public int? unit_id { get; set; }
        /// <summary>
        /// 院区
        /// </summary>
        public int? organ_id { get; set; }
        /// <summary>
        /// 设备
        /// </summary>
        public string device { get; set; } = string.Empty;
        /// <summary>
        /// 数据类型
        /// </summary>
        public int? data_type { get; set; }
        /// <summary>
        /// 数据
        /// </summary>
        public string data_obj { get; set; } = string.Empty;
        /// <summary>
        /// 状态
        /// </summary>
        public int status { get; set; }
        /// <summary>
        /// 创建时间
        /// </summary>
        public DateTime create_time { get; set; }
        /// <summary>
        /// 创建人id
        /// </summary>
        public int create_user_id { get; set; }
    }
}
