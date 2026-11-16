# -*- coding: utf-8 -*-
"""生成一个采样点清单：若干 (粗糙度, 视线夹角) 组合及其期望反射率参考区间。"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SAMPLES = [
    {"roughness": 0.10, "n_dot_v": 0.90, "expect_min": 0.02, "expect_max": 0.35},
    {"roughness": 0.35, "n_dot_v": 0.60, "expect_min": 0.02, "expect_max": 0.30},
    {"roughness": 0.70, "n_dot_v": 0.30, "expect_min": 0.02, "expect_max": 0.25},
    {"roughness": 0.95, "n_dot_v": 0.05, "expect_min": 0.01, "expect_max": 0.20},
    {"roughness": 0.100, "n_dot_v": 1.0, "expect_min": 0.01, "expect_max": 0.40},
]

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    path = os.path.join(HERE, "data", "samples.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(SAMPLES, f, ensure_ascii=False, indent=2)
    print("已生成", path, len(SAMPLES), "个采样点")
