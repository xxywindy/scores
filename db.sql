
CREATE Table score(
    id CHAR(50) PRIMARY KEY COMMENT '选课课号',
    year CHAR(9) COMMENT '学年',
    Semester CHAR(2) COMMENT '学期',
    name VARCHAR(20) COMMENT '课程名称',
    credits DECIMAL(2,1) COMMENT '学分',
    grade TINYINT COMMENT '成绩',
    gp DECIMAL(2,1) COMMENT '绩点',
    regrade TINYINT COMMENT '补考成绩',
    major CHAR(1) DEFAULT 'N' COMMENT '是否主修'
);
