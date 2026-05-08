import subprocess

import requests
import time
from datetime import datetime
import os
import getpass
import csv
import pandas as pd
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ========== 公共配置 ==========
api_url = "https://en.beatroad.co.kr/exec/front/order/Formproductmileage/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://en.beatroad.co.kr",
    "Pragma": "no-cache",
    "Referer": "https://en.beatroad.co.kr/order/orderform.html?basket_type=A0000&delvtype=B",
    "X-Requested-With": "XMLHttpRequest"
}

# ========== 账号 Cookies（请替换为最新的有效值） ==========
cookies_kkt = {
  "_fwb": "78Ui3Ydb1STc3hiwtCGQnb.1760608874392",
  "CUK45": "cuk45_beatroad_optn80hn9t3bsmsgofq0niu82j6fct9r",
  "CUK2Y": "cuk2y_beatroad_optn80hn9t3bsmsgofq0niu82j6fct9r",
  "siteLT": "e15262bf-063e-0a24-03d6-d172b2ee62a5",
  "analytics_longterm": "analytics_longterm.beatroad_2.544A4FF.1761292386221",
  "CVID_Y": "CVID_Y.535755404a5a515d6c02.1778214763204",
  "CFAE_CUK1Y": "CFAE_CUK1Y.beatroad_2.1R57RGP.1761292386488",
  "fb_event_id": "event_id.beatroad.2.KBNAXCDUG7GCRW29AEARNN78Q26W1DVDB",
  "fb_external_id": "e09ab6d2678455ea1a2bd5a61e59c85c98bcb99f817014308f3e527532e3495d",
  "CID": "CIDR77e712c934090655efd8e3b83583fc04",
  "CIDR77e712c934090655efd8e3b83583fc04": "319894c7d8207782c743f3ac3f918bb1%3A%3A%3A%3A%3A%3Ahttps%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DtDqAt3n5mS_o0V2SJJycXbpKpt9nU3kOEf3or6pe03o79DhH3q1nbYVy9QMAeGhn%26wd%3D%26eqid%3D892f29a50008e6ad0000000469fd6615%3A%3Abaidu%28%EC%A4%91%EA%B5%AD%29%3A%3A1%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2F%3A%3A1778214447%3A%3A%3A%3Appdp%3A%3A1778214447%3A%3A%3A%3A%3A%3A%3A%3A",
  "vt": "1778214706",
  "ECSESSID": "pvvuf9hohjs58ob09jnshdii2m0lggmm",
  "basketcount_1": "0",
  "basketprice_1": "%26%238361%3B0",
  "wish_id": "c79cc99ebb9a9ce5a00c3602b5a1fbfa",
  "wishcount_1": "0",
  "isviewtype": "pc",
  "siteSID": "dd3e4328-15f0-6e40-ad65-f9406dd4ee69",
  "analytics_session_id": "analytics_session_id.beatroad_2.B3EB4AB.1778214470340",
  "CVID": "CVID.535755404a5a515d6c02.1778214470340",
  "ec_ipad_device": "F",
  "CFAE_CID": "CFAE_CID.beatroad_2.U6ANPGI.1778214510384",
  "recent_plist2": "9880%7C10581%7C10614%7C10615%7C10605%7C10610%7C10940%7C11071",
  "org_phpsess_id_2": "pvvuf9hohjs58ob09jnshdii2m0lggmm",
  "return_url": "%2Forder%2Forderform.html%3Fbasket_type%3DA0000%26delvtype%3DB",
  "login_provider_2": "%7B%22member_id%22%3A%22qq20161441871984%22%2C%22provider%22%3Anull%2C%22client_id%22%3Anull%7D",
  "iscache": "F",
  "ec_mem_level": "2",
  "PHPSESSVERIFY": "3d30aa9855f8b7107f40f33890d071b5",
  "couponcount_2": "0",
  "atl_epcheck": "1",
  "atl_option": "1%2C1%2CH",
  "basketprice_2": "%26%2336%3B20.16",
  "ec_async_cache_avail_mileage_2": "0.00",
  "ec_async_cache_used_mileage_2": "0.00",
  "ec_async_cache_returned_mileage_2": "0",
  "ec_async_cache_unavail_mileage_2": "0",
  "ec_async_cache_used_deposit_2": "0",
  "ec_async_cache_all_deposit_2": "0",
  "ec_async_cache_deposit_refund_wait_2": "0",
  "ec_async_cache_member_total_deposit_2": "0",
  "wishcount_2": "0",
  "basketcount_2": "1",
  "CFAE_LC": "CFAE_LC.beatroad_2.4URXAHX.1778214763204"
}

