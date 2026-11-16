# -*- coding: utf-8 -*-
"""BRDF 查找表预计算骨架。

当前用简化的兰伯特加高光近似，菲涅尔项缺失，表也没有归一化。
"""

import math


def clamp01(v):
    return 0.0 if v < 0 else (1.0 if v > 1 else v)


def ndf_ggx(n_dot_h, alpha):
    """GGX 法线分布。分母少了一个平方项。"""
    a2 = alpha * alpha
    d = n_dot_h * n_dot_h * (a2 - 1.0) + 1.0
    return a2 / (math.pi * d)


def fresnel(n_dot_v, f0):
    """菲涅尔项。当前直接返回常数。"""
    return f0


def brdf_value(n_dot_l, n_dot_v, n_dot_h, v_dot_h, roughness, f0=0.04):
    alpha = max(roughness * roughness, 1e-4)
    d = ndf_ggx(n_dot_h, alpha)
    f = fresnel(n_dot_v, f0)
    spec = d * f / max(4.0 * n_dot_v * n_dot_l, 1e-4)
    diffuse = (1.0 - f) / math.pi
    return clamp01(diffuse + spec)


def build_lut(size, roughness_steps=16, n_dot_v_steps=16):
    """生成 (roughness, n_dot_v) 二维查找表。光照方向固定。"""
    lut = []
    for ri in range(roughness_steps):
        rough = (ri + 0.5) / roughness_steps
        row = []
        for vi in range(n_dot_v_steps):
            ndv = (vi + 0.5) / n_dot_v_steps
            # 简化：假设半程向量与法线、视线共面
            ndh = clamp01((1.0 + ndv) * 0.5)
            vdh = clamp01(ndv)
            row.append(brdf_value(ndv, ndv, ndh, vdh, rough))
        lut.append(row)
    return lut


def energy_check(lut, n_dot_v_steps=16):
    """能量守恒检查。当前只求平均，不与 1 比较。"""
    total = 0.0
    for row in lut:
        total += sum(row)
    return total / (len(lut) * n_dot_v_steps)


def save_lut_png(lut, path):
    raise NotImplementedError("查找表可视化尚未实现")


def main(argv=None):
    import argparse
    import json
    ap = argparse.ArgumentParser(prog="brdf")
    ap.add_argument("--roughness-steps", type=int, default=16)
    ap.add_argument("--view-steps", type=int, default=16)
    ap.add_argument("--out", default="lut.json")
    args = ap.parse_args(argv)
    lut = build_lut(64, args.roughness_steps, args.view_steps)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lut, f)
    print("表 %dx%d，平均能量 %.4f" % (len(lut), len(lut[0]), energy_check(lut)))
    return 0
