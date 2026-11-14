"""实验一：2001年是不是美国制造业就业占比的结构断点？
数据：FRED MANEMP（制造业就业）+ PAYEMS（总非农就业）
方法：Chow test + 断点扫描 + 分段斜率比较
"""
import urllib.request
import csv
import io
import math
from statistics import mean

def download_fred(series_id):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + series_id
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print("下载 %s 失败: %s" % (series_id, e))
        return None

def parse_fred_csv(text):
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    rows = []
    for row in reader:
        if len(row) < 2:
            continue
        date_str, val_str = row[0], row[1]
        if val_str in ('.', ''):
            continue
        try:
            year = int(date_str[:4])
            val = float(val_str)
            rows.append((year, val))
        except ValueError:
            continue
    return rows

def aggregate_annual(rows):
    by_year = {}
    for y, v in rows:
        by_year.setdefault(y, []).append(v)
    return {y: mean(vs) for y, vs in by_year.items()}

def linear_fit(xs, ys):
    n = len(xs)
    mx = mean(xs)
    my = mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return my, 0.0
    slope = num / den
    intercept = my - slope * mx
    return intercept, slope

def rss(xs, ys, intercept, slope):
    return sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))

def chow_test(years, values, break_year):
    xs = [y - 1970 for y in years]
    n = len(xs)
    i0 = sum(1 for y in years if y <= break_year)
    i1 = n - i0
    if i0 < 3 or i1 < 3:
        return None, None

    a, b = linear_fit(xs, values)
    rss_pooled = rss(xs, values, a, b)

    xs1, ys1 = xs[:i0], values[:i0]
    xs2, ys2 = xs[i0:], values[i0:]
    a1, b1 = linear_fit(xs1, ys1)
    a2, b2 = linear_fit(xs2, ys2)
    rss1 = rss(xs1, ys1, a1, b1)
    rss2 = rss(xs2, ys2, a2, b2)

    k = 2
    num = (rss_pooled - (rss1 + rss2)) / k
    den = (rss1 + rss2) / (n - 2 * k)
    if den <= 0:
        return None, None
    F = num / den

    # F 分布近似：k=2, df=n-4，用简单临界值近似
    return F, (b1, b2, a1, a2)

def main():
    print("=" * 70)
    print("实验一：2001年是不是结构断点？")
    print("=" * 70)

    print("\n下载 FRED 数据...")
    manuf_text = download_fred("MANEMP")
    total_text = download_fred("PAYEMS")
    if manuf_text is None or total_text is None:
        print("数据下载失败。请检查网络，或手动下载：")
        print("  https://fred.stlouisfed.org/graph/fredgraph.csv?id=MANEMP")
        print("  https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS")
        return

    manuf = aggregate_annual(parse_fred_csv(manuf_text))
    total = aggregate_annual(parse_fred_csv(total_text))

    years = sorted(set(manuf) & set(total))
    years = [y for y in years if y >= 1948 and y <= 2024]
    shares = [manuf[y] / total[y] * 100 for y in years]

    print("数据范围: %d - %d，共 %d 年" % (years[0], years[-1], len(years)))
    print()

    # 显示关键年份
    print("关键年份制造业就业占比:")
    for y in [1950, 1970, 1990, 2000, 2001, 2010, 2020, 2024]:
        if y in manuf and y in total:
            idx = years.index(y)
            print("  %d: %.2f%%" % (y, shares[idx]))
    print()

    # Chow test at 2001
    F2001, slopes = chow_test(years, shares, 2001)
    print("=" * 70)
    print("Chow test @ 2001年")
    if F2001 is not None:
        print("  F 统计量 = %.3f" % F2001)
        print("  2001前斜率 = %.4f 百分点/年" % slopes[0])
        print("  2001后斜率 = %.4f 百分点/年" % slopes[1])
        # 粗略临界值参考：F(2, n-4)，n 约 77，df 约 73
        # F(2, 70) 在 0.05 水平约 3.13，0.01 水平约 4.92
        if F2001 < 3.13:
            print("  结论：F < 3.13（5%临界值近似），2001年不是显著断点")
        elif F2001 < 4.92:
            print("  结论：3.13 < F < 4.92，2001年在5%水平显著，1%水平不显著")
        else:
            print("  结论：F > 4.92，2001年是显著断点（需进一步检查）")
    print()

    # 断点扫描
    print("=" * 70)
    print("断点扫描：每年做 Chow test，找 F 值最大的年份")
    scan = []
    for b in range(1960, 2020):
        F, _ = chow_test(years, shares, b)
        if F is not None:
            scan.append((b, F))

    scan.sort(key=lambda x: -x[1])
    print("  F 值最大的 10 个年份:")
    for b, F in scan[:10]:
        print("    %d: F = %.3f" % (b, F))
    print("  2001年的 F 值排名: %d / %d" % (
        next(i+1 for i, (b, _) in enumerate(scan) if b == 2001),
        len(scan)))
    print("=" * 70)

if __name__ == "__main__":
    main()