cookies_line ={
  "_fwb": "738FZEpghCH1lA4uaVMsRH.1778216461630",
  "fb_event_id": "event_id.beatroad.2.MCRF996GMJD4IEZQP7XBRDEFI3S9PYB",
  "fb_external_id": "1205e5b26fe16f08d555a1916a3707c7da283256836f4a84d8cf06e3dc28aff0",
  "CUK45": "cuk45_beatroad_a3f2qaumdr824o13jpihuhemu24h3fa9",
  "CUK2Y": "cuk2y_beatroad_a3f2qaumdr824o13jpihuhemu24h3fa9",
  "CID": "CIDRb7156a80e06d2f1f32d2797e34e95ab0",
  "CIDRb7156a80e06d2f1f32d2797e34e95ab0": "59c69afbc9b5057d2a27ec87deb21595%3A%3A%3A%3A%3A%3Ahttps%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D7yJXD6R3UaI4eOrK1xye0-jas0zl2GbPaGNcMtblJQupvI5vdxiNRpnnHvj63Mr9%26wd%3D%26eqid%3Ddbf364dd0018c1c30000000469fd6df5%3A%3Abaidu%28%EC%A4%91%EA%B5%AD%29%3A%3A1%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2F%3A%3A1778216462%3A%3A%3A%3Appdp%3A%3A1778216462%3A%3A%3A%3A%3A%3A%3A%3A",
  "vt": "1778217843",
  "ECSESSID": "utm3hupinqgo5da2jpkdp812d2vur4dg",
  "basketcount_1": "0",
  "basketprice_1": "%26%238361%3B0",
  "wish_id": "3d4c6dc4e1c12fde7ce740ad48b1b68f",
  "wishcount_1": "0",
  "isviewtype": "pc",
  "ec_ipad_device": "F",
  "CFAE_CID": "CFAE_CID.beatroad_2.L8ET286.1778216688963",
  "CFAE_CUK1Y": "CFAE_CUK1Y.beatroad_2.L8ET286.1778216688963",
  "CVID": "CVID.535755404a5a515d6c02.1778216688963",
  "CVID_Y": "CVID_Y.535755404a5a515d6c02.1778216688963",
  "siteLT": "ff383829-afcf-8669-ceb6-8c65d4210bee",
  "siteSID": "4615366d-b4ca-f05b-7a2f-1f9e8a4453fb",
  "analytics_session_id": "analytics_session_id.beatroad_2.1D59346.1778216688276",
  "analytics_longterm": "analytics_longterm.beatroad_2.1D59346.1778216688276",
  "recent_plist2": "11071",
  "org_phpsess_id_2": "utm3hupinqgo5da2jpkdp812d2vur4dg",
  "return_url": "%2Forder%2Forderform.html%3Fbasket_type%3DA0000%26delvtype%3DB",
  "login_provider_2": "%7B%22member_id%22%3A%22qq35142634547855%22%2C%22provider%22%3Anull%2C%22client_id%22%3Anull%7D",
  "iscache": "F",
  "ec_mem_level": "2",
  "PHPSESSVERIFY": "d1305d1ac1e91aaf1e29a1aa39698c82",
  "basketcount_2": "2",
  "basketprice_2": "%26%2336%3B20.16",
  "atl_epcheck": "1",
  "atl_option": "1%2C1%2CH",
  "wishcount_2": "0",
  "couponcount_2": "0",
  "CFAE_LC": "CFAE_LC.beatroad_2.NJEVSLA.1778218589473",
  "ec_async_cache_avail_mileage_2": "0.00",
  "ec_async_cache_used_mileage_2": "0.00",
  "ec_async_cache_returned_mileage_2": "0",
  "ec_async_cache_unavail_mileage_2": "0",
  "ec_async_cache_used_deposit_2": "0",
  "ec_async_cache_all_deposit_2": "0",
  "ec_async_cache_deposit_refund_wait_2": "0",
  "ec_async_cache_member_total_deposit_2": "0"
}

# ========== 统一日志文件路径 ==========
GITHUB_REPO = "Juineii/dailydirection_br0308"       # 您的仓库名
GITHUB_BRANCH = "main"
CSV_FILENAME = r"D:\fansign\ing\dailydirection_br0308\dailydirection_br线上团签.csv" if os.name == "nt" else os.path.expanduser("~/combined_monitor.csv")
os.makedirs(os.path.dirname(CSV_FILENAME), exist_ok=True)

