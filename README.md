# BRDF 查找表预计算

骨架能出一张粗糙度与视线夹角的二维表，但各项的物理含义是错的。

## 已知缺口

- `ndf_ggx` 的分母少了平方项，粗糙度越小高光越离谱，与真实 GGX 分布差一个数量级。
- `fresnel` 直接返回 0.04，与入射角无关，掠射角下没有反射增强。
- `build_lut` 里假设半程向量与法线、视线共面，光照方向被固定成视线方向，
  表其实是退化的一维曲线复制。
- 漫反射项用 `(1-f)/pi`，f 是常数，能量与粗糙度的关系是错的。
- `energy_check` 只报平均值，没有与 1 做比较，无法判断能量是否守恒。
- `save_lut_png` 抛 NotImplementedError。

## 运行

```
python gen_samples.py
python -m brdf.cli --roughness-steps 16 --view-steps 16 --out lut.json
python -m pytest tests -q
```

`samples.json` 给了 5 个采样点，每个带有期望反射率区间。注意最后一行的 `roughness` 写成了 0.100，
按浮点解析是 0.1，与第 1 行重复。
