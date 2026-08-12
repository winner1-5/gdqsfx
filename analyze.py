import json
from collections import Counter, defaultdict

with open(r'C:\Users\86155\Desktop\22\data\task5_tickets.json', 'r', encoding='utf-8') as f:
    tickets = json.load(f)

print('=== 总览 ===')
print(f'总工单: {len(tickets)}')
dates = [t['created_at'][:10] for t in tickets]
print(f'时间范围: {min(dates)} ~ {max(dates)}')

print('\n=== 1. 每日工单量 ===')
daily = Counter(dates)
for d in sorted(daily.keys()):
    print(f'{d}: {daily[d]}')

print('\n=== 2. 分类分布 ===')
cats = Counter(t['category'] for t in tickets)
for c, n in cats.most_common():
    print(f'{c}: {n} ({n/len(tickets)*100:.1f}%)')

print('\n=== 3. 优先级分布 ===')
pris = Counter(t['priority'] for t in tickets)
for p, n in pris.most_common():
    print(f'{p}: {n} ({n/len(tickets)*100:.1f}%)')

print('\n=== 4. 渠道分布 ===')
chs = Counter(t['channel'] for t in tickets)
for c, n in chs.most_common():
    print(f'{c}: {n} ({n/len(tickets)*100:.1f}%)')

print('\n=== 5. 解决率 ===')
resolved = Counter(t['is_resolved'] for t in tickets)
print(f'已解决: {resolved.get(True,0)}, 未解决: {resolved.get(False,0)}')
print(f'解决率: {resolved.get(True,0)/len(tickets)*100:.1f}%')

print('\n=== 6. 满意度统计 ===')
sats = [t['satisfaction'] for t in tickets]
print(f'平均: {sum(sats)/len(sats):.2f}')
print(f'分布: {Counter(sats)}')

print('\n=== 7. 处理时长统计 ===')
times = [t['resolution_time_hours'] for t in tickets]
print(f'平均: {sum(times)/len(times):.1f}h')
print(f'最长: {max(times)}h, 最短: {min(times)}h')

print('\n=== 8. 按分类的详细指标 ===')
cat_stats = defaultdict(lambda: {'count':0, 'sat_sum':0, 'time_sum':0, 'high':0, 'unresolved':0})
for t in tickets:
    c = t['category']
    cat_stats[c]['count'] += 1
    cat_stats[c]['sat_sum'] += t['satisfaction']
    cat_stats[c]['time_sum'] += t['resolution_time_hours']
    if t['priority'] == '高': cat_stats[c]['high'] += 1
    if not t['is_resolved']: cat_stats[c]['unresolved'] += 1
for c, s in sorted(cat_stats.items(), key=lambda x:-x[1]['count']):
    cnt = s['count']
    print(f'{c}: 数量={cnt}, 平均满意度={s["sat_sum"]/cnt:.2f}, 平均处理时长={s["time_sum"]/cnt:.1f}h, 高优先级={s["high"]}, 未解决={s["unresolved"]}')

print('\n=== 9. 未解决工单详情 ===')
for t in tickets:
    if not t['is_resolved']:
        print(f'{t["ticket_id"]} | {t["created_at"]} | {t["category"]} | {t["priority"]} | 满意度={t["satisfaction"]} | 时长={t["resolution_time_hours"]}h | {t["description"]}')

print('\n=== 10. 满意度<=2的低分工单 ===')
low = [t for t in tickets if t['satisfaction'] <= 2]
print(f'低分工单: {len(low)}条 ({len(low)/len(tickets)*100:.1f}%)')
low_cats = Counter(t['category'] for t in low)
print(f'低分分类分布: {low_cats}')

print('\n=== 11. 高优先级工单按分类 ===')
high = [t for t in tickets if t['priority']=='高']
print(f'高优先级: {len(high)}条 ({len(high)/len(tickets)*100:.1f}%)')
high_cats = Counter(t['category'] for t in high)
print(f'高优分类: {high_cats}')

print('\n=== 12. 每日各分类工单量(趋势) ===')
daily_cat = defaultdict(lambda: defaultdict(int))
for t in tickets:
    d = t['created_at'][:10]
    daily_cat[d][t['category']] += 1
all_cats = sorted(cats.keys())
print('日期,' + ','.join(all_cats) + ',合计')
for d in sorted(daily_cat.keys()):
    row = [d]
    total = 0
    for c in all_cats:
        v = daily_cat[d].get(c, 0)
        row.append(str(v))
        total += v
    row.append(str(total))
    print(','.join(row))

print('\n=== 13. 渠道x分类交叉 ===')
ch_cat = defaultdict(lambda: defaultdict(int))
for t in tickets:
    ch_cat[t['channel']][t['category']] += 1
for ch in ch_cat:
    print(f'{ch}: {dict(ch_cat[ch])}')

print('\n=== 14. 处理时长超过48h的工单 ===')
long_t = [t for t in tickets if t['resolution_time_hours'] >= 48]
for t in long_t:
    print(f'{t["ticket_id"]} | {t["category"]} | {t["resolution_time_hours"]}h | 满意度={t["satisfaction"]} | 已解决={t["is_resolved"]}')
