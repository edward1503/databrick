"""Build the Databricks & Governance lecture deck from the AIO2026 PowerPoint template.

Content follows databrick/databricks-governance-basics.md (theory) and the lab design in
databricks-governance-hands-on.md. Result values shown on slides are computed from the lab's
five sample orders and are labelled as expected results, not screenshots of a run.

Run with a Python that has python-pptx, lxml and Pillow:
  python databrick/governance-slides/build_deck.py
Output: output/databricks-governance-slides.pptx
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOPIC = os.path.dirname(HERE)
WORKSPACE = os.path.dirname(TOPIC)
sys.path.insert(0, os.path.join(WORKSPACE, "shared"))

from aio_deck import *  # noqa: E402,F401,F403  (template helpers, colours, Deck)

IMAGES = os.path.join(TOPIC, "assets", "images")
OUTPUT = os.path.join(WORKSPACE, "output", "databricks-governance-slides.pptx")

SECTIONS = [
    "Databricks và lakehouse",
    "Workspace, compute và jobs",
    "Tổ chức dữ liệu",
    "Governance và phân quyền",
]
TOTAL_LABEL = "Tổng kết"
UC_BLUE = RGBColor(0xDE, 0xEB, 0xF7)


LAB_URL = "https://github.com/edward1503/databrick/blob/main/databrick/databricks-governance-hands-on.md"


def IMG(name):
    return os.path.join(IMAGES, name)


def build(template, out):
    d = Deck(template, SECTIONS)
    S1, S2, S3, S4 = SECTIONS

    # ------------------------------------------------------------------ opening
    d.title_slide(
        "Databricks & Governance Basics",
        "Workspace, Unity Catalog và quyền truy cập dữ liệu",
        "AI VIET NAM – AIO2026",
        "Buổi học khoảng 60 phút lý thuyết, sau đó là lab. Ví dụ xuyên suốt: dữ liệu đơn hàng, kỹ sư xử lý dữ liệu "
        "gốc, analyst đọc doanh thu. Nút Data&Code dẫn tới hướng dẫn lab trên GitHub.",
        code_url=LAB_URL,
    )

    s = d.content("Mục tiêu buổi học", "Sau buổi học, bạn có thể",
                  "Học viên cần biết SQL cơ bản (SELECT, CREATE TABLE, GROUP BY). Tài liệu Databricks được đối chiếu "
                  "ngày 27/10/2026, dùng bản tài liệu trên AWS.")
    goals = [
        ("Giải thích", "vai trò của workspace, compute và jobs"),
        ("Đọc", "cấu trúc metastore → catalog → schema → table"),
        ("Viết", "tên đầy đủ ba cấp `catalog.schema.table`"),
        ("Thiết kế", "ma trận quyền theo nhóm từ nhu cầu công việc"),
        ("Xác định", "danh tính cần kiểm tra khi truy cập dữ liệu"),
    ]
    for i, (verb, rest) in enumerate(goals):
        y = 1.65 + i * 1.02
        box(s, 0.7, y, 0.75, 0.75, str(i + 1), fill=BLUE, line=BLUE, size=24, bold=True, color=WHITE,
            shape=MSO_SHAPE.OVAL, name=f"Goal {i + 1} number")
        label(s, 1.7, y + 0.13, 7.5, f"**{verb}** {rest}", size=20, align=PP_ALIGN.LEFT, h=0.5, name=f"Goal {i + 1}")
    callout(s, 9.4, 2.2, 3.4, 3.4,
            "**Tài liệu đi kèm**\n• Bài đọc nền tảng\n• Hướng dẫn lab\n• Quiz 10 câu\n\nVí dụ xuyên suốt: dữ liệu đơn hàng",
            kind="key", size=18, name="Materials")

    # ------------------------------------------------------------------ section 1
    d.outline(0, IMG("lakehouse-architecture.png"),
              "Phần 1: Databricks dùng để làm gì, lakehouse là gì, và vì sao cần governance ngay trong môi trường làm việc.")

    s = d.content(S1, "Một cửa hàng, nhiều nhóm cùng dùng dữ liệu đơn hàng",
                  "Kể tình huống: mỗi nhóm tải file về máy rồi xử lý riêng. Hỏi lớp đã gặp trường hợp hai báo cáo cùng "
                  "chỉ số mà khác số chưa. Đưa lớp tới hai nội dung của bài: môi trường làm việc chung và governance.")
    roles = [("Kỹ sư", "nạp và làm sạch đơn hàng"), ("Analyst", "tính doanh thu"), ("Quản lý", "theo dõi báo cáo")]
    for i, (who, what) in enumerate(roles):
        x = 0.6 + i * 2.15
        box(s, x, 1.75, 1.95, 1.25, f"**{who}**\n{what}", fill=WHITE, line=BLUE, size=16, name=f"Role {i + 1}")
    box(s, 0.6, 3.6, 6.25, 0.9, "Dữ liệu đơn hàng: hàng nghìn đơn mỗi ngày", fill=UC_BLUE, line=BLUE, size=17,
        bold=True, name="Orders data")
    for i in range(3):
        arrow(s, 1.575 + i * 2.15, 3.6, 1.575 + i * 2.15, 3.0, color=BLUE, name=f"Uses {i + 1}")
    label(s, 7.3, 1.55, 5.6, "Khi số người và tác vụ tăng, nhóm phải trả lời:", size=18, color=BLUE, bold=True,
          align=PP_ALIGN.LEFT, h=0.45, name="Questions title")
    qs = ["Bản dữ liệu nào là bản đang được sử dụng?", "Ai được sửa bảng nguồn?", "Vì sao hai báo cáo doanh thu cho kết quả khác nhau?"]
    for i, q in enumerate(qs):
        callout(s, 7.3, 2.15 + i * 0.95, 5.6, 0.78, q, kind="trap", size=17, name=f"Hard question {i + 1}")
    callout(s, 0.6, 5.35, 12.3, 1.2, "Môi trường làm việc chung giúp chia sẻ mã và dữ liệu, nhưng chưa đủ: nhóm còn cần "
            "**quy định trách nhiệm**, **tổ chức tài sản dữ liệu** và **kiểm soát hành động được phép**.",
            kind="key", size=17, name="Two topics")

    s = d.content(S1, "Databricks là gì? Ba việc cần nắm trước",
                  "Chưa cần hiểu công nghệ bên trong. Ba câu hỏi ở slide này là khung cho phần 2 (viết và chạy ở đâu) và "
                  "phần 3–4 (dữ liệu tổ chức và quản lý thế nào).")
    label(s, 0.6, 1.55, 12.3, "**Databricks** là nền tảng cho kỹ thuật dữ liệu, phân tích và AI: viết SQL hoặc mã, chạy tác "
          "vụ xử lý, tổ chức dữ liệu và chia sẻ kết quả trong cùng một hệ sinh thái.", size=18, align=PP_ALIGN.LEFT,
          h=0.9, name="Definition")
    cards = [("Viết công việc ở đâu?", "Workspace: notebook, file, truy vấn"),
             ("Tài nguyên nào thực thi?", "Compute: serverless, classic, SQL warehouse"),
             ("Dữ liệu được tổ chức, quản lý thế nào?", "Unity Catalog: namespace, metadata, quyền")]
    for i, (q, a) in enumerate(cards):
        x = 0.6 + i * 4.15
        box(s, x, 2.75, 0.7, 0.7, str(i + 1), fill=BLUE, line=BLUE, size=22, bold=True, color=WHITE,
            shape=MSO_SHAPE.OVAL, name=f"Card {i + 1} number")
        label(s, x, 3.6, 3.9, f"**{q}**", size=18, align=PP_ALIGN.LEFT, h=0.8, name=f"Card {i + 1} question")
        label(s, x, 4.45, 3.9, a, size=17, align=PP_ALIGN.LEFT, h=0.8, name=f"Card {i + 1} answer")
    callout(s, 0.6, 5.6, 12.3, 1.0, "Luồng ví dụ: đọc đơn hàng → loại đơn không hợp lệ → lưu bảng sạch → tính doanh thu "
            "theo ngày → chạy lại các bước theo lịch.", kind="key", size=17, name="Example flow")

    s = d.content(S1, "Data lake, data warehouse và lakehouse",
                  "Đây là cách phân biệt theo vai trò để bắt đầu học; tính năng thực tế của từng sản phẩm có thể rộng hơn. "
                  "Đọc hình từ trái sang phải: nguồn dữ liệu, các lớp bảng, phục vụ phân tích; phía trên là lớp quản trị.")
    table(s, 0.5, 1.55, [2.0, 5.2, 5.2], [
        ["Khái niệm", "Cách hiểu ở mức nhập môn", "Ví dụ đơn hàng"],
        ["**Data lake**", "Lưu dữ liệu nhiều dạng, kể cả chưa chuẩn hóa", "File đơn hàng gốc, log, JSON"],
        ["**Data warehouse**", "Tổ chức dữ liệu cho truy vấn phân tích", "Bảng phân tích doanh thu"],
        ["**Lakehouse**", "Lưu trữ linh hoạt + quản lý bảng, phân tích", "Lưu gốc, xử lý thành bảng, phân tích có quản trị"],
    ], size=16, name="Lake vs warehouse")
    picture(s, IMG("lakehouse-architecture.png"), 0.5, 3.45, 9.0, 3.3, name="Lakehouse architecture")
    caption(s, 0.5, 6.8, 9.0, "Nguồn: Databricks, What is a data lakehouse? (hình gốc).")
    callout(s, 9.8, 3.6, 3.1, 3.0, "Databricks dùng kiến trúc lakehouse. **Delta Lake** và **Unity Catalog** là hai "
            "thành phần liên quan trực tiếp đến bài này.", kind="key", size=16, name="Lakehouse note")

    s = d.content(S1, "Governance: bốn câu hỏi, Unity Catalog trả lời bằng gì?",
                  "Nhấn mạnh: phân quyền chỉ là một phần của governance. Một bảng có quyền đúng nhưng không ai hiểu ý nghĩa "
                  "các cột vẫn khó dùng. Unity Catalog là lớp quản trị dữ liệu và tài sản AI của Databricks.")
    pairs = [("Dữ liệu nào tồn tại, ở đâu?", "Namespace, metadata, khám phá dữ liệu"),
             ("Ai chịu trách nhiệm?", "Owner của đối tượng"),
             ("Ai được đọc, sửa, tạo?", "GRANT / REVOKE theo principal"),
             ("Lần theo nguồn gốc và hoạt động?", "Lineage và audit log")]
    label(s, 0.6, 1.5, 5.4, "Câu hỏi governance", size=18, color=ORANGE, bold=True, align=PP_ALIGN.LEFT, name="Left head")
    label(s, 7.4, 1.5, 5.4, "Cơ chế trong Unity Catalog", size=18, color=BLUE, bold=True, align=PP_ALIGN.LEFT, name="Right head")
    for i, (q, a) in enumerate(pairs):
        y = 2.0 + i * 1.02
        box(s, 0.6, y, 5.6, 0.8, q, fill=PEACH, line=ORANGE, size=17, name=f"Governance q{i + 1}")
        arrow(s, 6.25, y + 0.4, 7.35, y + 0.4, color=GRAY, name=f"Maps {i + 1}")
        box(s, 7.4, y, 5.5, 0.8, a, fill=UC_BLUE, line=BLUE, size=17, name=f"UC answer {i + 1}")
    callout(s, 0.6, 6.15, 12.3, 0.75, "Governance biến yêu cầu nghiệp vụ thành **cấu trúc dữ liệu** và **tập quyền có thể kiểm tra**.",
            kind="key", size=17, name="Governance takeaway")

    # ------------------------------------------------------------------ section 2
    d.outline(1, IMG("lakeflow-jobs-example.png"),
              "Phần 2: viết công việc ở đâu, chạy trên tài nguyên nào, điều phối lặp lại thế nào và chạy bằng danh tính nào.")

    s = d.content(S2, "Một câu SELECT đi qua những thành phần nào?",
                  "Theo dõi một thao tác: kỹ sư mở notebook, viết SELECT và chạy. Notebook nằm trong workspace, câu lệnh chạy "
                  "trên compute, bảng được gọi bằng tên trong catalog, quyền được kiểm tra theo danh tính đang thực thi. "
                  "Sơ đồ là quan hệ chức năng, không phải vị trí triển khai vật lý.")
    box(s, 0.6, 1.75, 2.9, 0.95, "**Workspace**\nnotebook, file, truy vấn", fill=WHITE, line=BLUE, size=16, name="Workspace")
    box(s, 0.6, 3.35, 2.9, 0.95, "**Jobs**\ntask, lịch chạy", fill=WHITE, line=BLUE, size=16, name="Jobs")
    box(s, 4.3, 2.55, 2.6, 0.95, "**Compute**\nthực thi câu lệnh", fill=GREEN_LIGHT, line=GREEN, size=16, name="Compute")
    box(s, 4.0, 4.85, 3.2, 0.95, "**Bảng dữ liệu**\nđọc và ghi", fill=WHITE, line=GREEN, size=16, name="Tables")
    box(s, 0.6, 4.85, 2.9, 0.95, "**Unity Catalog**\nnamespace, metadata, quyền", fill=UC_BLUE, line=BLUE, size=16, name="UC")
    arrow(s, 3.5, 2.22, 4.3, 2.85, name="Workspace to compute")
    arrow(s, 3.5, 3.82, 4.3, 3.2, name="Jobs to compute")
    arrow(s, 5.6, 3.5, 5.6, 4.85, name="Compute to tables")
    arrow(s, 3.5, 5.32, 4.0, 5.32, color=BLUE, dashed=True, name="Governs")
    label(s, 0.6, 5.85, 3.4, "quản trị truy cập (nét đứt)", size=12, color=GRAY, align=PP_ALIGN.LEFT, name="Dashed legend")
    table(s, 7.6, 1.6, [1.6, 3.7], [
        ["Thành phần", "Vai trò chính"],
        ["Workspace", "Tổ chức công việc, cộng tác"],
        ["Notebook", "Mã, diễn giải và kết quả"],
        ["Compute", "Tài nguyên thực thi"],
        ["Job", "Điều phối task và các lần chạy"],
        ["Catalog", "Nhóm tài sản trong namespace"],
        ["Unity Catalog", "Quản trị đối tượng và quyền"],
    ], size=15, name="Components", row_h=0.5)
    callout(s, 7.6, 5.4, 5.3, 1.2, "Không tìm thấy notebook, không dùng được compute, thiếu quyền đọc bảng: "
            "**ba lỗi khác nhau**.", kind="trap", size=16, name="Three errors")

    s = d.content(S2, "Workspace tổ chức công việc, compute thực thi",
                  "Một notebook trong /Shared/order-analytics/ vẫn cần quyền dữ liệu phù hợp để đọc lab_governance.bronze."
                  "orders_raw. Ngược lại, có quyền đọc bảng mà không được dùng warehouse đang chọn thì vẫn không chạy được.")
    end = code_box(s, 0.6, 1.6, 5.6, "Thư mục workspace của nhóm",
                   "/Shared/order-analytics/\n    01_prepare_orders\n    02_build_daily_sales\n    03_check_results",
                   kind="cmd", size=16, name="Workspace folder")
    label(s, 0.6, end + 0.25, 5.6, "Đường dẫn thư mục giúp thành viên hiểu công việc, nhưng **không** xác định quyền "
          "truy cập vào các bảng mà notebook dùng.", size=17, align=PP_ALIGN.LEFT, h=1.0, name="Folder note")
    label(s, 6.9, 1.55, 6.0, "Hai điều kiện độc lập khi chạy SQL", size=18, color=BLUE, bold=True, align=PP_ALIGN.LEFT,
          name="Two conditions title")
    box(s, 6.9, 2.15, 6.0, 1.0, "**1.** Được **sử dụng** tài nguyên thực thi (SQL warehouse, compute)?", fill=GREEN_LIGHT,
        line=GREEN, size=17, name="Condition compute")
    box(s, 6.9, 3.35, 6.0, 1.0, "**2.** Danh tính thực thi được **thao tác với bảng**?", fill=UC_BLUE, line=BLUE,
        size=17, name="Condition data")
    callout(s, 6.9, 4.65, 6.0, 1.5, "Cấp thêm quyền bảng **không** giải quyết lỗi sử dụng compute, và ngược lại.",
            kind="trap", size=17, name="Compute trap")

    s = d.content(S2, "Job, task, trigger và run",
                  "Databricks gọi sản phẩm điều phối là Lakeflow Jobs. Khi kiểm tra lỗi, mở đúng run và đúng task để đọc "
                  "thông báo, không suy đoán từ trạng thái chung của job. Ảnh bên phải là ví dụ trong tài liệu chính thức, "
                  "có nhánh điều kiện, không phải ảnh lab.")
    steps = ["Nạp đơn hàng", "Làm sạch", "Tính doanh thu", "Kiểm tra"]
    for i, st in enumerate(steps):
        box(s, 0.6 + i * 1.62, 1.75, 1.4, 0.8, st, fill=WHITE, line=GREEN, size=14, name=f"Task {i + 1}")
        if i:
            arrow(s, 0.6 + i * 1.62 - 0.22, 2.15, 0.6 + i * 1.62, 2.15, name=f"Depends {i}")
    table(s, 0.6, 2.9, [1.4, 5.0], [
        ["Khái niệm", "Ý nghĩa"],
        ["**Job**", "Điều phối công việc, gồm một hay nhiều task"],
        ["**Task**", "Một bước, ví dụ chạy notebook; có thể phụ thuộc task khác"],
        ["**Trigger**", "Khi nào job được khởi chạy, ví dụ theo lịch"],
        ["**Run**", "Một lần thực thi cụ thể của job"],
    ], size=15, name="Job terms", row_h=0.5)
    picture(s, IMG("lakeflow-jobs-example.png"), 7.3, 1.6, 5.6, 4.4, name="Lakeflow jobs UI")
    caption(s, 7.3, 6.05, 5.6, "Nguồn: Databricks, Lakeflow Jobs (ảnh tham khảo, không phải ảnh lab).")

    s = d.content(S2, "Người bấm chạy khác danh tính thực thi (Run as)",
                  "Câu hỏi cho lớp: job chạy thành công thì Lan có đọc trực tiếp được bảng silver không? Không thể kết luận: "
                  "job dùng quyền của danh tính Run as. Trong vận hành, nhóm thường dùng service principal để quyền thực thi "
                  "không phụ thuộc tài khoản cá nhân. Lab bước 9 quan sát điều này bằng current_user() trong notebook task.")
    box(s, 0.6, 2.0, 2.4, 1.1, "**Lan**\nđược bấm chạy job", fill=WHITE, line=BLUE, size=16, name="Lan")
    box(s, 4.0, 1.8, 3.4, 1.2, "**Job**\nRun as: **kỹ sư**\n(có SELECT trên silver)", fill=GREEN_LIGHT, line=GREEN,
        size=16, name="Job run as")
    box(s, 8.4, 2.0, 2.8, 1.1, "`silver.orders_clean`", fill=UC_BLUE, line=BLUE, size=16, name="Silver table")
    arrow(s, 3.0, 2.55, 4.0, 2.55, name="Trigger")
    label(s, 3.0, 2.05, 1.0, "kích hoạt", size=12, color=GRAY, name="Trigger label")
    arrow(s, 7.4, 2.55, 8.4, 2.55, name="Reads")
    label(s, 7.4, 2.05, 1.0, "đọc ✓", size=12, color=GREEN, name="Reads label")
    arrow(s, 1.8, 3.15, 9.8, 3.15, color=ORANGE, dashed=True, name="Direct query")
    label(s, 2.4, 3.25, 7.6, "Lan tự chạy SELECT trực tiếp? **Chưa biết**: phụ thuộc quyền của Lan", size=15,
          color=ORANGE, name="Direct label")
    bullets(s, 0.6, 4.2, 6.4, 2.4, [
        "Jobs có quyền quản lý riêng và cấu hình **Run as**.",
        "Khi notebook task đọc bảng, xét quyền của **danh tính Run as**.",
        "**Service principal**: danh tính cho ứng dụng hoặc tự động hóa.",
    ], size=17)
    callout(s, 7.4, 4.3, 5.5, 1.9, "Job đọc được silver **không chứng minh** người bấm chạy có quyền chạy SELECT trên "
            "bảng ấy.", kind="trap", size=17, name="Run as trap")

    # ------------------------------------------------------------------ section 3
    d.outline(2, IMG("unity-catalog-hierarchy.png"),
              "Phần 3: các cấp tổ chức dữ liệu, tên đầy đủ ba cấp và nơi dữ liệu thực sự được lưu.")

    s = d.content(S3, "Đọc cấu trúc từ trên xuống: metastore → catalog → schema → table",
                  "Khi mới học, đi theo nhánh giữa của hình: Metastore, Catalog, Schema, Table. Schema còn chứa view, volume, "
                  "function; bài này tập trung vào table.")
    picture(s, IMG("unity-catalog-hierarchy.png"), 0.5, 1.5, 12.4, 2.75, name="UC hierarchy")
    caption(s, 0.5, 4.25, 12.4, "Nguồn: Databricks, Unity Catalog securable objects reference (hình gốc).")
    table(s, 0.5, 4.65, [1.7, 6.3, 4.4], [
        ["Cấp", "Ý nghĩa", "Ví dụ"],
        ["**Metastore**", "Chứa metadata và các đối tượng Unity Catalog", "Metastore của workspace"],
        ["**Catalog**", "Nhóm tài sản theo phạm vi lớn: môi trường, đơn vị", "`lab_governance`"],
        ["**Schema**", "Chia nhỏ tài sản trong một catalog", "`bronze`, `silver`, `gold`"],
        ["**Table**", "Dữ liệu có cấu trúc theo dòng và cột", "`orders_raw`, `daily_sales`"],
    ], size=14, name="Hierarchy table", row_h=0.4)

    s = d.content(S3, "Namespace ba cấp: catalog.schema.table",
                  "Viết tên đầy đủ giúp chỉ rõ đối tượng khi các catalog hoặc schema khác nhau có bảng trùng tên. Lưu ý chữ "
                  "“schema” có hai nghĩa: namespace chứa đối tượng, hoặc cấu trúc cột của một bảng. Bronze/silver/gold là "
                  "cách tổ chức của ví dụ, không phải tên bắt buộc.")
    code_box(s, 0.6, 1.6, 5.4, "Dữ liệu đơn hàng theo ba lớp",
             "Metastore\n└── lab_governance        <- catalog\n    ├── bronze          <- schema\n"
             "    │   └── orders_raw  <- table\n    ├── silver\n    │   └── orders_clean\n    └── gold\n"
             "        └── daily_sales", kind="cmd", size=16, name="Namespace tree")
    parts = [("lab_governance", "catalog", UC_BLUE, BLUE), ("gold", "schema", GREEN_LIGHT, GREEN),
             ("daily_sales", "table", PEACH, ORANGE)]
    x = 6.6
    widths = [2.55, 1.2, 2.05]
    for i, ((txt, kind, fill, line), w) in enumerate(zip(parts, widths)):
        box(s, x, 1.85, w, 0.8, f"`{txt}`", fill=fill, line=line, size=16, name=f"Name part {i + 1}",
            shape=MSO_SHAPE.RECTANGLE)
        label(s, x, 2.7, w, kind, size=15, color=line, bold=True, name=f"Name kind {i + 1}")
        x += w
        if i < 2:
            label(s, x, 1.95, 0.2, "**.**", size=24, name=f"Dot {i + 1}")
            x += 0.2
    bullets(s, 6.6, 3.35, 6.3, 2.0, [
        "**Bronze**: giữ dữ liệu đơn hàng ban đầu.",
        "**Silver**: giữ đơn đáp ứng quy tắc làm sạch.",
        "**Gold**: giữ bảng doanh thu tổng hợp cho analyst.",
    ], size=17)
    callout(s, 6.6, 5.4, 6.3, 1.2, "Mỗi cấp dùng để phân chia **trách nhiệm**, **dữ liệu** và **quyền**.",
            kind="key", size=17, name="Levels purpose")

    s = d.content(S3, "Ba loại địa chỉ; managed table, external table và Delta Lake",
                  "Không suy ra đường dẫn file vật lý từ tên notebook hay tên schema. Managed table: Unity Catalog quản lý "
                  "metadata và vòng đời dữ liệu. External table: dữ liệu ở vị trí quản lý bên ngoài, nhưng truy cập qua "
                  "Databricks vẫn chịu quản trị của Unity Catalog. Lab dùng managed table.")
    table(s, 0.5, 1.6, [5.6, 3.3], [
        ["Địa chỉ", "Chỉ đến"],
        ["`/Shared/order-analytics/01_prepare_orders`", "Notebook trong workspace"],
        ["`lab_governance.bronze.orders_raw`", "Bảng trong namespace dữ liệu"],
        ["URI của object storage", "Vị trí vật lý của file dữ liệu"],
    ], size=15, name="Address types", row_h=0.5)
    box(s, 9.4, 1.6, 3.5, 1.15, "**Managed table**\nUnity Catalog quản lý metadata và vòng đời dữ liệu", fill=GREEN_LIGHT,
        line=GREEN, size=15, name="Managed")
    box(s, 9.4, 2.95, 3.5, 1.15, "**External table**\ndữ liệu ở vị trí do bên ngoài quản lý", fill=WHITE, line=GREEN,
        size=15, name="External")
    callout(s, 0.5, 4.4, 8.4, 2.2, "**Delta Lake** bổ sung transaction log cho các file Parquet để hỗ trợ giao dịch và "
            "quản lý bảng. Trong lab, `USING DELTA` chỉ rõ định dạng bảng; ta thao tác qua SQL, không sửa trực tiếp file.",
            kind="key", size=17, name="Delta")
    callout(s, 9.4, 4.4, 3.5, 2.2, "Catalog và schema là **tổ chức logic**, không phải thư mục vật lý.", kind="trap",
            size=17, name="Logical not physical")

    # ------------------------------------------------------------------ section 4
    d.outline(3, IMG("unity-catalog-lineage.png"),
              "Phần 4: metadata, ownership, kiểm soát truy cập, lineage, audit và mô hình quyền của Unity Catalog.")

    s = d.content(S4, "Metadata, ownership và access control",
                  "Tên daily_sales chưa cho biết doanh thu có gồm đơn hủy không; nên ghi rõ bảng được tạo từ đơn đã thanh "
                  "toán và có giá trị dương. Owner có quyền quản lý đối tượng, kể cả cấp quyền; analyst nhận SELECT nhưng "
                  "không trở thành owner. Ngoài grant còn workspace binding, ABAC, row filter, column mask: ngoài phạm vi bài.")
    bullets(s, 0.6, 1.55, 6.0, 2.6, [
        "**Metadata**: tên bảng, cấu trúc cột, mô tả, người sở hữu.",
        "**Owner**: principal sở hữu đối tượng, có quyền quản lý và cấp quyền.",
        "Ownership **khác** quyền chỉ đọc hoặc sửa dữ liệu.",
    ], size=17)
    callout(s, 7.0, 1.6, 5.9, 2.2, "`daily_sales` có gồm đơn hủy không? Chỉ nhìn tên thì không biết. Hãy mô tả quy tắc: "
            "**đơn đã thanh toán, số tiền dương**.", kind="trap", size=17, name="Metadata example")
    label(s, 0.6, 4.25, 12.3, "Một quyết định cấp quyền có ba thành phần", size=18, color=BLUE, bold=True,
          align=PP_ALIGN.LEFT, name="Grant parts title")
    triple = [("Ai?", "`lab_analysts`"), ("Được làm gì?", "`SELECT`"), ("Trên tài sản nào?", "`gold.daily_sales`")]
    for i, (q, a) in enumerate(triple):
        x = 0.6 + i * 4.2
        box(s, x, 4.8, 3.8, 1.5, f"**{q}**\n{a}", fill=UC_BLUE if i != 1 else GREEN_LIGHT, line=BLUE if i != 1 else GREEN,
            size=18, name=f"Grant part {i + 1}")
        if i < 2:
            arrow(s, x + 3.8, 5.55, x + 4.2, 5.55, color=GRAY, name=f"Grant arrow {i + 1}")

    s = d.content(S4, "Lineage và audit trả lời hai câu hỏi khác nhau",
                  "Lineage: bảng được tạo từ đâu, qua biến đổi nào. Audit: hoạt động nào đã diễn ra, ai làm, lúc nào. Ảnh là "
                  "ví dụ trong tài liệu Databricks, không phải lineage của bảng lab. Việc xem lineage và system table phụ "
                  "thuộc quyền và cấu hình workspace.")
    chain = [("`bronze.orders_raw`", WHITE), ("`silver.orders_clean`", WHITE), ("`gold.daily_sales`", WHITE)]
    notes_between = ["lọc đơn đã thanh toán, số tiền dương", "tổng hợp theo ngày"]
    for i, (txt, fill) in enumerate(chain):
        y = 1.65 + i * 1.45
        box(s, 0.6, y, 3.6, 0.75, txt, fill=fill, line=GREEN, size=16, name=f"Lineage node {i + 1}")
        if i < 2:
            arrow(s, 2.4, y + 0.75, 2.4, y + 1.45, name=f"Lineage edge {i + 1}")
            label(s, 2.55, y + 0.85, 4.2, notes_between[i], size=14, color=GRAY, align=PP_ALIGN.LEFT,
                  name=f"Lineage note {i + 1}")
    picture(s, IMG("unity-catalog-lineage.png"), 6.9, 1.55, 6.0, 3.35, name="Lineage UI")
    caption(s, 6.9, 4.9, 6.0, "Nguồn: Databricks, Lineage in Unity Catalog (ảnh tham khảo).")
    callout(s, 0.6, 5.85, 5.9, 0.95, "**Lineage**: kết quả được tạo **từ đâu**?", kind="key", size=17, name="Lineage q")
    callout(s, 6.9, 5.35, 6.0, 1.45, "**Audit log**: hoạt động **nào** đã xảy ra? Truy vấn qua `system.access.audit` khi có "
            "quyền và cấu hình phù hợp.", kind="key", size=16, name="Audit q")

    s = d.content(S4, "Principal và các quyền cần biết",
                  "Account group mới dùng để cấp quyền trên dữ liệu Unity Catalog; workspace-local group là loại cũ, không "
                  "dùng cho việc này. Có thể nhận quyền qua grant trực tiếp hoặc kế thừa từ cấp cha.")
    table(s, 0.5, 1.6, [2.3, 3.6], [
        ["Principal", "Vai trò"],
        ["User", "Danh tính một người dùng"],
        ["Group", "Tập danh tính, quản lý quyền theo nhóm"],
        ["Service principal", "Danh tính cho ứng dụng, tự động hóa"],
    ], size=15, name="Principals", row_h=0.5)
    table(s, 6.8, 1.6, [2.1, 1.3, 2.7], [
        ["Quyền", "Trên", "Mục đích"],
        ["`USE CATALOG`", "Catalog", "Đi qua catalog"],
        ["`USE SCHEMA`", "Schema", "Đi qua schema"],
        ["`SELECT`", "Table", "Đọc dữ liệu"],
        ["`MODIFY`", "Table", "INSERT, UPDATE, DELETE"],
        ["`CREATE TABLE`", "Schema", "Tạo bảng"],
    ], size=15, name="Privileges", row_h=0.5)
    label(s, 0.5, 4.75, 12.4, "Để **đọc một bảng** cần đủ ba quyền:", size=18, color=BLUE, bold=True,
          align=PP_ALIGN.LEFT, name="Chain title")
    chain = ["`USE CATALOG`\ntrên catalog", "`USE SCHEMA`\ntrên schema", "`SELECT`\ntrên bảng"]
    for i, c in enumerate(chain):
        x = 0.6 + i * 3.1
        box(s, x, 5.3, 2.6, 1.1, c, fill=UC_BLUE if i < 2 else GREEN_LIGHT, line=BLUE if i < 2 else GREEN, size=16,
            name=f"Read chain {i + 1}")
        if i < 2:
            arrow(s, x + 2.6, 5.85, x + 3.1, 5.85, color=GRAY, name=f"Read chain arrow {i + 1}")
    callout(s, 9.9, 5.15, 3.0, 1.4, "Chỉ có `SELECT` trên bảng: có thể **vẫn chưa đọc được**.", kind="trap", size=16,
            name="Select alone")

    s = d.content(S4, "Quyền trực tiếp, quyền kế thừa và GRANT / REVOKE / SHOW GRANTS",
                  "Trong privilege model hiện hành, quyền ở catalog và schema được kế thừa xuống đối tượng con, kể cả đối "
                  "tượng tạo sau. Lab chọn quyền trên bảng cụ thể: khi gold có bảng mới, nhóm phải chủ động quyết định "
                  "analyst có được đọc hay không. Người chạy GRANT cần quyền quản lý tương ứng, ví dụ owner.")
    end = code_box(s, 0.5, 1.6, 6.2, "Phạm vi hẹp: một bảng cụ thể",
                   "GRANT SELECT\n  ON TABLE lab_governance.gold.daily_sales\n  TO `lab_analysts`;", kind="cmd", size=15,
                   name="Grant table")
    code_box(s, 0.5, end + 0.3, 6.2, "Phạm vi rộng: cả schema, gồm bảng tạo sau",
             "GRANT SELECT\n  ON SCHEMA lab_governance.gold\n  TO `lab_analysts`;", kind="cmd", size=15, name="Grant schema")
    table(s, 7.1, 1.6, [2.2, 3.6], [
        ["Lệnh", "Tác dụng"],
        ["`GRANT`", "Cấp quyền"],
        ["`REVOKE`", "Thu hồi **một** grant"],
        ["`SHOW GRANTS`", "Xem grant trên đối tượng hoặc của principal"],
    ], size=15, name="Grant commands", row_h=0.5)
    callout(s, 0.5, 4.6, 12.4, 1.9, "**REVOKE không bảo đảm mất quyền.** User vẫn có thể nhận cùng quyền từ một group khác, "
            "từ cấp cha (schema, catalog) hoặc từ ownership. Khi kiểm tra, hãy **tìm nguồn của quyền** thay vì chỉ nhìn câu "
            "REVOKE vừa chạy.", kind="trap", size=17, name="Revoke trap")

    s = d.content(S4, "Áp dụng: ma trận quyền của lab",
                  "Ma trận được thiết kế từ nhu cầu công việc: analyst chỉ đọc doanh thu, kỹ sư đọc/sửa dữ liệu nguồn và tạo "
                  "bảng thử trong silver. Kỹ sư không có quyền gold là lựa chọn của lab để quan sát ranh giới quyền. Các con "
                  "số bên phải tính từ 5 đơn mẫu của lab: là kết quả kỳ vọng, không phải ảnh chụp lượt chạy.")
    table(s, 0.5, 1.55, [4.3, 1.6, 1.6], [
        ["Thao tác", "Kỹ sư", "Analyst"],
        ["Đọc, sửa bảng bronze", "Cho phép", "Từ chối"],
        ["Đọc, sửa bảng silver", "Cho phép", "Từ chối"],
        ["Tạo bảng trong silver", "Cho phép", "Từ chối"],
        ["Đọc bảng gold", "Từ chối", "Cho phép"],
        ["Sửa bảng gold", "Từ chối", "Từ chối"],
        ["Tạo bảng trong gold", "Từ chối", "Từ chối"],
    ], size=15, name="Permission matrix", row_h=0.5)
    end = code_box(s, 8.3, 1.6, 4.6, "Kỳ vọng: gold.daily_sales",
                   "order_date  order_count  revenue\n2026-10-26  2            200.00\n2026-10-27  1            200.00",
                   size=14, name="Expected gold")
    label(s, 8.3, end + 0.2, 4.6, "Bronze 5 đơn → silver 3 đơn (bỏ `o1003` đã hủy, `o1004` số tiền âm) → tổng doanh thu "
          "**400.00**.", size=16, align=PP_ALIGN.LEFT, h=1.1, name="Expected note")
    callout(s, 0.5, 5.4, 12.4, 1.1, "Kiểm tra bằng **đúng danh tính**, cả thao tác **được phép** lẫn **bị từ chối**. "
            "Xem `SHOW GRANTS` mới là kiểm tra cấu hình, chưa phải kiểm tra hành vi.", kind="key", size=17,
            name="Test identities")

    # ------------------------------------------------------------------ wrap-up
    s = d.content(TOTAL_LABEL, "Những điểm dễ nhầm",
                  "Có thể cho lớp bỏ phiếu đúng/sai cho từng dòng bên trái trước khi nói cột phải.")
    table(s, 0.5, 1.55, [6.2, 6.2], [
        ["Dễ nhầm", "Phù hợp"],
        ["Notebook ở thư mục chung thì đọc được mọi bảng", "Quyền dữ liệu do Unity Catalog quyết định"],
        ["Có quyền bảng thì chạy được trên mọi compute", "Quyền dùng compute là điều kiện riêng"],
        ["Chỉ cần `SELECT` để đọc bảng", "Cần thêm `USE CATALOG`, `USE SCHEMA`"],
        ["Job chạy được nghĩa là người bấm có quyền", "Job dùng quyền của danh tính Run as"],
        ["REVOKE xong là chắc chắn hết quyền", "Có thể còn quyền từ group, cấp cha, ownership"],
        ["Bảng CTAS tự cập nhật khi nguồn đổi", "CTAS lưu kết quả tại thời điểm tạo"],
        ["Workspace-local group dùng cho grant dữ liệu", "Dùng account group"],
    ], size=15, header_fill=ORANGE, name="Misconceptions", row_h=0.6)

    s = d.content(TOTAL_LABEL, "Kiểm tra nhanh",
                  "Đáp án: (1) Không; đường dẫn workspace không cấp quyền dữ liệu. (2) Không; CTAS lưu kết quả lúc tạo, cần "
                  "chạy lại logic biến đổi. (3) Không; dùng account group. (4) Ví dụ: SELECT ở schema hoặc catalog, một group "
                  "khác, ownership, quyền admin. (5) Lineage: dữ liệu được tạo từ đâu; audit: hoạt động nào đã xảy ra. Các câu "
                  "này không trùng quiz chính thức.")
    qs = [
        "Notebook nằm trong `/Shared/order-analytics/`. Điều đó có cho user quyền đọc bảng notebook dùng không?",
        "Silver và gold tạo bằng CTAS. Hôm sau bronze có thêm 10 đơn. Gold có tự cập nhật không?",
        "Workspace-local group có dùng để cấp quyền trên bảng Unity Catalog được không?",
        "Đã REVOKE SELECT trên bảng nhưng analyst vẫn đọc được. Nêu hai nguồn quyền có thể còn lại.",
        "Lineage và audit log trả lời hai câu hỏi khác nhau nào?",
    ]
    for i, q in enumerate(qs):
        yy = 1.65 + i * 1.02
        box(s, 0.7, yy, 0.75, 0.75, f"Q{i + 1}", fill=ORANGE, line=ORANGE, size=18, bold=True, color=WHITE,
            shape=MSO_SHAPE.OVAL, name=f"Question {i + 1} badge")
        label(s, 1.7, yy + 0.05, 11.2, q, size=19, align=PP_ALIGN.LEFT, h=0.7, name=f"Question {i + 1}")

    s = d.content(TOTAL_LABEL, "Từ nhu cầu công việc đến quyền có thể kiểm tra",
                  "Nhắc học viên: lab cần workspace có Unity Catalog, hai user không phải admin và hai account group. Nếu chỉ "
                  "có một tài khoản quản trị, chỉ tạo được đối tượng và xem grant, chưa xác nhận được hành vi phân quyền.")
    flow = ["Nhu cầu\ncông việc", "Cấu trúc\ndữ liệu", "Ma trận\nquyền", "GRANT\ntheo nhóm", "Kiểm thử bằng\nđúng danh tính"]
    for i, f in enumerate(flow):
        x = 0.5 + i * 2.5
        box(s, x, 1.75, 2.1, 1.2, f, fill=UC_BLUE if i < 4 else GREEN_LIGHT, line=BLUE if i < 4 else GREEN, size=16,
            bold=True, name=f"Flow {i + 1}")
        if i < 4:
            arrow(s, x + 2.1, 2.35, x + 2.5, 2.35, color=GRAY, name=f"Flow arrow {i + 1}")
    callout(s, 0.5, 3.4, 7.3, 3.2,
            "**Tiếp theo: lab**\n• Quản trị viên tạo catalog, schema, ba bảng đơn hàng\n• Cấp quyền cho `lab_engineers`, "
            "`lab_analysts`\n• Kiểm thử bằng user kỹ sư và user analyst\n• REVOKE, thử lại, rồi khôi phục\n"
            "• Job với Run as: xem `current_user()`", kind="key", size=17, name="Lab preview")
    callout(s, 8.2, 3.4, 4.7, 3.2, "**Chuẩn bị**\nWorkspace bật Unity Catalog, một SQL warehouse, hai user không phải "
            "admin trong hai account group.", kind="trap", size=17, name="Lab prerequisites")

    d.finish(out)
    return len(d.prs.slides)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else OUTPUT
    n = build(find_template(WORKSPACE), out)
    print(f"Wrote {out} ({n} slides)")
