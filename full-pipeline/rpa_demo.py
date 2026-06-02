"""
跨境电商 RPA 自动化脚本示例
============================
用 Playwright 代替人工鼠标点击，自动完成以下操作：

1. 打开 Amazon 竞品页面 → 自动截图价格/排名
2. 自动登录卖家后台 → 导出订单报表
3. 竞品价格变动 → 自动填表记录 + 飞书告警
4. 批量打开多个 ASIN 页面 → 对比价格后输出表格

实际运行时替换 # TODO 处的真实账号密码和 URL
"""

from playwright.sync_api import sync_playwright
import time

# ============================================================
# 场景一：自动打开 5 个竞品页面，截图价格和排名
# ============================================================
def rpa_competitor_price_check():
    """
    传统方式：运营每天打开 10+ 个竞品页面，手动复制价格到 Excel，耗时 1 小时
    RPA 方式：脚本自动打开 → 截图 → 提取价格 → 汇总表格，30 秒搞定
    """
    print("=== 场景一：竞品价格自动巡检 ===")

    competitors = [
        {"name": "TOZO A1", "url": "https://www.amazon.com/dp/B0BQJ7PX4X"},
        {"name": "Soundcore P20i", "url": "https://www.amazon.com/dp/B0CBPPLFJ8"},
        {"name": "JLab Go Air", "url": "https://www.amazon.com/dp/B0CQRSLMPB"},
    ]

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for comp in competitors:
            print(f"  正在检查: {comp['name']}...")
            page.goto(comp["url"], wait_until="domcontentloaded")

            # 自动提取价格（代替人手复制粘贴）
            try:
                price = page.locator(".a-price .a-offscreen").first.text_content()
            except:
                price = "价格获取失败"

            # 自动截图（代替人手按 PrintScreen）
            page.screenshot(path=f"screenshot_{comp['name'].replace(' ','_')}.png")

            results.append({"name": comp["name"], "price": price})
            print(f"    {comp['name']}: {price}")

        browser.close()

    return results


# ============================================================
# 场景二：自动登录后台 → 导出报表 → 保存到本地
# ============================================================
def rpa_auto_login_and_export():
    """
    传统方式：运营每天手动登录卖家后台，点好几层菜单导出数据
    RPA 方式：脚本自动登录 → 导航到报表页 → 点击导出按钮 → 保存文件
    """
    print("\n=== 场景二：自动登录 + 导出报表 ===")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False 可以看到操作过程
        page = browser.new_page()

        # 步骤 1：打开登录页
        page.goto("https://sellercentral.amazon.com/")

        # 步骤 2：自动填写账号密码（代替人手打字）
        # TODO：替换为真实账号
        page.fill('input[name="email"]', "YOUR_EMAIL")
        page.fill('input[name="password"]', "YOUR_PASSWORD")

        # 步骤 3：自动点击"登录"按钮（代替人手点击）
        page.click('input#signInSubmit')

        # 步骤 4：等待登录完成（机器人等页面加载，代替人眼盯着屏幕等）
        page.wait_for_load_state("networkidle")

        # 步骤 5：导航到报表页面（代替人手点菜单）
        page.click('text=Reports')
        page.click('text=Business Reports')

        # 步骤 6：点击"下载 CSV"（代替人手点下载按钮）
        with page.expect_download() as download_info:
            page.click('text=Download CSV')
        download = download_info.value
        download.save_as("daily_report.csv")

        print("  报表已自动下载: daily_report.csv")
        browser.close()


# ============================================================
# 场景三：批量自动填表——把 10 个产品的数据录入系统
# ============================================================
def rpa_batch_form_fill():
    """
    传统方式：拿到 10 个产品的参数表，一个一个复制粘贴到 ERP/后台
    RPA 方式：读 Excel → 自动打开后台 → 逐个字段填写 → 提交，2 分钟跑完 10 个
    """
    print("\n=== 场景三：批量自动填表 ===")

    # 模拟从 Excel 读出的产品数据
    products = [
        {"sku": "BT-001", "title": "蓝牙耳机 Pro", "price": "29.99", "stock": "500"},
        {"sku": "BT-002", "title": "蓝牙耳机 Lite", "price": "19.99", "stock": "300"},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for product in products:
            print(f"  正在上架: {product['sku']} - {product['title']}")

            # 打开产品上架页面
            page.goto("https://sellercentral.amazon.com/add-product")

            # 自动填写每个字段（代替人手一个个输入框点过去）
            page.fill('input[name="title"]', product["title"])
            page.fill('input[name="price"]', product["price"])
            page.fill('input[name="quantity"]', product["stock"])

            # 自动点击提交
            page.click('button[type="submit"]')
            page.wait_for_timeout(2000)
            print(f"    {product['sku']} 提交完成")

        browser.close()


# ============================================================
# 额外说明：以上脚本可以通过 Claude Code + MCP Playwright 实时执行
# ============================================================
"""
如何用 Claude Code 直接做 RPA？

在 VS Code 里对 Claude Code 说：

"帮我打开 amazon.com，搜索 bluetooth earbuds，
把前 5 个结果的标题和价格提取出来，存到 Excel"

Claude Code 会通过 MCP Playwright 直接操作浏览器，
等于你有了一个会听懂人话、会操作浏览器的 AI 机器人。

这个能力我可以在面试时现场演示。
"""


if __name__ == "__main__":
    print("跨境电商 RPA 自动化脚本库")
    print("=" * 50)
    print("包含 3 个场景：")
    print("  1. 竞品价格自动巡检 + 截图")
    print("  2. 自动登录后台 + 导出报表")
    print("  3. 批量自动填表上架")
    print("=" * 50)
    print("\n实际运行时取消注释对应的函数调用即可")
    # rpa_competitor_price_check()
    # rpa_auto_login_and_export()
    # rpa_batch_form_fill()