# ========== 日志配置 ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== Git 推送函数（占位，请根据实际需求实现） ==========
def git_push_update():
    """
    将最新的 CSV 文件提交并推送到 GitHub
    """
    try:
        # 1. 获取 GitHub Token（优先从环境变量读取）
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            # 如果环境变量未设置，尝试使用硬编码（请务必替换成真实 Token！）
            # 注意：硬编码 Token 有安全风险，建议使用环境变量
            token = "fansign"  # 请替换为您的 Personal Access Token
            logging.warning("使用代码中硬编码的 Token，建议通过环境变量 GITHUB_TOKEN 设置")

        # 2. 构建带认证的远程仓库 URL
        remote_url = f"https://{token}@github.com/{GITHUB_REPO}.git"

        # 3. 添加 CSV 文件到暂存区
        subprocess.run(['git', 'add', CSV_FILENAME], check=True, capture_output=True)

        # 4. 检查是否有文件变化（避免空提交）
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
        if result.returncode != 0:
            # 有变化，提交
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"自动更新数据 {timestamp}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)

            # 5. 推送到 GitHub（指定分支）
            push_result = subprocess.run(
                ['git', 'push', remote_url, f'HEAD:{GITHUB_BRANCH}'],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✅ 已推送到 GitHub: {commit_msg}")
        else:
            print("⏭️  CSV 文件无变化，跳过推送")

    except subprocess.CalledProcessError as e:
        logging.error(f"Git 操作失败: {e.stderr if e.stderr else e}")
    except Exception as e:
        logging.error(f"推送过程中发生错误: {e}")

# ========== requests 会话配置 ==========
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["POST"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

# ========== 写入CSV（Pandas版，带Git推送） ==========
def write_to_csv(product_name, data):
    """将库存变化写入CSV文件，并触发 Git 推送"""
    try:
        # 检查文件是否存在
        if os.path.exists(CSV_FILENAME):
            df_existing = pd.read_csv(CSV_FILENAME, encoding='utf-8-sig')
        else:
            df_existing = pd.DataFrame(columns=['时间', '商品名称', '库存变化', '单笔销量'])

        # 创建新数据行
        new_row = pd.DataFrame([data])
        df_updated = pd.concat([df_existing, new_row], ignore_index=True)

        # 保存到CSV
        df_updated.to_csv(CSV_FILENAME, index=False, encoding='utf-8-sig')
        print(f"💾 数据已写入 {CSV_FILENAME}")

        # 调用 Git 推送（每次写入后自动同步到 GitHub）
        git_push_update()

    except Exception as e:
        print(f"❌ 写入CSV失败: {e}")
        logging.error(f"写入CSV失败: {e}")

# ========== 获取库存（可指定cookies） ==========
def get_stock_from_api(cookies):
    """调用 API 获取 Beatroad 商品库存"""
    try:
        response = session.post(api_url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()
        data = response.json()
        product_list = data.get("product", [])
        stocks = {}
        for product in product_list:
            product_no = product.get("product_no")
            product_name = product.get("product_name", "未知商品")
            stock = product.get("stock_number", None)
            if product_no and stock is not None:
                stocks[product_no] = {"name": product_name, "stock": int(stock)}
        return stocks
    except Exception as e:
        print(f"{datetime.now()} ❌ API请求失败: {e}")
        return {}

# ========== 主监控函数（同时监控两个账号） ==========
def monitor_stocks():
    print(f"📄 统一日志输出路径: {CSV_FILENAME}")
    print("将同时监控 kkt 和 line 账号，数据合并到同一CSV文件")

    # 按账号区分的历史库存记录
    previous_stocks = {}   # {account: {product_no: stock}}
    initial_stocks = {}    # {account: {product_no: stock}}

    accounts = [
        {"name": "kkt", "cookies": cookies_kkt},
        {"name": "line", "cookies": cookies_line}
    ]

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for acc in accounts:
            account_name = acc["name"]
            cookies = acc["cookies"]

            current_stocks = get_stock_from_api(cookies)
            if not current_stocks:
                print(f"⚠️ 账号 {account_name} 无法获取库存数量")
                continue

            # 初始化该账号的记录字典
            if account_name not in previous_stocks:
                previous_stocks[account_name] = {}
                initial_stocks[account_name] = {}

            for product_no, info in current_stocks.items():
                product_name = info["name"]
                current_stock = info["stock"]

                # 第一次记录初始库存
                if product_no not in initial_stocks[account_name]:
                    initial_stocks[account_name][product_no] = current_stock
                    previous_stocks[account_name][product_no] = current_stock

                    # 构造数据字典并写入CSV
                    data = {
                        '时间': current_time,
                        '商品名称': account_name,
                        '库存变化': f"初始库存:{current_stock}",
                        '单笔销量': str(abs(current_stock))
                    }
                    write_to_csv(account_name, data)      # product_name 参数传递账号名（虽未使用）

                    # 打印详细信息（包含商品名称）
                    log_message = f"{current_time} [{account_name}] 商品[{product_name}]({product_no}) 初始库存: {current_stock}"
                    print(log_message)

                # 检测库存变化
                elif current_stock != previous_stocks[account_name][product_no]:
                    prev_stock = previous_stocks[account_name][product_no]
                    stock_diff = prev_stock - current_stock
                    stock_change_str = f"{prev_stock} -> {current_stock}"

                    data = {
                        '时间': current_time,
                        '商品名称': account_name,
                        '库存变化': stock_change_str,
                        '单笔销量': str(stock_diff)
                    }
                    write_to_csv(account_name, data)

                    change_message = (
                        f"{current_time} [{account_name}] 商品[{product_name}]({product_no}) "
                        f"库存变化： {prev_stock} -> {current_stock}, 销量:{stock_diff}"
                    )
                    print(change_message)
                    previous_stocks[account_name][product_no] = current_stock

        time.sleep(10)

# ========== 程序入口 ==========
if __name__ == "__main__":
    monitor_stocks()